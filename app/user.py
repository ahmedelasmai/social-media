from flask_login import UserMixin
from app import login_manager
import sqlite3

class User(UserMixin):
    
    def __init__(self, id):
        self.id = id
    

    @staticmethod
    def get(id):
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Username FROM User WHERE username=?",(id,))
            user_row = cursor.fetchone()

        if user_row:
            return User(id = user_row[0])
        return None

    @staticmethod
    def auth(id, password):
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM User WHERE username=? AND password=?",(id,password))
            user_row = cursor.fetchone()
        
        if user_row:
            return User(id=user_row[0])
        None

@login_manager.user_loader
def load_user(username):
    return User.get(username)