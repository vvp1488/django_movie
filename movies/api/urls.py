from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import api_views

urlpatterns = format_suffix_patterns([
    path('movies/', api_views.MovieViewSet.as_view({'get': 'list'})),
    path('movie/<int:pk>/', api_views.MovieViewSet.as_view({'get': 'retrieve'})),
    path('review/', api_views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path('rating/', api_views.AddStarRatingViewSet.as_view({'post': 'create'})),
    path('actors/', api_views.ActorsViewSet.as_view({'get': 'list'})),
    path('actors/<int:pk>/', api_views.ActorsViewSet.as_view({'get': 'retrieve'}))
])
#
# urlpatterns = [
#     path('movies/', api_views.MovieListView.as_view()),
#     path('movie/<int:pk>/', api_views.MovieDetailView.as_view()),
#     path('review/', api_views.ReviewCreateView.as_view()),
#     path('rating/', api_views.AddStarRatingView.as_view()),
#     path('actors/', api_views.ActorsListView.as_view()),
#     path('actors/<int:pk>/', api_views.ActorsDetailView.as_view())
# ]