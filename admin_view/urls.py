from django.urls import path
from admin_view import views 
from django.conf.urls.static import static
from eCommerce import settings

app_name = 'admin_view'

urlpatterns = [
    path('add-book', views.add_book, name="add_book"),
    path('add-category', views.add_category, name="add_category"),
    path('add-auhtor', views.add_author, name="add_author"),
    path('add-language', views.add_language, name="add_language"),
    path('add-year', views.add_year, name="add_year"),

    path('update-book/<slug>', views.update_book, name="update_book"),
    path('update-category/<slug>', views.update_category, name="update_category"),
    path('update-auhtor/<slug>', views.update_author, name="update_author"),
    path('update-language/<slug>', views.update_language, name="update_language"),
    path('update-year/<slug>', views.update_year, name="update_year"),

    path('delete-book/<slug>', views.delete_book, name="delete_book"),
    path('delete-category/<slug>', views.delete_category, name="delete_category"),
    path('delete-auhtor/<slug>', views.delete_author, name="delete_author"),
    path('delete-language/<slug>', views.delete_language, name="delete_language"),
    path('delete-year/<slug>', views.delete_year, name="delete_year"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
