from flask import Blueprint

carbon_bp = Blueprint('carbon', __name__, template_folder='templates')

from .views import *
