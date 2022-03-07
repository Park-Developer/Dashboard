from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


bp = Blueprint('setting', __name__,url_prefix='/Setting')

@bp.route("/setting_index")
def setting_index():
    '''
    초기 설정 정보는 외부 파일에서 옵로드 하게 하기

    '''
    loaded_setting_data={
        "Model Name":"Wono_o Bot", 
        "S/W Version" :"1.0",
        "H/W Version" :"1.0",
    }
    return render_template('Setting/setting_index.html')