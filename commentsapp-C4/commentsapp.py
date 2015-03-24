import os,hashlib,traceback

from flask import Flask, render_template, url_for, request,redirect,session
app = Flask(__name__)
import pymysql,json
def md5(word):
    hash = hashlib.md5()
    hash.update(word.encode('utf-8'))
    return hash.hexdigest()
@app.route('/')
def display_home():
    session['OwnerId'] = None
    return render_template("home.html",
                           the_title="Welcome to the OBD Reader application",
                           login_url=url_for("loginscreen"),
                           working_dir= os.getcwd())

@app.route('/loginscreen')
def loginscreen():
    return render_template("login.html",register_url=url_for('register'))

@app.route('/login', methods=['POST'])
def login():

    conn = pymysql.connect(host='mysql.server', port=3306, user='chiloutus', passwd='gaz360', db='chiloutus$obdreader')

    cur = conn.cursor()

    sql ="SELECT * FROM Owner WHERE email = \"" + request.form['Email'] + "\" AND password = \""+ md5(request.form['Password']) + "\""


    if cur.execute(sql) != 0:
        result = cur.fetchall()
        session['OwnerId'] = result[0][0]
        return render_template('webApp.html',vehicle_data_url = url_for('vehicleData'),add_vehicle_url = url_for('addVehicle'),owner_data_url =url_for('ownerData'),
                               sign_out_url=url_for('signOut') )
    else:
        error = "Invalid credentials"
        return render_template('login.html',
                               car_data_url=url_for("vehicleData"),
                               messages = error)

@app.route('/webApp')
def webApp():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the Word Game, where all the fun is at.",
                               login_url=url_for("loginscreen"),)

    return render_template('webApp.html',vehicle_data_url = url_for('vehicleData'),add_vehicle_url = url_for('addVehicle'),owner_data_url =url_for('ownerData'),
                               sign_out_url=url_for('signOut') )

@app.route('/vehicleData')
def vehicleData():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the Word Game, where all the fun is at.",
                               login_url=url_for("loginscreen"),)

    conn = pymysql.connect(host='mysql.server', port=3306, user='chiloutus', passwd='gaz360', db='chiloutus$obdreader')

    cur = conn.cursor()
    id = str(session['OwnerId'])
    print(id)
    sql = "SELECT * FROM Car WHERE OwnerId = {}".format(id)

    if cur.execute(sql) != 0:
        result = list(cur.fetchall())
        return render_template('vehicleData.html',result = result,home_url = url_for('webApp'))
    else:
        error = "There is no record of your vehicle, consider adding one."
        return render_template('webApp.html',vehicle_data_url = url_for('vehicleData'),add_vehicle_url = url_for('addVehicle'),owner_data_url =url_for('ownerData'),
                               sign_out_url=url_for('signOut'),messages = error )

@app.route('/ownerData')
def ownerData():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the Word Game, where all the fun is at.",
                               login_url=url_for("loginscreen"),)

    conn = pymysql.connect(host='mysql.server', port=3306, user='chiloutus', passwd='gaz360', db='chiloutus$obdreader')

    cur = conn.cursor()
    id = str(session['OwnerId'])
    print(id)
    sql = "SELECT Username,Name,Address,Email FROM Owner WHERE OwnerId = {}".format(id)

    if cur.execute(sql) != 0:
        result = list(cur.fetchall())
        return render_template('ownerData.html',result = result,home_url = url_for('webApp'))
    else:
        error = "An error has occured retrieving your account."
        return render_template('webApp.html',vehicle_data_url = url_for('vehicleData'),add_vehicle_url = url_for('addVehicle'),owner_data_url =url_for('ownerData'),
                               sign_out_url=url_for('signOut'), messages=error)
@app.route('/journeyData')
def ownerData():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the Word Game, where all the fun is at.",
                               login_url=url_for("loginscreen"),)

    conn = pymysql.connect(host='mysql.server', port=3306, user='chiloutus', passwd='gaz360', db='chiloutus$obdreader')

    cur = conn.cursor()

    sql = "SELECT * FROM Journey Inner Join  WHERE OwnerId = " + session['OwnerId']

    if cur.execute(sql) != 0:
        result = list(cur.fetchall())
        return render_template('ownerData.html',result = result,home_url = url_for('webApp'))
    else:
        error = "An error has occured retrieving your account."
        return render_template('webApp.html',vehicle_data_url = url_for('vehicleData'),add_vehicle_url = url_for('addVehicle'),owner_data_url =url_for('ownerData'),
                               sign_out_url=url_for('signOut'),messages = error )
@app.route('/addVehicle')
def addVehicle():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the Word Game, where all the fun is at.",
                               login_url=url_for("loginscreen"),)
    return render_template('addVehicle.html',home_url= url_for('webApp'))
@app.route('/addingVehicle', methods=['POST'])
def addingVehicle():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the Word Game, where all the fun is at.",
                               login_url=url_for("loginscreen"),)
    conn = pymysql.connect(host='mysql.server', port=3306, user='chiloutus', passwd='gaz360', db='chiloutus$obdreader')

    cur = conn.cursor()
    registration = request.form.get("Registration")
    make = request.form.get("Make")
    model = request.form.get("Model")

    sql = "INSERT INTO Car (`registration`, `OwnerId`, `make`, `model`) VALUES ('{0}','{1}','{2}','{3}')".format(registration,str(session['OwnerId']),make,model)
    print(sql)
    try:
        cur.execute(sql)
        conn.commit()
        update = "The vehicle was added to your account succesfully"
        return render_template('webApp.html', messages=update, home_url=url_for('webApp'), vehicle_data_url = url_for('vehicleData'),
                               add_vehicle_url=url_for('addVehicle'))
    except:
        conn.rollback()
        error = "There was an error adding your vehicle to the database, please contact customer support"
        return render_template('webApp.html', messages = error,home_url=url_for('webApp'), vehicle_data_url = url_for('vehicleData'),
                               add_vehicle_url=url_for('addVehicle'))
@app.route('/register')
def register():
    return render_template('register.html',home_url = url_for('webApp'))

@app.route('/registering',methods=['POST'])
def registering():
    conn = pymysql.connect(host='mysql.server', port=3306, user='chiloutus', passwd='gaz360', db='chiloutus$obdreader')

    cur = conn.cursor()
    username = request.form.get("username")
    name = request.form.get("name")
    email = request.form.get("email")
    passWord = md5((request.form.get("pass1")))
    address = request.form.get("address")

    #check if the username is already in the database
    sql = "SELECT Username FROM Owner WHERE Username = \"" + username + "\""

    try:
        cur.execute(sql)
        res = cur.rowcount
        if res != 0:
            return render_template('register.html',home_url = url_for('webApp'),
                                   messages= "This username has already been taken, please try again, there were  " + cur.rowcount + "other entries")


        sql = "SELECT OwnerId FROM Owner"
        cur.execute(sql)
        row = cur.fetchone()
        id = 0
        while row is not None:
            if(int(row[0]) > id):
                id = int(row[0])
            row = cur.fetchone()

        id += 1
        sql = "INSERT INTO Owner (OwnerId,Username,Password,Address,Email,Name) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')"\
            .format(id,username,passWord,address,email,name)

        cur.execute(sql)

        conn.commit()
        update = "Your account was created succesfully"
        return render_template("login.html",register_url=url_for('register'))
    except Exception as err:

        conn.rollback()
        error = "There was an error adding your account to the database, please contact customer support"
        return render_template('register.html',home_url = url_for('webApp'),messages= traceback.format_exc())


@app.route('/new/user', methods=['POST'])
def new_user():
    conn = pymysql.connect(host='mysql.server', port=3306, user='chiloutus', passwd='gaz360', db='chiloutus$obdreader')

    cur = conn.cursor()

    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            sql = "SELECT OwnerId FROM Owner"
            try:
                cur.execute(sql)
                row = cur.fetchone()
                id = 0
                while row is not None:
                    if(int(row[0]) > id):
                        id = int(row[0])
                    row = cur.fetchone()

                id += 1

                #unpack JSON
                # Parse the JSON
                objs = json.loads(request.POST)

                # Iterate through the stuff in the list
                for o in objs:
                    firstName = o.firstName
                    lastName = o.lastName
                    email = o.email
                    passwd = o.passwd



                sql = "INSERT INTO Owner (OwnerId,firstName,lastName,email,password) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(id,firstName,lastName,email,passwd)

                cur.execute(sql)

                conn.commit()
            except:
                #do something
                print("error")


@app.route('/signOut')
def signOut():
    session['OwnerId'] = None

    return render_template("home.html",
                           the_title="Welcome to the Word Game, where all the fun is at.",
                           login_url=url_for("loginscreen"))
app.config['SECRET_KEY'] = 'This is a secret key'
if __name__== "__main__":
    app.run(host='0.0.0.0',debug=True)
