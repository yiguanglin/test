from ast import Sub
import base64
from codecs import getreader
import hashlib
import random,json,jwt,time
from unittest import result
from typing_extensions import dataclass_transform

from flask import Blueprint, request, render_template, redirect, url_for, jsonify

from apps.admin.models import Admin, Game, Score, Subject
from apps.user.models import User
from exts import db
from sqlalchemy import desc

from apps.user.view import token

subject_bp = Blueprint('subject', __name__)


def get_token():
    global token
    # 生成一个字典，包含我们的具体信息
    d = {
        # 公共声明
        'exp':time.time()+86400000, # (Expiration Time) 此token的过期时间的时间戳 86400000毫秒=1天
        'iat':time.time(), # (Issued At) 指明此创建时间的时间戳
        'iss':'Issuer', # (Issuer) 指明此token的签发者
        
        # 私有声明
        'data':{
            'username':'zzz',
            'timestamp':time.time()
        }
    }

    token = jwt.encode(d,'JXYYJSZYXY',algorithm='HS256')
    return token

@subject_bp.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ



