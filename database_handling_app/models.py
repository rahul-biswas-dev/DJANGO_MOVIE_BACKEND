from django.db import models


class ProductionCompany(models.Model):
    name = models.CharField(max_length=255)
    logo_path = models.CharField(max_length=455, null=True, blank=True)
    origin_country = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class SpokenLanguage(models.Model):
    iso_639_1 = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductionCountry(models.Model):
    iso_3166_1 = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class OriginCountry(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cast(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    known_for_department = models.CharField(max_length=255)
    character = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.name} as {self.character}"


class Crew(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    known_for_department = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.job}"


class Video(models.Model):
    iso_639_1 = models.CharField(max_length=10)
    iso_3166_1 = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    size = models.IntegerField(null=True, blank=True)
    official = models.BooleanField(default=False)
    published_at = models.DateTimeField()

    class Meta:
        app_label = "database_handling_app"
        db_table = "database_handling_app_video"

    def __str__(self):
        return self.name


class Backdrops(models.Model):
    aspect_ratio = models.FloatField()
    height = models.IntegerField()
    width = models.IntegerField()
    iso_639_1 = models.CharField(max_length=10, default="en", null=True, blank=True)
    file_path = models.CharField(max_length=255)

    class Meta:
        app_label = "database_handling_app"
        db_table = "database_handling_app_backdrops"

    def __str__(self):
        return f"{self.file_path}"


class Posters(models.Model):
    aspect_ratio = models.FloatField()
    height = models.IntegerField()
    width = models.IntegerField()
    iso_639_1 = models.CharField(max_length=10, default="en", null=True, blank=True)
    file_path = models.CharField(max_length=255)

    class Meta:
        app_label = "database_handling_app"
        db_table = "database_handling_app_posters"

    def __str__(self):
        return f"{self.file_path}"


class Logos(models.Model):
    aspect_ratio = models.FloatField()
    height = models.IntegerField()
    width = models.IntegerField()
    iso_639_1 = models.CharField(max_length=10, default="en", null=True, blank=True)
    file_path = models.CharField(max_length=255)

    class Meta:
        app_label = "database_handling_app"
        db_table = "database_handling_app_logos"

    def __str__(self):
        return f"{self.file_path}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=50, default="N/A")
    released_date = models.DateField(null=True, blank=True)
    rated = models.CharField(max_length=20, default="Not Rated")
    imdb_rating = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=255)
    plot = models.TextField(default="No plot available")
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255, default="No Data Available")
    awards = models.TextField(default="No awards available")
    language = models.CharField(max_length=100, default="N/A")
    poster_url = models.CharField(max_length=455)
    imdb_id = models.CharField(max_length=20)
    imdb_votes = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, default="Unknown")
    boxoffice = models.CharField(max_length=100, default="Unknown", null=True)
    rotten_tomatoes_rating = models.CharField(
        max_length=20, null=True, blank=True, default="N/A"
    )
    runtime = models.CharField(max_length=20, null=True, blank=True, default="N/A")
    active = models.BooleanField(default=False)
    trailer_url = models.CharField(max_length=455, null=True, blank=True)
    logo_url = models.CharField(max_length=455, null=True, blank=True)
    backdrop_url = models.CharField(max_length=455, null=True, blank=True)
    status = models.CharField(max_length=100, default="Unknown")
    original_language = models.CharField(max_length=100, default="Unknown")
    homepage = models.URLField(max_length=455, null=True, blank=True)

    production_companies = models.ManyToManyField(ProductionCompany)
    spoken_languages = models.ManyToManyField(SpokenLanguage)
    production_countries = models.ManyToManyField(ProductionCountry)
    origin_countries = models.ManyToManyField(OriginCountry)
    cast = models.ManyToManyField(Cast)
    crew = models.ManyToManyField(Crew)
    videos = models.ManyToManyField(Video)

    def __str__(self):
        return self.title


class Images(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="images")
    logos = models.ManyToManyField(Logos)
    posters = models.ManyToManyField(Posters)
    backdrops = models.ManyToManyField(Backdrops)

    def __str__(self):
        return f"Images for {self.movie.title}"
