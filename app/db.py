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
        
        posts = self.posts(self.username)

        return user_info[:3], followers[0][0], follows[0][0]
    
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
    
    def posts(self,user=None):

        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            base_query = """
            SELECT 
                post.PostId,
                Post.Username, 
                Post.Content, 
                Post.Image, 
                Post.Timestamp,
                COUNT(Likes.LikeID) AS LikeCount,
                GROUP_CONCAT(Hashtag.Hashtag, ', ') AS Hashtags
            FROM 
                Post
            LEFT JOIN 
                Likes ON Post.PostID = Likes.PostID
            LEFT JOIN
                Hashtag ON Post.PostID = Hashtag.PostID
            GROUP BY 
                Post.PostID;
            """
            #if posts is not searching for specific user it will search all posts
            if user:
                query = f"{base_query} WHERE {user} GROUP BY Post.PostID;"
            else:
                query = f"{base_query} GROUP BY Post.PostID;"

            cursor.execute(query)
            post_info = cursor.fetchall()
        

                                                                                                                   
        #formats timestamp and hashtags
        for i in range(len(post_info)):
            post = list(post_info[i])
            del post_info[i]
            formated_date = post[4][:9]
            post[4] = formated_date
            post_info.insert(i,post) 
            if post[6]:
                post[6] = post[6].replace(" ", "").replace(",", "")

        return post_info
        
     #test this
    def comments(self, postId):  #DEAL WITH ITS NAME --------------------------------
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Content, Username, Timestamp FROM Comment WHERE PostID=?", (postId,))
            comment_info = cursor.fetchall()

        return comment_info


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
# post = db.posts()
# print(post)
# #[1, '@user1', 'First post content', 1, '2024-05-0', 2, '#food#travel']
