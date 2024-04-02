from django.urls import path
from author_sellers import views
urlpatterns = [
    path('authors_sellers',views.author_and_sellers),
]