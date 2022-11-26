from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('vendors', views.get_all_vendors),
    path('vendor/<int:id>', views.get_single_vendor),
    path('vendor/<int:id>/toggle-fav', views.toggle_favorite),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
