# import datetime
from datetime import datetime

from exts import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


    def __str__(self):
        return self.username





class Score(db.Model):      #得分表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result = db.Column(db.Integer, default=0)   #个人总得分
    accomplish = db.Column(db.Integer, default=0)   #完成的题目
    game_id = db.Column(db.Integer, db.ForeignKey('game.gameid'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   #设置与用户的外键
    usera = db.relationship('User', backref='scores')

    def __str__(self):
        return self.result


class Subject(db.Model):        #  题目表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    headline = db.Column(db.String(255), nullable=False)        #题目标题
    text = db.Column(db.String(20000), nullable=False)            #题目正文
    answer = db.Column(db.String(255))                          #题目答案
    grade = db.Column(db.Integer, default=0)                    #题目得分
    level = db.Column(db.Integer)                          #题目的难度等级


    def __str__(self):
        return self.headline



class Event(db.Model):      # 得分事件表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    headline = db.Column(db.String(255))
    grade = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.gameid'))

    def __str__(self):
        return self.headline



class Game(db.Model):
    gameid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    time = db.Column(db.DateTime, default=datetime.now)
    people = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0)
    falsedelete = db.Column(db.Boolean, default=False)
    user_test = db.relationship('User', backref='game')


    def __str__(self):
        return self.status


class Jroup(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    groupname = db.Column(db.String(255))
    groupsubject = db.relationship('GroupSubject', backref='jroup')
    def __str__(self):
        return self.groupname

class GroupSubject(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    headline = db.Column(db.String(255))  # 题目标题
    text = db.Column(db.String(255))  # 题目正文
    answer = db.Column(db.String(255))  # 题目答案
    grade = db.Column(db.Integer, default=0)  # 题目得分
    level = db.Column(db.Integer)  # 题目的难度等级
    subject_id = db.Column(db.Integer,db.ForeignKey('subject.id'),nullable=False)
    group_id = db.Column(db.Integer,db.ForeignKey("jroup.id"),nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.gameid'))

    def __str__(self):
        return self.headline
