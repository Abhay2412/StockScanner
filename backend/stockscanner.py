from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
import yaml

from forms import RegistrationForm, LoginForm
app = Flask(__name__) #Instantiating it here

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

posts = [ #from the database suppose it 
    {
    "ID":"MSFT",
    "StockPrice":"333.13",
    "Sector":"Technology",
    "Exchange":"NASDAQ",
    },

    {
    "ID":"AAPL",
    "StockPrice":"150.02",
    "Sector":"Technology",
    "Exchange":"NASDAQ",
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home', posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = 'testuser'
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)", (username, password, permissions))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showusers'))  
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form = form)
    return jsonify({'username': userDetails})

@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'abhaykhosla0@gmail.com' and form.password == 'thisisatestforcpsc471':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check your credentials again.', 'danger')
    return render_template('login.html', title='Login', form = form)


#----------------------------------------Start of the API Calls------------------------------------------------------------
@app.route("/usersall")
def showusers():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM USER")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return jsonify({'username': userDetails})

@app.route("/user/<string:username>", methods = ['GET'])
def getuser(username):
    cur = mysql.connection.cursor()
    select_stmt = "SELECT * FROM USER WHERE username = %s"
    cur.execute(select_stmt, (username,))
    userDetails = cur.fetchall()
    return jsonify({'username': userDetails})



# @app.route("/adduser", methods=['POST'])
# def adduser():
#     json = request.json
#     new_username = json['Username']
#     new_password = json['Password']
#     new_permissions = json['Permissions']
#     # new_permissions = 'testuser'
#     cur = mysql.connection.cursor()
#     cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
#                 (new_username, new_password, new_permissions))
#     mysql.connection.commit()
#     cur.close()
#     return "Stock inserted successfully"

# @app.route("/stocksshowing", methods = ['GET'])
# def showstocks():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector FROM STOCK")
#     stocks_row = cur.fetchall()
#     respone = jsonify({'Stock': stocks_row})
#     respone.status_code = 200
#     cur.close()
#     return respone

# @app.route("/addstocks", methods = ['POST'])
# def addstocks():
#         cur = mysql.connection.cursor()
#         json = request.json
#         new_ID = json['ID']
#         new_Company_ID = json['Company_ID']
#         new_Prediction_ID = json['Prediction_ID']
#         new_Predict_Stock_Price = json['Predict_Stock_Price']
#         new_Strong_Buy = json['Strong_Buy']
#         new_Rating_Buy = json['Rating_Buy']
#         new_Rating_Sell = json['Rating_Sell']
#         new_Strong_Sell = json['Strong_Sell']
#         new_Rating_Hold = json['Rating_Hold']
#         new_Stock_Price = json['Stock_Price']
#         new_Sector = json['Sector']
#         new_PID = json['P_ID']
#         new_Founding_Date = json['Founding_Date']
#         new_Address = json['Address']
#         new_Business_Name = json['Business_Name']
#
#         cur.execute("INSERT INTO PREDICTION(P_ID), VALUES(%s)", ([new_PID]))
#         cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name), VALUES(%s, %s, %s, %s)", (new_Company_ID, new_Founding_Date, new_Address, new_Business_Name))
#         cur.execute("INSERT INTO STOCK(ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy, new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector))
#         mysql.connection.commit()
#         cur.close()
#         return "Stock inserted successfully"

#----------------------------------------End of the API Calls--------------------------------------------------------------



if __name__ == '__main__':
    app.run(debug=True) #Run it here if the name equals name, also the debug ensures that any update made here will be 
    #changed here immediately onto the server 