from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    origin_country = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

