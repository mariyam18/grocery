from flask import Flask, escape, request , render_template, url_for,flash,redirect,session
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL,MySQLdb
import yaml
import bcrypt
app = Flask(__name__)

app.config['SECRET_KEY'] = '62380aa1db212b7b23d15f5aec36ba7b36'

#configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

posts = [
    {
        'author' : 'Nooras Fatima',
        'title' : 'Blog post 1',
        'content' : 'Fisrt post content',
        'date_posted' : 'April 20,2018'
    },
    {
        'author' : "Mariyam",
        'title' : "Blog post 2",
        'content' : 'Second post content',
        'date_posted' : "April 21,2018"
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title = 'About')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    '''
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    '''
    if request.method == 'POST':
        details = request.form
        email = details['email']
        password = details['password']
        #password = details['password'].encode('utf-8')
        #hash_password = bcrypt.hashpw(password,bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users(email,password) VALUES(%s,%s)",(email,password))
        mysql.connection.commit()
        session['email'] = email
        cur.close()
        flash(f'Account created for {form.email.data}!', 'Success')
        return redirect(url_for('home'))

    return render_template('reg.html',title = 'Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    '''
    if form.validate_on_submit():
        if form.email.data == 'anoor@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful.Please check username and password','danger')
    '''
    if request.method == 'POST':
        email =  request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * from Users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()
        if len(user) > 0:
            #if bcrypt.hashpw(password,user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
            if password == user['password']:
                session['email'] = user['email']
                return redirect(url_for('home'))
    return render_template('home.html',title = 'Login',form=form)

if __name__ == '__main__':
    app.run(port=5001,debug=True)
    #app.run(host="localhost", port=8000, debug=True)