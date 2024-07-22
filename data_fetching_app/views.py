from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
from django.db import transaction
from datetime import datetime
from database_handling_app.models import (
    Movie,
    ProductionCompany,
    SpokenLanguage,
    ProductionCountry,
    Cast,
    Crew,
    Video,
    Backdrops,
    Posters,
    Logos,
    OriginCountry,
    Images,
)
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

    def fetch_videos(self, data):
        movie_id = data.get("imdbID", "")
        api_key = os.getenv("TMDB_KEY")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"

        response = requests.get(url)
        data = response.json()

        trailer_keys = []
        for video in data.get("results", []):
            video_info = {
                "iso_639_1": video.get("iso_639_1"),
                "iso_3166_1": video.get("iso_3166_1"),
                "name": video.get("name"),
                "key": video.get("key"),
                "type": video.get("type"),
                "size": video.get("size"),
                "official": video.get("official"),
                "published_at": video.get("published_at"),
            }
            trailer_keys.append(video_info)

        return trailer_keys

    def fetch_logos(self, data):
        imdb_id = data.get("imdbID", "")
        api_key = os.getenv("TMDB_KEY2")
        url = f"https://api.themoviedb.org/3/movie/{imdb_id}/images?api_key={api_key}"

        response = requests.get(url)
        data = response.json()

        logos = []
        for logo in data.get("logos", []):
            logos.append(
                {
                    "file_path": logo["file_path"],
                    "aspect_ratio": logo.get("aspect_ratio", 1.0),
                    "height": logo.get("height", 1080),
                    "width": logo.get("width", 1920),
                    "iso_639_1": logo.get("iso_639_1", "en"),
                }
            )

        return logos

    def fetch_backdrops(self, data):
        movie_id = data.get("imdbID", "")
        api_key = os.getenv("TMDB_KEY2")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={api_key}"

        response = requests.get(url)
        data = response.json()

        backdrops = []
        for backdrop in data.get("backdrops", []):
            backdrops.append(
                {
                    "file_path": backdrop["file_path"],
                    "aspect_ratio": backdrop.get("aspect_ratio", 1.0),
                    "height": backdrop.get("height", 1080),
                    "width": backdrop.get("width", 1920),
                    "iso_639_1": backdrop.get("iso_639_1", "en"),
                }
            )

        return backdrops

    def fetch_posters(self, data):
        movie_id = data.get("imdbID", "")
        api_key = os.getenv("TMDB_KEY2")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={api_key}"

        response = requests.get(url)
        data = response.json()

        posters = []
        for poster in data.get("posters", []):
            posters.append(
                {
                    "file_path": poster["file_path"],
                    "aspect_ratio": poster.get("aspect_ratio", 1.0),
                    "height": poster.get("height", 1080),
                    "width": poster.get("width", 1920),
                    "iso_639_1": poster.get("iso_639_1", "en"),
                }
            )

        return posters

    def fetch_cast(self, data):
        movie_id = data.get("imdbID", "")
        api_key = os.getenv("TMDB_KEY2")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"

        response = requests.get(url)
        data = response.json()

        cast = []
        for cast_member in data.get("cast", []):
            cast_member_data = {
                "id": cast_member["id"],
                "name": cast_member["name"],
                "known_for_department": cast_member["known_for_department"],
                "character": cast_member["character"],
                "profile_path": cast_member["profile_path"],
                "order": cast_member["order"],
            }
            cast.append(cast_member_data)
        return cast

    def fetch_crew(self, data):
        movie_id = data.get("imdbID", "")
        api_key = os.getenv("TMDB_KEY2")
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            crew = []
            for crew_member in data.get("crew", []):
                crew_member_data = {
                    "id": crew_member["id"],
                    "name": crew_member["name"],
                    "known_for_department": crew_member["known_for_department"],
                    "department": crew_member.get("department"),
                    "profile_path": crew_member["profile_path"],
                    "job": crew_member["job"],
                }
                crew.append(crew_member_data)
            return crew
        except requests.RequestException as e:
            print(f"Error fetching crew data: {e}")
            return []

    def fetch_country(self, data_tmdb):
        country = data_tmdb.get("origin_country", [])

        country_list = []
        for c in country:
            country_list.append(c["name"])

        return country_list

    # data related work for database
    @transaction.atomic
    def save_movie_data(self, data, data_tmdb):

        imdb_id = data.get("imdbID", "")

        # handel single trailer key
        trailer = self.fetch_videos(data)
        for video in trailer:
            if video["type"] == "Trailer" and video["type"] == "Trailer":
                trailer_url = video["key"]

                break

        # handel single logo url
        logo = self.fetch_logos(data)
        for l in logo:
            if l["iso_639_1"] == "en":
                logo_url = l["file_path"]
                break

        # Handle production companies
        production_companies = []
        for company in data_tmdb.get("production_companies", []):
            prod_company, _ = ProductionCompany.objects.get_or_create(
                name=company["name"],
                defaults={
                    "logo_path": company.get("logo_path"),
                    "origin_country": company.get("origin_country"),
                    "imdb_id": imdb_id,
                },
            )
            production_companies.append(prod_company)

        # Handle spoken languages
        spoken_languages = []
        for language in data_tmdb.get("spoken_languages", []):
            lang, _ = SpokenLanguage.objects.get_or_create(
                iso_639_1=language["iso_639_1"],
                defaults={"name": language["name"], "imdb_id": imdb_id},
            )
            spoken_languages.append(lang)

        # Handle production countries
        production_countries = []
        for country in data_tmdb.get("production_countries", []):
            prod_country, _ = ProductionCountry.objects.get_or_create(
                iso_3166_1=country["iso_3166_1"],
                defaults={"name": country["name"], "imdb_id": imdb_id},
            )
            production_countries.append(prod_country)

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
                imdb_id=data.get("imdbID", ""),
                imdb_votes=imdb_votes,
                type=data.get("Type", ""),
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

            # Create the Images object
            images = Images.objects.create(movie=movie)

            # Add many-to-many relationships
            movie.production_companies.set(production_companies)
            movie.spoken_languages.set(spoken_languages)
            movie.production_countries.set(production_countries)

            # Handel origin country
            origin_countries = []
            for country in data_tmdb.get("production_countries", []):
                origin_country, _ = OriginCountry.objects.get_or_create(
                    name=country["name"]
                )
                origin_countries.append(origin_country)
            movie.origin_countries.set(origin_countries)

            # Handle crew
            crew = self.fetch_crew(data)
            if crew:
                crew_objects = [Crew(**member) for member in crew]
                Crew.objects.bulk_create(crew_objects, ignore_conflicts=True)
                movie.crew.set(crew_objects)

            # Handle cast
            cast = self.fetch_cast(data)
            if cast:
                cast_objects = [Cast(**member) for member in cast]
                Cast.objects.bulk_create(cast_objects, ignore_conflicts=True)
                movie.cast.set(cast_objects)

            # Handle videos
            videos = self.fetch_videos(data)
            if videos:
                video_objects = []
                for video_data in videos:
                    video, created = Video.objects.get_or_create(
                        key=video_data["key"], defaults=video_data
                    )
                    video_objects.append(video)
                movie.videos.set(video_objects)

            # Handle logos, backdrops, and posters
            logos_data = self.fetch_logos(data)
            backdrops_data = self.fetch_backdrops(data)
            posters_data = self.fetch_posters(data)

            if logos_data:
                logo_objects = [
                    Logos.objects.create(
                        iso_639_1=item.get("iso_639_1", "en"),
                        **{k: v for k, v in item.items() if k != "iso_639_1"},
                    )
                    for item in logos_data
                ]

                images.logos.set(logo_objects)

            if backdrops_data:
                backdrop_objects = [
                    Backdrops.objects.create(**item) for item in backdrops_data
                ]
                images.backdrops.set(backdrop_objects)

            if posters_data:
                poster_objects = [
                    Posters.objects.create(**item) for item in posters_data
                ]
                images.posters.set(poster_objects)

            return movie

        except (ValueError, IntegrityError) as e:
            print(f"Error saving movie data: {e}")
            return None

    # function to save the data to database
    def get(self, request, imdb_id):
        try:
            data = self.fetch_movie_data(imdb_id)
            data_tmdb = self.fetch_movie_data_tmdb(imdb_id)
            if data and data_tmdb:
                self.save_movie_data(data, data_tmdb)
                return JsonResponse(
                    {"message": f"Movie {imdb_id} saved successfully"}, status=200
                )
            else:
                return JsonResponse({"message": "Failed to fetch data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)


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
