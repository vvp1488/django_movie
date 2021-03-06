from rest_framework import generics, permissions, viewsets
from django.db import models

from django_filters.rest_framework import DjangoFilterBackend

from ..services import get_client_ip, MovieFilter, PaginationMovies
from ..models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer
)


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Информации о актерах и режиссерах"""
    queryset = Actor.objects.all()
    pagination_class = PaginationMovies

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retireve':
            return ActorDetailSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter
    # permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
           rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            # middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            middle_star=(models.Avg('ratings__star'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавления отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавления рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


# class ActorsDetailView(generics.RetrieveAPIView):
#     """Вывод полной информации актеров и режиссеров"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
#
#
# class ActorsListView(generics.ListAPIView):
#     """Вывод списка актеров и режиссеров"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer

#
# class MovieListView(generics.ListAPIView):
#     """Вывод списка фильмов"""
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated,]
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             # middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#             middle_star=(models.Avg('ratings__star'))
#         )
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     """Вывод списка фильмов"""
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer


# class ReviewCreateView(generics.CreateAPIView):
#     """Добавления отзыва к фильму"""
#     serializer_class = ReviewCreateSerializer


# class AddStarRatingView(generics.CreateAPIView):
#     """Добавления рейтинга к фильму"""
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
