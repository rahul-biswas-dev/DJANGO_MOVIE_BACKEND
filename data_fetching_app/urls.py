# data_fetching_app urls file
from django.urls import path
from .views import *
from data_fetching_app.views import (
    FetchUpcomingTvShow,
    FetchUpcomingMovies,
    FetchTrendingTvShow,
    FetchTrendingMovie,
    FetchPopularTvShow,
    FetchTopRatedTvShow,
    FetchCastById,
    FetchMovieImagesById,
    FetchMovieVideosById,
)

urlpatterns = [
    path("fetch/<str:imdb_id>/", FetchMovieData.as_view(), name="fetch_data"),
    path("search/<str:title>/", SearchMovies.as_view(), name="SearchMovie"),
    path(
        "upcoming/movie/<int:page>/",
        FetchUpcomingMovies.as_view(),
        name="FetchUpcomingMovies",
    ),
    path("upcoming/tv/", FetchUpcomingTvShow.as_view(), name="FetchUpcomingTvShow"),
    path("trending/tv/", FetchTrendingTvShow.as_view(), name="FetchTrendingTvShow"),
    path("trending/movie/", FetchTrendingMovie.as_view(), name="FetchTrendingMovie"),
    path("popular/tv/", FetchPopularTvShow.as_view(), name="FetchPopularTvShow"),
    path("top_rated/tv/", FetchTopRatedTvShow.as_view(), name="FetchTopRatedTvShow"),
    path("cast/<str:imdb_id>/", FetchCastById.as_view(), name="FetchMovieCast"),
    path("images/<str:imdb_id>/", FetchMovieImagesById.as_view(), name="FetchMovieImages"),
    path("videos/<str:imdb_id>/", FetchMovieVideosById.as_view(), name="FetchMovieVideos"),
]
