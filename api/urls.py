from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('vendors', views.get_all_vendors),
    path('vendor/<int:id>', views.get_single_vendor),
    path('trees', views.get_all_basetrees),
    path('trees/<str:space>', views.get_basetrees_with_space),
    path('tree/<int:id>', views.get_single_basetree),
    path('add_tree', views.add_tree),
    path('user/<int:user_id>/trees', views.get_trees_of_user)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
