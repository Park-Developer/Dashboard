from os import truncate
from re import T
from syslog import LOG_NOTICE
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import sqlite3
from bot_dash import page_status  

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
    print("INPUT IP1",request.get_data().decode('ascii'))
    recv_data=request.get_data().decode('ascii')
    tmp=recv_data.split("=")
    input_ip1=tmp[1]
    
    #
    #Check Logic
    #
    
    # IF IP is Available
    page_status["setting_part"]["Com1_ip"]=input_ip1
    page_status["setting_part"]["is_Com1_conOK"]=True

    return True, input_ip1

def click_com2():
    print("INPUT IP2",request.get_data().decode('ascii'))
    recv_data=request.get_data().decode('ascii')
    tmp=recv_data.split("=")
    input_ip2=tmp[1]
    
    #
    #Check Logic
    #

    # IF IP is Available
    page_status["setting_part"]["Com2_ip"]=input_ip2
    page_status["setting_part"]["is_Com2_conOK"]=True

    return True, input_ip2

@bp.route("/Setting/Communication/<Com_button>/",methods=['POST'])
def click_communication_btn(Com_button):
    # < COM1 URL Handling >
    if Com_button=="Com1_connect":
        is_connect1,input_ip1=click_com1()
        print("gg",input_ip1)
        return render_template('Setting/setting_index.html',is_connect1=is_connect1,input_ip1=input_ip1)
    elif Com_button=="Com1_disconnect":
        return render_template('Setting/setting_index.html',is_connect1=False)
    
    # < COM2 URL Handling >
    elif Com_button=="Com2_connect":
        is_connect2,input_ip2=click_com2()
        return render_template('Setting/setting_index.html',is_connect2=is_connect2,input_ip2=input_ip2)
    elif Com_button=="Com2_disconnect":
        return render_template('Setting/setting_index.html',is_connect2=False)

    else:
        return redirect("/")

    