from flask import Flask, render_template, request, redirect, url_for
import os
import redis

app = Flask(__name__)

db = redis.Redis.from_url("redis://localhost", decode_responses=True)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.debug = True

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/login')
def login():
	return render_template('login.html')
  
def messageReceived():
  print( 'message was received!!!' )

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
