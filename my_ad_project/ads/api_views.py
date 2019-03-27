from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django_filters import rest_framework as filters

from .serializers import UserSerializer, GroupSerializer, CategorySerializer, AdSerializer, UserFavouriteAdSerializer, \
    ImageSerializer, ChatMessageSerializer
from .models import Category, Ad, UserFavouriteAd, Image, ChatMessage
from .permissions import IsAuthorOrReadOnly



class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['icontains'],
            'id': ['exact'],
        }


class UserViewSet(viewsets.ModelViewSet):
    """
       API endpoint that modify the user instance

       retrieve:
       API endpoint that return the given user.

       list:
       API endpoint that return a list of all the existing users.

       create:
       API endpoint that create a new user instance.

       update:
       API endpoint that update the user instance.

       delete:
       API endpoint that delete the user instance.

    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filterset_class = UserFilter


class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'name': ['icontains'],
            'id': ['exact'],
        }


class GroupViewSet(viewsets.ModelViewSet):
    """
       API endpoint that modify the group instance

       retrieve:
       API endpoint that return the given group.

       list:
       API endpoint that return a list of all the existing groups.

       create:
       API endpoint that create a new group instance.

       update:
       API endpoint that update the group instance.

       delete:
       API endpoint that delete the group instance.

    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_class = GroupFilter


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
            'id': ['exact'],
        }


class CategoryViewSet(viewsets.ModelViewSet):
    """
       API endpoint that modify the category instance

       retrieve:
       API endpoint that return the given category.

       list:
       API endpoint that return a list of all the existing categories.

       create:
       API endpoint that create a new category instance.

       update:
       API endpoint that update the category instance.

       delete:
       API endpoint that delete the category instance.

    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter


class AdFilter(filters.FilterSet):
    class Meta:
        model = Ad
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
            'status': ['exact'],
            'price': ['exact', 'range'],
            'created_on': ['lte', 'gte'],
        }


class AdViewSet(viewsets.ModelViewSet):
    """
       API endpoint that modify the ad instance

       retrieve:
       API endpoint that return the given ad.

       list:
       API endpoint that return a list of all the existing ads.

       create:
       API endpoint that create a new ad instance.

       update:
       API endpoint that update the ad instance.

       delete:
       API endpoint that delete the ad instance.

    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filterset_class = AdFilter
    ordering_fields = ['category', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @method_decorator(cache_page(30))
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super(AdViewSet, self).dispatch(*args, **kwargs)


class UserFavouriteAdFilter(filters.FilterSet):
    class Meta:
        model = UserFavouriteAd
        fields = {
            'user__username': ['icontains'],
            'ad__title': ['icontains'],
        }


class UserFavouriteAdViewSet(viewsets.ModelViewSet):
    """
       API endpoint that modify the favourite ad of the user instance

       retrieve:
       API endpoint that return the given favourite ad of the user.

       list:
       API endpoint that return a list of all the existing favourite ads of the users.

       create:
       API endpoint that create a new favourite ad of the user instance.

       update:
       API endpoint that update the favourite ad of the user instance.

       delete:
       API endpoint that delete the favourite ad of the user instance.

    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = UserFavouriteAd.objects.all()
    serializer_class = UserFavouriteAdSerializer
    filterset_class = UserFavouriteAdFilter


class ImageFilter(filters.FilterSet):
    class Meta:
        model = Image
        fields = {
            'ad__title': ['icontains'],
        }


class ImageViewSet(viewsets.ModelViewSet):
    """
       API endpoint that modify the image instance

       retrieve:
       API endpoint that return the given image.

       list:
       API endpoint that return a list of all the existing images.

       create:
       API endpoint that create a new image instance.

       update:
       API endpoint that update the image instance.

       delete:
       API endpoint that delete the image instance.

    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_class = ImageFilter


class ChatMessageFilter(filters.FilterSet):
    class Meta:
        model = ChatMessage
        fields = {
            'author__username': ['icontains'],
            'ad__title': ['icontains'],
        }


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
       API endpoint that modify the chat message instance

       retrieve:
       API endpoint that return the given chat message.

       list:
       API endpoint that return a list of all the existing chat messages.

       create:
       API endpoint that create a new chat message instance.

       update:
       API endpoint that update the chat message instance.

       delete:
       API endpoint that delete the chat message instance.

    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    filterset_class = ChatMessageFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
