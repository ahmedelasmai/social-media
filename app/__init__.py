from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'key'

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


UPLOAD_FOLDER = r'C:\Users\trade\Documents\python2\social media\app\static\img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'ico', 'ppm', 'pgm', 'pbm'}



from app import routes


