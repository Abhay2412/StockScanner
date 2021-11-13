from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
import yaml

from forms import RegistrationForm, LoginForm

app = Flask(__name__)  # Instantiating it here

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

posts = [  # from the database suppose it
    {
        "ID": "MSFT",
        "StockPrice": "333.13",
        "Sector": "Technology",
        "Exchange": "NASDAQ",
    },

    {
        "ID": "AAPL",
        "StockPrice": "150.02",
        "Sector": "Technology",
        "Exchange": "NASDAQ",
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
            cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                        (username, password, permissions))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showusers'))
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'abhaykhosla0@gmail.com' and form.password == 'thisisatestforcpsc471':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check your credentials again.', 'danger')
    return render_template('login.html', title='Login', form=form)


# ----------------------------------------Start of the API Calls------------------------------------------------------------
# -----------USER API Calls----------------------------
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


@app.route("/newuser", methods=['POST'])
def newuser():
    cur = mysql.connection.cursor()
    json = request.json

    new_Username = json['Username']
    new_Password = json['Password']
    new_Permissions = json['Permissions']

    cur.execute("INSERT INTO USER(Username, Password, Permissions) VALUES(%s, %s, %s)",
                (new_Username, new_Password, new_Permissions))
    mysql.connection.commit()
    cur.close()

    return jsonify("New User Created")

# -----------Watchlist API Calls----------------------------
@app.route("/watchlist/<string:list_number>", methods=['PUT', 'GET', 'DELETE'])
def watchlist(list_number):

    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_ID = json['ID']
        new_Ranking = json['Ranking']

        cur.execute("UPDATE WATCHLIST SET ID=%s, Ranking=%s WHERE list_number=%s",
                    (new_ID, new_Ranking, list_number))

        mysql.connection.commit()
        cur.close()

        return jsonify("Watchlist updated successfully")

    if request.method == 'GET':
            cur = mysql.connection.cursor()
            select_stmt = "SELECT * FROM WATCHLIST WHERE list_number = %s"
            cur.execute(select_stmt, (list_number,))
            listDetails = cur.fetchall()
            return jsonify({'list_number': listDetails})

    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM WATCHLIST WHERE list_number = %s", ([list_number]))

        mysql.connection.commit()
        cur.close()

        return jsonify("Watchlist deleted successfully")

@app.route("/newWatchlist", methods=['POST'])
def newList():
    cur = mysql.connection.cursor()
    json = request.json

    new_ID = json['ID']
    new_List_Number = json['List_Number']
    new_Ranking = json['Ranking']

    cur.execute("INSERT INTO WATCHLIST(ID, List_Number, Ranking) VALUES(%s, %s, %s)",
                (new_ID, new_List_Number, new_Ranking))
    mysql.connection.commit()
    cur.close()

    return jsonify("New Watchlist Created")

# -----------Offering API Calls----------------------------
@app.route("/offering", methods=['POST', 'GET'])
def offering():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_ID = json['ID']
        new_Company_ID = json['Company_ID']
        new_Prediction_ID = json['Prediction_ID']
        new_Predict_Stock_Price = json['Predict_Stock_Price']
        new_Strong_Buy = json['Strong_Buy']
        new_Rating_Buy = json['Rating_Buy']
        new_Rating_Sell = json['Rating_Sell']
        new_Strong_Sell = json['Strong_Sell']
        new_Rating_Hold = json['Rating_Hold']
        new_Stock_Price = json['Stock_Price']
        new_Sector = json['Sector']
        new_Address = json['Address']
        new_Founding_Date = json['Founding_Date']
        new_Business_Name = json['Business_Name']

        new_Offering_ID = json['Offering_ID']
        new_Quantity_of_stock = json['Quantity_of_stock']
        new_Price_offered_at = json['Price_offered_at']
        new_Status_Complete = json['Status_Complete']
        new_Status_Incomplete = json['Status_Incomplete']

        cur.execute("INSERT INTO Prediction(P_ID) VALUES(%s)", ([new_Prediction_ID]))
        cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)",
                    (new_Company_ID, new_Address, new_Founding_Date, new_Business_Name))
        cur.execute(
            "INSERT INTO STOCK(ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy,
             new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector))

        cur.execute(
            "INSERT INTO OFFERING(Offering_ID, ID, Quantity_of_stock, Price_offered_at, Status_Complete, Status_Incomplete) VALUES(%s, %s, %s, %s, %s, %s)",
            (new_Offering_ID, new_ID, new_Quantity_of_stock, new_Price_offered_at, new_Status_Complete,
             new_Status_Incomplete))

        mysql.connection.commit()
        cur.close()

        return jsonify("Offering inserted successfully")

    if request.method == 'GET':
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM OFFERING")

        offering_row = cur.fetchall()
        respone = jsonify({'Offering': offering_row})
        respone.status_code = 200

        cur.close()

        return respone


@app.route("/offering/<string:Offering_ID>", methods=['DELETE'])
def delete_offering(Offering_ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM OFFERING WHERE Offering_ID = %s", ([Offering_ID]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Offering deleted successfully")


@app.route("/offering/<string:Offering_ID>", methods=['GET'])
def get_offering(Offering_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM OFFERING WHERE Offering_ID = %s", ([Offering_ID]))
    specific_offering_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Offering': specific_offering_details})


# -----------Belongs To API Calls--------------------------
@app.route("/belongsto", methods=['POST', 'GET'])
def belongsto():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_ID = json['ID']
        new_Company_ID = json['Company_ID']
        new_Prediction_ID = json['Prediction_ID']
        new_Predict_Stock_Price = json['Predict_Stock_Price']
        new_Strong_Buy = json['Strong_Buy']
        new_Rating_Buy = json['Rating_Buy']
        new_Rating_Sell = json['Rating_Sell']
        new_Strong_Sell = json['Strong_Sell']
        new_Rating_Hold = json['Rating_Hold']
        new_Stock_Price = json['Stock_Price']
        new_Sector = json['Sector']
        new_Address = json['Address']
        new_Founding_Date = json['Founding_Date']
        new_Business_Name = json['Business_Name']

        new_Name = json['Name']
        new_Location = json['Location']
        new_Number_of_Tickers = json['Number_of_Tickers']

        cur.execute("INSERT INTO Prediction(P_ID) VALUES(%s)", ([new_Prediction_ID]))
        cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)",
                    (new_Company_ID, new_Address, new_Founding_Date, new_Business_Name))
        cur.execute(
            "INSERT INTO STOCK(ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy,
             new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector))

        cur.execute("INSERT INTO EXCHANGES(Name, Location, Number_of_Tickers) VALUES(%s, %s, %s)",
                    (new_Name, new_Location, new_Number_of_Tickers))

        cur.execute("INSERT INTO BELONGSTO(ID, Name) VALUES(%s, %s)", (new_ID, new_Name))

        mysql.connection.commit()
        cur.close()

        return jsonify("BelongsTo inserted successfully")

    if request.method == 'GET':
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM BELONGSTO")

        belongsto_row = cur.fetchall()
        respone = jsonify({'Belongs To': belongsto_row})
        respone.status_code = 200

        cur.close()

        return respone


@app.route("/belongsto/<string:ID>", methods=['DELETE'])
def delete_belongsto(ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM BELONGSTO WHERE ID = %s", ([ID]))

    mysql.connection.commit()
    cur.close()

    return jsonify("BelongsTo deleted successfully")


@app.route("/belongsto/<string:ID>", methods=['GET'])
def get_belongsto(ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BELONGSTO WHERE ID = %s", ([ID]))
    specific_belongsto_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Belongs To': specific_belongsto_details})


# -----------Exchanges API Calls--------------------------
@app.route("/exchange", methods=['POST', 'GET', 'PUT'])
def exchange():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_Name = json['Name']
        new_Location = json['Location']
        new_Number_of_Tickers = json['Number_of_Tickers']

        cur.execute("INSERT INTO EXCHANGES(Name, Location, Number_of_Tickers) VALUES(%s, %s, %s)",
                    (new_Name, new_Location, new_Number_of_Tickers))

        mysql.connection.commit()
        cur.close()

        return jsonify("Exchange inserted successfully")

    if request.method == 'GET':
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM EXCHANGES")

        exchange_row = cur.fetchall()
        respone = jsonify({'Exchange': exchange_row})
        respone.status_code = 200

        cur.close()

        return respone

    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_Name = json['Name']
        new_Location = json['Location']
        new_Number_of_Tickers = json['Number_of_Tickers']

        cur.execute("UPDATE EXCHANGES SET Name=%s, Location=%s, Number_of_Tickers=%s WHERE Name=%s",
                    (new_Name, new_Location, new_Number_of_Tickers, new_Name))

        mysql.connection.commit()
        cur.close()

        return jsonify("Exchange updated successfully")


@app.route("/exchange/<string:Name>", methods=['DELETE'])
def delete_exchange(Name):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM EXCHANGES WHERE Name = %s", ([Name]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Exchange deleted successfully")


@app.route("/exchange/<string:Name>", methods=['GET'])
def get_exchange(Name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EXCHANGES WHERE Name = %s", ([Name]))
    specific_exchange_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Exchange': specific_exchange_details})


# -----------Analyst API Calls--------------------------
@app.route("/analyst", methods=['POST', 'GET', 'PUT'])
def analyst():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_ID = json['ID']
        new_Company_ID = json['Company_ID']
        new_Prediction_ID = json['Prediction_ID']
        new_Predict_Stock_Price = json['Predict_Stock_Price']
        new_Strong_Buy = json['Strong_Buy']
        new_Rating_Buy = json['Rating_Buy']
        new_Rating_Sell = json['Rating_Sell']
        new_Strong_Sell = json['Strong_Sell']
        new_Rating_Hold = json['Rating_Hold']
        new_Stock_Price = json['Stock_Price']
        new_Sector = json['Sector']
        new_Address = json['Address']
        new_Founding_Date = json['Founding_Date']
        new_Business_Name = json['Business_Name']
        new_Analyst_ID_Number = json['Analyst_ID_Number']
        new_Name = json['Name']
        new_Company = json['Company']

        cur.execute("INSERT INTO Prediction(P_ID) VALUES(%s)", ([new_Prediction_ID]))
        cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)",
                    (new_Company_ID, new_Address, new_Founding_Date, new_Business_Name))
        cur.execute(
            "INSERT INTO STOCK(ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy,
             new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector))

        cur.execute("INSERT INTO ANALYST(Analyst_ID_Number, ID, Name, Company) VALUES(%s, %s, %s, %s)",
                    (new_Analyst_ID_Number, new_ID, new_Name, new_Company))

        mysql.connection.commit()
        cur.close()

        return jsonify("Analyst inserted successfully")

    if request.method == 'GET':
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM ANALYST")

        analyst_row = cur.fetchall()
        respone = jsonify({'Analyst': analyst_row})
        respone.status_code = 200

        cur.close()

        return respone

    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_Analyst_ID_Number = json['Analyst_ID_Number']
        new_ID = json['ID']
        new_Name = json['Name']
        new_Company = json['Company']

        cur.execute("UPDATE ANALYST SET Analyst_ID_Number=%s, ID=%s, Name=%s, Company=%s WHERE Analyst_ID_Number=%s",
                    (new_Analyst_ID_Number, new_ID, new_Name, new_Company, new_Analyst_ID_Number))

        mysql.connection.commit()
        cur.close()

        return jsonify("Analyst updated successfully")


@app.route("/analyst/<string:Analyst_ID_Number>", methods=['DELETE'])
def delete_analyst(Analyst_ID_Number):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ANALYST WHERE Analyst_ID_Number = %s", ([Analyst_ID_Number]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Analyst deleted successfully")


@app.route("/analyst/<string:Analyst_ID_Number>", methods=['GET'])
def get_analyst(Analyst_ID_Number):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ANALYST WHERE Analyst_ID_Number = %s", ([Analyst_ID_Number]))
    specific_analyst_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Analyst': specific_analyst_details})


# -----------Business API Calls--------------------------
@app.route("/business", methods=['POST', 'GET', 'PUT'])
def business():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_Business_ID = json['Business_ID']
        new_Address = json['Address']
        new_Founding_Date = json['Founding_Date']
        new_Business_Name = json['Business_Name']

        cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)",
                    (new_Business_ID, new_Address, new_Founding_Date, new_Business_Name))

        mysql.connection.commit()
        cur.close()

        return jsonify("Business inserted successfully")

    if request.method == 'GET':
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM BUSINESS")

        business_row = cur.fetchall()
        respone = jsonify({'Business': business_row})
        respone.status_code = 200

        cur.close()

        return respone

    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_Business_ID = json['Business_ID']
        new_Address = json['Address']
        new_Founding_Date = json['Founding_Date']
        new_Business_Name = json['Business_Name']

        cur.execute(
            "UPDATE BUSINESS SET Business_ID=%s, Address=%s, Founding_Date=%s, Business_Name=%s WHERE Business_ID=%s",
            (new_Business_ID, new_Address, new_Founding_Date, new_Business_Name, new_Business_ID))

        mysql.connection.commit()
        cur.close()

        return jsonify("Business updated successfully")


@app.route("/business/<string:Business_ID>", methods=['DELETE'])
def delete_business(Business_ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM BUSINESS WHERE Business_ID = %s", ([Business_ID]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Business deleted successfully")


@app.route("/business/<string:Business_ID>", methods=['GET'])
def get_business(Business_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([Business_ID]))
    specific_business_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Stock': specific_business_details})


# -----------Stock API Calls--------------------------
@app.route("/stocks", methods=['POST', 'GET', 'PUT'])
def stocks():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_ID = json['ID']
        new_Company_ID = json['Company_ID']
        new_Prediction_ID = json['Prediction_ID']
        new_Predict_Stock_Price = json['Predict_Stock_Price']
        new_Strong_Buy = json['Strong_Buy']
        new_Rating_Buy = json['Rating_Buy']
        new_Rating_Sell = json['Rating_Sell']
        new_Strong_Sell = json['Strong_Sell']
        new_Rating_Hold = json['Rating_Hold']
        new_Stock_Price = json['Stock_Price']
        new_Sector = json['Sector']
        new_Address = json['Address']
        new_Founding_Date = json['Founding_Date']
        new_Business_Name = json['Business_Name']

        cur.execute("INSERT INTO Prediction(P_ID) VALUES(%s)", ([new_Prediction_ID]))
        cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)",
                    (new_Company_ID, new_Address, new_Founding_Date, new_Business_Name))
        cur.execute(
            "INSERT INTO STOCK(ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy,
             new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector))

        mysql.connection.commit()
        cur.close()

        return jsonify("Stock inserted successfully")

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM STOCK")

        stocks_row = cur.fetchall()
        respone = jsonify({'Stock': stocks_row})
        respone.status_code = 200

        cur.close()

        return respone

    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_ID = json['ID']
        new_Company_ID = json['Company_ID']
        new_Prediction_ID = json['Prediction_ID']
        new_Predict_Stock_Price = json['Predict_Stock_Price']
        new_Strong_Buy = json['Strong_Buy']
        new_Rating_Buy = json['Rating_Buy']
        new_Rating_Sell = json['Rating_Sell']
        new_Strong_Sell = json['Strong_Sell']
        new_Rating_Hold = json['Rating_Hold']
        new_Stock_Price = json['Stock_Price']
        new_Sector = json['Sector']

        cur.execute(
            "UPDATE STOCK SET ID=%s, Company_ID=%s, Prediction_ID=%s, Predict_Stock_Price=%s, Strong_Buy=%s, Rating_Buy=%s, Rating_Sell=%s, Strong_Sell=%s, Rating_Hold=%s, Stock_Price=%s, Sector=%s WHERE ID=%s",
            (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy,
             new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector, new_ID))

        mysql.connection.commit()
        cur.close()

        return jsonify("Stock updated successfully")


@app.route("/stocks/<string:ID>", methods=['DELETE'])
def delete_stocks(ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM STOCK WHERE ID = %s", ([ID]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Stock deleted successfully")


@app.route("/stocks/<string:ID>", methods=['GET'])
def get_stock(ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([ID]))
    specific_stock_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Stock': specific_stock_details})


# ----------------------------------------End of the API Calls--------------------------------------------------------------


if __name__ == '__main__':
    app.run(
        debug=True)  # Run it here if the name equals name, also the debug ensures that any update made here will be
    # changed here immediately onto the server