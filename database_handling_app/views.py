from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie
from .serializer import MovieSerializer
from rest_framework import status
from data_fetching_app.views import FetchMovieData
from datetime import datetime, timedelta


# to get all movies from database
class GetAllMovies(APIView):

    def get(self, request):
        try:
            movies = Movie.objects.all()
            serializer = MovieSerializer(movies, many=True)
            return Response(
                {
                    "movies": serializer.data,
                    "Response": True,
                }
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"An error occurred: {str(e)}",
                    "data": None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


#  this class checks if a particular movie is in data base by (imdb_id)
class CheckMovieExistence(APIView):
    def get(self, request, imdb_id=None):
        try:
            if imdb_id is None:
                return Response({"error": "Movie ID not provided"}, status=400)
            movies = Movie.objects.filter(imdb_id=imdb_id)
            if movies.exists():
                return Response({"exists": True, "title": movies.first().title})
            else:
                return Response({"exists": False, "title": None})
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"An error occurred: {str(e)}",
                    "data": None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# this returns a single movie data by imdbid
class SingleMovie(APIView):
    def get(self, request, imdb_id=None):
        # Check if the movie exists in the database
        existence_response = CheckMovieExistence().get(request, imdb_id)
        if existence_response.status_code == status.HTTP_200_OK:
            exists = existence_response.data.get("exists", False)
            if exists:
                # Movie exists, get the movie data from the database
                movie_data = Movie.objects.filter(imdb_id=imdb_id).first()
                serializer = MovieSerializer(movie_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Movie doesn't exist, fetch data from external API and save to the database
                fetch_response = FetchMovieData().get(request, imdb_id)
                if fetch_response.status_code == status.HTTP_200_OK:
                    # Retrieve the newly saved movie data from the database
                    movie_data = Movie.objects.filter(imdb_id=imdb_id).first()
                    serializer = MovieSerializer(movie_data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Failed to fetch movie data"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            return Response(
                {"error": "Failed to check movie existence"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# newly released movies past 6 months
class NewReleasedSixMonth(APIView):
    def get(self, request):

        try:
            # Get the current date
            current_date = datetime.now()

            # Calculate the date 6 months ago from the current date
            six_months_ago = current_date - timedelta(days=30 * 6)

            # Query movies released within the last 6 months
            new_releases = Movie.objects.filter(released_date__gte=six_months_ago)
            serializer = MovieSerializer(new_releases, many=True)

            # Additional metadata
            movies_returned = len(new_releases)
            return Response(
                {
                    "data": serializer.data,
                    "movies_returned": movies_returned,
                    "Response": True,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "Response": False,
                    "message": f"An error occurred: {str(e)}",
                    "data": None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# newly released past year
class NewReleasedThisYear(APIView):
    def get(self, request):

        try:
            # Get the current year
            current_year = datetime.now().year

            # Query movies released in the current year
            new_releases = Movie.objects.filter(released_date__year=current_year)
            serializer = MovieSerializer(new_releases, many=True)

            # Additional metadata
            movies_returned = len(new_releases)
            return Response(
                {
                    "data": serializer.data,
                    "movies_returned": movies_returned,
                    "Response": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "Response": False,
                    "message": f"An error occurred: {str(e)}",
                    "data": None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# top movies of the decade
class TopMoviesDecade(APIView):
    def get(self, request):

        try:
            # Get the current year
            current_year = datetime.now().year

            # Calculate the start year (10 years ago)
            start_year = current_year - 10

            # Query top 10 movies based on IMDb rating released in the past 10 years
            top_movies = Movie.objects.filter(
                released_date__year__gte=start_year
            ).order_by("-imdb_rating")[:100]
            serializer = MovieSerializer(top_movies, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "Response": True,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "Response": False,
                    "message": f"An error occurred: {str(e)}",
                    "data": None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# top movies last year
class TopMoviesLastYear(APIView):
    def get(self, request):
        try:
            # Get the previous year
            current_year = datetime.now().year
            previous_year = current_year - 1

            # Query top 100 movies based on IMDb rating released in the previous year
            top_movies = Movie.objects.filter(
                released_date__year=previous_year
            ).order_by("-imdb_rating")[:10]
            serializer = MovieSerializer(top_movies, many=True)

            # Additional metadata
            movies_returned = len(top_movies)
            total_movies_last_year = Movie.objects.filter(
                released_date__year=previous_year
            ).count()

            return Response(
                {
                    "data": serializer.data,
                    "movies_returned": movies_returned,
                    "total_movies_last_year": total_movies_last_year,
                    "Response": True,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "Response": False,
                    "message": f"An error occurred: {str(e)}",
                    "data": None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# top movies of all time
class TopMoviesAllTime(APIView):
    def get(self, request):
        try:
            top_movies = Movie.objects.order_by("-imdb_rating")[:100]
            serializer = MovieSerializer(top_movies, many=True)
            return Response(
                {
                    "data": serializer.data,
                    "Response": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "Response": False,
                    "message": f"An error occurred: {str(e)}",
                    "data": None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
