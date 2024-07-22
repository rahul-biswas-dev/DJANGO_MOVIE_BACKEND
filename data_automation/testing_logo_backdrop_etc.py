import requests

def get_movie_videos(movie_id):
    api_key = "864652493e0d189c6fa554212812c137"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"

    response = requests.get(url)
    data = response.json()

    video_data = []
    for video in data.get("results", []):
        video_info = {
            "iso_639_1": video.get("iso_639_1"),
            "iso_3166_1": video.get("iso_3166_1"),
            "name": video.get("name"),
            "key": video.get("key"),
            "type": video.get("type"),
            "size": video.get("size"),
            "official": video.get("official"),
            "published_at": video.get("published_at")}
        video_data.append(video_info)

    return video_data

# Example usage
movie_videos = get_movie_videos("tt3371366")
for video in movie_videos:
    print(video)
