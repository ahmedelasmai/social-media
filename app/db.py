import sqlite3

class Db:

    def __init__(self):            #debug     
        self.username = '@user1'   #
        self.user = '@user1' 
        
    #                                     DEBUG
    def loggedin(self):
        self.user = '@user1' 
    
    def user_already_following(self,follows_list):
        mutual = []
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT target FROM follows WHERE stalker=?", (self.user,))
            user_follows = cursor.fetchall()
    
        for follower in follows_list:
            if follower in user_follows:
                mutual.append(follower)
        return mutual

    def follow(self, target_user):
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO follows (stalker,target) VALUES (?,?)", (self.user, target_user))
            conn.commit()

    def unfollow(self, target_user):
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM follows WHERE stalker=? AND target=?",(self.user,target_user))
            conn.commit()

    def load_profile(self):
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Username, Name, Bio FROM User WHERE Username=?", (self.username,))
            user_info = cursor.fetchone()  #tuple
            cursor.execute("SELECT COUNT(stalker) FROM Follows WHERE target=?", (self.username,))
            followers = cursor.fetchall()
            cursor.execute("SELECT COUNT(target) FROM Follows WHERE stalker=?", (self.username,))
            follows = cursor.fetchall()
            cursor.execute("SELECT PostID, Content, Image, Timestamp FROM Post WHERE Username=? ORDER BY Timestamp ASC",
                            (self.username,))
            posts = cursor.fetchall() #tupil
            post_count = len(posts)
                                                                                                                                
            #removes seconds from timestamp
            for i in range(len(posts)):
                post = list(posts[i])
                del posts[i]
                formated_date = post[3][:9]
                post[3] = formated_date
                posts.insert(i,post)   

        return user_info[:3], followers[0][0], follows[0][0], posts, post_count
    
    def get_followers(self): 
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stalker FROM follows WHERE target=?", (self.username,))
            followers = cursor.fetchall()
    
        mutual = self.user_already_following(followers) 
        
        return followers, mutual

    def get_following(self):
        mutual = []
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT target FROM follows WHERE stalker=?", (self.username,))
            following = cursor.fetchall()   

        mutual = self.user_already_following(following)

        return following, mutual
    
     #test this
    def post_info(self, postId): 
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Content, Username, Timestamp FROM Comment WHERE PostID=?", (postId,))
            comment_info = cursor.fetchall()
            cursor.execute("SELECT COUNT(LikeID) FROM Likes WHERE PostID=?", (postId,))
            likes = cursor.fetchone()
            cursor.execute("SELECT Hashtag FROM Hashtag WHERE PostID=?", (postId,))
            hashtags = cursor.fetchall()

        return comment_info, likes, hashtags


    def user_exists(self, username):
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT Username FROM User WHERE Username='{username}'")
            user = cursor.fetchone()  

        if user is None:
            return False
        else:
            self.username = user[0]
            return True
        
    def create_user(self):
        pass
        #ADD AN @ INFORT OF USERNAME
        #create default pfp

# db = Db()
# db.user_exists('@user1')
# followers = db.get_followers()
# print(followers)

#[('@user2',), ('@user3',)]

