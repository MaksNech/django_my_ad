from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
from .models import Category, Ad, Image, UserFavouriteAd, ChatMessage
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_filter=(
        ('parent', TreeRelatedFieldListFilter),
    )
)


class UserFavouriteAdInline(admin.TabularInline):
    model = UserFavouriteAd
    extra = 1


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 1


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('ad', 'author', 'body',)
    list_filter = ('ad__category__name',)
    search_fields = ('body', 'ad__title', 'ad__description', 'author__username',)


@admin.register(UserFavouriteAd)
class UserFavouriteAdAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user')
    list_filter = ('ad__category__name',)
    search_fields = ('ad__title', 'ad__description', 'ad__category__name', 'user__username')


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    model = Ad
    list_display = ('title', 'author', 'status')
    search_fields = ('title', 'description', 'category__name', 'author__username', 'status')
    list_filter = (
        ('category', TreeRelatedFieldListFilter),
    )
    inlines = (UserFavouriteAdInline, ChatMessageInline)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('img', 'ad')
    list_filter = ('ad__category__name',)
    search_fields = ('img',)


class CustomUserAdmin(UserAdmin):
    inlines = (UserFavouriteAdInline, ChatMessageInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
