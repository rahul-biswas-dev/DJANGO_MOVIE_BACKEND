import openpyxl
from django.core.management.base import BaseCommand
from database_handling_app.models import Movie


def read_data_from_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path)
    worksheet = workbook.active
    headers = [cell.value for cell in worksheet[1]]  # Get the header row
    data = []
    for row in worksheet.iter_rows(min_row=2, values_only=True):
        data.append([cell for cell in row])
    return headers, data


def save_data_to_database(headers, data):
    for row in data:
        movie_data = dict(zip(headers, row))
        movie = Movie(**movie_data)
        movie.save()


class Command(BaseCommand):
    help = "Clear database and upload data from XLSX"

    def handle(self, *args, **options):
        # Clear the database
        Movie.objects.all().delete()

        # Read data from XLSX file
        xlsx_file_path = "E:/movie_website/BACKEND/data.xlsx"
        headers, data = read_data_from_xlsx(xlsx_file_path)

        # Save data to the database
        save_data_to_database(headers, data)

        self.stdout.write(self.style.SUCCESS("Data uploaded successfully"))
