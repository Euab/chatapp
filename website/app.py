from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

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


if __name__ == '__main__':
  socketio.run( app, debug = True )
