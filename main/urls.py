from django.urls import path
from main import views
from django.conf.urls.static import static
from eCommerce import settings

app_name = 'main'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),

    path('featured-books', views.FeaturedBooksListView.as_view(), name='featured_books_list'),
    path('sales-off-books', views.SalesOffBooksListView.as_view(), name='sales_off_books_list'),
    path('A-Z-books', views.AtoZBooksListView.as_view(), name='a_z_books_list'),
    path('Z-A-books', views.ZtoABooksListView.as_view(), name='z_a_books_list'),

    path('categories', views.CategoriesListView.as_view(), name='categories_list'),
    path('languages', views.LanguagesListView.as_view(), name='languages_list'),
    path('years', views.YearsListView.as_view(), name='years_list'),
    path('authors', views.AuthorsListView.as_view(), name='authors_list'),
    path('favourites/<slug>', views.favourite_books_list, name="favourite_books_list"),
    path('user-comments/', views.user_comments_list, name="user_comments_list"),

    path('categories/<slug>', views.category_books_list, name='category_books_list'),
    path('languages/<slug>', views.language_books_list, name='language_books_list'),
    path('authors/<slug>', views.author_books_list, name='author_books_list'),
    path('years/<slug>', views.year_books_list, name='year_books_list'),

    path('books/<slug>', views.book_details_view, name='book_details'),

    path('search/', views.SearchView.as_view(), name='search'),
    path('autoComplete-search/', views.autoComplete_search, name='autoComplete_search'),

    path('add-comment/<int:proid>', views.comment_add, name="add_comment"),
    path('delete-comment/<int:proid>', views.delete_comment, name="delete_comment"),
    path('favourite-books-add/<int:proid>', views.favourite_book_add, name="favourite_book_add"),

    #for admin
    path('add-book', views.add_book, name="add_book"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
