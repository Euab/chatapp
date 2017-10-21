from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.debug = True
socketio = SocketIO(app)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    socketio.run(app)
