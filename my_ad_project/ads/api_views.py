from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, CategorySerializer, AdSerializer, UserFavouriteAdSerializer, \
    ImageSerializer, ChatMessageSerializer
from .models import Category, Ad, UserFavouriteAd, Image, ChatMessage
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows categories to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows ads to be viewed or edited.
    """
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserFavouriteAdViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows favourite ad of user to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = UserFavouriteAd.objects.all()
    serializer_class = UserFavouriteAdSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows favourite ad of user to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows chat message to be viewed or edited.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
