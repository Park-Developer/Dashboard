import os
from flask import Flask, render_template, request, redirect
import datetime

# 2022.03.15. 작업
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db=SQLAlchemy()
migrate=Migrate()

page_status={
    "login_part":{
        "is_loginOK":False,
        "User_ID":" ",
        "User_IP":" ",
    },

    "setting_part":{
        "is_Com1_conOK":False, # Com1 통신 연결 유무
        "is_Com2_conOK":False, # Com2 통신 연결 유무
        "Com1_ip":" ",
        "Com2_ip":" ",
    }
}

def create_app(test_config=None): # Application 및 blueprint 등록 함수
    # create and configure the app
    print('################### Restarting : ', datetime.datetime.now(), '###################')
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path,'dashboard.sqlite'),
            )

    # configuring
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        print("app.instance_path", app.instance_path)
    except OSError:
        pass

    # 2022.03.15 수정
    # origianl code
    #from . import db
    #db.init_app(app)
    # ---
    # revision code
    app.config.from_object(config) # Q ?
    db.init_app(app) # init_app 메서드를 이요한 초기화
    migrate.init_app(app,db)
    from . import models


    from . import auth
    app.register_blueprint(auth.bp)

    #from . import blog
    #app.register_blueprint(blog.bp)
    #app.add_url_rule('/',endpoint='index')

    # Add dashboard 2022.02.03
    from . import dashboard
    app.register_blueprint(dashboard.bp)

    from . import setting
    app.register_blueprint(setting.bp)
    
    from . import test
    app.register_blueprint(test.bp)

    from . import index
    app.register_blueprint(index.bp)


    return app
