from flask import render_template, flash, redirect, url_for, request
from app import app
from app.reels import Reels

profiles = 'james'   #  FOR TESTIN
search = 'sea'
reel = Reels()
reel.search(search)

@app.route('/')      
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form['search']
        reel.search(search)
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

    if request.method == 'POST':  
        print('requestform', request.form)          
        if 'next' in request.form:
            link, video_index, page = reel.change('next')
            return render_template('reels.html', link=link,video_index=video_index,page=page)
        
        elif 'back' in request.form:
            link, video_index, page = reel.change('back')
            return render_template('reels.html', link=link,video_index=video_index,page=page)
        
    else:
        link, video_index, page = reel.change('none')
        return render_template('reels.html',link=link,video_index=video_index,page=page)






 
















