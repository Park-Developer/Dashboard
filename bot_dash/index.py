from flask import (
    Blueprint, flash, g, make_response, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import sqlite3

from bot_dash import page_status  

bp = Blueprint('index', __name__)

@bp.route("/") # Setting main
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
    #is_loginOK=False # login 여부
    #page_status["is_loginOK"]=False
    return render_template('index.html',is_loginOK=page_status["login_part"]["is_loginOK"],is_user_empty=is_user_empty,user_db_data=user_db_data)
    


def click_login_Btn(): #is_loginOK=True # 데모용 모든 조건 True로 설정
    print("login btn click!")
    print("url_for inde",request.get_data())
    recv_data=request.get_data().decode('ascii')
    tmp=recv_data.split("&")
    
    user_id=tmp[0].split("=")[1]
    user_ip=tmp[1].split("=")[1]

    # 전역 변수 저장
    page_status["login_part"]["is_loginOK"]=True
    page_status["login_part"]["User_ID"]=user_id
    page_status["login_part"]["User_IP"]=user_ip

    return True, user_id, user_ip

def click_logout_Btn():
    print("logout btn click!")

    page_status["login_part"]["is_loginOK"]=False # 일단 모든 조건 True로 설정
    page_status["login_part"]["User_ID"]=""
    page_status["login_part"]["User_IP"]=""
    user_id=""
    user_ip=""
    
    return False, user_id, user_ip

@bp.route("/User/<user_btn>/",methods=['POST'])
def click_user_btn(user_btn):
    if user_btn=="Login":
        is_loginOK,user_id, user_ip=click_login_Btn()
    elif user_btn=="Logout":
        is_loginOK,user_id, user_ip=click_logout_Btn()
      
    #response=make_response(render_template('index.html',is_loginOK=is_loginOK))
    #response.mimetype="text/html"
    return render_template('index.html',is_loginOK=is_loginOK,user_id=user_id, user_ip=user_ip)
    #return redirect(location=url_for('index.setting_index'),code=302,Response=response)