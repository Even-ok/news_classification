from flask import Blueprint

basic = Blueprint('basic',__name__)

from . import views