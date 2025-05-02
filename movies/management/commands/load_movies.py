import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre  # Import Genre

class Command(BaseCommand):
    help = 'Load movies from movies.json'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'movies.json')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            movies = json.load(f)
            for data in movies:
                # Update atau create Movie berdasarkan external_id
                movie, created = Movie.objects.update_or_create(
                    external_id=data['id'],  # Gunakan external_id, bukan id
                    defaults={
                        'name': data['name'],
                        'description': data['description'],
                        'imgPath': data['imgPath'],
                        'duration': data['duration'],
                        'language': data['language'],
                        'mpaa_type': data['mpaaRating']['type'],  # Sesuai nama field di model
                        'mpaa_label': data['mpaaRating']['label'],  # Sesuai nama field di model
                        'userRating': float(data['userRating'])
                    }
                )
                
                # Handle genres (ManyToMany)
                genres = []
                for genre_name in data['genre']:
                    genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
                    genres.append(genre)
                
                movie.genres.set(genres)  # Update relasi ManyToMany

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(movies)} movies'))