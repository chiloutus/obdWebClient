import os,hashlib,traceback,time
from flask import Flask, render_template, url_for, request,redirect,session
app = Flask(__name__)
import pymysql,json
def md5(word):
    hash = hashlib.md5()
    hash.update(word.encode('utf-8'))
    return hash.hexdigest()

def connectToDB():
    return pymysql.connect(host='localhost', port=3306, user='root', passwd='gaz360', db='obdreader')
@app.route('/')
def display_home():
    return render_template("home.html",
                           the_title="Welcome to the OBD Reader application",
                           login_url=url_for("loginscreen"),
                           working_dir= os.getcwd())

@app.route('/loginscreen')
def loginscreen():
    return render_template("login.html",register_url=url_for('register'))

@app.route('/login', methods=['POST'])
def login():

    conn = connectToDB()

    cur = conn.cursor()

    sql ="SELECT * FROM Owner WHERE email = \"" + request.form['Email'] + "\" AND password = \""+ md5(request.form['Password']) + "\""


    if cur.execute(sql) != 0:
        result = cur.fetchall()
        session['OwnerId'] = str(result[0][0])
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
                               the_title="Welcome to the OBD Reader, where all the fun is at.",
                               login_url=url_for("loginscreen"),)

    return render_template('webApp.html',vehicle_data_url = url_for('vehicleData'),add_vehicle_url = url_for('addVehicle'),owner_data_url =url_for('ownerData'),
                               sign_out_url=url_for('signOut') )

@app.route('/vehicleData')
def vehicleData():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the OBD Reader, where all the fun is at.",
                               login_url=url_for("loginscreen"),)

    conn = connectToDB()

    cur = conn.cursor()
    i = session['OwnerId']
    sql = "SELECT * FROM Car WHERE OwnerId = \" "+ i + "\""

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
                               the_title="Welcome to the OBD Reader, where all the fun is at.",
                               login_url=url_for("loginscreen"),)

    conn = connectToDB()

    cur = conn.cursor()
    id = session['OwnerId']
    print(id)
    sql = "SELECT Username,Name,Address,Email FROM Owner WHERE OwnerId = {}".format(id)

    if cur.execute(sql) != 0:
        result = list(cur.fetchall())
        return render_template('ownerData.html',result = result,home_url = url_for('webApp'))
    else:
        error = "An error has occured retrieving your account."
        return render_template('webApp.html',vehicle_data_url = url_for('vehicleData'),add_vehicle_url = url_for('addVehicle'),owner_data_url =url_for('ownerData'),
                               sign_out_url=url_for('signOut'), messages=error)
@app.route('/addVehicle')
def addVehicle():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the OBD Reader, where all the fun is at.",
                               login_url=url_for("loginscreen"),)
    return render_template('addVehicle.html',home_url= url_for('webApp'))
@app.route('/getJourney')
def getJourney():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the OBD Reader, where all the fun is at.",
                               login_url=url_for("loginscreen"),)
    conn = connectToDB()
    cur = conn.cursor()
    reg = request.args.get('reg')
    sql = "SELECT * FROM Journey WHERE Registration = \"{}\"".format(reg)
    if cur.execute(sql) != 0:
        result = list(cur.fetchall())
        return render_template('getJourney.html',result = result,home_url = url_for('webApp'))
    else:
        conn.rollback()
        error = "Sorry, we could not find any Journey data for that car"
        return render_template('webApp.html', messages = error,home_url=url_for('webApp'), vehicle_data_url = url_for('vehicleData'),
                               add_vehicle_url=url_for('addVehicle'))
@app.route('/getTimeStamp')
def getTimestamp():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the OBD Reader, where all the fun is at.",
                               login_url=url_for("loginscreen"))
    conn = connectToDB()
    cur = conn.cursor()
    id = request.args.get('id')
    sql = "SELECT * FROM Timestamp WHERE idJourney = \"{}\"".format(id)
    if cur.execute(sql) != 0:
        result = list(cur.fetchall())
        return render_template('getJourney.html',result = result,home_url = url_for('webApp'))
    else:
        conn.rollback()
        error = "Sorry, we could not find any Journey data for that car"
        return render_template('webApp.html', messages = error,home_url=url_for('webApp'), vehicle_data_url = url_for('vehicleData'),
                               add_vehicle_url=url_for('addVehicle'))


@app.route('/addingVehicle', methods=['POST'])
def addingVehicle():
    if session['OwnerId'] is None:
        return render_template("home.html",
                               the_title="Welcome to the OBD Reader, where all the fun is at.",
                               login_url=url_for("loginscreen"),)
    conn = connectToDB()

    cur = conn.cursor()
    registration = request.form.get("Registration")
    make = request.form.get("Make")
    model = request.form.get("Model")
    ftype = request.form.get("FType")

    sql = "INSERT INTO Car (registration, OwnerId, Make, Model, FuelType) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(registration, str(session['OwnerId']), make, model, ftype)
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
    conn = connectToDB()

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

        sql = "INSERT INTO Owner (Username,Password,Address,Email,Name) VALUES ('{0}','{1}','{2}','{3}','{4}')"\
            .format(username,passWord,address,email,name)

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
    conn = connectToDB()

    cur = conn.cursor()

    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            print("The post statement worked")
            sql = "SELECT OwnerId FROM Owner"
            try:
                cur.execute(sql)
                print("STEVE?")
                row = cur.fetchone()
                print("STEVE???")
                id = 0
                while row is not None:
                    print("STEVE>>>")
                    if(int(row[0]) > id):
                        id = int(row[0])
                        print("ALAN!")
                    row = cur.fetchone()

                id += 1
                print("The while loop finished, I mean it should")
                #unpack JSON
                # Parse the JSON
                raw_obj = request.get_json()
                obj = json.loads(raw_obj)
                print(obj['address'])

                username = obj['username']
                email = obj['email']
                passWord = obj['passwd']
                address = obj['address']
                name = obj['name']


                print(username,email,passWord,address,name)

                sql = "INSERT INTO Owner (OwnerId,Username,Password,Address,Email,Name) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')" \
                    .format(id,username,passWord,address,email,name)
                cur.execute(sql)

                conn.commit()

                return "Success"
            except Exception as e:
                #do something
                print("error")
                print(traceback.format_exc())
                return "Error, bad one"

    else:
        return "Error"

@app.route('/new/journey', methods=['POST'])
def new_journey():
    conn = connectToDB()

    cur = conn.cursor()

    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            try:
                row = cur.fetchone()
                #unpack JSON
                # Parse the JSON
                raw_obj = request.get_json()
                obj = json.loads(raw_obj)
                #get current time
                curTime = time.strftime("%c")
                registration = obj['registration']


                print(username,email,passWord,address,name)

                sql = "INSERT INTO Journey (startTime,endTime,Registration) VALUES ('{0}','{1}','{2}')" \
                    .format(curTime,"",registration)
                cur.execute(sql)

                conn.commit()

                return "Success"
            except Exception as e:
                #do something
                print("error")
                print(traceback.format_exc())
                return "Error, bad one"

    else:
        return "Error"

@app.route('/signOut')
def signOut():
    session['OwnerId'] = None

    return render_template("home.html",
                           the_title="Welcome to the OBD Reader, where all the fun is at.",
                           login_url=url_for("loginscreen"))
app.config['SECRET_KEY'] = 'This is a secret key'
if __name__== "__main__":
    app.run(host='0.0.0.0',debug=True)
