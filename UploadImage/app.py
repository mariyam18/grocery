import os
import time
import hashlib
from flask import flash
from flask import url_for
from werkzeug.utils import secure_filename
from flask import Flask,session, render_template, redirect, url_for, request, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_mysqldb import MySQL,MySQLdb
import MySQLdb
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '/home/project/grocery/UploadImage/uploads'
app = Flask(__name__)
app.config['SECRET_KEY'] = '62380aa1db212b7b23d15f5aec36ba7b36'

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

PEOPLE_FOLDER = os.path.join('static','uploads')
app.config['UPLOAD_FOLDER'] =PEOPLE_FOLDER

app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads') # you'll need to create a folder named uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

ALLOWED_EXTENSIONS = {'jpg'}
class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image Only!'), FileRequired('Choose a file!')])
    submit = SubmitField('Upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/hj', methods=['GET', 'POST'])
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


@app.route('/deletefile/<filename>')
def delete_file(filename):
    file_path = photos.path(filename)
    os.remove(file_path)
    return redirect(url_for('manage_file'))




@app.route('/home')
def home():
    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Fruits.jpg')
    return render_template('home.html')


@app.route('/product_find/<ty>',methods=['GET', 'POST'])
def product_find(ty):
    session['user'] = 'anoor@gmail.com'
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
        itemArray = { str(row['Product_id']) : { 'name':row['P_name'], 'price':row['P_actual_price'], 'quantity': quantity, 'total_price':quantity*row['P_actual_price'], 'shopname':row['shop_name'], 'shop_add':row['shop_add'],'shop_city':row['shop_city'],'shop_district':row['shop_district'], 'shop_state':row['shop_state'] }}
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
        cur.execute("INSERT INTO cart_order(order_id,total_price,total_quantity,lane1,lane2,city,state,uid,status_value) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,0)",(id(x),total_price,total_quantity,lane1,lane2,city,state,uid))
        #Inserting data into order_item  
        for key, value in session['cart_item'].items():
            Product_id = int(key)
            name = session['cart_item'][key]['name']
            price = int(session['cart_item'][key]['price'])
            individual_quantity = int(session['cart_item'][key]['quantity'])
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
            cur.execute("INSERT INTO order_item(Product_id,P_name,P_price,P_quantity,P_total_price,order_id,shop_id) VALUES(%s,%s,%s,%s,%s,%s,%s)",(Product_id,name,price,individual_quantity,individual_price,id(x),user['shop_id']))
            mysql.connection.commit()
            cur.close()
        session.pop('all_total_quantity',None)
        session.pop('all_total_price',None)
        session.pop('cart_item',  None)
    return redirect(url_for('.track'))


@app.route('/track',methods=['GET', 'POST'])
def track():
    uid = int(session['uid'])
    print(session['uid'],uid,"hiiiiiiiiiiiiiiii",type(session['uid']))
    cur = mysql.connection.cursor()
    cur.execute("select order_item.P_name , order_item.P_price , order_item.P_quantity , order_item.P_total_price,order_item.order_id , cart_order.total_price , cart_order.total_quantity , cart_order.lane1 , cart_order.lane2 , cart_order.city , cart_order.state , cart_order.uid , cart_order.status_value ,Shopkeeper.shop_name , Shopkeeper.shopkeeper_contact , Shopkeeper.shop_add , Shopkeeper.shop_city from order_item , cart_order , Shopkeeper where order_item.order_id = cart_order.order_id and order_item.shop_id = Shopkeeper.shop_id and cart_order.uid=%s",(uid,))
    data = cur.fetchall()
    print("DATAA",data)
    temp_orderid = {} #storing order_id 
    temp_shop_product1 = {} #storing product details of shop
    temp_shop_product2 = {} #storing shop details
    for da in data:
        print(da)
        if(da[4] not in temp_orderid):
            print(da[4])
            key = da[4]
            temp_orderid.setdefault(key,[])
            temp_orderid[key].append(da[13])  
            if(da[13] not in temp_shop_product1):
                print(da[13])
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
                temp_orderid[key].append(da[13])
            if (da[13] not in temp_shop_product1):
                print(da[13])
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
    '''
    temp_details1 = []
    temp_details2 = []
    order_details1 = []
    order_details2 = []
    print(data)
    for da in data:
        temp_details1.append(da[0])
        temp_details1.append(da[1])
        temp_details1.append(da[2])
        temp_details1.append(da[3])
        temp_details2.append(da[4])
        temp_details2.append(da[5])
        temp_details2.append(da[6])
        temp_details2.append(da[7])
        temp_details2.append(da[8])
        temp_details2.append(da[9])
        temp_details2.append(da[10])
        temp_details2.append(da[11])
        temp_details2.append(da[12])
        temp_details2.append(da[13])
        temp_details2.append(da[14])
        temp_details2.append(da[15])
        temp_details2.append(da[16])
        order_details1.append(temp_details1)
        order_details1.append(temp_details2)
    '''
    return render_template('track.html',odrer_id=temp_orderid,product1=temp_shop_product1,product2=temp_shop_product2)

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
    return render_template('spice.html')


@app.route('/prod')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM product")
    data = cur.fetchall()
    cur.close()
    return render_template('adding.html', prod=data )




@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        price = request.form['price']
        available = request.form['available']
        category = request.form['category']
        weight = request.form['weight']
        manufacture = request.form['manufacture']
        expiry = request.form['expiry']
        file = request.files['file']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO product (name, price,category, available,weight,manu_date,expiry_date,image) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)", (name, price,category, available,weight,manufacture,expiry,file.filename))
        mysql.connection.commit()
        file = request.files['file']
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
	    #os.rename(UPLOAD_FOLDER +filename,UPLOAD_FOLDER +'bear.jpg')
        
        return redirect(url_for('Index'))



@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM product WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))




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
        cur = mysql.connection.cursor()
        cur.execute("UPDATE product SET name=%s, price=%s,category=%s, available=%s,weight=%s,manu_date=%s,expiry_date=%s WHERE id=%s",(name, price,category, available,weight,manufacture,expiry, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/orderdetail')
def orderdetail():
    lis = []
    order =[]
    detail = []
    cur = mysql.connection.cursor()
    cur.execute("select distinct order_id from order_item where shop_id = 2")
    order = cur.fetchall()
    print(order)
    res= len(order)
    print(res)
    for i in range(0,res):
        cur.execute("select distinct order_id,P_name,P_quantity,P_price,P_total_price,lane1,lane2,city,state,email from order_item natural join cart_order natural join Users where order_id=%s and shop_id=2",(order[i]))
        detail=cur.fetchall()


    dd =len(lis)
    print(dd)
    print('sajgagfhegs')
    cur.close()
    return render_template('orderdetail.html',det=lis,order_id=order,length=dd )



@app.route('/send',methods=['POST','GET'])
def send():
	return render_template('sendotp.html')

@app.route('/sendotp',methods=['POST','GET'])
def sendotp():
	if request.method == 'POST':
		num = request.form['number']
		print(num)
		verification_code = generate_code()
		session['number'] = verification_code
		payload = {'sender_id': 'FSTSMS', 'language':'english','route':'qt','numbers': num, 'message': '21251','variables': '{#AA#}', 'variables_values': verification_code}
		response = requests.request("POST", url, data=payload, headers=headers)
		print(payload)
		print(response.text)
	return render_template('confirmotp.html')

@app.route('/confirmotp',methods=['POST','GET'])
def confirmotp():
	if request.method == 'POST':
		num = request.form['verification']
		print(session['number'])
		if(num == session['number']):
			print(session['number'],num)
			return render_template('sendotp.html')
	return render_template('confirmotp.html')


def generate_code():
    return str(random.randrange(10000, 99999))


    

@app.route('/shopreg',methods=['POST'])
def shopreg():
    #flash("Data Inserted Successfully")
    if request.method == "POST":
        flash("Data Inserted Successfully")
        shopname = request.form['shopname']
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        dob = request.form['dob']
        shopadd = request.form['shopadd']
        city = request.form['city']
        district = request.form['district']
        state = request.form['state']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Shopkeeper (shop_name,shopkeeper_contact ,shopkeeper_name, shopkeeper_dob,shopkeeper_email,shop_add,shop_city,shop_district,shop_state) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)",(name, number,shopname, dob,email,shopadd,city,district,state))
        mysql.connection.commit()
    return render_template('shopregister.html')

'''
        file = request.files['file']
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
	    #os.rename(UPLOAD_FOLDER +filename,UPLOAD_FOLDER +'bear.jpg')
        
        return redirect(url_for('Index'))
'''






if __name__ == '__main__':
    app.run(port=5003,debug=True)
