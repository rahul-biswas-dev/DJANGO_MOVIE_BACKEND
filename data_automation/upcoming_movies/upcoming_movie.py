# import requests

# # Replace 'YOUR_API_KEY' with your actual TMDb API key
# api_key = "864652493e0d189c6fa554212812c137"

# # Base URL for the TMDb API
# base_url = "https://api.themoviedb.org/3"

# # Endpoint for upcoming movies
# endpoint = f"{base_url}/movie/upcoming"

# # Parameters including the API key and optional settings
# params = {
#     "api_key": api_key,
#     "language": "en-US",
#     "page": 1,  # Page number for pagination
# }

# # Make the request to TMDb API
# response = requests.get(endpoint, params=params)

# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#     print(data)
#     print("Upcoming Movies:\n")
#     for movie in data["results"]:
#         title = movie["title"]
#         release_date = movie["release_date"]
#         overview = movie["overview"]
#         print(f"Title: {title}")
#         print(f"Release Date: {release_date}")
#         print(f"Overview: {overview}\n")
# else:
#     print(f"Failed to fetch data: {response.status_code}")

import requests

def get_upcoming_movies(release_date):
    base_url = f"https://api.themoviedb.org/3/discover/movie?"
    api_key = "864652493e0d189c6fa554212812c137"

    params = {
        "api_key": "21b13c128bd411a0c38bb67b5702fb00",
        "language": "en-US",
        "page": 1,
        "include_adult": True,
        "include_video": False,
        "sort_by": "popularity.desc",
        "primary_release_date.gte": release_date,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Upcoming Movies:\n")
        for movie in data["results"]:
            title = movie["title"]
            release_date = movie["release_date"]
            overview = movie["overview"]
            print(f"Title: {title}")
            print(f"Release Date: {release_date}")
            print(f"Overview: {overview}\n")
    else:
        print(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    release_date = input("Enter the release date (YYYY-MM-DD): ")

    get_upcoming_movies(release_date)
