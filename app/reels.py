import requests  


class Reels:

    def __init__(self):
        self.index = 0
        self.page = 1
    
    def search(self, search):
        self.search = search
        print(search)
    def change(self, move='none'):
        links = self.get_video()
        if move == 'next':
            #go next page
            if self.index >= 14:
                self.index = 0
                self.page += 1
                links = self.get_video()
                print('next page')
                return links[self.index], self.index, self.page
            #next video
            else:
                self.index += 1
                print('next vid:', self.index)
                return links[self.index], self.index, self.page

        elif move == 'back':
            #previous page
            if self.index == 0 and self.page > 1:
                self.index = 14
                self.page -= 1
                links = self.get_video()
                print('back')
                return links[self.index], self.index, self.page
            #previous video
            elif self.index > 0:
                self.index -= 1
                print('prev vid', self.index)
                return links[self.index], self.index, self.page
            
            else:
                print('back when 0')
                return links[self.index], self.index, self.page

        #when at first video
        else:
            print('first vid',self.index)
            return links[self.index], self.index, self.page
            


    def get_video(self):

        links = []

        headers = {
            'Authorization': 'AzTxNqak0lM0K8DYZvTwHOirmCF9vRD4URwMNhizm6kShLiqdEd1ii2F'
        }

        params = {
            "query" : self.search,
            "page"  : self.page
        }

        response = requests.get('https://api.pexels.com/videos/search', params=params, headers=headers)  

        if response.status_code == 200:
            data = response.json()
            videos = data['videos']
            
            for link in videos:
                links.append(link['video_files'][0]['link'])
                
        else:
            print('error', response.status_code)    
            
        return links