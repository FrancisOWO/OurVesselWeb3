from flask import Blueprint

demo_bp = Blueprint('demo', __name__,url_prefix='/demo',template_folder='templates')

from .views import *