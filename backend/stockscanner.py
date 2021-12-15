from flask import Flask, render_template, sessions, url_for, flash, redirect, request, jsonify, session
from flask.helpers import make_response
from flask_mysqldb import MySQL
from analystapi import analyst_api
from businessapi import delete_business
from exchangeapi import delete_exchange
from belongstoapi import belongsto_api
from businessapi import business_api
from exchangeapi import exchange_api
from offeringapi import offering_api
from stockapi import stock_api
from random import randrange

import yaml

from forms import RegistrationForm, LoginForm, DeleteFormUser, UpdateFormUser, AddFormExchange, DeleteFormExchange
from forms import UpdateFormExchange, AddFormBusiness, DeleteFormBusiness, UpdateFormBusiness

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
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = request.form['user_type']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if(existsStatus == 1):
                flash(f'Account cannot be created for {form.username.data} since it already exists!', 'danger')
                return render_template('register.html', title='Register', form=form)
            else: 
                cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                            (username, password, permissions))    
                flash(f'Account created for {form.username.data}!', 'success')
                if(permissions == 'Private'):
                    watchlistId = randrange(1, 10001)
                    existsStatus1 = cur.execute("SELECT * FROM Watchlist WHERE List_Number = %s", ([watchlistId]))
                    if(existsStatus1 == 1):
                        watchlistIdNew = randrange(10001, 20000)
                        if(watchlistId != watchlistIdNew):
                            cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                            ([watchlistIdNew])) 
                            cur.execute("INSERT INTO PRIVATE(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                            (username, watchlistId, permissions))    
                    else:                            
                        cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                ([watchlistId]))   
                        cur.execute("INSERT INTO PRIVATE(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                            (username, watchlistId, permissions))    

                if(permissions == 'Professional'):
                    watchlistId = randrange(20001, 30001)
                    existsStatus2 = cur.execute("SELECT * FROM Watchlist WHERE List_Number = %s", ([watchlistId]))
                    if(existsStatus2 == 1):
                        watchlistIdNew = randrange(30002, 40002)
                        if(watchlistId != watchlistIdNew):
                            cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                            ([watchlistIdNew])) 
                            cur.execute("INSERT INTO PROFESSIONAL(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                            (username, watchlistId, permissions))    
                    else:                            
                        cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                ([watchlistId]))   
                        cur.execute("INSERT INTO PROFESSIONAL(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                            (username, watchlistId, permissions)) 
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
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = request.form['user_type']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if(existsStatus == 1):
                flash(f'Account cannot be created for {form.username.data} since it already exists!', 'danger')
                return render_template('register.html', title='Register', form=form)
            else: 
                cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                            (username, password, permissions))    
                flash(f'Account created for {form.username.data}!', 'success')
                if(permissions == 'Private'):
                    watchlistId = randrange(1, 10001)
                    existsStatus1 = cur.execute("SELECT * FROM Watchlist WHERE List_Number = %s", ([watchlistId]))
                    if(existsStatus1 == 1):
                        watchlistIdNew = randrange(10001, 20000)
                        if(watchlistId != watchlistIdNew):
                            cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                            ([watchlistIdNew])) 
                            cur.execute("INSERT INTO PRIVATE(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                            (username, watchlistId, permissions))    
                    else:                            
                        cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                ([watchlistId]))   
                        cur.execute("INSERT INTO PRIVATE(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                            (username, watchlistId, permissions))    

                if(permissions == 'Professional'):
                    watchlistId = randrange(20001, 30001)
                    existsStatus2 = cur.execute("SELECT * FROM Watchlist WHERE List_Number = %s", ([watchlistId]))
                    if(existsStatus2 == 1):
                        watchlistIdNew = randrange(30002, 40002)
                        if(watchlistId != watchlistIdNew):
                            cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                            ([watchlistIdNew])) 
                            cur.execute("INSERT INTO PROFESSIONAL(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                            (username, watchlistId, permissions))    
                    else:                            
                        cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                ([watchlistId]))   
                        cur.execute("INSERT INTO PROFESSIONAL(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                            (username, watchlistId, permissions)) 
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

@app.route('/addExchangeAdmin', methods=['GET', 'POST'])
def addExchangeAdmin():
    form = AddFormExchange()
    if form.validate_on_submit():
        if request.method == 'POST':
            exchangeDetails = request.form
            name = exchangeDetails['name']
            location = exchangeDetails['location']
            numberOfTickers = request.form['number_of_tickers']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM EXCHANGES WHERE NAME = %s", ([name]))
            if(existsStatus == 1):
                flash(f'Exchange with the name {form.name.data} cannot be created since it already exists!', 'danger')
                return render_template('addExchangeAdmin.html', title='Add Exchange Admin', form=form)
            else:
                cur.execute("INSERT INTO EXCHANGES(Name, Location, Number_of_Tickers) VALUES(%s, %s, %s)", (name, location, numberOfTickers))
                flash(f'Exchange with the name {form.name.data} created successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('addExchangeAdmin.html', title='Add Exchange Admin', form=form)

@app.route('/deleteExchangeAdmin', methods=['GET', 'POST'])
def deleteExchangeAdmin():
    form = DeleteFormExchange()
    if form.validate_on_submit():
        if request.method == 'POST':
            exchangeDetails = request.form
            name = exchangeDetails['name']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM EXCHANGES WHERE NAME = %s", ([name]))
            if(existsStatus == 0):
                flash(f'Exchange with the name {form.name.data} does not exist!', 'danger')
                return render_template('deleteExchangeAdmin.html', title='Delete Exchange Admin', form=form)
            else:
                delete_exchange(name)
                flash(f'Exchange with the name {form.name.data} deleted successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('deleteExchangeAdmin.html', title='Delete Exchange Admin', form=form)

@app.route('/updateExchangeAdmin', methods=['GET', 'POST'])
def updateExchangeAdmin():
    form = UpdateFormExchange()
    if form.validate_on_submit():
        if request.method == 'POST':
            exchangeDetails = request.form
            cur = mysql.connection.cursor()
            name = exchangeDetails['name']
            location = exchangeDetails['location']
            numberOfTickers = request.form['number_of_tickers']
            existsStatus = cur.execute("SELECT * FROM EXCHANGES WHERE NAME = %s", ([name]))
            if(existsStatus == 0):
                flash(f'Exchange with the name {form.name.data} cannot be updated since it does not exists!', 'danger')
                return render_template('updateExchangeAdmin.html', title='Update Exchange Admin', form=form)
            else:
                cur.execute("UPDATE EXCHANGES SET Name = %s, Location = %s, Number_of_Tickers = %s WHERE Name = %s", (name, location, numberOfTickers, name))
                flash(f'Exchange with the name {form.name.data} updated successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('updateExchangeAdmin.html', title='Update Exchange Admin', form=form)

@app.route('/showExchangeAdmin')
def showExchangeAdmin():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM EXCHANGES")
    if resultValue > 0:
        exchangeDetails = cur.fetchall()

    return render_template('showExchanges.html', title='Show Exchanges Admin', exchangeDetails=exchangeDetails)

@app.route('/addBusinessAdmin', methods=['GET', 'POST'])
def addBusinessAdmin():
    form = AddFormBusiness()
    if form.validate_on_submit():
        if request.method == 'POST':
            businessDetails = request.form
            business_id = businessDetails['business_id']
            address = businessDetails['address']
            founding_date = businessDetails['founding_date']
            business_name = businessDetails['business_name']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([business_id]))
            if(existsStatus == 1):
                flash(f'Business with the name {form.business_name.data} cannot be created since it already exists!', 'danger')
                return render_template('addBusinessAdmin.html', title='Add Business Admin', form=form)
            else:
               cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)", (business_id, address, founding_date, business_name))
               flash(f'Business with the name {form.business_name.data} created successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('addBusinessAdmin.html', title='Add Business Admin', form=form)

@app.route('/deleteBusinessAdmin', methods=['GET', 'POST'])
def deleteBusinessAdmin():
    form = DeleteFormBusiness()
    if form.validate_on_submit():
        if request.method == 'POST':
            businessDetails = request.form
            business_id = businessDetails['business_id']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([business_id]))
            if(existsStatus == 0):
                flash(f'Business with the ID {form.business_id.data} does not exist!', 'danger')
                return render_template('deleteBusinessAdmin.html', title='Delete Business Admin', form=form)
            else:
                delete_business(business_id)
                flash(f'Business with the ID {form.business_id.data} deleted successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('deleteBusinessAdmin.html', title='Delete Business Admin', form=form)

@app.route('/updateBusinessAdmin', methods=['GET', 'POST'])
def updateBusinessAdmin():
    form = UpdateFormBusiness()
    if form.validate_on_submit():
        if request.method == 'POST':
            businessDetails = request.form
            business_id = businessDetails['business_id']
            address = businessDetails['address']
            founding_date = businessDetails['founding_date']
            business_name = businessDetails['business_name']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([business_id]))
            if(existsStatus == 0):
                flash(f'Business with the name {form.business_name.data} cannot be updated since it does not exists!', 'danger')
                return render_template('updateBusinessAdmin.html', title='Update Business Admin', form=form)
            else:
               cur.execute("UPDATE BUSINESS SET Business_ID=%s, Address=%s, Founding_Date=%s, Business_Name=%s WHERE Business_ID=%s", (business_id, address, founding_date, business_name, business_id))
               flash(f'Business with the name {form.business_name.data} updated successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('updateBusinessAdmin.html', title='Update Business Admin', form=form)

@app.route('/showBusinessAdmin')
def showBusinessAdmin():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM BUSINESS")
    if resultValue > 0:
        businessDetails = cur.fetchall()

    return render_template('showBusinesses.html', title='Show Businesses Admin', businessDetails=businessDetails)

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

        resultValue = cur.execute("SELECT * FROM STOCKEVENT WHERE STOCK_ID = %s", ([ID]))
        if resultValue > 0:
            dateDetails = cur.fetchall()
        else:
            dateDetails = resultValue

        resultValue = cur.execute("SELECT * FROM STOCKEVENT WHERE STOCK_ID = %s", ([ID]))
        if resultValue > 0:
            sDetails = cur.fetchone()
            newPID = sDetails[2]
            cur.execute("SELECT * FROM PR WHERE P_ID = %s", ([newPID]))
            prDetails = cur.fetchall()

        else: prDetails = resultValue

        return render_template('stockInformation.html', username=session['username'], stockDetails=stockDetails,dateDetails=dateDetails, prDetails=prDetails)

    # if request.method == 'POST':
    #
    #     cur = mysql.connection.cursor()
    #     new_User = session['username']
    #     select_stmt = "SELECT List_Number FROM PRIVATE WHERE Username = %s"
    #     cur.execute(select_stmt, (new_User,))
    #     listDetails = cur.fetchone()
    #     newWatchlist = listDetails
    #
    #     cur.execute("INSERT INTO CONTAIN(Stock_ID, Watchlist_ID) VALUES(%s, %s)",
    #                 (ID, newWatchlist))
    #     mysql.connection.commit()
    #     cur.close()
    #     return redirect(url_for('watchlistDetails'))


@app.route('/watchlistDetails', methods=['GET', 'POST'])
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
        if request.method == 'POST':
            post_id = request.form.get('postStock')
            select_stmt = "SELECT * FROM CONTAIN WHERE Watchlist_ID = %s AND Stock_ID=%s "
            cur.execute(select_stmt, (newWatchlist, post_id))
            msg = cur.fetchall()
            if not msg:
                cur.execute("INSERT INTO CONTAIN(Stock_ID, Watchlist_ID) VALUES(%s, %s)",
                            (post_id, newWatchlist))
                mysql.connection.commit()

        cur.execute("SELECT * FROM CONTAIN WHERE Watchlist_ID = %s", ([newWatchlist]))
        allListDetails = cur.fetchall()

    else: allListDetails = resultValue

    # add listDetails to render then make an if statment to check if it exists  if not "contact admin to make watchlist"
    return render_template('watchlist.html', username=session['username'], allListDetails=allListDetails, resultValue=resultValue)


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
