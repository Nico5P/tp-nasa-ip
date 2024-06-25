from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('login/', views.login_page, name='login'),
    path('', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('buscar/', views.search, name='buscar'),
    path('accounts/', include('django.contrib.auth.urls')),
    

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

]