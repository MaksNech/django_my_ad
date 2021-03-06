from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic.edit import FormView
from django.forms import modelformset_factory
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

from .models import Category, Ad, Image, ChatMessage
from .forms import AdCreateForm, ChatMessageCreateForm


def permission_denied(request):
    name = request.session.get('permission_name')
    return render(request, 'ads/permission_denied.html', context={'permission': name})


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
        queryset = Ad.objects.order_by('-created_on')[:9]
        data = []
        for ad in queryset:
            image = Image.objects.filter(ad=ad.id).first()
            data.append({'title': ad.title, 'category': ad.category, 'image': image})
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
        queryset = Ad.objects.order_by('-created_on')
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


def ad_detail(request, ad_slug):
    ad = Ad.objects.get(slug=ad_slug)
    form = ChatMessageCreateForm(request.POST, request.FILES)
    messages = ChatMessage.objects.filter(ad=ad)
    images = Image.objects.filter(ad=ad)
    data = []
    number = -1
    for image in images:
        number = number + 1
        data.append({'number': number, 'image': image})
    images = data
    if ad:
        token = ''
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)
        return render(request, 'ads/detail.html', context={
            'ad': ad,
            'images': images,
            'form': form,
            'messages': messages,
            'token': token})


@login_required(login_url='/accounts/login/')
def ad_create(request):
    if request.user.is_authenticated:
        ImageFormset = modelformset_factory(Image, fields=('img',), extra=8, max_num=8)

        if request.method == 'POST':
            form = AdCreateForm(request.POST)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                ad = form.save(commit=False)
                ad.author = request.user
                ad.save()

                for f in formset:
                    try:
                        image = Image(ad=ad, img=f.cleaned_data['img'])
                        image.save()

                    except Exception as e:
                        break

                cache.clear()
                return HttpResponseRedirect(reverse('detail', kwargs={'ad_slug': ad.slug}))
        else:
            form = AdCreateForm()
            formset = ImageFormset(queryset=Image.objects.none())

        context = {
            'form': form,
            'formset': formset,
            'categories': Category.objects.all(),
        }
        return render(request, 'ads/create.html', context)
    else:
        request.session['permission_name'] = '"Create Ad" action. You must at first to register and then to login.'
        return HttpResponseRedirect(reverse('permission_denied'))


@login_required(login_url='/accounts/login/')
def ad_edit(request, ad_id):
    ad = Ad.objects.get(id=ad_id)
    if request.user == ad.author:
        if ad:
            ImageFormset = modelformset_factory(Image, fields=('img',), extra=8, max_num=8)

            if request.method == 'POST':
                form = AdCreateForm(request.POST, instance=ad)
                formset = ImageFormset(request.POST or None, request.FILES or None)
                if form.is_valid() and formset.is_valid():
                    Image.objects.filter(ad=ad_id).delete(),
                    ad = form.save(commit=False)
                    ad.author = request.user
                    ad.save()

                    for f in formset:
                        try:
                            image = Image(ad=ad, img=f.cleaned_data['img'])
                            image.save()

                        except Exception as e:
                            break

                    cache.clear()
                    return HttpResponseRedirect(reverse('detail', kwargs={'ad_slug': ad.slug}))
            else:
                form = AdCreateForm()
                formset = ImageFormset(queryset=Image.objects.none())

            context = {
                'form': form,
                'formset': formset,
                'ad': ad,
                'categories': Category.objects.all(),
            }
            return render(request, 'ads/edit.html', context)

    else:
        request.session['permission_name'] = '"Edit Ad" action. Only the author of the Ad can edit it.'
        return HttpResponseRedirect(reverse('permission_denied'))


class AdDeleteView(DeleteView):
    model = Ad

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Ad.objects.filter(author=self.request.user)
        else:
            return Ad.objects.none()

    def get_object(self, queryset=None):
        obj = super(AdDeleteView, self).get_object()
        if not obj.author == self.request.user:
            self.request.session['permission_name'] = '"Delete Ad" action. Only the author of the Ad can delete it.'
            return HttpResponseRedirect(reverse('permission_denied'))
        return obj

    def get_success_url(self):
        cache.clear()
        return reverse('list')
