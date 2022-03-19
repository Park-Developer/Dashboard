from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort
import cv2
import zmq
import base64
import numpy as np

from bot_dash import page_status  



bp = Blueprint('test', __name__)

@bp.route('/Test/test_index')
def index_setting(): # index화면 구성 함수

    #return render_template('index.html')
    is_commu_connect=False
    Robot_IP=page_status["login_part"]["Robot_IP"]
    return render_template('/Test/test_index.html',is_commu_connect=is_commu_connect,Robot_IP=Robot_IP)
    
def tcp_test():
    print("tcp_test")
    # IP 주소 입력받고 연결 확인

def sensor_test():
    print("sensor_test")
    # IP 주소 입력받고 연결 확인


def motor_test():
    print("motor_test")
    # IP 주소 입력받고 연결 확인

def camera_test():
    print("camera_test")


def gen_frames():  # generate frame by frame from camera
    # Mode Decision
    self_mode=False

    if self_mode==True:
        camera = cv2.VideoCapture(0)
        while True:
            # Capture frame-by-frame
            success, frame = camera.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    else:
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.bind('tcp://192.168.219.152:5555')
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

        while True:
            print("camera loading")
            try:
                frame1 = footage_socket.recv_string()
                print(frame)
                img = base64.b64decode(frame1)
                npimg = np.fromstring(img, dtype=np.uint8)
                frame = cv2.imdecode(npimg, 1)
                ###
                #cv2.imshow("Stream", source)
                #cv2.waitKey(1)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # conat f

            except:
                print("Err!")
                cv2.destroyAllWindows()
                break


@bp.route('/Test/Camera/video_stream/')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/Test/<index_button>/',methods=['POST'])
def index_btn_click(index_button): # index화면 구성 함수
    if index_button=="tcp_test":
        print("request test",request.get_data())
   
        #print("chck",request.is_json)
        
        #print("req debug3",request.form['button'])
       
        tcp_test()
        selected_test="communication"
    elif index_button=="motor_test":
        selected_test="motor"
        motor_test()
    else:
        selected_test="None"
    #return redirect("/")#(request.url)
    
    return render_template('/Test/test_index.html',selected_test=selected_test)

# Communication Test Display
@bp.route('/Test/selected_test/<select_test>/',methods=['POST'])
def display_test_setting(select_test): # index화면 구성 함수
    if select_test=="commu":

        print("button",request.get_data())
        is_commu_connect=True
    elif select_test=="cancel":
        print("cancel btn click!")

        is_commu_connect=False
    return render_template('/Test/test_index.html',is_commu_connect=is_commu_connect)


# Motor Test Display
@bp.route('/Test/selected_test/motor/control/<direction>/',methods=['POST'])
def motor_ctrl(direction):
    selected_test="motor"
    selected_direction=direction
    
    return render_template('/Test/test_index.html',selected_direction=selected_direction,selected_test=selected_test)