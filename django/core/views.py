from django.shortcuts import render
from django.views.generic import ListView, DetailView

from core.models import Movie


class MovieList(ListView):
    model = Movie
    template_name = 'core/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 3


class MovieDetail(DetailView):
    model = Movie
    template_name = 'core/movie_detail.html'
    context_object_name = 'movie'
