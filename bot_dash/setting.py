from os import truncate
from re import T
from syslog import LOG_NOTICE
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import sqlite3
from bot_dash import page_status  

import socket 

bp = Blueprint('setting', __name__)

@bp.route("/Setting/setting_index") # Setting main
def setting_index():
    
    # N : 초기 설정 정보는 외부 파일에서 옵로드 하게 하기

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
    '''

    # [Com1 Check]
    is_connect1=page_status["setting_part"]["is_Com1_conOK"]
    input_ip1=page_status["setting_part"]["Com1_ip"]

    # [Com2 Check2]
    is_connect2=page_status["setting_part"]["is_Com2_conOK"]
    input_ip2=page_status["setting_part"]["Com2_ip"]

 
    return render_template('Setting/setting_index.html',is_connect1=is_connect1,input_ip1=input_ip1,
        is_connect2=is_connect2,input_ip2=input_ip2)
    

def click_register_Btn():
    print("register btn click!")

    is_loginOK=True # 일단 모든 조건 True로 설정
    return is_loginOK


def click_TCP_connect(com_id:int):
    # Com id Check
    if (com_id!=1 and com_id!=2):
        return False, "Unavailable IP"
    
    # IP Check
    print("COM{com_id} IP : {input_ip}".format(com_id=com_id, input_ip=request.get_data().decode('ascii')))

    # TCP Connection
    try:
        recv_data=request.get_data().decode('ascii')
        tmp=recv_data.split("=")
        input_ip=tmp[1]

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect((input_ip, 9008))
        sock.send(page_status["message"]["TCP_test"]["tcp_connection_request"].encode()) # 내가 전송할 데이터를 보냄.

        tcp_recv=sock.recv(65535)
    except Exception as tcp_Err:
        print('[Setting] TCP Connection Error : ', tcp_Err)
        return False, "Connection Fail"


    if (tcp_recv.decode()==page_status["message"]["TCP_test"]["tcp_connection_respond"]): # connection Success
        if (com_id==1):
            page_status["setting_part"]["Com1_ip"]=input_ip
            page_status["setting_part"]["is_Com1_conOK"]=True
        elif (com_id==2):
            page_status["setting_part"]["Com2_ip"]=input_ip
            page_status["setting_part"]["is_Com2_conOK"]=True
            
        return True, input_ip

    else: 
        return False, "Connection Fail"

def click_TCP_disconnect(com_id:int):
    if (com_id==1):
        page_status["setting_part"]["Com1_ip"]=""
        page_status["setting_part"]["is_Com1_conOK"]=""
    elif (com_id==2):
        page_status["setting_part"]["Com2_ip"]=""
        page_status["setting_part"]["is_Com2_conOK"]=""


@bp.route("/Setting/Communication/<Com_button>/",methods=['POST'])
def click_communication_btn(Com_button):
    # < COM1 URL Handling >
    if Com_button=="Com1_connect":
        # Com1값 변경
        is_connect1,input_ip1=click_TCP_connect(com_id=1)

        # Com2는 현재값 그대로 return
        is_connect2=page_status["setting_part"]["is_Com2_conOK"]
        input_ip2=page_status["setting_part"]["Com2_ip"]

        return render_template('Setting/setting_index.html',is_connect1=is_connect1,input_ip1=input_ip1,is_connect2=is_connect2,input_ip2=input_ip2)
    
    elif Com_button=="Com1_disconnect":
        click_TCP_disconnect(com_id=1)

        # Com2는 현재값 그대로 return
        is_connect2=page_status["setting_part"]["is_Com2_conOK"]
        input_ip2=page_status["setting_part"]["Com2_ip"]

        return render_template('Setting/setting_index.html',is_connect1=False,is_connect2=is_connect2,input_ip2=input_ip2)
    
    # < COM2 URL Handling >
    elif Com_button=="Com2_connect":
        # Com2값 변경
        is_connect2,input_ip2=click_TCP_connect(com_id=2)

        # Com1은 현재값 그대로 return 
        is_connect1=page_status["setting_part"]["is_Com1_conOK"]
        input_ip1=page_status["setting_part"]["Com1_ip"]

        return render_template('Setting/setting_index.html',is_connect1=is_connect1,input_ip1=input_ip1,is_connect2=is_connect2,input_ip2=input_ip2)
    
    elif Com_button=="Com2_disconnect":
        click_TCP_disconnect(com_id=2)

        # Com1는 현재값 그대로 return
        is_connect1=page_status["setting_part"]["is_Com1_conOK"]
        input_ip1=page_status["setting_part"]["Com1_ip"]

        return render_template('Setting/setting_index.html',is_connect1=is_connect1,input_ip1=input_ip1,is_connect2=False)

    else:
        return redirect("/")

    