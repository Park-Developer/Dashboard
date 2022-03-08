from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('index', __name__)

@bp.route('/')
def index_setting(): # index화면 구성 함수
    return render_template('index.html')


@bp.route('/<index_button>/',methods=['POST'])
def index_btn_click(index_button): # index화면 구성 함수
    print(index_button)
    #return redirect("/")#(request.url)
    return render_template('index.html')