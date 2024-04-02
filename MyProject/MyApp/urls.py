from django.urls import path
from MyApp import views
urlpatterns = [
    path('authors', views.authors),
    path('sellers', views.sellers),
]
