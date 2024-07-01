# data_fetching_app urls file
from django.urls import path
from .views import *
from data_fetching_app.views import FetchHDPoster

urlpatterns = [
    path("fetch/<str:imdb_id>/", FetchMovieData.as_view(), name="fetch_data"),
    path("search/<str:title>/", SearchMovies.as_view(), name="SearchMovie"),
]
