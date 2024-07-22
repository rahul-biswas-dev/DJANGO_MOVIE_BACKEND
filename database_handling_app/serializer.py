from rest_framework import serializers
from .models import (
    Movie,
    ProductionCompany,
    SpokenLanguage,
    ProductionCountry,
    OriginCountry,
    Cast,
    Crew,
    Backdrops,
    Video,
    Posters,
    Logos,
    Images
)


class ProductionCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCompany
        fields = "__all__"


class SpokenLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = "__all__"


class ProductionCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCountry
        fields = "__all__"


class OriginCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginCountry
        fields = "__all__"


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class BackdropsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backdrops
        fields = "__all__"


class PostersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posters
        fields = "__all__"


class LogosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logos
        fields = "__all__"

class ImagesSerializer(serializers.ModelSerializer):
    logos = LogosSerializer(many=True)
    posters = PostersSerializer(many=True)
    backdrops = BackdropsSerializer(many=True)

    class Meta:
        model = Images
        fields = ('logos', 'posters', 'backdrops')






class MovieSerializer(serializers.ModelSerializer):
    production_companies = ProductionCompanySerializer(many=True)
    spoken_languages = SpokenLanguageSerializer(many=True)
    production_countries = ProductionCountrySerializer(many=True)
    origin_countries = OriginCountrySerializer(many=True)
    cast = CastSerializer(many=True)
    crew = CrewSerializer(many=True)
    videos = VideoSerializer(many=True)
    images = ImagesSerializer(many=True)


    class Meta:
        model = Movie
        fields = "__all__"
