import requests
import os

def get_tmdb_trailer_url(movie_id):
    api_key = os.getenv("TMDB_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"

    response = requests.get(url)
    data = response.json()

    for video in data.get('results', []):
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f"https://www.youtube.com/watch?v={video['key']}"

    return None

# Test the function
movie_id = "tt0087332"  # Example: Fight Club
trailer_url = get_tmdb_trailer_url(movie_id)
print(f"Trailer URL: {trailer_url}")
