from django.urls import path
from .views import RegisterView, IndexView, AdListView, AdDetailView, ad_create, ad_edit, AdDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', IndexView.as_view(), name='index'),
    path('list/', AdListView.as_view(), name='list'),
    path('<int:pk>/', AdDetailView.as_view(), name='detail'),
    path('create/', ad_create, name='create'),
    path('edit/<int:ad_id>/', ad_edit, name='edit'),
    path('delete/<int:pk>/', AdDeleteView.as_view(), name='delete'),
]
