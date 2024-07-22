from django.contrib import admin
from .models import (
    Movie,
    ProductionCompany,
    SpokenLanguage,
    ProductionCountry,
    OriginCountry,
    Cast,
    Crew,
    Video,
    Images,
)
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


class ImagesInline(admin.StackedInline):
    model = Images



class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "imdb_id",
        "year",
        "released_date",
        "rated",
        "imdb_rating",
        "genres",
        "language",
        "imdb_votes",
        "type",
        "boxoffice",
        "rotten_tomatoes_rating",
        "active",
        "trailer_url",
        "logo_url",
        "status",
        "homepage",
    )
    search_fields = (
        "title",
        "language",
        "imdb_id",
        "active",
        "year",
        "writer",
        "director",
    )
    list_filter = (
        "active",
        "year",
        "rated",
        "imdb_rating",
        "type",
    )
    actions = [edit_selected]
    inlines = [ImagesInline]
    raw_id_fields = ("production_companies", "spoken_languages", "production_countries", "origin_countries")


class ProductionCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "origin_country", "imdb_id")
    search_fields = ("name", "imdb_id")


class SpokenLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_639_1", "imdb_id")
    search_fields = ("name", "imdb_id")


class ProductionCountryAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_3166_1", "imdb_id")
    search_fields = ("name", "imdb_id")


class OriginCountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class CastAdmin(admin.ModelAdmin):
    list_display = ("name", "character", "known_for_department")
    search_fields = ("name", "character")


class CrewAdmin(admin.ModelAdmin):
    list_display = ("name", "job", "department")
    search_fields = ("name", "job")


class VideoAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "official")
    list_filter = ("type", "official")
    search_fields = ("name",)


admin.site.register(OriginCountry, OriginCountryAdmin)
admin.site.register(Cast, CastAdmin)
admin.site.register(Crew, CrewAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(ProductionCompany, ProductionCompanyAdmin)
admin.site.register(SpokenLanguage, SpokenLanguageAdmin)
admin.site.register(ProductionCountry, ProductionCountryAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Images)
