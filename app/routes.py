from flask import render_template, redirect, url_for, request, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_login import login_user, logout_user, login_required, current_user
from app import app, socketio
from app.videos import video
from app.db import db
from app.user import User





# @socketio.on('join')
# def handle_join():
#     can_message_tuple = db.can_message()
    
#     for room_name in can_message_tuple:
#         join_room
    

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.auth(username, password)
        if user:
            login_user(user,remember=True)
            db.user_var_setup(current_user.get_id()) 
            return redirect(url_for("index"))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')      
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    a = current_user.get_id()
    if request.method == 'POST':
        search = request.form['search']
        if search[0] == '#':
            does_hashtag_exist = db.hashtag_exists(search)

            if does_hashtag_exist is False:
                return redirect(url_for('index')) 
            else:
                feed, hashtags = db.posts(search_hashtag=search)
                return render_template('index.html',feed=feed,hashtags=hashtags)
                  
                        
        if search[0] == '@':
            profiles = db.user_exists(search)
            if profiles:                          
                return redirect(url_for('profile')) 
            else:
                return redirect(url_for('index'))
            
        video.search(search)
        return redirect(url_for('videos')) 

    feed, hashtags = db.posts()                    
    return render_template('index.html',feed=feed,hashtags=hashtags)

@app.route('/likes', methods=['POST'])
@login_required
def likes():
    if request.method == 'POST':
        post_id = request.json['post_id']
    db.like(post_id)
    return ''


@app.route('/message', methods = ['GET', 'POST'])
@login_required
def message():
    return render_template('message.html')

@app.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        tweet = request.form.get('tweet')
        img_file = request.files.get('file')
        successful = db.upload(tweet=tweet, image_file=img_file)

        if successful:
            return redirect(url_for('profile'))
    return render_template('post.html')

@app.route('/profile')
@login_required
def profile():
    user_info,followers, following, feed,hashtags = db.load_profile()  
    username, name , bio = user_info[:3]
    
    return render_template('profile.html',username=username,name=name
                           ,bio=bio, followers=followers,following=following,feed=feed,hashtags=hashtags)

@app.route('/followers', methods = ['GET', 'POST'])
@login_required
def followers():
    #when press follow button
    if request.method == 'POST':
        if 'follow' in request.form:
            target_user = request.form['follow']
            db.follow(target_user)

        elif 'unfollow' in request.form:
            target_user = request.form['unfollow']
            db.unfollow(target_user)
        
     
    #display follower list
    followers_list, mutual= db.get_followers()
    return render_template('followers.html',followers_list=followers_list, mutual=mutual)

@app.route('/following', methods = ['GET', 'POST'])
@login_required
def following():
    #when press follow button
    if request.method == 'POST':
        if 'follow' in request.form:
            target_user = request.form['follow']
            db.follow(target_user)

        elif 'unfollow' in request.form:
            target_user = request.form['unfollow']
            db.unfollow(target_user)

    #display following list
    following_list, mutual = db.get_following()
    return render_template('following.html',following_list=following_list,mutual=mutual)


@app.route('/video', methods = ['GET', 'POST'])
@login_required
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






 
















