import requests
import json

def fetch_tmdb_data(movie_id):
    api_key = "864652493e0d189c6fa554212812c137"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage
movie_id = "tt1375666"
movie_data = fetch_tmdb_data(movie_id)


backdrop_path = movie_data["backdrop_path"]

homepage = movie_data["homepage"]

origin_country = movie_data["origin_country"]

original_language = movie_data["original_language"]

production_companies = movie_data["production_companies"]

production_countries = movie_data["production_countries"]

spoke_languages = movie_data["spoken_languages"]

status = movie_data["status"]

