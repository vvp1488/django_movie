from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Movie, Actor, Genre, Rating, Category
from .forms import ReviewForm, RatingForm
from .services import get_client_ip


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").order_by('year').distinct()


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    #Рандомный порядок вывода фильмов
    queryset = Movie.objects.filter(draft=False).order_by("?")
    paginate_by = 3


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["avg_rating"] = self.get_object().get_rating()
        context['form'] = ReviewForm()

        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST or None)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie_id = pk
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(LoginRequiredMixin, GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 3

    def get_queryset(self):
        if 'genre' in self.request.GET and 'year' in self.request.GET:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")), Q(genres__in=self.request.GET.getlist("genre"))
            ).distinct()
        else:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) | Q(genres__in=self.request.GET.getlist("genre"))
            ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist('year')])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist('genre')])
        return context


class AddStarRating(View):
    """Добавления рейтинга к фильму"""

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(GenreYear, ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        queryset = Movie.objects.filter(title__icontains=self.request.GET.get("q").capitalize())
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


class MoviesByCategory(GenreYear, ListView):
    """Список фильмов по категориям"""
    paginate_by = 3
    model = Movie

    def get_queryset(self):
        category = Category.objects.get(url=self.kwargs.get('slug'))
        queryset = Movie.objects.filter(category=category.pk)
        return queryset


class MoviesByRating(GenreYear, ListView):
    """Список фильмов по рейтингу"""
    paginate_by = 3
    model = Movie
    # template_name = 'movies/base.html'

    def get_queryset(self):
        star = self.kwargs.get('star')
        queryset = Movie.objects.all()
        return queryset


class Test(View):
    def get(self, request):
        return render(request, 'movies/test.html')