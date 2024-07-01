from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
import datetime
from database_handling_app.models import Movie

# this fetch hd poster from tmdb
CONFIG_PATTERN = "http://api.themoviedb.org/3/configuration?api_key={key}"
IMG_PATTERN = "http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}"
KEY = os.getenv("TMDB_KEY")


# this fetch data by id from omdb website trailer url from youtube api and saves it
class FetchMovieData(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_keys = [
            os.getenv("API_KEY_FETCH"),
            os.getenv("API_KEY_FETCH2"),
            os.getenv("API_KEY_FETCH3"),
            os.getenv("API_KEY_FETCH4"),
            os.getenv("API_KEY_FETCH5"),
            os.getenv("API_KEY_FETCH6"),
        ]
        self.current_key_index = 0

    # fetch data from omdb
    def fetch_movie_data(self, imdb_id):
        while self.current_key_index < len(self.api_keys):
            api_key = self.api_keys[self.current_key_index]
            url = f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if (
                    data.get("Response", "") == "False"
                    and data.get("Error", "") == "Request limit reached!"
                ):
                    self.current_key_index += 1
                    if self.current_key_index < len(self.api_keys):
                        print(
                            f"API limit was reached. Key was changed to API_KEY_FETCH{self.current_key_index + 1}"
                        )
                    continue  # Try the next key
                else:
                    return data
            elif response.status_code == 400:
                data = response.json()
                if data.get("Error", "") == "Request limit reached!":
                    self.current_key_index += 1
                    if self.current_key_index < len(self.api_keys):
                        print(
                            f"API limit was reached. Key was changed to API_KEY_FETCH{self.current_key_index + 1}"
                        )
                    continue  # Try the next key
                else:
                    print(
                        f"Failed to fetch movie data for IMDb ID: {imdb_id} - Status Code: {response.status_code}"
                    )
                    return None
            elif response.status_code == 401:
                self.current_key_index += 1
                if self.current_key_index < len(self.api_keys):
                    print(
                        f"Unauthorized access. Key was changed to API_KEY_FETCH{self.current_key_index + 1}"
                    )

                else:
                    print(
                        f"Unauthorized access and all API keys exhausted. IMDb ID: {imdb_id}"
                    )
                    return None
                continue  # Try the next key
            else:
                print(
                    f"Unexpected response for IMDb ID: {imdb_id} - Status Code: {response.status_code}"
                )
                return None
        return None

    # fetch trailer url from youtube api
    def search_movie_trailer(self, data):
        movie_title = data.get("Title", "")
        api_key = os.getenv("YOUTUBE_API_KEY")
        base_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": f"{movie_title} trailer",
            "type": "video",
            "maxResults": 1,
            "key": api_key,
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["pageInfo"]["totalResults"] > 0:
                video_id = data["items"][0]["id"]["videoId"]
                video_title = data["items"][0]["snippet"]["title"]
                if "official" in video_title.lower():
                    video_url = video_id
                    print(
                        f"Official trailer found for {movie_title} - Video ID: {video_id}"
                    )
                    return video_url, "Success"
                else:
                    return None, "No official trailer found"
            else:
                return None, "No trailer found"
        else:
            return None, f"Error: {response.status_code}"

    # data related work for database
    def save_movie_data(self, data):

        # Trailer
        trailer_url, trailer_status = self.search_movie_trailer(data)

        # Creating a instance of the FetchHDPoster class
        fetch_hd_poster = FetchHDPoster()

        # Get the poster URL from FetchHDPoster
        poster_urls = fetch_hd_poster.fetch_poster_urls(data.get("imdbID", ""), limit=1)

        # If poster URLs are available, use the first one
        if poster_urls:
            poster_url = poster_urls[0]
        else:
            poster_url = data.get("Poster", "N/A")

        # Convert released date to YYYY-MM-DD format
        released_date_str = data.get("Released", "")
        try:
            release_date = datetime.datetime.strptime(
                released_date_str, "%d %b %Y"
            ).strftime("%Y-%m-%d")
            print(release_date)
        except ValueError:
            release_date = None

        # Handle the IMDb votes, setting to 0 if 'N/A'
        imdb_votes_str = data.get("imdbVotes", "0")
        if imdb_votes_str == "N/A":
            imdb_votes = 0
        else:
            imdb_votes = int(imdb_votes_str.replace(",", ""))

        #  check if there are any ratings
        if not data["Ratings"]:
            rotten_tomatoes_rating = "None"
        else:
            # Extract Rotten Tomatoes rating
            if len(data["Ratings"]) >= 2:
                rotten_tomatoes_rating = data["Ratings"][1]
                if rotten_tomatoes_rating == "N/A":
                    rotten_tomatoes_rating = "None"
                else:
                    rotten_tomatoes_rating = rotten_tomatoes_rating["Value"]
            else:
                rotten_tomatoes_rating = "None"

        # Convert IMDb rating to float or set to None if 'N/A'
        imdb_rating_str = data.get("imdbRating", "")
        if imdb_rating_str == "N/A":
            imdb_rating = "None"
        else:
            try:
                imdb_rating = float(imdb_rating_str)
            except ValueError:
                imdb_rating = "None"

        # Save all data in the database
        try:
            movie = Movie.objects.create(
                title=data.get("Title", ""),
                year=data.get("Year", ""),
                released_date=release_date,
                rated=data.get("Rated", ""),
                imdb_rating=imdb_rating,
                genres=data.get("Genre", ""),
                plot=data.get("Plot", ""),
                director=data.get("Director", ""),
                writer=data.get("Writer", ""),
                awards=data.get("Awards", ""),
                language=data.get("Language", ""),
                poster_url=poster_url,
                website=data.get("Website", ""),
                imdb_id=data.get("imdbID", ""),
                imdb_votes=imdb_votes,
                type=data.get("Type", ""),
                country=data.get("Country", ""),
                actors=data.get("Actors", ""),
                boxoffice=data.get("BoxOffice", ""),
                rotten_tomatoes_rating=rotten_tomatoes_rating,
                runtime=data.get("Runtime", ""),
                trailer_url=trailer_url if trailer_status == "Success" else None,
            )
            return movie
        except (ValueError, IntegrityError) as e:
            print(f"Error saving movie data: {e}")
            return None

    # function to save the data to database
    def get(self, request, imdb_id):
        data = self.fetch_movie_data(imdb_id)
        if data and data.get("Response", "") == "True":
            self.save_movie_data(data)
            return JsonResponse(
                {"message": f"Movie {imdb_id} saved successfully"}, status=200
            )
        else:
            return JsonResponse({"message": "Failed to fetch data"}, status=400)


# this fetch data by title from omdb website
class SearchMovies(APIView):
    def search_movies(self, title):
        api_key = os.getenv("API_KEY_SEARCH")
        url = f"http://www.omdbapi.com/?apikey={api_key}&s={title}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get(self, request, title):
        data = self.search_movies(title)
        if data and data.get("Response", "") == "True":
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data, status=Response.status_code)


class FetchHDPoster(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.api_key = KEY
        self.config_url = CONFIG_PATTERN.format(key=self.api_key)
        self.base_url = None
        self.max_size = None
        self._configure()  # Fetch the configuration during initialization

    def _get_json(self, url):
        """Fetch JSON data from the given URL."""
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()

    def _configure(self):
        """Fetch and set up configuration from TMDb API."""
        config = self._get_json(self.config_url)
        self.base_url = config["images"]["base_url"]
        sizes = config["images"]["poster_sizes"]

        # Determine the maximum size available
        self.max_size = max(sizes, key=self.size_str_to_int)

    @staticmethod
    def size_str_to_int(size_str):
        """Convert size strings like 'w500' to an integer value, treating 'original' as infinite."""
        return float("inf") if size_str == "original" else int(size_str[1:])

    def fetch_poster_urls(self, imdb_id, limit=1):
        """Return image URLs of posters for a given IMDb ID, limited to the specified number."""
        img_url = IMG_PATTERN.format(imdbid=imdb_id, key=self.api_key)
        posters = self._get_json(img_url)["posters"]
        poster_urls = [
            f"{self.base_url}{self.max_size}{poster['file_path']}" for poster in posters
        ]
        return poster_urls[:limit]

    def get(self, request, imdb_id, *args, **kwargs):
        """Handle GET requests with imdb_id from URL path."""
        if not imdb_id:
            return Response(
                {"error": "IMDb ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            poster_urls = self.fetch_poster_urls(imdb_id, limit=1)
            return Response({"posters": poster_urls}, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
