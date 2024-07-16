from rest_framework import serializers
from .models import Movie, ProductionCompany, SpokenLanguage, ProductionCountry


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


class MovieSerializer(serializers.ModelSerializer):
    production_companies = ProductionCompanySerializer(many=True)
    spoken_languages = SpokenLanguageSerializer(many=True)
    production_countries = ProductionCountrySerializer(many=True)

    class Meta:
        model = Movie
        fields = "__all__"
