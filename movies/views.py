from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Movie

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Ambil parameter
        min_rating = float(self.request.GET.get('min_rating', 0))
        sort = self.request.GET.get('sort', '')
        
        # Filter
        queryset = queryset.min_rating(min_rating)
        
        # Order
        if sort == 'genre':
            queryset = queryset.order_by_genre_asc()
        else:
            queryset = queryset.order_by_rating_desc()
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Data untuk filter
        context['all_genres'] = Movie.genres.field.related_model.objects.distinct()
        context['all_languages'] = Movie.objects.values_list('language', flat=True).distinct()
        context['all_mpaa_types'] = Movie.objects.values_list('mpaa_type', flat=True).distinct()
        # Data untuk search form
        context['search_query'] = self.request.GET.get('q', '')
        context['min_rating'] = self.request.GET.get('min_rating', '0')
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'