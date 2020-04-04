import os
import time
import hashlib

from flask import flash
from flask import url_for
from werkzeug.utils import secure_filename

from flask import Flask, session, render_template, redirect, url_for, request, send_from_directory, escape, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_mysqldb import MySQL,MySQLdb
import MySQLdb
import yaml
import bcrypt
from forms import RegistrationForm, LoginForm, ShopkeeperForm, DBoyForm #For Registration login
import random 
import requests



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '62380aa1db212b7b23d15f5aec36ba7b36'

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads') # you'll need to create a folder named uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

ALLOWED_EXTENSIONS = {'jpg','jpeg'}
class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
    submit = SubmitField('Upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
    submit = SubmitField('Upload')

'''
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):
            #name = hashlib.md5('admin' + str(time.time())).hexdigest()[:15]
            #photos.save(filename, name=name + '.')
            photos.save(filename)
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
'''

headers = {
    'authorization': "ZJXba1yRxkuV36o9O0tPcgh5YNfHW2eGEdvUCSsqm8MrLKl7iTiyQE1j3W6eBMqAbfwuHF5LgKDYJNlm",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded"
    }

url = "https://www.fast2sms.com/dev/bulk"

PEOPLE_FOLDER = os.path.join('static','uploads')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

#------------->>User<<--------------
@app.route('/home')
def home():
    #session.clear()
    #print(session['email']==None)
    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Fruits.jpg')
    return render_template('home.html')

#Updateing Flag variable while registring User
flag = 0
def global_var_change():
    global flag
    if flag == 0:
        flag = 1
    elif flag == 1:
        flag = 0

#Updating sflag variable while registring Shopkeeper
sflag = 0
def global_sflag_change():
    global sflag
    if sflag == 0:
        sflag = 1
    elif sflag == 1:
        sflag = 0

#Updating dbflag variable while registring Shopkeeper
dbflag = 0
def global_dbflag_change():
    global dbflag
    if dbflag == 0:
        dbflag = 1
    elif dbflag == 1:
        dbflag = 0

#Function for otp generation
@app.route('/sendotp',methods=['POST','GET'])
def sendotp():
    form = RegistrationForm()
    if request.method == 'POST':
        details = request.form
        session['email'] = details['email']
        session['password'] = details['password']
        session['cpassword'] = details['confirm_password']
        num=session['phone'] = request.form['phone']
        verification_code = generate_code()
        session['number'] = verification_code
        print("Sesssionnnn---",session['number'])
        payload = {'sender_id': 'FSTSMS', 'language':'english','route':'qt','numbers': num, 'message': '21251','variables': '{#AA#}', 'variables_values': verification_code}
        response = requests.request("POST", url, data=payload, headers=headers)
        print(payload)
        print(response.text)
        return render_template('confirmotp.html')

#Function for Confirm OTP
@app.route('/confirmotp',methods=['POST','GET'])
def confirmotp():
    if request.method == 'POST':
        num = request.form['verification']
        print(session['number'])
        if(num == session['number']):
            print("--->>>",session['number'],num)
            #global flag
            #flag = 1
            global_var_change()
            print("InCOnnn",flag)
            return redirect(url_for('register'))
        return render_template('reg.html')

#Random code generation for sendotp
def generate_code():
    return str(random.randrange(10000, 99999))

#Registration for user
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    '''
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    '''
    if(session.get('number') is not None and flag==1):
        global_var_change()
        print("hhjhhbhbhb")
        details = request.form
        no = int(session['phone'])
        print("Noooo",no)
        email = session['email']
        password = session['password']
        cpassword = session['cpassword']
        #password = details['password'].encode('utf-8')
        #hash_password = bcrypt.hashpw(password,bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users(email,mob_no,password) VALUES(%s,%s,%s)",(email,no,password))
        mysql.connection.commit()
        session['email'] = email
        cur.close()
        flash(f'Account created!', 'Success')
        return render_template('login.html',title = 'Register',form=form)
    print("hiiiii",flag)

    return render_template('reg.html',title = 'Register',form=form)

#Login for User
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
                session['em']=session['email'] = user['email']
                print(session['email'])
                return redirect(url_for('home'))
    return redirect(url_for('register'))
    #return render_template('home.html',title = 'Login',form=form)

#product_find Function
@app.route('/product_find/<ty>',methods=['GET', 'POST'])
def product_find(ty):
    form = RegistrationForm()
    if(session.get('email') is not None):
        session['user'] = session['email']
        #session['user'] = 'anoor@gmail.com'
        email = session['user']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT uid from Users WHERE email=%s",(email,))
        user = cur.fetchone()
        session['uid']=int(user['uid'])
        print(ty)
        cur = mysql.connection.cursor()
        cur.execute("select Product.Product_id,Product.P_name,Product.P_actual_price,Product.P_quantity,Product.P_quantity_type,Shopkeeper.shop_name,Shopkeeper.shop_add,Shopkeeper.shop_city,Shopkeeper.shop_district,Shopkeeper.shop_state from Product join Shopkeeper on Product.shop_id = Shopkeeper.shop_id where P_category= %s",(ty,))
        data = cur.fetchall()
        a=[]
        b=[]
        temp = []
        for da in data:
            if (da[1] not in temp):
                fruitname = da[1] + '.jpeg'
                # filename = os.path.join(app.instance_path, 'UploadImageUpdate', 'Apple.jpeg')
                # print("Fillllll", filename)
                fpath = os.path.join('/',app.config['UPLOAD_FOLDER'], fruitname)
                fpathhh = os.path.join(app.config['UPLOAD_FOLDER'], fruitname)
                if not os.path.exists(fpathhh):
                    fruitname = da[1] + '.jpg'
                    fpath = os.path.join('/',app.config['UPLOAD_FOLDER'], fruitname)
                a.append(fpath)
                a.append(da[0]) #id
                a.append(da[1]) #name
                a.append(da[2]) #actual price
                a.append(da[3]) #Available quantity
                a.append(da[4]) #weight/unit
                a.append(da[5]) #shopname
                a.append(da[6]) #shopadd
                a.append(da[7]) #shopcity
                a.append(da[8]) #shopDistrict
                a.append(da[9]) #shopstate
                b.append(a)
                a=[]
                print(fpath,da[0],da[1],da[2],da[3],da[4],da[5],da[6],da[7],da[8],da[9])
                print(b)
                temp.append(da[1])
        cur.close()
        return render_template('product_find.html', data=b)
    else:
        flash("You have to login first!!")
        return redirect(url_for('register'))

#Function for adding product in cart
@app.route('/addHome/<name>/<shopname>',methods=['GET', 'POST'])
def addHome(name=None,shopname=None):
    print(name,shopname)
    cursor = None
    if(request.method == 'POST'):
        cur = mysql.connection.cursor()
        cur.execute("select Product_id from Product where P_name= %s",(name,)) #Only for loop
        data = cur.fetchall()
        print("Data",data)
        for da in data:
            x=str(da[0])
            print("XXX",x)
            #print("REQQQ",request.form.get("3"))
            #print("REQQQ",request.form.get("7"))
            if(request.form.get(x) == None):
                pass
            else:
                print(da[0],request.form.get(x),type(request.form.get(x)))
                quantity = int(request.form[x])
                print("QUANTITY",quantity)
            #print("Q",da[0],type(da[0]),request.form.get(x))
        db = MySQLdb.connect(host='localhost', db='grocery', user='admin', passwd='admin')
        dict_cursor = db.cursor(MySQLdb.cursors.DictCursor)
        #conn = MySQLdb.connect
        #cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        dict_cursor.execute("select Product.Product_id,Product.P_name,Product.P_actual_price,Product.P_quantity,Product.P_quantity_type,Shopkeeper.shop_name,Shopkeeper.shop_add,Shopkeeper.shop_city,Shopkeeper.shop_district,Shopkeeper.shop_state from Product join Shopkeeper on Product.shop_id = Shopkeeper.shop_id where P_name=%s and shop_name=%s",(name,shopname))
        #cursor.execute("select * from Product join Shopkeeper on Product.shop_id = Shopkeeper.shop_id where P_name=%s and shop_name=%s",(name,shopname))
        #dict_cursor.execute("select * from Product where P_name=%s",(name,))
        row = dict_cursor.fetchone()
        print("ROW",row)
        itemArray = { str(row['Product_id']) : { 'name':row['P_name'], 'price':row['P_actual_price'], 'quantity': quantity,'quan_type':row['P_quantity_type'], 'total_price':quantity*row['P_actual_price'], 'shopname':row['shop_name'], 'shop_add':row['shop_add'],'shop_city':row['shop_city'],'shop_district':row['shop_district'], 'shop_state':row['shop_state'] }}
        print("Item array",itemArray)
        all_total_price = 0
        all_total_quantity = 0
        print("Session Bfore",session)
        session.modified  = True
        print("Session AFtre",session)
        if 'cart_item' in session:
            if(str(row['Product_id']) in session['cart_item']):
                print("IFFFF")
                for key,value in session['cart_item'].items():
                    if(str(row['Product_id']) == key):
                        print("InnerIFF")
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * row['P_actual_price']
                        print('total ::',total_quantity,old_quantity,quantity) 
            else:
                print("elsee",session,"Session",session['cart_item'])
                session['cart_item'] = array_merge(session['cart_item'], itemArray)
                print("Session cart item ",session['cart_item'])
            
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = int(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price
                print("Forrr")
        else:
            session['cart_item'] = itemArray
            all_total_quantity = all_total_quantity + quantity
            all_total_price = all_total_price + quantity * row['P_actual_price']
        print("Before",session)
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price
        print("LAst",session)
        
        return render_template('home.html')
    else:
        print('Else')
        print(request.form)
        return 'Error while adding item to cart'
    return redirect(url_for('.home'))

#Checkout Page
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

def func():
      global x
      x = x+1

x = 50
#func()
#print 'Value of x is', x
#print id(x)

#Order confirmation of users and data will go into cart_order and order_item
@app.route('/confirm',methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        uid = int(session['uid']) 
        lane1 = request.form['lane1']
        lane2 = request.form['lane2']
        city = request.form['city']
        state = request.form['state']
        #For cart_order insert
        total_quantity = session['all_total_quantity']
        total_price = session['all_total_price']
        func()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cart_order(order_id,total_price,total_quantity,lane1,lane2,city,state,uid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(id(x),total_price,total_quantity,lane1,lane2,city,state,uid))
        #Inserting data into order_item  
        for key, value in session['cart_item'].items():
            Product_id = int(key)
            name = session['cart_item'][key]['name']
            price = int(session['cart_item'][key]['price'])
            individual_quantity = int(session['cart_item'][key]['quantity'])
            quantity_type = session['cart_item'][key]['quan_type']
            individual_price = int(session['cart_item'][key]['total_price'])
            shop_name = session['cart_item'][key]['shopname']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT shop_id from Shopkeeper WHERE shop_name=%s",(shop_name,)) #fetching shop_id for inserting it in order_item (foreign key)
            user = cur.fetchone()
            #print("shop_id",user['shop_id'])
            cur.execute("SELECT P_quantity from Product WHERE Product_id=%s",(Product_id,))
            quant = cur.fetchone()
            Find_quantity = quant['P_quantity'] - individual_quantity   #Finding decreses product quantity
            cur = mysql.connection.cursor()
            cur.execute("update Product set P_quantity =%s where Product_id=%s",(abs(Find_quantity),Product_id))
            cur.execute("INSERT INTO order_item(Product_id,P_name,P_price,P_quantity,P_quantity_type,P_total_price,order_id,shop_id,status_value) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,0)",(Product_id,name,price,individual_quantity,quantity_type, individual_price,id(x),user['shop_id']))
            mysql.connection.commit()
            cur.close()
        session.pop('all_total_quantity',None)
        session.pop('all_total_price',None)
        session.pop('cart_item',  None)
    return redirect(url_for('.track'))

#Tracking of product
@app.route('/track',methods=['GET', 'POST'])
def track():
    print("--------------------------------********************-------------------------****----")
    uid = int(session['uid'])
    print(session['uid'],uid,"hiiiiiiiiiiiiiiii",type(session['uid']))
    cur = mysql.connection.cursor()
    cur.execute("select order_item.P_name , order_item.P_price , order_item.P_quantity , order_item.P_total_price,order_item.order_id , cart_order.total_price , cart_order.total_quantity , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , order_item.status_value ,Shopkeeper.shop_name , Shopkeeper.shopkeeper_contact , Shopkeeper.shop_add , Shopkeeper.shop_city , order_item.cart_item_id from order_item , cart_order , Shopkeeper where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and cart_order.uid=%s",(uid,))
    data = cur.fetchall()
    print("DATAA",data)
    temp_orderid = {} #storing order_id with product id
    temp_shop_product1 = {} #storing product details of shop
    #temp_shop_product2 = {} #storing shop details
    for da in data:
        key = da[4]
        if(da[4] not in temp_orderid):
            print("YEEE>>>>>>>>>>> ",da[4])
            temp_orderid.setdefault(key,[])
            temp_orderid[key].append(da[17])  
            key_shop = da[17]
            temp_shop_product1.setdefault(key_shop,[])
            listA = []
            listA.append(da[0])
            listA.append(da[1])
            listA.append(da[2])
            listA.append(da[3])
            listA.append(da[4])
            listA.append(da[5])
            listA.append(da[6])
            listA.append(da[7])
            listA.append(da[8])
            listA.append(da[9])
            listA.append(da[10])
            listA.append(da[11])
            listA.append(da[12])
            listA.append(da[13])
            listA.append(da[14])
            listA.append(da[15])
            listA.append(da[16])
            listA.append(da[17])
            temp_shop_product1[key_shop] = listA
        else:
            temp_orderid[key].append(da[17])  
            key_shop = da[17]
            temp_shop_product1.setdefault(key_shop,[])
            listA = []
            listA.append(da[0])
            listA.append(da[1])
            listA.append(da[2])
            listA.append(da[3])
            listA.append(da[4])
            listA.append(da[5])
            listA.append(da[6])
            listA.append(da[7])
            listA.append(da[8])
            listA.append(da[9])
            listA.append(da[10])
            listA.append(da[11])
            listA.append(da[12])
            listA.append(da[13])
            listA.append(da[14])
            listA.append(da[15])
            listA.append(da[16])
            listA.append(da[17])
            temp_shop_product1[key_shop] = listA
    print(temp_shop_product1,"**************")
    print(temp_orderid,"////////////////////////////")
    return render_template('track.html',odrer_id=temp_orderid,product1=temp_shop_product1)
    '''
    for da in data:
        print("Data>>>>>>>>>>>>> ",da)
        if(da[4] not in temp_orderid):
            print("YEEE>>>>>>>>>>> ",da[4])
            key = da[4]
            temp_orderid.setdefault(key,[])
            temp_orderid[key].append(da[17])  
            if(da[13] not in temp_shop_product1):
                print("INNN IFFF >>>>>",da[13])
                listA = []
                listB = []
                key_shop = da[13]
                temp_shop_product1.setdefault(key_shop,[])
                temp_shop_product2.setdefault(key_shop, [])
                listA.append(da[0])
                listA.append(da[1])
                listA.append(da[2])
                listA.append(da[3])
                listA.append(da[12])
                listA.append(da[17])
                listB.append(da[5])
                listB.append(da[6])
                listB.append(da[7])
                listB.append(da[8])
                listB.append(da[9])
                listB.append(da[10])
                listB.append(da[11])
                listB.append(da[14])
                listB.append(da[15])
                listB.append(da[16])
                temp_shop_product1[key_shop].append(listA)
                temp_shop_product2[key_shop].append(listB)
                print(listA,listB,"ifff")
        else:
            key = da[4]
            x = temp_orderid[key]
            if da[13] not in x:
                temp_orderid[key].append(da[17])
            if (da[13] not in temp_shop_product1):
                print("Down>>",da[13])
                listA = []
                listB = []
                key_shop = da[13]
                temp_shop_product1.setdefault(key_shop, [])
                temp_shop_product2.setdefault(key_shop, [])
                listA.append(da[0])
                listA.append(da[1])
                listA.append(da[2])
                listA.append(da[3])
                listA.append(da[12])
                listA.append(da[17])
                listB.append(da[5])
                listB.append(da[6])
                listB.append(da[7])
                listB.append(da[8])
                listB.append(da[9])
                listB.append(da[10])
                listB.append(da[11])
                listB.append(da[14])
                listB.append(da[15])
                listB.append(da[16])
                temp_shop_product1[key_shop].append(listA)
                temp_shop_product2[key_shop].append(listB)
                print(listA, listB, "ifffbeloww")
            else:
                listA = []
                listB = []
                key_shop = da[13]
                listA.append(da[0])
                listA.append(da[1])
                listA.append(da[2])
                listA.append(da[3])
                listA.append(da[12])
                listA.append(da[17])
                listB.append(da[5])
                listB.append(da[6])
                listB.append(da[7])
                listB.append(da[8])
                listB.append(da[9])
                listB.append(da[10])
                listB.append(da[11])
                listB.append(da[14])
                listB.append(da[15])
                listB.append(da[16])
                temp_shop_product1[key_shop].append(listA)
                temp_shop_product2[key_shop].append(listB)
                print(listA, listB, "elsebelow")
    print(temp_shop_product1)
    print(temp_shop_product2)
    print(temp_orderid)
    print(temp_shop_product2[key_shop][0][8],"xxxxxxxx")
    return render_template('track.html',odrer_id=temp_orderid,product1=temp_shop_product1,product2=temp_shop_product2)
    '''

#For cart empty
@app.route('/empty_cart')
def empty_cart():
    try:
        #session.clear()
        session.pop('all_total_quantity',None)
        session.pop('all_total_price',None)
        session.pop('cart_item',  None)
        return redirect(url_for('.home'))
    except Exception as e:
        print(e)

#For delete product from cart
@app.route('/delete_product/<string:name>')
def delete_product(name):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        for item in session['cart_item'].items():
            print(item[0],name)
            if item[0] == name:             
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = int(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
        return redirect(url_for('.home'))
    except Exception as e:
        print(e)

#ArrayMerge function session cart
def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False    

@app.route('/add<ty>',methods=['GET', 'POST'])
def add(ty):
    return render_template('product_find.html')

#For finding shop of particular product
@app.route('/product_find_shop/<ty>',methods=['GET', 'POST'])
#@app.url_defaults
def product_find_shop(ty):
    print(ty)
    cur = mysql.connection.cursor()
    cur.execute("select Product.Product_id,Product.P_name,Product.P_actual_price,Product.P_quantity,Product.P_quantity_type,Shopkeeper.shop_name,Shopkeeper.shop_add,Shopkeeper.shop_city,Shopkeeper.shop_district,Shopkeeper.shop_state from Product join Shopkeeper on Product.shop_id = Shopkeeper.shop_id where P_name= %s",(ty,))
    data = cur.fetchall()
    a=[]
    b=[]
    temp = []
    for da in data:
            fruitname = da[1] + '.jpeg'
            fpath = os.path.join('/',app.config['UPLOAD_FOLDER'], fruitname)
            fpathhh = os.path.join(app.config['UPLOAD_FOLDER'], fruitname)
            if not os.path.exists(fpathhh):
                fruitname = da[1] + '.jpg'
                fpath = os.path.join('/',app.config['UPLOAD_FOLDER'], fruitname)
            a.append(fpath)
            a.append(da[0]) #id
            a.append(da[1]) #name
            a.append(da[2]) #actual price
            a.append(da[3]) #Available quantity
            a.append(da[4]) #weight/unit
            a.append(da[5]) #shopname
            a.append(da[6]) #shopadd
            a.append(da[7]) #shopcity
            a.append(da[8]) #shopDistrict
            a.append(da[9]) #shopstate
            b.append(a)
            a=[]
            print(fpath,da[0],da[1],da[2],da[3],da[4],da[5],da[6],da[7],da[8],da[9])
            print(b)
            temp.append(da[1])
    print("B",b[0])
    cur.close()
    return render_template('product_find_shop.html', data=b)
'''
    #ty=request.args.get('ty')
    #all=request.args.get('all')
    temp =[]
    tempfruit = []
    print(ty)
    cur = mysql.connection.cursor()
    cur.execute("select Shopkeeper.shop_name,Shopkeeper.shop_add,Shopkeeper.shop_city,Shopkeeper.shop_district,Shopkeeper.shop_state from Product join Shopkeeper on Product.shop_id = Shopkeeper.shop_id where P_name=%s", (ty,))
    detail = cur.fetchall()
    print(detail)
    product = mysql.connection.cursor()
    product.execute("select * from Product where P_name=%s",(ty,))
    pro = product.fetchall()
    for da in pro:
        fruitname = da[1] + '.jpeg'
        fpath = os.path.join('/',app.config['UPLOAD_FOLDER'], fruitname)
        temp.append(fpath)
        temp.append(da[1]) #name
        temp.append(da[2]) #actual price
        temp.append(da[4]) #discount price
        temp.append(da[5]) #Available quantity
        temp.append(da[6]) #weight/unit
        tempfruit.append(temp)
        temp=[]
        print(fpath,da[0],da[1],da[2],da[4],da[5],da[6])
        print(tempfruit)
    return render_template('product_find_shop.html',detail=detail,data=tempfruit)
'''

@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./static/uploads')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("uploads", filename)

@app.route('/fresh_healthy')
def fresh_healthy():
    return render_template('fresh_healthy.html')

@app.route('/care')
def care():
    return render_template('care.html')

@app.route('/spice')
def spice():
    form = ShopkeeperForm()
    return render_template('loginshop.html',form=form)

#------------->>Shopkeeper<<--------------

#Function for otp generation of Shopkeeper
@app.route('/sendotpshop',methods=['POST','GET'])
def sendotpshop():
    form = RegistrationForm()
    if request.method == 'POST':
        details = request.form
        session['shopname'] = details['shopname']
        session['shop_address'] = details['shop_address']
        session['shop_city'] = details['shop_city']
        session['shop_state'] = details['shop_state']
        session['shopkeeper_name'] = details['shopkeeper_name']
        session['shopkeeper_address'] = details['shopkeeper_address']
        session['shopkeeper_city'] = details['shopkeeper_city']
        session['shopkeeper_state'] = details['shopkeeper_state']
        num = session['shopkeeper_phone'] = details['shopkeeper_phone']
        session['shopkeeper_email'] = details['shopkeeper_email']
        session['password'] = details['password']
        session['cpassword'] = details['confirm_password']
        if(session['password'] == session['cpassword']):
            verification_code = generate_code()
            session['number'] = verification_code
            payload = {'sender_id': 'FSTSMS', 'language':'english','route':'qt','numbers': num, 'message': '21251','variables': '{#AA#}', 'variables_values': verification_code}
            response = requests.request("POST", url, data=payload, headers=headers)
            print(payload)
            print(response.text)
            return render_template('confirmotpshop.html')
        else:
            flash("Password should be same!!")
            return render_template('regshop.html', title='Shopkeeper Reg', form=form)

#Function for Confirm OTP of Shopkeeper
@app.route('/confirmotpshop',methods=['POST','GET'])
def confirmotpshop():
    if request.method == 'POST':
        num = request.form['verification']
        print(session['number'])
        if(num == session['number']):
            print("--->>>",session['number'],num)
            global_sflag_change()
            print("InCOnnn",sflag)
            return redirect(url_for('shopreg'))
        return render_template('shopreg.html')

#Function for registering of Shopkeeper
@app.route('/shopreg',methods=['GET','POST'])
def shopreg():
    form = ShopkeeperForm()
    #flash("Data Inserted Successfully")
    if(session.get('shopkeeper_phone') is not None and sflag==1):
        global_sflag_change()
        flash("Data Inserted Successfully")
        shopname = session['shopname']
        shop_address = session['shop_address']
        shop_city = session['shop_city']
        shop_state = session['shop_state']
        shopkeeper_name = session['shopkeeper_name']
        shopkeeper_address = session['shopkeeper_address']
        shopkeeper_city = session['shopkeeper_city']
        shopkeeper_state = session['shopkeeper_state']
        shopkeeper_phone = session['shopkeeper_phone']
        shopkeeper_email = session['shopkeeper_email']
        password = session['password']
        cpassword = session['cpassword']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Shopkeeper (shop_name,shopkeeper_contact ,shopkeeper_name,shopkeeper_email,shop_add,shop_city,shop_state,shopkeeper_address,shopkeeper_city,shopkeeper_state,pass ) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)",(shopname, shopkeeper_phone,shopkeeper_name, shopkeeper_email,shop_address,shop_city,shop_state,shopkeeper_address,shopkeeper_city,shopkeeper_state,password))
        mysql.connection.commit()
        #session['email'] = email
        cur.close()
        flash(f'Account created!', 'Success')
        return render_template('loginshop.html',title = 'Register',form=form)   
    return render_template('regshop.html', title='Shopkeeper Reg', form=form)

#For registering of Shopkeeper
@app.route('/loginshop',methods=['GET','POST'])
def loginshop():
    form = ShopkeeperForm()
    '''
    if form.validate_on_submit():
        if form.email.data == 'anoor@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful.Please check username and password','danger')
    '''
    if request.method == 'POST':
        email =  request.form['shopkeeper_email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * from Shopkeeper WHERE shopkeeper_email=%s",(email,))
        user = cur.fetchone()
        cur.close()
        if len(user) > 0:
            #if bcrypt.hashpw(password,user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
            if password == user['pass']:
                session['semail'] = user['shopkeeper_email']
                session['id'] = user['shop_id']
                print(session['semail'])
                return redirect(url_for('index'))
    return render_template('loginshop.html', title='Shopkeeper Reg', form=form)
    #return render_template('home.html',title = 'Login',form=form)

#mariyam
#Showing Add product page to Shopkeeper
@app.route('/index')
def index():
    form = ShopkeeperForm()
    if(session.get('id') is not None):
        session['shopk'] = session['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM Product where shop_id=%s",(session['shopk'],))
        #cur.execute("SELECT  * FROM product")
        data = cur.fetchall()
        cur.close()
        return render_template('adding.html', prod=data )
    else:
        flash("You have to login first!!")
        return render_template('regshop.html', title='Shopkeeper Reg', form=form)

#mariyam
#Adding Product in Shopkeeper Account
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        #flash("Data Inserted Successfully")
        name = request.form['name']
        price = request.form['price']
        available = request.form['available']
        category = request.form['category']
        weight = request.form['weight']
        manufacture = request.form['manufacture']
        expiry = request.form['expiry']
        file = request.files['ifile']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Product (P_name, P_actual_price,P_category, P_quantity,P_quantity_type,shop_id,manu_date,exp_date,image) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)", (name, price,category, available,weight,session['shopk'],manufacture,expiry,file.filename))
        mysql.connection.commit()
        file = request.files['ifile']
        print("Hiii")
        print(file)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print(allowed_file(file.filename))
        print(allowed_file(file.filename))
        if file and allowed_file(file.filename):
            print("Inn insert")
            filename = secure_filename(file.filename)
            #name,file_extension = os.path.splitext(filename)
            #print(name)
            #print(file_extension)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],name+'.jpg'))
            print(file.filename)
            if(file.filename == False):
                print("----------?????????????????????????????????")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],name+'.jpeg'))
                print(file.filename)
        #os.rename(UPLOAD_FOLDER +filename,UPLOAD_FOLDER +'bear.jpg')       
        return redirect(url_for('index'))

#mariyam
#Delete Product from Shopkeer Account
@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Product WHERE product_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index'))

#mariyam
#update Product from Shopkeeper Account
@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        available = request.form['available']
        weight = request.form['weight']
        manufacture = request.form['manufacture']
        expiry = request.form['expiry']
        file = request.files['imgfile']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Product SET P_name=%s, P_actual_price=%s,P_category=%s, P_quantity=%s,P_quantity_type=%s,shop_id=%s,manu_date=%s,exp_date=%s WHERE Product_id=%s",(name, price,category, available,weight,session['shopk'],manufacture,expiry, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        file = request.files['imgfile']
        print(file)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print(allowed_file(file.filename))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #name,file_extension = os.path.splitext(filename)
            #print(name)
            #print(file_extension)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],name+'.jpg'))
            print(file.filename)
        return redirect(url_for('index'))

#Shopkeeper will get Order
@app.route('/shopgetorder',methods=['GET', 'POST'])
def shopgetorder():
    form = ShopkeeperForm()
    if(session.get('id') is not None):
        cur = mysql.connection.cursor()
        cur.execute("select  order_item.cart_item_id ,order_item.P_name , order_item.P_price , order_item.P_quantity , order_item.P_quantity_type ,  order_item.P_total_price,order_item.order_id , cart_order.total_price , cart_order.total_quantity , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , order_item.status_value  from order_item , cart_order , Shopkeeper where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and order_item.shop_id=%s",(int(session['id']),))
        order = cur.fetchall()
        print(order)
        return render_template('shop_get_order.html',data=order)
    else:
        flash("You have to login first!!")
        return render_template('regshop.html', title='Shopkeeper Reg', form=form)

#Accepting order of Shopkeeper
@app.route('/accept_Order/<product_order_id>',methods=['GET','POST'])
def accept_Order(product_order_id):
    temp = 0
    cur = mysql.connection.cursor()
    cur.execute("select status_value  from order_item where order_item.cart_item_id=%s",(int(product_order_id),))
    status_value = cur.fetchone()
    print("Status Value : ",status_value[0])
    temp = status_value[0] + 1
    print("Status Value : ",status_value[0])
    cur.execute("update order_item set status_value =%s where cart_item_id = %s",(temp,int(product_order_id)))
    cur.execute("select  order_item.cart_item_id ,order_item.P_name , order_item.P_price , order_item.P_quantity , order_item.P_quantity_type ,  order_item.P_total_price,order_item.order_id , cart_order.total_price , cart_order.total_quantity , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , order_item.status_value  from order_item , cart_order , Shopkeeper where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and order_item.shop_id=%s",(int(session['shopk']),))
    order = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    print(order)
    return render_template('shop_get_order.html',data=order)

#--------------search------------

@app.route('/product_search/<ty>',methods=['GET', 'POST'])
def product_search(ty):
    if(session.get('email') is not None):
        session['user'] = session['email']
        #session['user'] = 'anoor@gmail.com'
        email = session['user']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT uid from Users WHERE email=%s",(email,))
        user = cur.fetchone()
        session['uid']=int(user['uid'])
        print(ty)
        cur = mysql.connection.cursor()
        cur.execute("select Product.Product_id,Product.P_name,Product.P_actual_price,Product.P_quantity,Product.P_quantity_type,Shopkeeper.shop_name,Shopkeeper.shop_add,Shopkeeper.shop_city,Shopkeeper.shop_district,Shopkeeper.shop_state from Product join Shopkeeper on Product.shop_id = Shopkeeper.shop_id where P_name= %s",(ty,))
        data = cur.fetchall()
        a=[]
        b=[]
        temp = []
        for da in data:
            if (da[1] not in temp):
                fruitname = da[1] + '.jpeg'
                # filename = os.path.join(app.instance_path, 'UploadImageUpdate', 'Apple.jpeg')
                # print("Fillllll", filename)
                fpath = os.path.join('/',app.config['UPLOAD_FOLDER'], fruitname)
                fpathhh = os.path.join(app.config['UPLOAD_FOLDER'], fruitname)
                if not os.path.exists(fpathhh):
                    fruitname = da[1] + '.jpg'
                    fpath = os.path.join('/',app.config['UPLOAD_FOLDER'], fruitname)
                a.append(fpath)
                a.append(da[0]) #id
                a.append(da[1]) #name
                a.append(da[2]) #actual price
                a.append(da[3]) #Available quantity
                a.append(da[4]) #weight/unit
                a.append(da[5]) #shopname
                a.append(da[6]) #shopadd
                a.append(da[7]) #shopcity
                a.append(da[8]) #shopDistrict
                a.append(da[9]) #shopstate
                b.append(a)
                a=[]
                print(fpath,da[0],da[1],da[2],da[3],da[4],da[5],da[6],da[7],da[8],da[9])
                print(b)
                temp.append(da[1])
        cur.close()
        return render_template('product_search.html', data=b)


@app.route('/search',methods=['POST','GET'])
def search():
    if request.method == "POST":
        text = request.form['search']
        cur = mysql.connection.cursor()
        cur.execute("select * from Product where  P_category=%s",[text])
        category=cur.fetchall()
        cur.execute("select * from Product where  P_name=%s",[text])
        product=cur.fetchall()
        #cur.execute("select * from Shopkeeper where shop_name=%s or shopkeeper_name=%s",(text,text))
        #shop=cur.fetchall()
        if(len(category)>0):
            #strprod='product_find/',
            return redirect(url_for('product_find',ty=text))
        elif(len(product)>0):
            return redirect(url_for('product_search',ty=text))
        else:
            flash("NO search found")
        mysql.connection.commit()
        return render_template('base.html')
    return render_template('base.html')

#------------->>Delivery Boy<<--------------

#Function for otp generation of Delivery Boy
@app.route('/sendotpDBoy',methods=['POST','GET'])
def sendotpDBoy():
    form = DBoyForm()
    if request.method == 'POST':
        details = request.form
        session['db_name'] = details['db_name']
        session['db_address'] = details['db_address']
        session['db_city'] = details['db_city']
        session['db_state'] = details['db_state']
        num = session['db_phone'] = details['db_phone']
        session['db_email'] = details['db_email']
        session['password'] = details['password']
        session['cpassword'] = details['confirm_password']
        if(session['password'] == session['cpassword']):
            verification_code = generate_code()
            session['dbnumber'] = verification_code #Code generation
            payload = {'sender_id': 'FSTSMS', 'language':'english','route':'qt','numbers': num, 'message': '21251','variables': '{#AA#}', 'variables_values': verification_code}
            response = requests.request("POST", url, data=payload, headers=headers)
            print(payload)
            print(response.text)
            return render_template('confirmotpDBoy.html')
        else:
            flash("Password should be same!!")
            return render_template('regDBoy.html', title='Delivery Boy Reg', form=form)

#Function for Confirm OTP of Delivery Boy
@app.route('/confirmotpDBoy',methods=['POST','GET'])
def confirmotpDBoy():
    if request.method == 'POST':
        num = request.form['verification']
        print(session['dbnumber'])
        if(num == session['dbnumber']):
            print("--->>>",session['dbnumber'],num)
            global_dbflag_change()
            print("InCOnnn",dbflag)
            return redirect(url_for('regDBoy'))
        return render_template('regDBoy.html')

#Function for registering of Delivery Boy
@app.route('/regDBoy',methods=['GET','POST'])
def regDBoy():
    form = DBoyForm()
    #flash("Data Inserted Successfully")
    if(session.get('db_phone') is not None and dbflag==1):
        global_dbflag_change()
        flash("Data Inserted Successfully")
        db_name = session['db_name']
        db_address = session['db_address']
        db_city = session['db_city']
        db_state = session['db_state']
        db_phone = session['db_phone']
        db_email = session['db_email']
        password = session['password']
        cpassword = session['cpassword']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO DeliveryBoy (db_name,db_address ,db_city,db_state,db_phone,db_email,db_pass) VALUES (%s, %s, %s, %s, %s, %s, %s)",(db_name, db_address,db_city, db_state,db_phone,db_email,password))
        mysql.connection.commit()
        cur.close()
        flash(f'Account created!', 'Success')
        return render_template('loginDBoy.html',title = 'Register',form=form)   
    return render_template('regDBoy.html', title='Delivery boy Reg', form=form)

#For registering of Delivery Boy
@app.route('/loginDBoy',methods=['GET','POST'])
def loginDBoy():
    form = DBoyForm()
    '''
    if form.validate_on_submit():
        if form.email.data == 'anoor@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful.Please check username and password','danger')
    '''
    if request.method == 'POST':
        db_email =  request.form['db_email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * from DeliveryBoy WHERE db_email=%s",(db_email,))
        user = cur.fetchone()
        cur.close()
        if len(user) > 0:
            #if bcrypt.hashpw(password,user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
            if password == user['db_pass']:
                session['db_email'] = user['db_email']
                session['db_id'] = user['db_id']
                print(session['db_email'])
                return redirect(url_for('Db_home'))
    return render_template('loginDBoy.html', title='Delivery Boy Reg', form=form)

#Delivery Boy will get Order packed 
@app.route('/Db_home',methods=['GET','POST'])
def Db_home():
    form = DBoyForm()
    if(session.get('db_id') is not None):
        cur = mysql.connection.cursor()
        cur.execute("select  order_item.cart_item_id , order_item.order_id , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , order_item.status_value , Shopkeeper.shop_name , Shopkeeper.shopkeeper_contact , Shopkeeper.shopkeeper_name , Shopkeeper.shop_add , Shopkeeper.shop_city , Shopkeeper.shop_district , Shopkeeper.shop_state   from order_item , cart_order , Shopkeeper where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and order_item.status_value=2")
        orderPacked = cur.fetchall()
        print(orderPacked)
        return render_template('Db_order_packed.html',data=orderPacked)
    else:
        flash("You have to login first!!")
        return render_template('regDBoy.html', title='Delivery Boy Reg', form=form)
    #return render_template('Db_home.html')

@app.route('/accept_Order_pick/<product_order_id>',methods=['GET','POST'])
def accept_Order_pick(product_order_id):
    form = DBoyForm()
    if(session.get('db_id') is not None):
        temp = 0
        cur = mysql.connection.cursor()
        cur.execute("select status_value  from order_item where order_item.cart_item_id=%s",(int(product_order_id),))
        status_value = cur.fetchone()
        print("Status Value : ",status_value[0])
        if(status_value[0] == 2):
            temp = status_value[0] + 1
            print("Status Value : ",status_value[0])
            cur.execute("update order_item set status_value =%s , db_id = %s where cart_item_id=%s",(temp,int(session['db_id']),int(product_order_id)))
            flash("Order Accepted for pick. Select Order Pick option from Menu")
        cur.execute("select  order_item.cart_item_id , order_item.order_id , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , order_item.status_value , Shopkeeper.shop_name , Shopkeeper.shopkeeper_contact , Shopkeeper.shopkeeper_name , Shopkeeper.shop_add , Shopkeeper.shop_city , Shopkeeper.shop_district , Shopkeeper.shop_state   from order_item , cart_order , Shopkeeper where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and order_item.status_value=2")
        orderPacked = cur.fetchall()    
        mysql.connection.commit()
        cur.close()
        print(orderPacked)
        return render_template('Db_order_packed.html',data=orderPacked)
    else:
        flash("You have to login first!!")
        return render_template('regDBoy.html', title='Delivery Boy Reg', form=form)

@app.route('/Order_pick',methods=['GET','POST'])
def Order_pick():
    form = DBoyForm()
    if(session.get('db_id') is not None):
        flash("Go to shop and pick order. Order is ready to pick. Deliver it to User")
        cur = mysql.connection.cursor()
        cur.execute("select  order_item.cart_item_id , order_item.order_id , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , order_item.status_value , order_item.db_id , Shopkeeper.shop_name , Shopkeeper.shopkeeper_contact , Shopkeeper.shopkeeper_name , Shopkeeper.shop_add , Shopkeeper.shop_city , Shopkeeper.shop_district , Shopkeeper.shop_state , Users.name   from order_item , cart_order , Shopkeeper , Users where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and cart_order.uid = Users.uid and order_item.status_value=3 and order_item.db_id=%s",(int(session['db_id']),))
        orderPick = cur.fetchall()    
        mysql.connection.commit()
        cur.close()
        print(orderPick)
        return render_template('Order_pick.html',data=orderPick)
    else:
        flash("You have to login first!!")
        return render_template('regDBoy.html', title='Delivery Boy Reg', form=form)    

#--???????
@app.route('/Order_delivered/<product_order_id>',methods=['GET','POST'])
def Order_delivered(product_order_id):
    form = DBoyForm()
    if(session.get('db_id') is not None):
        temp = 0
        cur = mysql.connection.cursor()
        cur.execute("select status_value  from order_item where order_item.cart_item_id=%s",(int(product_order_id),))
        status_value = cur.fetchone()
        print("Status Value : ",status_value[0])
        if(status_value[0] == 3):
            temp = status_value[0] + 1
            print("Status Value : ",status_value[0])
            cur.execute("update order_item set status_value =%s , db_id = %s where cart_item_id=%s",(temp,int(session['db_id']),int(product_order_id)))
            flash("Order is delivered. Select Order Delivered option from Menu!")
        cur.execute("select  order_item.cart_item_id , order_item.order_id , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , order_item.status_value , order_item.db_id , Shopkeeper.shop_name , Shopkeeper.shopkeeper_contact , Shopkeeper.shopkeeper_name , Shopkeeper.shop_add , Shopkeeper.shop_city , Shopkeeper.shop_district , Shopkeeper.shop_state , Users.name   from order_item , cart_order , Shopkeeper , Users where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and cart_order.uid = Users.uid and order_item.status_value=3 and order_item.db_id=%s",(int(session['db_id']),))
        orderPacked = cur.fetchall()    
        mysql.connection.commit()
        cur.close()
        print(orderPacked)
        return render_template('Order_pick.html',data=orderPacked)
    else:
        flash("You have to login first!!")
        return render_template('regDBoy.html', title='Delivery Boy Reg', form=form)
    
@app.route('/Order_confirm',methods=['GET','POST'])
def Order_confirm():
    form = DBoyForm()
    if(session.get('db_id') is not None):
        flash("Successfully Deliver it to User")
        cur = mysql.connection.cursor()
        cur.execute("select  order_item.cart_item_id , order_item.order_id , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , order_item.status_value , order_item.db_id , Shopkeeper.shop_name , Shopkeeper.shopkeeper_contact , Shopkeeper.shopkeeper_name , Shopkeeper.shop_add , Shopkeeper.shop_city , Shopkeeper.shop_district , Shopkeeper.shop_state , Users.name   from order_item , cart_order , Shopkeeper , Users where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and cart_order.uid = Users.uid and order_item.status_value=4 and order_item.db_id=%s",(int(session['db_id']),))
        orderPick = cur.fetchall()    
        mysql.connection.commit()
        cur.close()
        print(orderPick)
        return render_template('Order_pick.html',data=orderPick)
    else:
        flash("You have to login first!!")
        return render_template('regDBoy.html', title='Delivery Boy Reg', form=form) 


@app.route('/start',methods=['GET','POST'])
def start():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  lane1,lane2,city,state FROM cart_order where uid=2 ")
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('try.html', prod=data )


@app.route('/tryadd',methods=['GET','POST'])
def tryadd():
    if request.method == 'POST':
        lane1 = request.form['lane1']
        lane2 = request.form['lane2']
        city = request.form['city']
        state = request.form['state']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cart_order (order_id,lane1,lane2,city,state,uid) VALUES (%s,%s, %s, %s,%s,%s)", (48851966,lane1,lane2,city,state,2))
        mysql.connection.commit()
        return redirect('base.html')
    return render_template('try.html')


if __name__ == '__main__':
    app.run(port=5004,debug=True)
