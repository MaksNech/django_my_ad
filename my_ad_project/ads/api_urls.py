from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken import views as authtoken_views
from .api_views import UserViewSet, GroupViewSet, CategoryViewSet, AdViewSet, UserFavouriteAdViewSet, ImageViewSet, \
    ChatMessageViewSet

schema_view = get_swagger_view(title='My Ad API')

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'ads', AdViewSet)
router.register(r'user_favourite_ad', UserFavouriteAdViewSet)
router.register(r'images', ImageViewSet)
router.register(r'chat_messages', ChatMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view),
    path('rest-auth/', include('rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', authtoken_views.obtain_auth_token, name='api-token-auth'),
]
