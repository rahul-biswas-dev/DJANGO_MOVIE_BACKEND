# database_handling_app urls file
from django.urls import path
from .views import (
    GetAllMovies,
    CheckMovieExistence,
    SingleMovie,
    NewReleasedSixMonth,
    NewReleasedThisYear,
    TopMoviesDecade,
    TopMoviesLastYear,
    TopMoviesAllTime,
)

urlpatterns = [
    path("movies/", GetAllMovies.as_view(), name="get_all_movies"),
    path(
        "check/<str:imdb_id>/",
        CheckMovieExistence.as_view(),
        name="check_movie_existence",
    ),
    path(
        "movie/<str:imdb_id>/",
        SingleMovie.as_view(),
        name="single_movie",
    ),
    path(
        "new-releases-m/",
        NewReleasedSixMonth.as_view(),
        name="NewReleasedSixMonth",
    ),
    path(
        "new-releases-y/",
        NewReleasedThisYear.as_view(),
        name="NewReleasedThisYear",
    ),
    path(
        "top-d/",
        TopMoviesDecade.as_view(),
        name="TopMoviesDecade",
    ),
    path(
        "top-y/",
        TopMoviesLastYear.as_view(),
        name="TopMoviesLastYear",
    ),
    path(
        "top-a/",
        TopMoviesAllTime.as_view(),
        name="TopMoviesAllTime",
    ),
]
