from django.urls import path
from MyApp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('authors', views.authors),
    path('sellers', views.sellers),
    path('upload_book/', views.upload_book, name='upload_book'),
    path('view_book/',views.view_book,name="view_book"),
    path('view_user_books/',views.view_user_books,name="view_user_books"),
    path('fetch_data/',views.fetch_data,name="fetch_data")
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
