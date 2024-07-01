# main project urls file
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('f/', include('data_fetching_app.urls')),
    path('h/', include('database_handling_app.urls')),
    # path('all/', include('database_handling_app.urls')),
    # path('find/', include('database_handling_app.urls')),
    # path('fetch/', include('data_fetching_app.urls')),
    # path('search/',include('data_fetching_app.urls')),
    # path('single/',include('database_handling_app.urls')),
    # path('actor/',include('data_fetching_app.urls')),
    # path('this/',include('database_handling_app.urls')),
    # path('this/',include('database_handling_app.urls')),
    # path('top/',include('database_handling_app.urls')),
    # path('top/',include('database_handling_app.urls')),


]
