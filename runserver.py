from flask import render_template, Flask, request, session, flash, abort, redirect, g, url_for
import sqlite3
import time
from datetime import datetime
import os
from werkzeug import secure_filename

ALLOWED_EXTENTIONS = set(['png','jpg','jpeg','bmp','gif','mp3','wav','aac','flac' \
    'PNG','JPG','JPEG','BMP','GIF','MP3','WAV','AAC','FLAC'])
ALLOWED_EXTENTIONS_LIST = ['png','PNG','jpg','JPG','jpeg','JPEG','bmp','BMP','gif'\
                           ,'GIF','mp3','MP3','wav','WAV','aac','AAC','flac','FLAC']

app = Flask(__name__)
app.config.from_pyfile('server.ini',silent=False)

#数据库 database operation functions
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#路由 routes
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g,'db',None)
    if db is not None:
        db.close()
    g.db.close()

@app.route('/', methods=['GET','POST'])
def login(name=None):
    try:
        if request.method == 'GET':
            if session['logged_in'] == True:
                return redirect(url_for('index'))
            else:
                return render_template('login.html')
    except:
        return render_template('login.html')
    if request.method == 'POST':
        if request.form['username'] == 'FemalName' and request.form['password'] == 'password':
            session['user']='female'
            session['logged_in']=True
            return redirect(url_for('index',user='male'))
        elif request.form['username'] == 'MaleName' and request.form['password'] == 'password':
            session['user']='male'
            session['logged_in']=True
            return redirect(url_for('index',user='male'))
        else:
            return 'bad passwd'

@app.route('/index', methods=['GET','POST'])
@app.route('/index.html', methods=['GET','POST'])
def index(user='none'):
    cur = g.db.execute('SELECT time,passage,sex,type FROM passage ORDER BY id DESC;')
    data = [dict(time=row[0], passage=row[1], sex=row[2] ,type=row[3]) for row in cur.fetchall()]
    days = (datetime.now() - datetime(2015,1,1)).days #将2015,1,1换为你们的纪念日
    try:
        if session['user']=='male' and request.method == 'GET': #GET请求的处理
            return render_template('index.html',name='male' ,data=data,days=days)
        elif session['user']=='female' and request.method == 'GET':
            return render_template('index.html',name='female' ,data=data,days=days)
        elif request.method == 'POST':  #POST请求的处理
            text = request.form['content']
            if text == "":
                flash("内容不能为空哦")
                return redirect(url_for('index'))
            g.db.execute('insert into passage (time,passage,sex) values(?,?,?);', ['20' + time.strftime('%y.%m.%d %H:%M',time.localtime()), text, session['user']] )
            g.db.commit()
            flash('发表成功')
            return redirect(url_for('index'))
        else:
            abort(401)
            this_is_never_executed()
    except:
        return redirect(url_for('login'))

@app.route('/logout')   #登出
def logout():
    session['logged_in']=False
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def file_upload():
    file = request.files['user-file']
    filename = file.filename
    if allowed_file(filename):
        filename = secure_filename(filename)
        filepath = app.config['UPLOAD_FOLDER'] + filename
        file.save(filepath)
        flash('上传成功')
        i = 0
        while i < 18:
            if '.' + ALLOWED_EXTENTIONS_LIST[i] in filename:
                if i < 10:
                    g.db.execute('insert into passage (time,passage,sex,type) values(?,?,?,?);', \
                        ['20' + time.strftime('%y.%m.%d %H:%M',time.localtime()), filepath, session['user'], 'image'] )
                    g.db.commit()
                else:
                    g.db.execute('insert into passage (time,passage,sex,type) values(?,?,?,?);', \
                        ['20' + time.strftime('%y.%m.%d %H:%M',time.localtime()), filepath, session['user'], 'audio'] )
                    g.db.commit()
            i = i + 1
    else:
        flash('不支持的文件类型')
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENTIONS

if __name__=='__main__':
    connect_db()
    app.secret_key = app.config['SECURE_KEY']
    app.run('0.0.0.0', port = app.config['PORT'], debug = app.config['DEBUG'],threaded=True)
