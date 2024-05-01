# from flask import render_template, flash, redirect, url_for, request
# from app import app
# from app.reels import Reels

# profiles = 'james'   #  FOR TESTIN
# video_index = 13
# page = 1

# @app.route('/')      
# @app.route('/index', methods = ['GET', 'POST'])
# def index():
#     global search
#     if request.method == 'POST':
#         search = request.form['search']
#         if search[0] == '@':
#             search = search[1:]
#         if profiles == search:
#             return redirect(url_for('profile')) 
        
#         return redirect(url_for('reels'))    
#     return render_template('index.html')

# @app.route('/profile')
# def profile():
#     return render_template('profile.html', profiles=profiles)

# @app.route('/reels', methods = ['GET', 'POST'])
# def reels():
#     global video_index, page
#     reel = Reels()
#     search = 'melon'    #DEBUG

#     #go to next page at end of list
#     if video_index >= 14:  
#         video_index = -1
#         page += 1

#     #go to preivous page if start of list
#     elif video_index < 0:
#         video_index = 15
#         page -= 1

#         if page < 1:         #if press back when page is first loaded
#             video_index = 0
#             page = 1
            
#     links = reel.get_video(search, page)

#     if request.method == 'POST':            
#         if 'next' in request.form:
#             video_index += 1
#             print(video_index)                  #DEBUG
#             link = links[video_index]
#             return render_template('reels.html', link=link,video_index=video_index,page=page)
        
#         elif 'back' in request.form:
#             video_index -= 1
#             print(video_index)                  #DEBUG
#             link = links[video_index]
#             #display nothing if user is at the beginning of list and wants to go back
#             if video_index < 0:  
#                 return render_template('reels.html',video_index=video_index,page=page)
#             return render_template('reels.html', link=link,video_index=video_index,page=page)
        
#     return render_template('reels.html',video_index=video_index,page=page)






 
















