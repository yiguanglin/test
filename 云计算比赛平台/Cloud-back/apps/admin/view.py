from ast import Sub
import base64
from codecs import getreader
from curses.ascii import SO
import hashlib
# from multiprocessing import Event
import random,json,jwt,time
from re import sub
from typing_extensions import dataclass_transform
import redis

from flask import Blueprint, request, render_template, redirect, url_for, jsonify

from apps.admin.models import Admin, Game, Subject, Score, Jroup, GroupSubject, Event
from apps.user.models import User
from exts import db
from sqlalchemy import desc, null

admin_bp = Blueprint('admin', __name__,url_prefix="/admin")

redis_conn= redis.Redis(host='172.16.100.151', port= 6379, password= 'Huawei@123',db =1,decode_responses=True)


def get_token():
    global token
    # 生成一个字典，包含我们的具体信息
    d = {
        # 公共声明
        'exp':time.time()+86400000, # (Expiration Time) 此token的过期时间的时间戳 86400000毫秒=1天
        'iat':time.time(), # (Issued At) 指明此创建时间的时间戳
        'iss':'JXYYJSZYXY', # (Issuer) 指明此token的签发者
        
        # 私有声明
        'data':{
            'username':'XXGCXY',
            'timestamp':time.time()
        }
    }

    token = jwt.encode(d,'JXYYJSZYXY',algorithm='HS256')
    return token

@admin_bp.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ


@admin_bp.route('/login', methods=['GET', "POST","PUT","DELETE"])               #管理员登录
def login_admin():
    try:
        if request.method=="POST":
            data = request.get_data()
            data = str(data,encoding='utf-8')
            data =json.loads(data)
            username = data["username"]
            password = data["password"]
            user = Admin.query.filter_by(username=username, password=password).first()
            password = user.password
            password = hashlib.shake_128(password.encode('utf-8')).hexdigest(16)
            if user:
                aaa = redis_conn.get(username)
                if aaa == None:
                    redis_conn.set(username,get_token(),ex=86400)
                    token = redis_conn.get(username)
                    res = {
                            "data": {
                                "id": user.id,
                                "username": user.username,
                                "password": password,
                                "token": token
                            },
                            "msg": "Success",
                            "status": 200
                        }
                    return json.dumps(res, ensure_ascii=False)
                else:
                    token = redis_conn.get(username)
                    res = {
                            "data": {
                                "id": user.id,
                                "username": user.username,
                                "password": password,
                                "token": token
                            },
                            "msg": "Success",
                            "status": 200
                        }
                    return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                        "data": "null",
                        "msg": "帐号或密码错误",
                        "status": 401
                }
                return json.dumps(res, ensure_ascii=False)
        return '请使用post请求'
    except:
        res = {"status": 400, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/foundGame', methods=['GET', "POST","PUT","DELETE"])           #创建game和hash
def foundgame():
    try:
        if request.method=="POST":
            data = request.get_data()
            data = str(data,encoding='utf-8')
            data =json.loads(data)
            gamename = data["gamename"]
            num = int(data["num"])
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                name = Game.query.filter_by(name=gamename).all()
                for i in name:
                    if gamename == i.name:
                        res = {
                            "data": "null",
                            "msg":"用户名已重复",
                            "status": 404
                        }
                        return json.dumps(res, ensure_ascii=False)
                else:
                    game = Game()
                    game.people = num
                    game.name = gamename
                    db.session.add(game)
                    db.session.commit()
                    gamename = data["gamename"]
                    gameid = Game.query.filter_by(name=gamename).first()
                    gameid = gameid.gameid
                    for i in range(num):
                        r = str(random.randint(1, 99999))
                        hash = hashlib.shake_128(r.encode('utf-8')).hexdigest(8)
                        user = User()
                        user.hash = hash
                        user.game_id = gameid
                        db.session.add(user)
                        db.session.commit()
                    hash_list = []
                    hashcode_list = User.query.filter_by(game_id=gameid).all()
                    for i in hashcode_list:
                        score = Score()
                        hash = i.hash
                        id = i.id
                        score.user_id = i.id
                        score.game_id = gameid
                        db.session.add(score)
                        db.session.commit()
                        liuhui = {"id": id,"hash": hash,"game_name": game.name}
                        hash_list.append(liuhui)
                    res = {
                        "data": {
                            "game_id": game.gameid,
                            "people": game.people,
                            "hash_list": hash_list,
                            "game_status": game.status,
                            "falsedelete": game.falsedelete
                        },
                        "msg": "Success",
                        "status": 200
                    }
                    return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                        "data": "null",
                        "msg": "token不可用",
                        "status": 403
                }
        return '请使用post请求'
    except:
        res = {"status": 400, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/lastGame', methods=['GET', 'POST', 'PUT', 'DELETE'])              #获取最近一场比赛信息
def getGame():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                game = Game.query.order_by(desc("gameid")).first()
                gameid = game.gameid
                hashcode_list = User.query.filter_by(game_id=gameid).all()
                hash_list = []
                for i in hashcode_list:
                    hash = i.hash
                    id = i.id
                    liuhui = {"id": id,"hash": hash,"game_name": game.name}
                    hash_list.append(liuhui)
                res = {
                        "data": {
                            "game_id": game.gameid,
                            "people": game.people,
                            "hash_list": hash_list,
                            "game_status": game.status,
                            "falsedelete": game.falsedelete
                        },
                        "msg": "Success",
                        "status": 200
                    }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/getallGame', methods=['GET', 'POST', 'PUT', 'DELETE'])           #获取比赛信息
def get_game():
    # try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                game_list = Game.query.filter_by(falsedelete="Flase").all()
                list_game = []
                for i in game_list:
                    id = i.gameid
                    name = i.name
                    time = str(i.time)
                    people = i.people
                    status = i.status
                    falsedelete = i.falsedelete
                    game_id = i.gameid
                    groupsubject = GroupSubject.query.filter_by(game_id=game_id).first()
                    if groupsubject != None:
                        groupname = groupsubject.jroup.groupname
                        liuhui = {"game_id": id,"game_name": name,"game_time": time,"game_people": people,"game_status":status,"game_falsedelete":falsedelete,"group_name": groupname}
                        list_game.append(liuhui)
                    else:
                        liuhui = {"game_id": id,"game_name": name,"game_time": time,"game_people": people,"game_status":status,"game_falsedelete":falsedelete}
                        list_game.append(liuhui)
                res = {
                        "data": {
                            "all_game": list_game
                        },
                        "msg": "Success",
                        "status": 200
                    }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    # except:
    #     res = {"status": 404, "msg": "缺少所需参数!"}
    #     return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/inspectName', methods=['GET', 'POST', 'PUT', 'DELETE'])       #查询所有待审核用户名
def get_username():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                user = User.query.filter_by(status="wating",falsedelete="False").all()
                user_list= []
                for i in user:
                    id = i.id
                    hash = i.hash
                    username = i.username
                    status = i.status
                    falsedelete = i.falsedelete
                    gameid = i.game_id
                    user_all = {
                            "id": id,
                            "game_id": gameid,
                            "gamename": i.game.name,
                            "hashcode": hash,
                            "username": username ,
                            "falsedelete": falsedelete,
                            "status": status
                        }
                    user_list.append(user_all)
                res = {
                        "data": user_list,
                        "msg": "Success",
                        "status": 200
                    }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/success', methods=['GET', "POST","PUT","DELETE"])             #管理员审核成功状态
def success():
    try:
        if request.method == "POST":
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            id = data["id"]
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                user = User.query.get(id)
                user.status = "runing"
                db.session.commit()
                status = user.status
                res = {
                    "data":{
                        "id": id,
                        "status":status,
                    },
                    "msg":"审核成功状态",
                    "status":201
                }
            else:
                res = {
                        "data": "null",
                        "msg": "token不可用",
                        "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 400, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/refuse', methods=['GET', "POST","PUT","DELETE"])              #管理员驳回状态
def refuse():
    try:
        if request.method == "POST":
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            id = data["id"]
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                user = User.query.get(id)
                user.status = "noruning"
                db.session.commit()
                status = user.status
                res = {
                    "data": {
                        "id": id,
                        "status": status,
                    },
                    "msg": "驳回状态，名字不和规范，请重新输入名字",
                    "status": 404
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                        "data": "null",
                        "msg": "token不可用",
                        "status": 403
                }
        return "请用post请求"
    except:
        res = {"status": 400, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/deleteGame', methods=['GET', 'POST', 'PUT', 'DELETE'])        #删除比赛
def deletegame():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            gamename = data["gamename"]
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                game = Game.query.filter_by(name=gamename).first()
                gameid = game.gameid
                game.status = 3
                game.falsedelete = True
                db.session.add(game)
                db.session.commit()
                userid = User.query.filter_by(game_id=gameid).all()
                for i in userid:
                    id =i.id
                    user = User.query.get(id)
                    user.falsedelete = True
                    db.session.add(user)
                    db.session.commit()
                res = {
                    "data":{
                        "id":id,
                        "gameid":gameid,
                        "gamestatus": game.status,
                        "gamename":gamename
                    },
                    "msg":"删除比赛成功",
                    "status":200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)

        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/upload', methods=['GET', 'POST', 'PUT', 'DELETE'])            #上传题目和答案
def subject_answer():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            headline = data["headline"]
            text = data["text"]
            answer = data["answer"]
            grade = data["grade"]
            level = data["level"]
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                subject = Subject()
                subject.headline = headline
                subject.text = text
                subject.answer = answer
                subject.grade = grade
                subject.level = level
                db.session.add(subject)
                db.session.commit()
                res = {
                    "data": {
                        "id": subject.id,
                        "headline": subject.headline,
                        "text": subject.text,
                        "answer": subject.answer,
                        "grade": subject.grade,
                        "level": subject.level
                    },
                    "msg": "Success",
                    "status": 200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/rankingList', methods=['GET', 'POST', 'PUT', 'DELETE'])       #排行榜
def ranking_list():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            game_id = data["game_id"]
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token: 
                # score = Score.query.filter(Score.game_id == game_id).order_by(-Score.result).all()
                # score_list= []
                # for i in range(30):
                #     for j in score:
                #         id = j.id
                #         userid = j.id
                #         username = j.user.username
                #         result = j.result
                #         accomplish = j.accomplish
                #         score_all = {
                #                 "id": id,
                #                 "user_id": userid,
                #                 "username": username ,
                #                 "result": result,
                #                 "accomplish": accomplish
                #             }
                #         score_list.append(score_all)
                scores = Score.query.filter_by(game_id=game_id).all()
                score_list= []
                for i in scores:
                    if i.user.status == "runing":
                        id = i.id
                        userid = i.id
                        username = i.user.username
                        result = i.result
                        accomplish = i.accomplish
                        score_all = {
                                "id": id,
                                "user_id": userid,
                                "username": username ,
                                "result": result,
                                "accomplish": accomplish,
                            }
                        score_list.append(score_all)
                ranking = sorted(score_list, key=lambda x: x['result'], reverse=True)
                res = {
                        "data":{ 
                            "all_score": ranking
                        },
                        "msg": "Success",
                        "status": 200
                    }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/getHash', methods=['GET', 'POST', 'PUT', 'DELETE'])           #获取单场比赛的hash
def get_hash():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            game_id = data["game_id"]
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                hash_list = []
                hashcode_list = User.query.filter_by(game_id=game_id,falsedelete=0).all()
                for i in hashcode_list:
                    id = i.id
                    gameid = i.game_id
                    gamename = i.game.name
                    hash = i.hash
                    username = i.username
                    status = i.status
                    falsedelete = i.falsedelete
                    liuhui = {"id": id,"game_id":gameid,"game_name": gamename,"hash": hash,"username":username,"status":status,"falsedelete": falsedelete}
                    hash_list.append(liuhui)
                res = {
                        "data": {
                            "all_hash": hash_list
                        },
                        "msg": "Success",
                        "status": 200
                    }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/foundGroup', methods=['GET', 'POST', 'PUT', 'DELETE'])         #创建题目组
def foundGroup():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            username = data["username"]
            groupname = data["groupname"]
            subject_list = data["subject_list"]
            # game_id = data["game_id"]
            token1 = data["token"]
            token = redis_conn.get(username)
            if token1 == token:
                jroup = Jroup()
                jroup.groupname = groupname
                db.session.add(jroup)
                db.session.commit()
                group = Jroup.query.filter_by(groupname=groupname).first()
                id = group.id
                all_subject = []
                for i in subject_list:
                    subject = Subject.query.filter_by(id=i).first()
                    groupsubject = GroupSubject()
                    groupsubject.headline = subject.headline
                    groupsubject.text = subject.text
                    groupsubject.grade = subject.grade
                    groupsubject.level = subject.level
                    groupsubject.answer = subject.answer
                    groupsubject.subject_id = i
                    groupsubject.group_id = id
                    # groupsubject.game_id = game_id
                    db.session.add(groupsubject)
                    db.session.commit()
                    a = {"id":i,"headline":subject.headline,"text":subject.text,"grade":subject.grade,"level":subject.level,"answer":subject.answer}
                    all_subject.append(a)
                res = {
                    "data":{
                        "id":id,
                        "groupname":groupname,
                        "subject_list":all_subject
                    },
                    "msg": "Success",
                    "status": 200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/allSubject', methods=['GET', 'POST', 'PUT', 'DELETE'])        #管理员查询所有题目
def allSubject():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                subject = Subject.query.all()
                subject_list = []
                for i in subject:
                    id = i.id
                    headline = i.headline
                    grade = i.grade
                    text = i.text
                    answer = i.answer
                    level = i.level
                    a = {"id":id, "headline":headline, "grade":grade, "text":text, "answer":answer, "level":level}
                    subject_list.append(a)
                res = {
                    "data":{
                        "all_subject":subject_list
                    },
                    "msg": "Success",
                    "status": 200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/updateSubject', methods=['GET', 'POST', 'PUT', 'DELETE'])     #编辑题目
def updateSubject():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            id = data['id']
            headline = data['headline']
            text = data['text']
            answer = data['answer']
            grade = data['grade']
            level = data['level']
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                subject = Subject.query.filter_by(id=id).first()
                subject.headline = headline
                subject.text = text
                subject.answer = answer
                subject.grade = grade
                subject.level = level
                db.session.add(subject)
                db.session.commit()
                group_subject = GroupSubject.query.filter_by(subject_id=id).all()
                for i in group_subject:
                    i.headline = headline
                    i.text = text
                    i.answer = answer
                    i.grade = grade
                    i.level = level
                    db.session.add(i)
                    db.session.commit()
                res = {
                    "data":{
                        "id": id,
                        "headline": headline,
                        "text": text,
                        "answer": answer,
                        "grade": grade,
                        "level": level
                    },
                    "msg": "Success",
                        "status": 200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/deleteGroup', methods=['GET', 'POST', 'PUT', 'DELETE'])       #删除单个题目组
def deleteGroup():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            id = data["id"]
            token = redis_conn.get(username)
            if token1 == token:
                group_subject = GroupSubject.query.filter(GroupSubject.group_id==id).all()
                if group_subject != None:
                    for i in group_subject:
                        a = i.id
                        group_id = GroupSubject.query.get(a)
                        db.session.delete(group_id)
                        db.session.commit()
                    b = Jroup.query.get(id)
                    jroup = Jroup.query.filter_by(id=id).first()
                    if jroup != None:
                        groupname = jroup.groupname
                        db.session.delete(b)
                        db.session.commit()
                        res = {
                            "data":{
                                "id": id,
                                "groupname": groupname
                            },
                            "msg": "Success",
                                "status": 200
                        }
                        return json.dumps(res, ensure_ascii=False)
                    else:
                        res = {
                        "data": "null",
                        "msg": "题目组不存在",
                        "status": 200
                        }
                        return json.dumps(res, ensure_ascii=False)
                else:
                    c = Jroup.query.filter_by(id=id).first()
                    jroup = Jroup.query.get(id)
                    if jroup != None:
                        groupname = jroup.groupname
                        db.session.delete(c)
                        db.session.commit()
                        res = {
                            "data":{
                                "id": id,
                                "groupname": groupname
                            },
                            "msg": "Success",
                                "status": 200
                        }
                        return json.dumps(res, ensure_ascii=False)
                    else:
                        res = {
                        "data": "null",
                        "msg": "题目组不存在",
                        "status": 200
                        }
                        return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/showGroup',  methods=['GET', 'POST', 'PUT', 'DELETE'])        #获取所有题目组
def showGroup():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            token = redis_conn.get(username)
            if token1 == token:
                group = Jroup.query.all()
                if group != None:
                    jroup_list = []
                    for i in group:
                        sum = 0
                        id = i.id
                        groupname = i.groupname
                        a = {"id":id, "groupname":groupname}
                        jroup_list.append(a)
                        groupsubject = GroupSubject.query.filter_by(group_id=id).all()
                        for i in groupsubject:
                            sum += 1
                        a["sum"] = sum
                    res = {
                        "data": {
                            "all_group": jroup_list
                        },
                        "msg": "Success",
                        "status": 200
                    }
                    return json.dumps(res, ensure_ascii=False)
                else:
                    res = {"msg":"题目组为空","status":400}
                    return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
                return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/deleteGroupSubject', methods=['GET', 'POST', 'PUT', 'DELETE'])#删除题目组里面的题目
def deleteGroupSubject():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            group_id = data["group_id"]
            all_subject = data['all_subject']
            token = redis_conn.get(username)
            if token1 == token:
                # subject_list = []
                groupsubject = GroupSubject.query.filter_by(group_id=group_id, subject_id=all_subject).first()
                id = groupsubject.id
                headline = groupsubject.headline
                text = groupsubject.text
                answer = groupsubject.answer
                level = groupsubject.level
                grade = groupsubject.grade
                subject_id = groupsubject.subject_id
                groupsubject = GroupSubject.query.get(id)
                db.session.delete(groupsubject)
                db.session.commit()
                a = {"id":subject_id,"headline":headline,"text":text,"answer":answer,"level":level,"grade":grade}
                # subject_list.append(a)
                res = {
                    "data":{
                        "group_id":id,
                        "subject_list": a
                    },
                    "msg":"Success",
                    "status":200
                }
                return json.dumps(res,ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/deleteSubject', methods=['GET', 'POST', 'PUT', 'DELETE'])     #管理员删除单个题目
def deleteSubject():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            subject_id = data['subject_id']
            token = redis_conn.get(username)
            if token1 == token:
                groupsubject = GroupSubject.query.filter_by(subject_id=subject_id).all()
                if groupsubject != None:
                    for i in groupsubject:
                        id = i.id
                        a = GroupSubject.query.get(id)
                        db.session.delete(a)
                        db.session.commit()
                    event = Event.query.filter_by(subject_id=subject_id).all()
                    if event != None:
                        for j in event:
                            aa = j.id
                            b = Event.query.get(aa)
                            db.session.delete(b)
                            db.session.commit()
                    subject = Subject.query.filter_by(id=subject_id).first()
                    aaa= subject.id
                    h = subject.headline
                    t = subject.text
                    g = subject.grade
                    w = subject.answer
                    l = subject.level
                    c = Subject.query.get(aaa)
                    db.session.delete(c)
                    db.session.commit()
                    res = {
                        "data":{
                            "id":subject_id,
                            "headline":h,
                            "text":t,
                            "answer":w,
                            "grade":g,
                            "level":l
                        },
                        "msg":"Success",
                        "status":200
                    }
                    return json.dumps(res, ensure_ascii=False)
                else:
                    subject = Subject.query.filter_by(id=subject_id).first()
                    aaa= subject.id
                    h = subject.headline
                    t = subject.text
                    g = subject.grade
                    w = subject.answer
                    l = subject.level
                    c = Subject.query.get(aaa)
                    db.session.delete(c)
                    db.session.commit()
                    res = {
                        "data":{
                            "id":subject_id,
                            "headline":h,
                            "text":t,
                            "answer":w,
                            "grade":g,
                            "level":l
                        },
                        "msg":"Success",
                        "status":200
                    }
                    return json.dumps(res, ensure_ascii=False)
            else:
                event = Event.query.filter_by(subject_id=subject_id).all()
                if event != None:
                    for j in event:
                        aa = j.id
                        b = Event.query.get(aa)
                        db.session.delete(b)
                        db.session.commit()
                    subject = Subject.query.filter_by(id=subject_id).first()
                    aaa= subject.id
                    h = subject.headline
                    t = subject.text
                    g = subject.grade
                    w = subject.answer
                    l = subject.level
                    c = Subject.query.get(aaa)
                    db.session.delete(c)
                    db.session.commit()
                    res = {
                        "data":{
                            "id":subject_id,
                            "headline":h,
                            "text":t,
                            "answer":w,
                            "grade":g,
                            "level":l
                        },
                        "msg":"Success",
                        "status":200
                    }
                    return json.dumps(res, ensure_ascii=False)
                else:
                    subject = Subject.query.filter_by(id=subject_id).first()
                    aaa= subject.id
                    h = subject.headline
                    t = subject.text
                    g = subject.grade
                    w = subject.answer
                    l = subject.level
                    c = Subject.query.get(aaa)
                    db.session.delete(c)
                    db.session.commit()
                    res = {
                        "data":{
                            "id":subject_id,
                            "headline":h,
                            "text":t,
                            "answer":w,
                            "grade":g,
                            "level":l
                        },
                        "msg":"Success",
                        "status":200
                    }
                    return json.dumps(res, ensure_ascii=False)
        else:
            res = {
                "data": "null",
                "msg": "token不可用",
                "status": 403
            }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/onegroup', methods=['GET', 'POST', 'PUT', 'DELETE'])          #获取单个题目组中的全部题目
def onegroup():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            username = data["username"]
            group_id = data['group_id']
            token = redis_conn.get(username)
            if token1 == token:
                groupsubject = GroupSubject.query.filter_by(group_id=group_id).all()
                subject_list = []
                for i in groupsubject:
                    subject_id = i.subject_id
                    headline = i.headline
                    text = i.text
                    answer = i.answer
                    grade = i.grade
                    level = i.level
                    a = {"subject_id":subject_id,"headline":headline,"text":text,"answer":answer,"grade":grade,"level":level}
                    subject_list.append(a)
                res = {
                    "data":{
                        "subject_list":subject_list
                    },
                    "msg":"Success",
                    "status":200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/setGameid', methods=['GET', 'POST', 'PUT', 'DELETE'])         #题目组设置比赛ID
def set_game():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            username = data["username"]
            game_id = data['game_id']
            group_id = data['group_id']
            token1 = data["token"]
            token = redis_conn.get(username)
            if token1 == token:
                groupid = GroupSubject.query.filter_by(game_id=game_id).all()
                for i in groupid:
                    i.game_id = None
                    db.session.add(i)
                    db.session.commit()
                groupsubject = GroupSubject.query.filter_by(group_id=group_id).all()
                for i in groupsubject:
                    i.game_id = game_id
                    db.session.add(i)
                    db.session.commit()
                    group = Jroup.query.filter_by(id=i.group_id).first()
                    groupname = group.groupname
                res = {
                    "data":{
                        "game_id": game_id,
                        "group_id": group_id,
                        "groupname":groupname
                    },
                    "msg":"Success",
                    "status":200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/addsubject', methods=['GET', 'POST', 'PUT', 'DELETE'])        #在题目组里面添加题目
def addsubject():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            username = data["username"]
            group_id = data['group_id']
            subject_list = data["subject_list"]
            token1 = data["token"]
            token = redis_conn.get(username)
            if token1 == token:
                groupsub_list = []
                for i in subject_list:
                    subject = Subject.query.filter_by(id=i).first()
                    groupsubject = GroupSubject()
                    groupsubject.headline = subject.headline
                    groupsubject.text = subject.text
                    groupsubject.subject_id = i
                    groupsubject.grade = subject.grade
                    groupsubject.answer = subject.answer
                    groupsubject.level = subject.level
                    groupsubject.group_id = group_id
                    db.session.add(groupsubject)
                    db.session.commit()
                    a = {"subject_id":groupsubject.subject_id,"headline":groupsubject.headline,"text":groupsubject.text,"grade":groupsubject.grade,"answer":groupsubject.answer,"level":groupsubject.level,"group_id":group_id}
                    groupsub_list.append(a)
                res = {
                    "data":{
                        "subject_list":groupsub_list
                    },
                    "msg":"Success",
                    "status":200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/startGame', methods=['GET', 'POST', 'PUT', 'DELETE'])         #开始比赛
def start_game():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            username = data["username"]
            game_id = data['game_id']
            token1 = data["token"]
            token = redis_conn.get(username)
            if token1 == token:
                game = Game.query.filter_by(gameid=game_id).first()
                game.status = 1
                db.session.add(game)
                db.session.commit()
                res = {
                    "data":{
                        "game_id": game.gameid,
                        "game_name": game.name,
                        "people": game.people,
                        "game_status": game.status,
                        "falsedelete": game.falsedelete
                    },
                    "msg":"Success",
                    "status":200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@admin_bp.route('/stopGame', methods=['GET', 'POST', 'PUT', 'DELETE'])         #暂停比赛
def stop_game():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            username = data["username"]
            game_id = data['game_id']
            token1 = data["token"]
            token = redis_conn.get(username)
            if token1 == token:
                game = Game.query.filter_by(gameid=game_id).first()
                game.status = 2
                db.session.add(game)
                db.session.commit()
                res = {
                    "data":{
                        "game_id": game.gameid,
                        "game_name": game.name,
                        "people": game.people,
                        "game_status": game.status,
                        "falsedelete": game.falsedelete
                    },
                    "msg":"Success",
                    "status":200
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "token不可用",
                    "status": 403
                }
            return json.dumps(res, ensure_ascii=False)
        return "请用post请求"
    except:
        res = {"status": 404, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)
