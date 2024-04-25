import requests  

headers = {
    'Authorization': 'AzTxNqak0lM0K8DYZvTwHOirmCF9vRD4URwMNhizm6kShLiqdEd1ii2F'
}

response = requests.get('https://api.pexels.com/videos/popular', headers=headers)  

if response.status_code == 200:
    data = response.json()
    videos = data['videos']
    
    
    links = []
    
    for video in videos:
        video_files = video['video_files']
        for file in video_files:
            link = file['link']
            links.append(link)  
    
    
else:
    print('error', response.status_code)
