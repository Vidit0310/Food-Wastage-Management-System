import json
from django.core.management.base import BaseCommand
from complaints.models import area_master

class Command(BaseCommand):
    help = 'Import station names into area names'

    def handle(self, *args, **options):
        json_file_path = 'copy.json' 

        try:
            with open(json_file_path, 'r') as file:
                station_data = json.load(file)

                for station in station_data:
                    station_name = station.get('station_name')

                    if station_name:
                        # Check if the area with the same name already exists
                        existing_area = area_master.objects.filter(area_name=station_name).first()

                        if not existing_area:
                            # Create a new area with the station name
                            new_area = area_master(area_name=station_name)
                            new_area.save()

                            self.stdout.write(self.style.SUCCESS(f'Area "{new_area.area_name}" created successfully.'))
                        else:
                            self.stdout.write(self.style.SUCCESS(f'Area "{existing_area.area_name}" already exists.'))
                    else:
                        self.stdout.write(self.style.ERROR('Invalid station data: station_name is missing.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('JSON file not found. Please provide the correct file path.'))

        self.stdout.write(self.style.SUCCESS('Finished importing station names into area names.'))