import requests

def search_movie_trailer(movie_title, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{movie_title} trailer",
        "type": "video",
        "maxResults": 2,
        "key": api_key,}

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["pageInfo"]["totalResults"] > 0:
            video_id = data["items"][0]["id"]["videoId"]
            video_title = data["items"][0]["snippet"]["title"]
            if "official" in video_title.lower():
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                return video_url, "Success"
            else:
                return None, "No official trailer found"
        else:
            return None, "No trailer found"
    else:
        return None, f"Error: {response.status_code}"


api_key = ("AIzaSyCY2-y7g1tb7bkhBH-q09eMK8RYUk9BL1A")
print(search_movie_trailer("The Matrix", api_key))
