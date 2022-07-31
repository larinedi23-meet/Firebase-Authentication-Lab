from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDK2dmKa_A2oXs_TZ3UhiCHreE6uJKVqiE",
  "authDomain": "idkk-730f4.firebaseapp.com",
  "projectId": "idkk-730f4",
  "storageBucket": "idkk-730f4.appspot.com",
  "messagingSenderId": "981788536542",
  "appId": "1:981788536542:web:778dd82b9edf0f233b1c4f",
  "measurementId": "G-3RJTLGM40T",
  "databaseURL":""

}

firebase = pyrebase.initialize_app(config)
auth=firebase.auth()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('add_tweet'))
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('add_tweet'))
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)