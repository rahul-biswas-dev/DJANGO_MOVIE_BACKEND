from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=5, default="Data Not Available")
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
    website = models.URLField(max_length=455, null=True, blank=True)
    imdb_id = models.CharField(max_length=20)
    imdb_votes = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, default="Unknown")
    country = models.CharField(max_length=100, default="Unknown")
    actors = models.TextField(default="Unknown")
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

    def __str__(self):
        return self.title
