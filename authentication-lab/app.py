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
  "databaseURL":"https://idkk-730f4-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

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
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        user={"full_name":full_name,"username":username,"bio":bio}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            print("yo")
            # return redirect(url_for('home'))
            db.child("Users").child(login_session["user"]["localId"]).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error=""
    if request.method == 'POST':
        text = request.form['text']
        title = request.form['title']
        print (login_session)
        tweet={"text":text , "title":title,"username":(db.child("Users").child(login_session["user"]["localId"]).get().val())["username"]}
        try:
            db.child("tweets").push(tweet)

            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("add_tweet.html")
    else:
        try:
            tweets = db.child('tweets').get().val()
            


#@app.route('/all_tweets', methods=['GET', 'POST'])
   # def all_tweets():

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)