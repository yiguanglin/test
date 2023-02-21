import hashlib
import json
# from datetime import time
import time

import jwt
import redis
from flask import Blueprint, render_template, request, redirect, url_for

from flask import Flask
import random

from sqlalchemy import desc

from apps.admin.models import Admin, Game, GroupSubject, Subject, Score, Event
from apps.user.models import User
from exts import db

user_bp = Blueprint('user', __name__,url_prefix="/user")

redis_conn= redis.Redis(host='172.16.100.151', port= 6379, password= 'Huawei@123',db =0,decode_responses=True)

#生成token
def get_token():
    # 生成一个字典，包含我们的具体信息
    d = {
        # 公共声明
        'exp': time.time() + 86400000,  # (Expiration Time) 此token的过期时间的时间戳 86400000毫秒=1天
        'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
        'iss': 'JXYYJSZYXY',  # (Issuer) 指明此token的签发者

        # 私有声明
        'data': {
            'username': 'XXGCXY',
            'timestamp': time.time()
        }
    }

    token = jwt.encode(d, 'JXYYJSZYXY', algorithm='HS256')
    return token

#跨域
@user_bp.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

#用户登入
@user_bp.route('/login', methods=['GET', "POST", "PUT", "DELETE"])  # 用户登录
def login():
    # try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            hashcode = data["hashcode"]
            code = User.query.filter_by(hash=hashcode, falsedelete="False").first()
            if code:
                game_status = code.game.status
                if game_status == 1 or game_status == 2:
                    aaa = redis_conn.get(hashcode)
                    if aaa == None:
                        redis_conn.set(hashcode, get_token(), ex=86400)
                        token = redis_conn.get(hashcode)
                        res = {
                            "data": {
                                "id": code.id,
                                "hashcode": hashcode,
                                "status": code.status,
                                "falsedelete": code.falsedelete,
                                "game_id": code.game_id,
                                "token": token
                            },
                            "msg": "Success",
                            "status": 200
                        }
                        return json.dumps(res, ensure_ascii=False)
                    else:
                        token = redis_conn.get(hashcode)
                        res = {
                            "data": {
                                "id": code.id,
                                "hashcode": hashcode,
                                "status": code.status,
                                "falsedelete": code.falsedelete,
                                "game_id": code.game_id,
                                "token": token
                            },
                            "msg": "Success",
                            "status": 200
                        }
                        return json.dumps(res, ensure_ascii=False)
                else:
                    res = {
                            "data": {
                                "id": code.id,
                                "hashcode": hashcode,
                                "status": code.status,
                                "falsedelete": code.falsedelete,
                                "game_id": code.game_id,
                            },
                            "msg": "比赛未开始!",
                            "status": 200
                        }
                    return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "data": "null",
                    "msg": "hash输入错误",
                    "status": 400
                }
                return json.dumps(res, ensure_ascii=False)
    #     return "请用post请求"
    # except:
    #     res = {"status": 400, "msg": "缺少所需参数!"}
    #     return json.dumps(res, ensure_ascii=False)


#用户编辑名字
@user_bp.route('/updateName', methods=['GET', "POST", "PUT", "DELETE"])  # 用户编辑用户名
def update_username():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            id = data["id"]
            username = data["username"]
            token1 = data["token"]
            hashcode = data["hashcode"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                user_id = User.query.filter_by(id=id).first()
                user_id.username = username
                user_id.status = "wating"
                db.session.add(user_id)
                db.session.commit()
                status = user_id.status
                res = {
                    "data": {
                        "id": id,
                        "username": username,
                        "status": status
                    },
                    "msg": "用户名待审核状态",
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
        return '请使用post请求'
    except:
        res = {"status": 400, "msg": "缺少所需参数!"}
        return json.dumps(res, ensure_ascii=False)


@user_bp.route('/userSubject', methods=['POST', 'GET', 'PUT', 'DELETE'])  # 用户获取题目
def userSubject():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            hashcode = data["hashcode"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                subject_list = []
                user = User.query.filter_by(hash=hashcode).first()
                game_id = user.game_id
                group_list = GroupSubject.query.filter_by(game_id=game_id).all()
                for i in group_list:
                    id = i.subject_id
                    headline = i.headline
                    text = i.text
                    answer = i.answer
                    grade = i.grade
                    level = i.level
                    sub = {"id": id, "headline": headline, "text": text, "answer": answer, "grade": grade,
                           "level": level}
                    subject_list.append(sub)
                res = {
                    "data": {
                        "subject_list": subject_list
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


@user_bp.route('/allUser', methods=['GET', 'POST', 'PUT', 'DELETE'])  # 查询所有用户名
def modify_username():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            hashcode = data["hashcode"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                user = User.query.filter_by(hash=hashcode, falsedelete="False").all()
                user_list = []
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
                        "username": username,
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


@user_bp.route('/rankingList', methods=['GET', 'POST', 'PUT', 'DELETE'])  # 用户排行榜
def ranking_list():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            game_id = data["game_id"]
            hashcode = data["hashcode"]
            token = redis_conn.get(hashcode)
            if token1 == token:
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
                            "all_score": ranking[:30]
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


@user_bp.route('/post_answer', methods=['GET', 'POST', 'PUT', 'DELETE'])  # 提交答案
def get_score():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            id = data["id"]
            user_id = data["user_id"]
            game_id = data["game_id"]
            headline = data["headline"]
            answer = data["answer"]
            grade = int(data["grade"])
            token1 = data["token"]
            hashcode = data["hashcode"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                game = Game.query.filter_by(gameid=game_id).first()
                if game.status == 1: 
                    subject = Subject.query.filter_by(id=id, answer=answer).first()
                    event = Event()
                    if subject != None:
                        score = Score.query.filter_by(user_id=user_id).first()
                        result = score.result + subject.grade
                        accomplish = score.accomplish + 1
                        score.result = result
                        score.accomplish = accomplish
                        event.headline = headline
                        event.grade = subject.grade
                        event.subject_id = id
                        event.user_id = user_id
                        event.game_id = game_id
                        db.session.add(event)
                        db.session.add(score)
                        db.session.commit()
                        res = {
                            "data": {
                                "id": score.id,
                                "user_id": score.user_id,
                                "game_id": score.game_id,
                                "result": score.result,
                                "accomplish": score.accomplish,
                            },
                            "msg": "提交答案正确",
                            "status": 200
                        }
                        return json.dumps(res, ensure_ascii=False)
                    else:
                        event.headline = headline
                        event.grade = 0
                        event.subject_id = id
                        event.user_id = user_id
                        event.game_id = game_id
                        db.session.add(event)
                        db.session.commit()
                        res = {
                            "data": "null",
                            "msg": "提交答案不正确",
                            "status": 404
                        }
                        return json.dumps(res, ensure_ascii=False)
                else:
                    score = Score.query.filter_by(user_id=user_id).first()
                    res = {
                            "data": {
                                "id": score.id,
                                "user_id": score.user_id,
                                "game_id": score.game_id,
                                "result": score.result,
                                "accomplish": score.accomplish,
                            },
                            "msg": "比赛暂停,不可提交答案",
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


@user_bp.route('/event', methods=['GET', 'POST', 'PUT', 'DELETE'])      #获取所有得分事件
def get_event():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            game_id = data["game_id"]
            token1 = data["token"]
            hashcode = data["hashcode"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                event_list = []
                event = Event.query.filter_by(game_id=game_id).all()
                for i in event:
                    id = i.id
                    headline = i.headline
                    grade = i.grade
                    time = str(i.time)
                    subject_id = i.subject_id
                    user_id = i.user_id
                    user = User.query.filter_by(id=user_id).first()
                    eve = {"id": id, "headline": headline, "grade": grade, "time": time, "subject_id": subject_id,
                           "user_id": user_id,"username":user.username}
                    event_list.append(eve)
                all_event = sorted(event_list, key=lambda x: x['id'], reverse=True)
                res = {
                    "data": {
                        "all_event": all_event
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


@user_bp.route('/completeID', methods=['GET', 'POST', 'PUT', 'DELETE'])
def completeID():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            hashcode = data["hashcode"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                user = User.query.filter_by(hash=hashcode).first()
                user_id = user.id
                event = Event.query.filter(Event.user_id==user_id,Event.grade!=0).all()
                id_list = []
                for i in event:
                    subject_id = i.subject_id
                    id_list.append(subject_id)
                res = {
                    "data":{
                        "subject_id":id_list
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


@user_bp.route('/usergrade', methods=['GET', 'POST', 'PUT', 'DELETE'])
def usergrade():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            hashcode = data["hashcode"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                user = User.query.filter_by(hash=hashcode).first()
                id = user.id
                score = Score.query.filter_by(user_id=id).first()
                result = score.result
                res = {
                    "data":{
                        "result":result
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


@user_bp.route('/userThing', methods=['GET', 'POST', 'PUT', 'DELETE'])          #个人得分事件
def userThing():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            token1 = data["token"]
            hashcode = data["hashcode"]
            user_id = data["user_id"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                event = Event.query.filter_by(user_id=user_id).all()
                event_list = []
                for i in event:
                    id = i.id
                    headline = i.headline
                    grade = i.grade
                    time = str(i.time)
                    subject_id = i.subject_id
                    user_id = i.user_id
                    game_id = i.game_id
                    user = User.query.filter_by(id=user_id).first()
                    eve = {"id": id, "headline": headline, "grade": grade, "time": time, "subject_id": subject_id,
                           "user_id": user_id, "game_id": game_id,"username":user.username}
                    event_list.append(eve)
                user_event = sorted(event_list, key=lambda x: x['id'], reverse=True)
                res = {
                    "data": {
                        "subject_list": user_event
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


@user_bp.route('/stopGame', methods=['GET', 'POST', 'PUT', 'DELETE'])         #暂停比赛
def stop_game():
    try:
        if request.method == 'POST':
            data = request.get_data()
            data = str(data, encoding='utf-8')
            data = json.loads(data)
            hashcode = data["hashcode"]
            game_id = data['game_id']
            token1 = data["token"]
            token = redis_conn.get(hashcode)
            if token1 == token:
                game = Game.query.filter_by(gameid=game_id).first()
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
