from django.core.management.base import BaseCommand
from django.db.models import Count
from database_handling_app.models import Movie

class Command(BaseCommand):
    help = 'Find and display duplicate movies by imdb_id'

    def handle(self, *args, **kwargs):
        # Query for duplicate movie imdb_ids
        duplicate_movies = Movie.objects.values('imdb_id').annotate(count=Count('id')).filter(count__gt=1)

        if duplicate_movies.exists():
            self.stdout.write(self.style.WARNING("Duplicate movies found:"))
            for duplicate_movie in duplicate_movies:
                self.stdout.write(f"IMDB ID: {duplicate_movie['imdb_id']}, Count: {duplicate_movie['count']}")
        else:
            self.stdout.write(self.style.SUCCESS("No duplicate movies found."))
