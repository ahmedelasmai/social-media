import sqlite3

class Db:

    def __init__(self):            #debug     
        self.username = '@user2'   #
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
            found = False
            for user_follow in user_follows:
                if follower[0] == user_follow[0]:
                    found = True
                    break
            if found:
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
        
        posts, hashtags = self.posts(self.username)

        return user_info[:3], followers[0][0], follows[0][0],posts, hashtags
    
    def get_followers(self): 
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT follows.stalker, User.Name, User.bio  
                           FROM follows
                           LEFT JOIN User ON follows.stalker = User.Username
                           WHERE target=?""", (self.username,))
            follower = cursor.fetchall()   
            
        mutual = self.user_already_following(follower)

        return follower, mutual

    def get_following(self):
        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT follows.target, User.Name, User.bio  
                           FROM follows
                           LEFT JOIN User ON follows.target = User.Username
                           WHERE stalker=?""", (self.username,))
            following = cursor.fetchall()   
            
        mutual = self.user_already_following(following)

        return following, mutual
    
    def posts(self,user=None):

        with sqlite3.connect('social media.db') as conn:
            cursor = conn.cursor()
            base_query = """
            SELECT 
                Post.PostID,
                Post.Username, 
                User.Name, 
                Post.Content, 
                Post.Image, 
                Post.Timestamp,
                COUNT(Likes.LikeID) AS LikeCount,
                GROUP_CONCAT(Hashtag.Hashtag, ' ') AS Hashtags,
                COUNT(Comment.CommentID) AS CommentCount
            FROM 
                Post
            LEFT JOIN 
                Likes ON Post.PostID = Likes.PostID
            LEFT JOIN 
                Hashtag ON Post.PostID = Hashtag.PostID
            LEFT JOIN 
                User ON Post.Username = User.Username
            LEFT JOIN
                Comment ON Post.PostID = Comment.PostID
            """
            #if posts is not searching for specific user it will search all posts
            if user:
                
                query = f"{base_query} WHERE Post.Username = ? GROUP BY Post.PostID"
                cursor.execute(query, (user,))
            else:
                
                query = f"{base_query} GROUP BY Post.PostID"
                cursor.execute(query)
            post_info = cursor.fetchall()

            #gets hashtags array
            cursor = conn.cursor()
            cursor.execute("SELECT Hashtag, Timestamp FROM Hashtag LIMIT 6")
            hashtags = cursor.fetchall()                

        #formats timestamp
        for i in range(len(post_info)):
            post = list(post_info[i])
            del post_info[i]
            formated_date = post[5][:10]
            post[5] = formated_date
            post_info.insert(i,post) 
            #formats hashtags in posts
            if post[7] == None:
                post[7] = ''

        #formats time stamp in hashtags list
        for i in range(6):
            hashtag = list(hashtags[i])
            del hashtags[i]
            formated_date = hashtag[1][:10]
            hashtag[1] = formated_date
            hashtags.insert(i,hashtag)

        return post_info, hashtags 


     #test this
    def get_comments(self, postId): 
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
# post = db.get_hashtags()
# print('fo',post)


# #[1, '@user1', 'User One', 'First post content by @user1', 1, '2024-06-0', 2, '#food #travel', 2]