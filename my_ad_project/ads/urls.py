from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list/', AdListView.as_view(), name='list'),
    path('<int:pk>/', AdDetailView.as_view(), name='detail'),
]
