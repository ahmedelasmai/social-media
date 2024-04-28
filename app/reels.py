import requests  


class Reels:
    
    def get_video(self, search):
        
        links = []

        headers = {
            'Authorization': 'AzTxNqak0lM0K8DYZvTwHOirmCF9vRD4URwMNhizm6kShLiqdEd1ii2F'
        }

        params = {
            "query" : f"{search}"   
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






