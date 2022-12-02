from flask import render_template #, flash, redirect, url_for
from app import app,login
from app.app_map import map_bp
from .models import *
from .forms import *

from app.app_demo import demolinks # 导航栏链接
from app.utils.config import ak

@map_bp.route('/helloMap', methods=['GET','POST'])
def hello_map():
    return render_template(
        "helloMap.html",
        title = "地图示例",
        ak = ak,
        demolinks = demolinks,
    )
