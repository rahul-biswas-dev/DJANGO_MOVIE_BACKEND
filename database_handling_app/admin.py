# from django.contrib import admin
# from .models import Movie
# from django.shortcuts import redirect
# from django.urls import reverse


# def edit_selected(modeladmin, request, queryset):
#     if queryset.count() == 1:
#         obj = queryset.first()
#         return redirect(
#             reverse("admin:database_handling_app_movie_change", args=[obj.id])
#         )
#     else:
#         modeladmin.message_user(request, "Please select only one movie to edit.")


# edit_selected.short_description = "Edit selected movie"

# # Register your models here.
# class MovieAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "imdb_id",
#         "year",
#         "released_date",
#         "rated",
#         "imdb_rating",
#         "genres",
#         "plot",
#         "director",
#         "writer",
#         "awards",
#         "language",
#         "poster_url",
#         "backdrop_url",
#         "website",
#         "imdb_votes",
#         "type",
#         "country",
#         "actors",
#         "boxoffice",
#         "rotten_tomatoes_rating",
#         "runtime",
#         "active",
#         "trailer_url",
#         "logo_url",
#     )
#     search_fields = (
#         "title",
#         "country",
#         "language",
#         "imdb_id",
#         "active",
#         "year",
#         "actors",
#         "writer",
#         "director",
#     )
#     list_filter = (
#         "trailer_url",
#         "active",
#         "year",
#         "rated",
#         "imdb_rating",
#         "type",
#         "country",
#     )
#     actions = [edit_selected]

# admin.site.register(Movie, MovieAdmin)

from django.contrib import admin
from .models import Movie
from django.shortcuts import redirect
from django.urls import reverse


def edit_selected(modeladmin, request, queryset):
    if queryset.count() == 1:
        obj = queryset.first()
        return redirect(
            reverse("admin:database_handling_app_movie_change", args=[obj.id])
        )
    else:
        modeladmin.message_user(request, "Please select only one movie to edit.")


edit_selected.short_description = "Edit selected movie"


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
        "backdrop_url",
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
        "logo_url",
        "status",
        "homepage",
    )
    search_fields = (
        "title",
        "country",
        "language",
        "imdb_id",
        "active",
        "year",
        "actors",
        "writer",
        "director",
    )
    list_filter = (
        "active",
        "year",
        "rated",
        "imdb_rating",
        "type",
        "country",
    )
    actions = [edit_selected]



admin.site.register(Movie, MovieAdmin )
