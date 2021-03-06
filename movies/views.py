from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q, Prefetch, Avg, Func, IntegerField, DecimalField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .models import Movie, Actor, Genre, Rating, Category, Profile, LogoProfile
from .forms import ReviewForm, RatingForm
from .services import get_client_ip
from django.contrib.auth.models import User
from django.contrib import messages

class Round(Func):
    function = 'ROUND'
    arity = 2

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
    queryset = Movie.objects.filter(draft=False).annotate(star_avg=Round(Avg('ratings__star'), 2, output_field=DecimalField())).order_by('title')
    paginate_by = 3

    def get_context_data(self):
        context = super().get_context_data()
        context['range'] = range(5)
        return context


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
            if str(request.user) != 'AnonymousUser' :
                form.profile_user = Profile.objects.get(user=request.user)
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
        context['range'] = range(5)
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
        context['range'] = range(5)
        return context


class MoviesByCategory(GenreYear, ListView):
    """Список фильмов по категориям"""
    paginate_by = 3
    model = Movie

    def get_queryset(self):
        category = Category.objects.get(url=self.kwargs.get('slug'))
        queryset = Movie.objects.filter(category=category.pk)
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['range'] = range(5)
        return context


class Test(View):

    def get(self, request):
        movies = Movie.objects.all().select_related('category').prefetch_related(
            Prefetch('genres', queryset=Genre.objects.only('name'))
        ).only('category__id')
        context = {
            'movies': movies,
        }
        return render(request, 'movies/test.html', context)


class MoviesByRating(GenreYear, ListView):
    """Фильтрация по рейтингу из сайд-бара"""
    model = Movie
    paginate_by = 3

    def get_context_data(self):
        contex = super().get_context_data()
        contex['range'] = range(5)
        return contex

    def get_queryset(self):
        queryset = Movie.objects.filter(draft=False).annotate(star_avg=Round(Avg('ratings__star'), 2, output_field=DecimalField())).filter(star_avg=self.kwargs['star_avg'])
        return queryset


class MoviesMostViews(GenreYear, ListView):
    model = Movie
    paginate_by = 3

    def get_context_data(self):
        context = super().get_context_data()
        context['range'] = range(5)
        return context

    def get_queryset(self):
        if self.kwargs['how_sort'] == 'mostviews':
            queryset = Movie.objects.filter(draft=False).annotate(
            star_avg=Round(Avg('ratings__star'), 2, output_field=DecimalField())).filter(star_avg__gte=1).order_by('-star_avg')
        elif self.kwargs['how_sort'] == 'lessviews':
            queryset = Movie.objects.filter(draft=False).annotate(
                star_avg=Round(Avg('ratings__star'), 2, output_field=DecimalField())).filter(star_avg__gte=1).order_by('star_avg')
        return queryset


class ProfileView(DetailView):
    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args,**kwargs)
        context['logos'] = LogoProfile.objects.all()
        return context


class ChangeAvatarView(View):
    """Изменить аватар в профиле"""
    def post(self, request, *args, **kwargs):
        profile_id = self.kwargs['pk']
        logo_id = request.POST['logo']
        profile = Profile.objects.get(pk=profile_id)
        with transaction.atomic():
            profile.logo_id = logo_id
            profile.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'pk': profile_id}))


class AddToFavourite(View):
    '''Добавить фильм в избранные'''
    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        with transaction.atomic():
            profile.favourite_movies.add(movie)
            profile.save()
        messages.add_message(request, messages.INFO, 'Фильм успешно добавлен!')

        return HttpResponseRedirect(reverse('main_page'))
