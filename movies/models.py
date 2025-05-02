from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q 

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True) #dibuat terpisah untuk menghindari duplikasi data
    def __str__(self):
        return self.name

class MovieQuerySet(models.QuerySet):
    # ----- UNTUK FILTER -----
    def by_title(self, title_name):
        return self.filter(name__iexact=title_name)
    def by_genre(self, genre_name):
        return self.filter(genres__name=genre_name).distinct()
    def min_rating(self, min_rating=0.0):
        return self.filter(userRating__gte=min_rating)
    def max_duration(self, max_duration=160):
        return self.filter(duration__lt=max_duration)
    def by_language(self, language):
        return self.filter(language__iexact=language)
    def by_mpaa_type(self, mpaa_type):
        return self.filter(mpaa_type=mpaa_type)
    def by_title_and_rating(self, keyword, min_rating=0):
        return self.filter(Q(name__icontains=keyword) | Q(genres__name__icontains=keyword),userRating__gte=min_rating).distinct()
    # ----- UNTUK MENGURUTKAN -----
    def order_by_rating_desc(self):
        """Urutkan dari rating tertinggi ke terendah"""
        return self.order_by('-userRating')
    def order_by_genre_asc(self):
        """Urutkan berdasarkan genre pertama (A-Z)"""
        return self.annotate(first_genre=Min('genres__name')).order_by('first_genre')
    def by_title_and_rating(self, keyword, min_rating=0):
    #Kombinasi pencarian judul/genre dengan rating minimal
        return self.filter(Q(name__icontains=keyword) | Q(genres__name__icontains=keyword),userRating__gte=min_rating).distinct()
    

class Movie(models.Model):
    external_id = models.IntegerField(unique=True, null=True) #id dari json untuk membedakan dari default autofield primary key dari json
    name = models.CharField(max_length=200)
    description = models.TextField()
    imgPath = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    language = models.CharField(max_length=100)
    mpaa_type = models.CharField(max_length=10)  
    mpaa_label = models.TextField()  
    userRating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    genres = models.ManyToManyField(Genre, related_name="movies")    # Relasi many-to-many ke Genre
    objects = MovieQuerySet.as_manager()

    def __str__(self):
        return self.name
    
