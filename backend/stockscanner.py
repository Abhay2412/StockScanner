from flask import Flask, render_template, sessions, url_for, flash, redirect, request, jsonify, session
from flask.helpers import make_response
from flask_mysqldb import MySQL
from analystapi import analyst_api
from belongstoapi import belongsto_api
from businessapi import business_api
from exchangeapi import exchange_api
from offeringapi import offering_api
from stockapi import stock_api

import yaml

from forms import RegistrationForm, LoginForm
app = Flask(__name__) #Instantiating it here

app.register_blueprint(analyst_api)
app.register_blueprint(belongsto_api)
app.register_blueprint(business_api)
app.register_blueprint(exchange_api)
app.register_blueprint(offering_api)
app.register_blueprint(stock_api)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

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

@app.route("/usersall")
def showusers():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM USER")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('usersall.html', title = 'UsersAll', userDetails=userDetails)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            usernameForm = request.form.get('username')
            passwordForm = request.form.get('password')
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM USER Where Username = %s And Password = %s", (usernameForm, passwordForm))
            singleUser = cur.fetchone()
            if singleUser:
                session['loggedin'] = True
                session['username'] = singleUser[0]
                flash('You have been logged in!', 'success')
                return redirect(url_for('profile'))                
            else:
                flash('Login Failed. Please check your credentials again.', 'danger')
    return render_template('login.html', title='Login', form = form)

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('profile.html', username = session['username'])

if __name__ == '__main__':
    app.run(debug=True) #Run it here if the name equals name, also the debug ensures that any update made here will be 
    #changed here immediately onto the server 