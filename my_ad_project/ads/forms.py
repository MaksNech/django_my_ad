from django.forms import ModelForm
from .models import Ad, Image, UserFavouriteAd, ChatMessage


class AdCreateForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'category', 'description', 'price', 'negotiable_price']


class ImageCreateForm(ModelForm):
    class Meta:
        model = Image
        fields = ['img', 'ad']


class UserFavouriteAdCreateForm(ModelForm):
    class Meta:
        model = UserFavouriteAd
        fields = ['ad', 'user']


class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['ad', 'author', 'body']
