from flask import render_template, flash, redirect, url_for, request
from app import app
from app.reels import Reels

profiles = 'james'   #  FOR TESTIN
video_index = 0

reel = Reels()

@app.route('/')      
@app.route('/index', methods = ['GET', 'POST'])
def index():
    global search
    if request.method == 'POST':
        search = request.form['search']
        if search[0] == '@':
            search = search[1:]
        if profiles == search:
            return redirect(url_for('profile')) 
        
        return redirect(url_for('reels'))    
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', profiles=profiles)

@app.route('/reels', methods = ['GET', 'POST'])
def reels():
    links = reel.get_video(search)
    global video_index

    if request.method == 'POST':    
        if 'next' in request.form and video_index < len(links):
            video_index += 1
            link = links[video_index]
            return render_template('reels.html', reel=link)
        
        if 'back' in request.form and video_index > 1:
            video_index -= 1
            link = links[video_index]
            return render_template('reels.html', reel=link)
    link = links[0]
    return render_template('reels.html', reel=link)






 
















