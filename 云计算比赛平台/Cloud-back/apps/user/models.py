# 创建类来映射表


from exts import db
# from school02.apps.admin.models import Score

class User(db.Model):       #用户表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # game_id = db.Column(db.Integer, nullable=False)     #某一场比赛的id
    hash = db.Column(db.String(255), nullable=False)    #登入产生的哈希值
    username = db.Column(db.String(255))   #选手对应的名字
    status = db.Column(db.String(255), default='init')                           #名字的审核状态
    falsedelete = db.Column(db.Boolean, default=False)                #是否要删除
    game_id = db.Column(db.Integer,db.ForeignKey('game.gameid'),nullable=False)   #某一场比赛的id
    score = db.relationship('Score', backref='user')
    event = db.relationship('Event', backref='user')
    # score_id = db.Column(db.Integer,db.ForeignKey('score.id'),nullable=False)   #某一场比赛的id


    def __str__(self):
        return self.username
