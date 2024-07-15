from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
from datetime import datetime
from database_handling_app.models import Movie
from django.utils.dateparse import parse_datetime


# this fetch hd poster from tmdb
CONFIG_PATTERN = "http://api.themoviedb.org/3/configuration?api_key={key}"
IMG_PATTERN = "http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}"
KEY = os.getenv("TMDB_KEY")
KEY2 = os.getenv("TMDB_KEY2")


# fetching data from API and saving to database
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
        if not imdb_id or imdb_id == "undefined":
            print(f"Invalid IMDB ID: {imdb_id}")
            return None

        while self.current_key_index < len(self.api_keys):
            api_key = self.api_keys[self.current_key_index]
            url = f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                if data.get("Response") == "False":
                    if data.get("Error") == "Request limit reached!":
                        self.current_key_index += 1
                        if self.current_key_index < len(self.api_keys):
                            print(
                                f"API limit was reached. Key was changed to API_KEY_FETCH{self.current_key_index + 1}"
                            )
                        continue
                    else:
                        print(f"API returned an error: {data.get('Error')}")
                        return None
                return data

            except requests.exceptions.RequestException as e:
                print(f"Request failed for IMDb ID: {imdb_id}. Error: {str(e)}")
                if (
                    isinstance(e, requests.exceptions.HTTPError)
                    and e.response.status_code == 401
                ):
                    self.current_key_index += 1
                    if self.current_key_index < len(self.api_keys):
                        print(
                            f"Unauthorized access. Key was changed to API_KEY_FETCH{self.current_key_index + 1}"
                        )
                        continue
                    else:
                        print(
                            f"Unauthorized access and all API keys exhausted. IMDb ID: {imdb_id}"
                        )
                return None

            except ValueError as e:
                print(f"JSON decoding failed for IMDb ID: {imdb_id}. Error: {str(e)}")
                return None

        return None

    # fetch data from tmdb
    def fetch_movie_data_tmdb(self, imdb_id):
        if not imdb_id or imdb_id == "undefined":
            print(f"Invalid IMDB ID for TMDB fetch: {imdb_id}")
            return None

        try:
            api_key = os.getenv("TMDB_KEY")
            url = f"https://api.themoviedb.org/3/movie/{imdb_id}?api_key={api_key}"
            response = requests.get(url)
            response.raise_for_status()  # This will raise an HTTPError for bad responses
            data_tmdb = response.json()
            return data_tmdb
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Movie not found in TMDB for IMDB ID: {imdb_id}")
            else:
                print(f"HTTP error occurred while fetching data from TMDB: {e}")
            return None
        except requests.RequestException as e:
            print(f"Error fetching data from TMDB: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing JSON response from TMDB: {e}")
            return None

    # fetch trailer url from tmdb api
    def search_movie_trailer(self, data):
        movie_id = data.get("imdbID", "")
        api_key = os.getenv("TMDB_KEY")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"

        response = requests.get(url)
        data = response.json()

        for video in data.get("results", []):
            if video["type"] == "Trailer" and video["site"] == "YouTube":
                return f"{video['key']}"

    # fetch movie logo from tmdb
    def fetch_movie_logo(self, data):
        imdb_id = data.get("imdbID", "")
        url = IMG_PATTERN.format(imdbid=imdb_id, key=KEY)
        response = requests.get(url)
        logos = [logo for logo in response.json()["logos"] if logo["iso_639_1"] == "en"]
        if logos:
            logo_url = f"{logos[0]['file_path']}"
            return logo_url
        else:
            return None


    # data related work for database
    def save_movie_data(self, data, data_tmdb):

        # movie Logo
        logo_url = self.fetch_movie_logo(data)

        # Trailer
        trailer_url = self.search_movie_trailer(data)

        # Convert released date to YYYY-MM-DD format
        released_date_str = data.get("Released", "")
        try:
            release_date = datetime.strptime(released_date_str, "%d %b %Y").strftime(
                "%Y-%m-%d"
            )
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
                poster_url=data_tmdb.get("poster_path", ""),
                website=data.get("Website", ""),
                imdb_id=data.get("imdbID", ""),
                imdb_votes=imdb_votes,
                type=data.get("Type", ""),
                actors=data.get("Actors", ""),
                boxoffice=data.get("BoxOffice", ""),
                rotten_tomatoes_rating=rotten_tomatoes_rating,
                runtime=data.get("Runtime", ""),
                trailer_url=trailer_url,
                logo_url=logo_url,
                backdrop_url=data_tmdb.get("backdrop_path", ""),
                status=data_tmdb.get("status", ""),
                original_language=data_tmdb.get("original_language", ""),
                homepage=data_tmdb.get("homepage", ""),
            )
            return movie
        except (ValueError, IntegrityError) as e:
            print(f"Error saving movie data: {e}")
            return None

    # function to save the data to database
    def get(self, request, imdb_id):
        data = self.fetch_movie_data(imdb_id)
        data_tmdb = self.fetch_movie_data_tmdb(imdb_id)
        if data and data_tmdb:
            self.save_movie_data(data, data_tmdb)
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


# this fetch data of upcoming movies from TMDB
class FetchUpcomingMovies(APIView):
    def get(self, request, page):
        print(request)
        # Replace 'YOUR_API_KEY' with your actual TMDb API key
        api_key = KEY

        # Base URL for the TMDb API
        base_url = "https://api.themoviedb.org/3"

        # Endpoint for upcoming movies
        endpoint = f"{base_url}/discover/movie?"

        # Parameters including the API key and optional settings
        params = {
            "api_key": api_key,
            "language": "en-US",
            "page": page,
            "include_adult": True,
            # "sort_by": "primary_release_date.asc",  # to short by release date /
            "sort_by": "popularity.desc",  # to sort by popularity /
            # "primary_release_date.gte": "2024-07-11",  # to get movies after this date /
            "primary_release_year": "2024",
        }

        # Make the request to TMDb API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
            # for movie in data["results"]:
            #     adult = movie["adult"]
            #     # genre_ids = movie["genre_ids"]
            #     id = movie["id"]
            #     title = movie["title"]
            #     backdrop_path = movie["backdrop_path"]
            #     poster_path = movie["poster_path"]
            #     release_date = movie["release_date"]
            #     overview = movie["overview"]
            #     original_language = movie["original_language"]
            #     popularity = movie["popularity"]
            #     vote_count = movie["vote_count"]
            #     return Response(
            #         {
            #             "title": title,
            #             "release_date": release_date,
            #             "overview": overview,
            #             "backdrop_path": backdrop_path,
            #             "adult": adult,
            #             "id": id,
            #             "poster_path": poster_path,
            #             "original_language": original_language,
            #             "popularity": popularity,
            #             "vote_count": vote_count,
            #         },
            #         status=status.HTTP_200_OK,
            #     )
        else:
            return Response(
                {"message": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST
            )


class FetchUpcomingTvShow(APIView):
    def get(self, request):
        # Replace 'YOUR_API_KEY' with your actual TMDb API key
        api_key = KEY

        # Base URL for the TMDb API
        base_url = "https://api.themoviedb.org/3"

        # Endpoint for upcoming movies
        endpoint = f"{base_url}/discover/tv?"

        # Parameters including the API key and optional settings
        params = {
            "api_key": api_key,
            "language": "en-US",
            "page": 1,
            "include_adult": True,
            "include_null_first_air_dates": True,
            "first_air_date.gte": "2024-07-08",  # to get movies after this date /
            "sort_by": "popularity.desc",  # to sort by popularity /
            # "sort_by": "first_air_date.asc",  # to short by release date /
            # "first_air_date_year": "2024",  # to get movies by this year /
        }

        # Make the request to TMDb API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
            # for movie in data["results"]:
            #     adult = movie["adult"]
            #     # genre_ids = movie["genre_ids"]
            #     id = movie["id"]
            #     title = movie["title"]
            #     backdrop_path = movie["backdrop_path"]
            #     poster_path = movie["poster_path"]
            #     release_date = movie["release_date"]
            #     overview = movie["overview"]
            #     original_language = movie["original_language"]
            #     popularity = movie["popularity"]
            #     vote_count = movie["vote_count"]
            #     return Response(
            #         {
            #             "title": title,
            #             "release_date": release_date,
            #             "overview": overview,
            #             "backdrop_path": backdrop_path,
            #             "adult": adult,
            #             "id": id,
            #             "poster_path": poster_path,
            #             "original_language": original_language,
            #             "popularity": popularity,
            #             "vote_count": vote_count,
            #         },
            #         status=status.HTTP_200_OK,
            #     )
        else:
            return Response(
                {"message": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST
            )


class FetchTrendingTvShow(APIView):
    def get(self, request):
        # Replace 'YOUR_API_KEY' with your actual TMDb API key
        api_key = KEY

        # Base URL for the TMDb API
        base_url = "https://api.themoviedb.org/3"

        # Endpoint for upcoming movies
        endpoint = f"{base_url}/trending/tv/week?"

        # Parameters including the API key and optional settings
        params = {
            "api_key": api_key,
            "language": "en-US",
        }

        # Make the request to TMDb API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST
            )


class FetchTrendingMovie(APIView):
    def get(self, request):
        # Replace 'YOUR_API_KEY' with your actual TMDb API key
        api_key = KEY

        # Base URL for the TMDb API
        base_url = "https://api.themoviedb.org/3"

        # Endpoint for upcoming movies
        endpoint = f"{base_url}/trending/movie/week?"

        # Parameters including the API key and optional settings
        params = {
            "api_key": api_key,
            "language": "en-US",
        }

        # Make the request to TMDb API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST
            )


class FetchPopularTvShow(APIView):
    def get(self, request):
        # Replace 'YOUR_API_KEY' with your actual TMDb API key
        api_key = KEY

        # Base URL for the TMDb API
        base_url = "https://api.themoviedb.org/3"

        # Endpoint for upcoming movies
        endpoint = f"{base_url}/tv/popular?"

        # Parameters including the API key and optional settings
        params = {
            "api_key": api_key,
            "language": "en-US",
        }

        # Make the request to TMDb API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST
            )


class FetchTopRatedTvShow(APIView):
    def get(self, request):
        # Replace 'YOUR_API_KEY' with your actual TMDb API key
        api_key = KEY

        # Base URL for the TMDb API
        base_url = "https://api.themoviedb.org/3"

        # Endpoint for upcoming movies
        endpoint = f"{base_url}/tv/top_rated?"

        # Parameters including the API key and optional settings
        params = {
            "api_key": api_key,
            "language": "en-US",
        }

        # Make the request to TMDb API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST
            )


class FetchCastById(APIView):
    def get(self, request, imdb_id):
        api_key = KEY
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"{base_url}/movie/{imdb_id}/credits"

        params = {"api_key": api_key, "language": "en-US"}

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            filtered_cast = []
            filtered_crew = []

            for cast in data.get("cast", []):
                if cast.get("profile_path"):
                    filtered_cast.append(
                        {
                            "known_for_department": cast.get("known_for_department"),
                            "original_name": cast.get("original_name"),
                            "profile_path": cast.get("profile_path"),
                            "character": cast.get("character"),
                            "order": cast.get("order"),
                        }
                    )

            for crew in data.get("crew", []):
                if crew.get("profile_path"):
                    filtered_crew.append(
                        {
                            "known_for_department": crew.get("known_for_department"),
                            "name": crew.get("name"),
                            "profile_path": crew.get("profile_path"),
                            "job": crew.get("job"),
                        }
                    )

            return Response(
                {"cast": filtered_cast, "crew": filtered_crew},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST
            )


class FetchMovieImagesById(APIView):
    def get(self, request, imdb_id):
        api_key = KEY
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"{base_url}/movie/{imdb_id}/images"

        params = {"api_key": api_key}

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            filtered_images = {"backdrops": [], "logos": [], "posters": []}

            for image_type in ["backdrops", "logos", "posters"]:
                for image in data.get(image_type, []):
                    if image.get("iso_639_1") == "en":
                        filtered_images[image_type].append(
                            {
                                "height": image.get("height"),
                                "width": image.get("width"),
                                "aspect_ratio": image.get("aspect_ratio"),
                                "file_path": image.get("file_path"),
                                "iso_639_1": image.get("iso_639_1"),
                            }
                        )

            return Response(filtered_images, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Failed to fetch movie images"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FetchMovieVideosById(APIView):
    def get(self, request, imdb_id):
        api_key = KEY2
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"{base_url}/movie/{imdb_id}/videos"

        params = {"api_key": api_key, "language": "en"}

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            filtered_videos = []

            for video in data.get("results", []):
                filtered_videos.append(
                    {
                        "name": video.get("name"),
                        "key": video.get("key"),
                        "type": video.get("type"),
                        "official": video.get("official"),
                        "published_at": video.get("published_at"),
                        "iso_639_1": video.get("iso_639_1"),
                    }
                )

            # Sort videos by published_at, oldest first
            filtered_videos.sort(key=lambda x: parse_datetime(x["published_at"]))

            return Response({"videos": filtered_videos}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Failed to fetch movie videos"},
                status=status.HTTP_400_BAD_REQUEST,
            )
