from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
from .models import Category, Ad, Image

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_filter=(
        ('parent', TreeRelatedFieldListFilter),
    )
)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    model = Ad
    list_display = ('title', 'author')
    search_fields = ('title', 'author')
    list_filter = (
        ('category', TreeRelatedFieldListFilter),
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('img', 'ad')
    list_filter = ('ad__category__name',)
    search_fields = ('img',)
