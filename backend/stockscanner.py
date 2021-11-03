from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)



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
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form = form)

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


if __name__ == '__main__':
    app.run(debug=True)