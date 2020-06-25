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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
