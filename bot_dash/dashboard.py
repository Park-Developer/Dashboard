import functools
from re import A
from flask import Flask, render_template, Response, render_template_string
import cv2
import socket

# for map
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


# for real time graph
import time
from matplotlib import pyplot as plt
from matplotlib import animation

# map function
import bot_dash.tool_func.map_func as map_func 

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for

)

from werkzeug.security import check_password_hash, generate_password_hash

from bot_dash.db import get_db

bp=Blueprint('dashboard', __name__,url_prefix='/dashboard')

@bp.route('/monitoring')
def monitoring(): 
    return render_template('dashboard/dashboard.html')

def gen_frames():  # generate frame by frame from camera
    camera = cv2.VideoCapture(0)  # use 0 for web camera
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

@bp.route('/video_feed')
def camera_run():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1) # add_subplot(nrows, ncols, index, **kwargs)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

import base64
@bp.route('/animation.png')
def ani_png():
    return Response(create_grpa(), mimetype='multipart/x-mixed-replace; boundary=frame')

def create_grpa():
    xs=[]
    ys=[]
    t=0
    motion_para={
    "x_origin":0, # Robot X-dir origin
    "y_origin":0, # Robot Y-dir origin
    "x_upper_limit":50,
    "x_lower_limit":0,
    "y_upper_limit":50,
    "y_lower_limit":0,
    }

    while True: # debug mode
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1) # add_subplot(nrows, ncols, index, **kwargs)
        
        output = io.BytesIO()
        time.sleep(1)
        x_move=0 # move dist debug
        y_move=0 # move dist debug
        t=t+1 # dehub sensor data
        if t%7==0:
            x_move=10
            motion_para["x_origin"]=motion_para["x_origin"]+x_move
        xs.append(motion_para["x_origin"]+t)
        ys.append(motion_para["y_origin"]+t*2)

        map_func.set_range(x_move,y_move,motion_para)

        axis.set_xlim(motion_para["x_lower_limit"],motion_para["x_upper_limit"])
        axis.set_ylim(motion_para["y_lower_limit"],motion_para["y_upper_limit"])
        
        axis.scatter(xs, ys)
        FigureCanvas(fig).print_png(output)
        print("xs ys ",xs,ys)
        yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + output.getvalue() + b'\r\n')


@bp.route('/sensor_monitor')
def read_sensor():
    '''
    1. UDP 통신을 이용해서 Sensor 데이터 수신(Server)
    2. 수신받은 센서 데이터를 dashboard.html에 text 반영
    
    '''
    # [debug]
    debug_mode=False

    # [UDP Setting]
    sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1',8080)) # test IP
    
    
    # [Loop Function]
    def sensor_generate():
        while True:
            if debug_mode==False:
                data,addr=sock.recvfrom(200)
                print("server is received data", data.decode())
                yield data.decode()
            else:
                current_time=time.strftime("%H:%M:%S\n")
                print(current_time)
                yield current_time
                time.sleep(1)

    return Response(sensor_generate(), mimetype='text/plain')


