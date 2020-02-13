'''
import os
from flask import Flask, render_template, request

__author__ = 'nooras'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'images/')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)

        print(request.files.getlist("file[]"))
        print(request.files['file'])
        for file in request.files.getlist("file[]"):
            print("heyy",file)
            filename = file.filename
            destination = "/".join([target,filename])
            print("dest",destination)
            file.save(destination)
    return render_template("temp.html")

if __name__ == "__main__":
    app.run(debug=True)

'''
import os
import time
import hashlib

from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_mysqldb import MySQL,MySQLdb
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = '62380aa1db212b7b23d15f5aec36ba7b36'

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads') # you'll need to create a folder named uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
    submit = SubmitField('Upload')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):
            #name = hashlib.md5(('admin' + str(time.time())).encode('utf-8')).hexdigest()[:15]
            #photos.save(filename, name=name + '.')
            photos.save(filename)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Product(Product_img) VALUES(%s)", (filename,))
            mysql.connection.commit()
            cur.close()
        success = True
    else:
        success = False
    return render_template('index.html', form=form, success=success)


@app.route('/manage')
def manage_file():
    files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('manage.html', files_list=files_list)


@app.route('/open/<filename>')
def open_file(filename):
    file_url = photos.url(filename)
    return render_template('browser.html', file_url=file_url)


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = photos.path(filename)
    os.remove(file_path)
    return redirect(url_for('manage_file'))

PEOPLE_FOLDER = os.path.join('static','uploads')
appp = Flask(__name__)
appp.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


@app.route('/fruit')
def fruit():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Fruits.jpg')
    return render_template('fruits.html',filename = full_filename)

@app.route('/fruit_find/<ty>',methods=['GET', 'POST'])
def fruit_find(ty):
    print(ty)
    cur = mysql.connection.cursor()
    cur.execute("select * from Product where P_category = %s",(ty,))
    data = cur.fetchall()
    '''
    a=[]
    for da in data:
        a.append(fname)
        a.append(da)
    '''
    cur.close()
    return render_template('fruit_find.html', data=data)

if __name__ == '__main__':
    app.run(port=5001,debug=True)