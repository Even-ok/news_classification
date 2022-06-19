from werkzeug.utils import secure_filename
from . import basic
import os
from .scraper import scrap_test, scrap, get_iprocess
from .predicter import predict, get_news_from_file, store_file,trans_number
from time import sleep

from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash, make_response

def allowed_file_csv(filename):  # 通过将文件名分段的方式查询文件格式是否在允许上传格式范围之内
    return '.' in filename and filename.rsplit('.', 1)[1] in ['csv']

def allowed_file_xlsx(filename):  # 通过将文件名分段的方式查询文件格式是否在允许上传格式范围之内
    return '.' in filename and filename.rsplit('.', 1)[1] in ['xlsx']

@basic.route('/')
def welcome():
    return render_template('welcome.html')

@basic.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':  # 当以post方式提交数据时
        file = request.files['file']  # 将上传的文件赋予file
        if file and allowed_file_csv(file.filename):  # 当确认有上传文件并且格式合法
            filename = secure_filename(file.filename)  # 使用secure_filename()让文件名变得安全
            file.save(os.path.join('static/Uploads', 'news.csv'))
            current_file = 'news.csv'
            # 保存文件，也可以直接写成f.save(os.path.join(UPLOAD_FOLDER, fname))
        elif file and allowed_file_xlsx(file.filename):  # 当确认有上传文件并且格式合法
            filename = secure_filename(file.filename)  # 使用secure_filename()让文件名变得安全
            file.save(os.path.join('static/Uploads', 'news.xlsx'))
            current_file = 'news.xlsx'
        else :
            return render_template('upload.html', download_sign=2)
        if allowed_file_csv(file.filename) or allowed_file_xlsx(file.filename):
            # return '''<h1>上传成功</h1>'''
            title,text=get_news_from_file(allowed_file_xlsx(file.filename))
            type=(predict(title,text))
            type=trans_number(type)
            store_file(title,text,type)
            return render_template('upload.html', download_sign=1)
        else:
            # return '<h1>上传失败</h1>'
            return render_template('upload.html', download_sign=0)
    return render_template('upload.html',download_sign=None)

@basic.route('/index')
def index():
    return render_template('index.html')

@basic.route('/download')
def download():
    return render_template('download.html')

@basic.route('/single', methods=['get'])
def show_news():
    return render_template('2_single_news.html')

@basic.route('/single', methods=['post'])
def single_news():
    title = request.form.get('title')
    content = request.form.get('content')
    model = request.form.get('modelSelect')
    if (len(title) != 0 and len(content) != 0):
        outcome = predict([title], [content],model)
        outcome = trans_number(outcome[0])
        return render_template('2_single_news.html', outcome=outcome)
    else:
        return render_template('2_single_news.html', outcome=None)

@basic.route('/scraper')
def scrapper():
    return render_template("scraper.html", res=None)

@basic.route('/scraper', methods=['post'])
def go_scrap():
    # res=scrap_test()
    res = scrap()
    return render_template("scraper.html", res=res)

@basic.route('/get_process', methods=['post','get'])
def get_i():
    i_process,j_process=get_iprocess()
    print(i_process)
    ans=str(i_process)+"/"+str(j_process)
    print(ans)
    return ans