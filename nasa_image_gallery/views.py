# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request, 'registration/login.html')

def logout_page(request):
    return render(request, 'index.html/accounts/logout')
    

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    
    images = services_nasa_image_gallery.getAllImages(input=None)
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return images, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].

    images, favourite_list = getAllImagesAndFavouriteList(request)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


# Función utilizada en el buscador.
def search(request):
    # Obtiene todas las imágenes y la lista de favoritos.
    images, favourite_list = getAllImagesAndFavouriteList(request)

    # Obtiene el mensaje de búsqueda desde la solicitud POST.
    search_msg = request.POST.get('query', '').lower()

    if search_msg:
        # Filtra las imágenes de NASACard que contienen el texto de búsqueda en el título o descripción.
        filtered_images = [
            image for image in images
            if search_msg in image.title.lower() or search_msg in image.description.lower()
        ]
    else:
        search_msg = "moon"
        # Si no hay texto de búsqueda, se filtran las imágenes con la palabra "moon".
        filtered_images = [
            image for image in images
            if search_msg in image.title.lower() or search_msg in image.description.lower()
        ]

    # Renderiza la plantilla 'home.html' con las imágenes filtradas y la lista de favoritos.
    return render(request, 'home.html', {'images': filtered_images, 'favourite_list': favourite_list})
    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    pass


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    services_nasa_image_gallery.saveFavourite(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
    

@login_required
def deleteFavourite(request):
     services_nasa_image_gallery.deleteFavourite(request)
     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

