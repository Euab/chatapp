from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
import os
import redis

app = Flask(__name__)

db = redis.Redis.from_url("redis://localhost", decode_responses=True)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.debug = True
socketio = SocketIO(app)

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
	#return render_template('login.html')
	return "Login page ¯\_(ツ)_/¯"


def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'emit event' )
def handler( json ):
  print( 'recived emit event: ' + str( json ) )
  socketio.emit( 'resp', json, callback=messageRecived )

# Handling HTTP errors
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/#', methods=['POST', 'GET'])
def email_submit():
  email = request.form.get('email_submit')
  db.append('user_email_list', email)
  emaillist = db.smembers('user_email_list')
  with open('./test.txt', 'w') as test:
    print(emaillist, file=test)
  

if __name__ == '__main__':
  socketio.run( app, debug = True )
  db.set('user_email_list', )
