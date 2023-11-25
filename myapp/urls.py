# myapp/urls.py
from django.urls import path
from .views import search_places

urlpatterns = [
    path('search/', search_places, name='search_places'),
]
