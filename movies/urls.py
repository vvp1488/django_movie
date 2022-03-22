from django.urls import path

from . import views

urlpatterns = [
    path("", views.MoviesView.as_view(), name='main_page'),
    path('test/', views.Test.as_view(), name='test'),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("add_rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review'),
    path("actor/<str:slug>/", views.ActorView.as_view(), name='actor_detail'),
    path("category/<slug:slug>/", views.MoviesByCategory.as_view(), name='movies_by_category'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name='single_movie'),
]