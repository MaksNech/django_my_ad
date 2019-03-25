from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from django.contrib.auth.models import User, Group
from .models import Category, Ad, UserFavouriteAd, Image, ChatMessage


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.ListSerializer(source="children", child=RecursiveField())

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'subcategories')


class AdSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=False, required=True)

    class Meta:
        model = Ad
        fields = ('id', 'title', 'category', 'description', 'img_count', 'price', 'negotiable_price', 'author', 'users',
                  'status', 'created_on', 'updated_on')


class UserFavouriteAdSerializer(serializers.ModelSerializer):
    ad = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all(), allow_null=False, required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=False, required=True)

    class Meta:
        model = UserFavouriteAd
        fields = ('id', 'ad', 'user', 'created_on')


class ImageSerializer(serializers.ModelSerializer):
    ad = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all(), allow_null=False, required=True)

    class Meta:
        model = Image
        fields = ('id', 'img', 'ad', 'created_on')


class ChatMessageSerializer(serializers.ModelSerializer):
    ad = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all(), allow_null=False, required=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = ChatMessage
        fields = ('id', 'ad', 'body', 'author')
