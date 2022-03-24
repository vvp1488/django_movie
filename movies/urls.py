from django.urls import path

from . import views

urlpatterns = [
    path("", views.MoviesView.as_view(), name='main_page'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('add_to_favourite/<int:pk>/', views.AddToFavourite.as_view(), name='add_to_favourite'),
    path('profile/change_avatar/<int:pk>/', views.ChangeAvatarView.as_view(), name='change_avatar'),
    path('movie_list_by_rating/<int:star_avg>/', views.MoviesByRating.as_view(), name='movie_list_by_rating'),
    path('movies/<str:how_sort>/', views.MoviesMostViews.as_view(), name='movie_list_most_view'),
    path('test/', views.Test.as_view(), name='test'),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("add_rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review'),
    path("actor/<str:slug>/", views.ActorView.as_view(), name='actor_detail'),
    path("category/<slug:slug>/", views.MoviesByCategory.as_view(), name='movies_by_category'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name='single_movie'),
]