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
            permissions = 'testuser'
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                        (username, password, permissions))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showusers'))
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
        resultValue = cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([ID]))
        if resultValue > 0:
            stockDetails = cur.fetchone()

        return render_template('stockInformation.html', username=session['username'], stockDetails=stockDetails)

    if request.method == 'POST':
        #if request.form['postStock'] == 'StockID':
            cur = mysql.connection.cursor()
            new_User = session['username']
            select_stmt = "SELECT List_Number FROM PRIVATE WHERE Username = %s"
            cur.execute(select_stmt, (new_User,))
            listDetails = cur.fetchall()
            newWatchlist = listDetails

            newStockID = request.form.get('StockID')

            cur.execute("INSERT INTO CONTAIN(Stock_ID, Watchlist_ID) VALUES(%s, %s)",
                        (newStockID, newWatchlist))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('watchlistDetails'))


@app.route('/watchlistDetails', methods=['GET'])
def showWatchlist():
    cur = mysql.connection.cursor()
    json = request.json
    new_User = session['username']
    select_stmt = "SELECT List_Number FROM PRIVATE WHERE Username = %s"
    cur.execute(select_stmt, (new_User,))
    listDetails = cur.fetchall()

    newWatchlist = listDetails

    allListDetails=listDetails

    resultValue = cur.execute("SELECT * FROM CONTAIN WHERE Watchlist_ID = %s", ([newWatchlist]))
    if resultValue > 0:
        allListDetails = cur.fetchall()

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
