import os
import redis
import pymongo
import hashlib
import base64
import binascii

from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, session, \
flash, abort

app = Flask(__name__)
db = redis.Redis.from_url("redis://localhost", decode_responses=True)

app.config['SECRET_KEY'] = os.urandom(24)
client = MongoClient('mongodb://127.0.0.1:27017/')
mongo = client['accounts_db']
collection = mongo['accounts']
app.debug = True

# CSRF security
@app.before_request
def csrf_protect():
  if request.method == "POST":
    token = session.pop('_csrf_token', None)
    if not token or token != request.form.get('_csrf_token'):
      abort(403)

def generate_csrf_token():
  if '_csrf_token' not in session:
    session['_csrf_token'] = str(binascii.hexlify(os.urandom(15)))
  return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/signup')
def signup():
  return render_template('register.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/chat')
def chat():
  return render_template('chat.html')


# Login logic
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  if request.method == 'POST':
    # Execute register backend
    if request.form['password'] != request.form['confirm-password']:
      flash("Passwords do not match!", "danger")
      return redirect(url_for('register'))
    elif bool(collection.find_one({'username': request.form['username']})):
      flash('Account taken!', 'danger')
      return redirect(url_for('register'))
    else:
      username = request.form['username']
      password = request.form['password']
      salt = str(base64.b64encode(os.urandom(16)))
      password_hash = hashlib.sha3_224(
        str(password + salt).encode('utf-8')
      ).hexdigest()
      to_db = {
        'Username': username,
        'Password': password_hash,
        'Salt': salt
      }
      collection.insert_one(to_db)
      flash("Account created!", "success")
      return redirect(url_for('index'))

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return render_template("login.html")
  elif request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    # If the username exists, log them in.
    if bool(collection.find_one({"Username": username})):
      salt = collection.find_one({"Username": username})['Salt']
      password_hash = hashlib.sha3_224(str(password + salt).encode('utf-8')).hexdigest()
      if password_hash == collection.find_one({"Username": username})['Password']:
        # The password hash matches. Log in
        # This string is just a placeholder until the dashboard is made.
        session['username'] = username
        return str("You have been logged in as username " + username)
      else:
        # Username does not exist
        return str("Can't find account " + username)

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect(url_for('index'))

# Handling HTTP errors
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/#', methods=['POST', 'GET'])
def email_submit():
  email = request.form.get('email_submit')
  db.append('user_email_list', email)
  emaillist = db.get('user_email_list')
  with open('./test.txt', 'w') as test:
    print(emaillist, file=test)
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run()
  db.set('user_email_list', '')
