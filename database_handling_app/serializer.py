from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "title",
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
            "imdb_id",
            "imdb_votes",
            "type",
            "country",
            "actors",
            "boxoffice",
            "rotten_tomatoes_rating",
            "runtime",
            "active",
            "trailer_url",
        ]
