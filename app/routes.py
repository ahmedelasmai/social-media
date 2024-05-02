from flask import render_template, redirect, url_for, request
from app import app
from app.videos import Videos

profiles = 'james'   #  FOR TESTIN
search = 'sea'       #
video = Videos()
video.search(search)  #

@app.route('/')      
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form['search']
        video.search(search)
        if search[0] == '@':
            search = search[1:]
            if profiles == search:                          
                return redirect(url_for('profile')) 
         
        return redirect(url_for('videos'))    
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', profiles=profiles)

@app.route('/video', methods = ['GET', 'POST'])
def videos():

    if request.method == 'POST':           
        if 'next' in request.form:
            link, video_index, page = video.search('next')
            return render_template('videos.html', link=link,video_index=video_index,page=page)
        
        elif 'back' in request.form:
            link, video_index, page = video.search('back')
            return render_template('videos.html', link=link,video_index=video_index,page=page)
        
    else:
        link, video_index, page = video.search('none')
        return render_template('videos.html',link=link,video_index=video_index,page=page)






 
















