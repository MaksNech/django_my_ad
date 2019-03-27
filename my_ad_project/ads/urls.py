from django.urls import path
from .views import RegisterView, IndexView, AdListView, ad_detail, ad_create, ad_edit, AdDeleteView, \
    permission_denied

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('permission_denied/', permission_denied, name='permission_denied'),
    path('', IndexView.as_view(), name='index'),
    path('list/', AdListView.as_view(), name='list'),
    path('<slug:ad_slug>/', ad_detail, name='detail'),
    path('create/', ad_create, name='create'),
    path('edit/<int:ad_id>/', ad_edit, name='edit'),
    path('delete/<int:pk>/', AdDeleteView.as_view(), name='delete'),
]
