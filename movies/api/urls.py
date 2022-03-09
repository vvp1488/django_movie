from django.urls import path

from . import api_views

urlpatterns = [
    path('movies/', api_views.MovieListView.as_view()),
    path('movie/<int:pk>/', api_views.MovieDetailView.as_view()),
    path('review/', api_views.ReviewCreateView.as_view()),
    path('rating/', api_views.AddStarRatingView.as_view()),
    path('actors/', api_views.ActorsListView.as_view()),
    path('actors/<int:pk>/', api_views.ActorsDetailView.as_view())
]