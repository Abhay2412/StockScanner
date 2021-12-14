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

from forms import RegistrationForm, LoginForm, DeleteFormUser, UpdateFormUser

app = Flask(__name__)  # Instantiating it here

app.register_blueprint(analyst_api)
app.register_blueprint(belongsto_api)
app.register_blueprint(business_api)
app.register_blueprint(exchange_api)
app.register_blueprint(offering_api)
app.register_blueprint(stock_api)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'


@app.route("/", methods=['GET', 'POST'])
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
            permissions = request.form['user_type']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                        (username, password, permissions))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/usersall")
def showusers():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM USER")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('usersall.html', title='UsersAll', userDetails=userDetails)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            usernameForm = request.form.get('username')
            passwordForm = request.form.get('password')
            userAdmin = "Admin"

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM USER Where Username = %s And Password = %s And Permissions= %s", (usernameForm, passwordForm, userAdmin))
            singleUser = cur.fetchone()
            if singleUser and userAdmin == 'Admin':
                session['loggedin'] = True
                session['username'] = singleUser[0]
                flash('You have been logged in!', 'success')
                return redirect(url_for('showAdminView'))

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM USER Where Username = %s And Password = %s", (usernameForm, passwordForm))
            singleUser = cur.fetchone()
            if singleUser:
                session['loggedin'] = True
                session['username'] = singleUser[0]
                flash('You have been logged in!', 'success')
                return redirect(url_for('showStocks'))
            else:
                flash('Login Failed. Please check your credentials again.', 'danger')


    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/showAdminView')
def showAdminView():
    return render_template('showAdminView.html', username=session['username'])

@app.route('/addUserAdmin', methods=['GET', 'POST'])
def addUserAdmin():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = request.form['user_type']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                        (username, password, permissions))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('addUserAdmin.html', title='Add User Admin', form=form)

@app.route('/deleteUserAdmin', methods=['GET', 'POST'])
def deleteUserAdmin():
    form = DeleteFormUser()
    if form.validate_on_submit():
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if(existsStatus == 0):
                flash(f'Account cannot be deleted for {form.username.data} since it does not exist!', 'danger')
                return render_template('deleteUserAdmin.html', title='Delete User Admin', form=form)
            else:
                cur.execute("DELETE FROM USER WHERE USERNAME = %s", ([username]))
                mysql.connection.commit()
                cur.close()
                flash(f'Account deleted for {form.username.data}!', 'success')
                return redirect(url_for('showAdminView'))
    return render_template('deleteUserAdmin.html', title='Delete User Admin', form=form)

@app.route('/updateUserAdmin', methods=['GET', 'POST'])
def updateUserAdmin():
    form = UpdateFormUser()
    if form.validate_on_submit():
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = request.form['user_type']
            cur = mysql.connection.cursor()
            existStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if(existStatus == 0):
                flash(f'Account cannot be updated for {form.username.data} since it does not exist!', 'danger')
                return render_template('updateUserAdmin.html', title='Update User Admin', form=form)
            else:
                cur.execute("UPDATE USER SET username = %s, password = %s, permissions = %s WHERE username = %s", (username, password, permissions, username))
                mysql.connection.commit()
                cur.close()
                flash(f'Account updated for {form.username.data} successfully!', 'success')
                return redirect(url_for('showAdminView'))
    return render_template('updateUserAdmin.html', title='Update User Admin', form=form)


@app.route('/showStocks')
def showStocks():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM STOCK")
    if resultValue > 0:
        stockDetails = cur.fetchall()

    return render_template('showStocks.html', username=session['username'], stockDetails=stockDetails)


@app.route("/stockInformation/<string:ID>", methods=['GET', 'POST'])
def showStockInformation(ID):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([ID]))
        stockDetails = cur.fetchone()
        newPID = stockDetails[2]

        cur.execute("SELECT * FROM PR WHERE P_ID = %s", ([newPID]))
        prDetails = cur.fetchall()

        return render_template('stockInformation.html', username=session['username'], stockDetails=stockDetails, prDetails=prDetails)

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        new_User = session['username']
        select_stmt = "SELECT List_Number FROM PRIVATE WHERE Username = %s"
        cur.execute(select_stmt, (new_User,))
        listDetails = cur.fetchall()
        newWatchlist = listDetails

        newStockID = ID

        cur.execute("INSERT INTO CONTAIN(Stock_ID, Watchlist_ID) VALUES(%s, %s)",
                    (newStockID, newWatchlist))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('watchlistDetails'))


@app.route('/watchlistDetails', methods=['GET'])
def showWatchlist():
    cur = mysql.connection.cursor()
    new_User = session['username']

    select_stmt = "SELECT List_Number FROM PRIVATE WHERE Username = %s"
    resultValue = cur.execute(select_stmt, (new_User,))
    if resultValue > 0:
        listDetails = cur.fetchall()
        newWatchlist = listDetails

    #if listDetail < 0 then scan PRIVATE
    if resultValue <= 0:
        select_stmt = "SELECT List_Number FROM PROFESSIONAL WHERE Username = %s"
        resultValue = cur.execute(select_stmt, (new_User,))
        if resultValue > 0:
            listDetails = cur.fetchall()
            newWatchlist = listDetails

    #newWatchlist > 0 scan for watchlist
    if resultValue > 0:
        cur.execute("SELECT * FROM CONTAIN WHERE Watchlist_ID = %s", ([newWatchlist]))
        allListDetails = cur.fetchall()

    else: allListDetails = resultValue

    # add listDetails to render then make an if statment to check if it exists  if not "contact admin to make watchlist"
    return render_template('watchlist.html', username=session['username'], allListDetails=allListDetails)


@app.route('/eventDetails')
def showEvents():
    return render_template('event.html', username=session['username'])


@app.route('/prDetails')
def showPR():
    return render_template('pr.html', username=session['username'])


@app.route('/week52Details')
def showWeek52():
    return render_template('week52.html', username=session['username'])


if __name__ == '__main__':
    app.run(
        debug=True)  # Run it here if the name equals name, also the debug ensures that any update made here will be
    # changed here immediately onto the server
