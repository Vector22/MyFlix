from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('movies/', views.MovieList.as_view(), name='movie_list'),
    path('movie/<int:pk>', views.MovieDetail.as_view(),
         name='movie_detail'),
    path('person/<int:pk>', views.PersonDetail.as_view(),
         name='person_detail'),
]
