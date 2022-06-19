import os
from flask import Flask
from basic import basic
from gevent import pywsgi

app=Flask(__name__)
app = Flask(__name__, template_folder='templates')

from flask_wtf.csrf import CSRFProtect
CSRFProtect(app)

UPLOAD_FOLDER = 'static/Uploads'#\u6587\u4ef6\u4e0b\u8f7d\u8def\u5f84
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])#\u6587\u4ef6\u5141\u8bb8\u4e0a\u4f20\u683c\u5f0f
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER#\u8bbe\u7f6e\u6587\u4ef6\u4e0b\u8f7d\u8def\u5f84
app.register_blueprint(basic)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.debug = True
bind = "0.0.0.0:5000"
daemon = True

if __name__=='__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()