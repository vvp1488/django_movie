from django_filters import rest_framework as filters
from .models import Movie
from rest_framework.pagination import PageNumberPagination


def get_client_ip(request):
    """Получения IP пользователя"""
    x_forwarder_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarder_for:
        ip = x_forwarder_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class MovieFilter(filters.FilterSet):
    genres = filters.CharFilter(field_name='genres__name', lookup_expr='icontains')
    # genres = filters.BaseInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']


class PaginationMovies(PageNumberPagination):
    page_size = 3
    max_page_size = 1000