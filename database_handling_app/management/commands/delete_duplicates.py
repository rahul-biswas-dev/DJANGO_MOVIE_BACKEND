from django.core.management.base import BaseCommand
from django.db.models import Count
from database_handling_app.models import Movie

class Command(BaseCommand):
    help = 'Delete duplicate movie records'

    def handle(self, *args, **kwargs):
        # Query for duplicate movie titles
        duplicate_movies = Movie.objects.values('title').annotate(count=Count('id')).filter(count__gt=1)

        if duplicate_movies.exists():
            self.stdout.write(self.style.WARNING("Deleting duplicate movies..."))
            for duplicate_movie in duplicate_movies:
                # Get duplicate movie instances
                movies_to_delete = Movie.objects.filter(title=duplicate_movie['title'])[1:]

                # Delete duplicate movie instances
                for movie in movies_to_delete:
                    movie.delete()
            self.stdout.write(self.style.SUCCESS("Duplicate movies deleted successfully."))
        else:
            self.stdout.write(self.style.SUCCESS("No duplicate movies found."))
