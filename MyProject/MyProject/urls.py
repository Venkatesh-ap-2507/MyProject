
from django.contrib import admin
from django.urls import path,include
from MyApp import views as MyApp
from api import views as api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("",MyApp.register,name="register"),
    path("login/",MyApp.login,name="login"),
    path("home/", MyApp.home, name="home"),
    path("logout/", MyApp.logout_page, name="logout"),
    path('app/', include("MyApp.urls")),
    path('api/', include("api.urls")),
    # path('authors', MyApp.authors),
    # path('sellers', MyApp.sellers),
    # path('upload_book/', MyApp.upload_book, name='upload_book'),
    # path('view_book/',MyApp.view_book,name="view_book"),
    # path('view_user_books/',MyApp.view_user_books,name="view_user_books"),
    # path('fetch_data/',MyApp.fetch_data,name="fetch_data"),
    path('logout/', MyApp.logout_view, name='logout'),
   

   #api
    path("reg/", MyApp.RegisterView.as_view(), name="reg"),
    path("log/", MyApp.LoginView.as_view(), name='log'),
    path("user/", MyApp.UserView.as_view(), name='user'),
    path('upload/', MyApp.BookUploadAPIView.as_view(), name='book_upload'),
    # path('api-token-auth/', genrate_jwt_token.as_view())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
