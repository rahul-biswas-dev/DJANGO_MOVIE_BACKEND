import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from django.apps import apps
from django.utils.timezone import is_aware


class Command(BaseCommand):
    help = "Export all data from the database to an Excel file"

    def handle(self, *args, **kwargs):
        output_file = "database_export.xlsx"

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            for model in apps.get_models():
                model_name = model.__name__
                self.stdout.write(f"Exporting {model_name}...")

                queryset = model.objects.all()
                if queryset.exists():
                    data = list(queryset.values())

                    # Convert timezone-aware datetime fields to naive
                    for item in data:
                        for key, value in item.items():
                            if isinstance(value, pd.Timestamp) and is_aware(value):
                                item[key] = value.tz_localize(
                                    None
                                )  # Convert to naive datetime
                            elif isinstance(value, datetime) and is_aware(value):
                                item[key] = value.replace(
                                    tzinfo=None
                                )  # Convert to naive datetime

                    df = pd.DataFrame(data)
                    df.to_excel(writer, sheet_name=model_name, index=False)
                else:
                    self.stdout.write(f"No data found for {model_name}. Skipping...")

        self.stdout.write(f"Data exported successfully to {output_file}")
