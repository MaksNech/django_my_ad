from django.urls import path
from .views import RegisterView, IndexView, AdListView, AdDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', IndexView.as_view(), name='index'),
    path('list/', AdListView.as_view(), name='list'),
    path('<int:pk>/', AdDetailView.as_view(), name='detail'),
]
