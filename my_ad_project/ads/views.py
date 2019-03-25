from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from .models import Category, Ad, Image
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect('index')


class IndexView(ListView):
    model = Ad
    template_name = 'ads/index.html'
    context_object_name = 'ads'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Ad.objects.order_by('created_on')[:9]
        data = []
        for ad in queryset:
            image = Image.objects.filter(ad=ad.id).first()
            data.append({'title': ad.title, 'category': ad.category, 'img': image.img})
        context['ads'] = data
        return context


class AdListView(ListView):
    model = Ad
    template_name = 'ads/list.html'
    queryset = Ad.objects.all()
    context_object_name = 'ads'
    paginate_by = 18

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', None)
        queryset = Ad.objects.order_by('created_on')
        if query is not None:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        data = []
        for ad in queryset:
            image = Image.objects.filter(ad=ad.id).first()
            data.append({'ad': ad, 'image': image})
        context['ads'] = data

        paginator = Paginator(data, self.paginate_by)
        page = self.request.GET.get('page')
        context['ads'] = paginator.get_page(page)
        context['categories'] = Category.objects.all()
        return context

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super(AdListView, self).dispatch(*args, **kwargs)


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.filter(ad=self.kwargs['pk'])
        data = []
        number = -1
        for image in images:
            number = number + 1
            data.append({'number': number, 'img': image.img})

        context['images'] = data
        return context
