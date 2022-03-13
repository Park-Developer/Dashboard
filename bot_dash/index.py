from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('index', __name__)

@bp.route('/')
def index_setting(): # index화면 구성 함수

    return render_template('index.html')

def tcp_test():
    print("tcp_test")
    # IP 주소 입력받고 연결 확인

def sensor_test():
    print("sensor_test")
    # IP 주소 입력받고 연결 확인


def motor_test():
    print("motor_test")
    # IP 주소 입력받고 연결 확인



@bp.route('/<index_button>/',methods=['POST'])
def index_btn_click(index_button): # index화면 구성 함수
    if index_button=="tcp_test":
        print("request test",request.get_data(),type(request))
        print("req debug1",request.form)
        print("req debug2",request.files)
        print("req debug3",request.data)
        print("mimeyrpe",request.accept_mimetypes)
        test_obj=request.get_json()
        print("req debug4",test_obj,type(test_obj))
        print("req debug4",type(request.json))
        #print("chck",request.is_json)
        
        #print("req debug3",request.form['button'])
       
        tcp_test()
    elif index_button=="sensor_test":
        sensor_test()
    elif index_button=="motor_test":
        motor_test()
    
    #return redirect("/")#(request.url)
    return render_template('index.html',index_button=index_button)