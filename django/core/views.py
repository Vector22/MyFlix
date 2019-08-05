from django.shortcuts import render
from django.views.generic import ListView, DetailView

from core.models import Movie, Person


class MovieList(ListView):
    model = Movie
    # template_name can be omited see below
    template_name = 'core/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 3


class MovieDetail(DetailView):
    queryset = Movie.objects.all_related_persons()
    # We can omit the template_name because django
    # search the associated template with this pattern
    # 'app_name/ModelName_detail.html'
    # template_name = 'core/movie_detail.html'
    context_object_name = 'movie'


class PersonDetail(DetailView):
    # No need to add Model attribut because
    # it's automatically deduced from the queryset
    queryset = Person.objects.all_prefetched_movies()
    context_object_name = 'person'
