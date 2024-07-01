from django.contrib import admin
from .models import Movie
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect


# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "imdb_id",
        "year",
        "released_date",
        "rated",
        "imdb_rating",
        "genres",
        "plot",
        "director",
        "writer",
        "awards",
        "language",
        "poster_url",
        "website",
        "imdb_votes",
        "type",
        "country",
        "actors",
        "boxoffice",
        "rotten_tomatoes_rating",
        "runtime",
        "active",
        "trailer_url",
    )
    search_fields = ("title", "country", "language", "imdb_id", "active","year","actors","writer","director")
    list_filter = (
        "country",
        "year",
        "imdb_rating",
        "genres",
        "language",
        "type",
        "active",
    )


admin.site.register(Movie, MovieAdmin)
