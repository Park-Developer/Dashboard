from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import sqlite3

bp = Blueprint('setting', __name__)

@bp.route("/Setting/setting_index") # Setting main
def setting_index():
    '''
    초기 설정 정보는 외부 파일에서 옵로드 하게 하기

    '''
    # fetching from 'user' table 
    connect=sqlite3.connect("pybo.db")
    cur=connect.cursor()
    cur.execute("SELECT * FROM user")
    user_db_data=cur.fetchall()
    #print(user_db_data)
    if (user_db_data==[]): # 등록된 데이터가 없는 경우
        is_user_empty=True
    else:
        is_user_empty=False
    
    connect.close()
    is_loginOK=False # login 여부

    return render_template('Setting/setting_index.html',is_loginOK=is_loginOK,is_user_empty=is_user_empty,user_db_data=user_db_data)
    

def click_register_Btn():
    print("register btn click!")

    is_loginOK=True # 일단 모든 조건 True로 설정
    return is_loginOK

def click_login_Btn():
    print("login btn click!")

    is_loginOK=True # 일단 모든 조건 True로 설정
    return is_loginOK

def click_logout_Btn():
    print("logout btn click!")

    is_loginOK=False # 일단 모든 조건 True로 설정
    return is_loginOK

@bp.route("/Setting/User/<user_btn>/",methods=['POST'])
def click_user_btn(user_btn):
    if user_btn=="Register":
        is_loginOK=click_register_Btn()
    elif user_btn=="Login":
        is_loginOK=click_login_Btn()
    elif user_btn=="Logout":
        is_loginOK=click_logout_Btn()

    return render_template('Setting/setting_index.html',is_loginOK=is_loginOK)

def click_com1():
    is_connect1=True
    return is_connect1

def click_com2():
    is_connect2=True
    return is_connect2
    

@bp.route("/Setting/Communication/<Com>/",methods=['POST'])
def click_communication_btn(Com):
    if Com=="Com1":
        is_connect1=click_com1()
        return render_template('Setting/setting_index.html',is_connect1=is_connect1)
    elif Com=="Com2":
        is_connect2=click_com2()
        return render_template('Setting/setting_index.html',is_connect2=is_connect2)


    