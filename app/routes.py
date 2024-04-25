from flask import render_template, flash, redirect, url_for, request
from app import app
from app.reels import links
profiles = 'james'   #  FOR TESTING

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    print(profiles)
    if request.method == 'POST':
        search = request.form['search']
        
        if profiles == search:
            return redirect(url_for('profile')) 
    
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', profiles=profiles)

@app.route('/reels')
def reels():
    return render_template('reels.html',links=links)






 
















