from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView

import json
from main import models
from order.models import ShopCart
from order.views import total_price
from users import models as users_models


# class returns data for the home page.
class HomePageView(TemplateView):

    template_name = 'main/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context["categories"] = models.Category.objects.all()
        context["featured_books"] = models.Book.objects.all().order_by(
            '-Publication_date')[:6]
        context["sales_off_books"] = models.Book.objects.filter(
            discount_price__gt=0).order_by('-Publication_date')[:6]
        context['rate'] = models.Comment.objects.all().order_by()
        context.update(total_price_items(self.request.user.id))
        return context


# class returns data for the books list page.
class FeaturedBooksListView(ListView):

    template_name = 'main/books_list.html'
    model = models.Book
    queryset = models.Book.objects.all().order_by('-Publication_date')
    context_object_name = 'featured_books'
    count = queryset.count()
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super(FeaturedBooksListView,
                        self).get_context_data(*args, **kwargs)
        context['paginate_by'] = self.paginate_by
        context['count'] = self.count
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))
        return context


# class returns data for the books list page (sales off group).
class SalesOffBooksListView(ListView):

    template_name = 'main/books_list.html'
    model = models.Book
    queryset = models.Book.objects.filter(
        discount_price__gt=0).order_by('-Publication_date')
    context_object_name = 'sales_off_books'
    count = queryset.count()
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super(SalesOffBooksListView,
                        self).get_context_data(*args, **kwargs)
        context['paginate_by'] = self.paginate_by
        context['count'] = self.count
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))
        return context


# class returns data for the books list page (a-z).
class AtoZBooksListView(ListView):

    template_name = 'main/books_list.html'
    model = models.Book
    queryset = models.Book.objects.all().order_by('name')
    context_object_name = 'A_Z_books'
    count = queryset.count()
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super(AtoZBooksListView, self).get_context_data(
            *args, **kwargs)
        context['paginate_by'] = self.paginate_by
        context['count'] = self.count
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))
        return context


# class returns data for the books list page(z-a).
class ZtoABooksListView(ListView):

    template_name = 'main/books_list.html'
    model = models.Book
    queryset = models.Book.objects.all().order_by('-name')
    context_object_name = 'Z_A_books'
    count = queryset.count()
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super(ZtoABooksListView, self).get_context_data(
            *args, **kwargs)
        context['paginate_by'] = self.paginate_by
        context['count'] = self.count
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))
        return context


# class returns data for the categories list page.
class CategoriesListView(TemplateView):

    template_name = 'main/types_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoriesListView, self).get_context_data(
            *args, **kwargs)
        context['categories_list'] = 'Categories'
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))
        return context


# class returns data for the languages list page.
class LanguagesListView(TemplateView):

    template_name = 'main/types_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LanguagesListView, self).get_context_data(
            *args, **kwargs)
        context['languages_list'] = 'Languages'
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))
        return context


# class returns data for the years list page.
class YearsListView(TemplateView):

    template_name = 'main/types_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(YearsListView, self).get_context_data(
            *args, **kwargs)
        context['years_list'] = 'Years'
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))
        return context


# class returns data for the authors list page.
class AuthorsListView(TemplateView):

    template_name = 'main/types_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorsListView, self).get_context_data(
            *args, **kwargs)
        context['authors_list'] = 'Authors'
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))
        return context


# class for the search engine in the home page
class SearchView(TemplateView):

    def get(self, request, *args, **kwargs):
        text_before = request.GET['search_text']
        if '(Author)' in text_before or '(Book)' in text_before or '(Category)' in text_before or '(Language)' in text_before or '(Year)' in text_before:
            text = self.strip_text(text_before)
        else:
            text = text_before

        search_results = []
        author_name = models.Author.objects.filter(Q(name__icontains=text))
        category_name = models.Category.objects.filter(Q(name__icontains=text))
        language_name = models.Language.objects.filter(Q(name__icontains=text))
        year_name = models.Year.objects.filter(Q(name__icontains=text))
        if text:
            if author_name:
                search_results = models.Book.objects.filter(
                    authors=author_name[0])
            elif category_name:
                search_results = models.Book.objects.filter(
                    categories=category_name[0])
            elif language_name:
                search_results = models.Book.objects.filter(
                    language=language_name[0])
            elif year_name:
                search_results = models.Book.objects.filter(
                    year=year_name[0])
            else:
                search_results = models.Book.objects.filter(
                    Q(name__icontains=text))
        context = {
            'search_results': search_results,
            'text': text,
        }
        context.update(left_filter())
        context.update(total_price_items(self.request.user.id))

        return render(request, 'main/books_list.html', context)

    def strip_text(self, text_before):
        text = ''
        for word in text_before.split()[0:len(text_before.split())-1]:
            text = text + word + ' '
        return text.strip(' ')


# function to display the details of a specific movie.
def book_details_view(request, slug):

    book_slug = models.Book.objects.filter(slug__iexact=slug)
    slug = check_on_slug(book_slug)
    if slug is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    def rating_average(slug):
        sum, avg, count = 0, 0, 0
        all_rates = models.Comment.objects.filter(book=slug).values('rating')
        for rate in all_rates:
            sum += rate['rating']
            count += 1
        if sum == 0 and count == 0:
            rating_average = 0.1
        else:
            rating_average = sum/count
        return round(rating_average, 1)

    def related_books(slug):
        books = models.Book.objects.filter(name=slug).values('authors__name')
        books_for_author = models.Book.objects.filter(authors__name='')
        for author in books:
            books_author = models.Book.objects.filter(
                ~Q(name=slug), authors__name=author["authors__name"])
            books_for_author = books_for_author | books_author
        related_books = books_for_author.distinct()
        return related_books

    def rating_system(slug):
        rate_system = {}
        count = 0
        rate_system['star1'] = models.Comment.objects.filter(
            book=slug, rating='1').count()
        rate_system['star2'] = models.Comment.objects.filter(
            book=slug, rating='2').count()
        rate_system['star3'] = models.Comment.objects.filter(
            book=slug, rating='3').count()
        rate_system['star4'] = models.Comment.objects.filter(
            book=slug, rating='4').count()
        rate_system['star5'] = models.Comment.objects.filter(
            book=slug, rating='5').count()
        count = sum(rate_system.values())
        if count == 0:
            rate_system['count'] = 0
        else:
            rate_system['count'] = float(100/count)
        return(rate_system)

    user_comment = ''
    comments_count = 0
    if request.user.is_authenticated:
        book_comments = models.Comment.objects.filter(
            ~Q(user_id=request.user), book=slug).order_by('-create_at')
        user_comment = models.Comment.objects.filter(
            user_id=request.user, book=slug)
        comments_count = user_comment.count() + book_comments.count()
    else:
        book_comments = models.Comment.objects.filter(
            book=slug).order_by('-create_at')
        comments_count = book_comments.count()

    profiles = users_models.Profile.objects.all()
    context = {
        'book_details': slug,
        'book_comments': book_comments,
        'user_comment': user_comment,
        'comments_count': comments_count,
        'related_books': related_books(slug),
        'rating_average': rating_average(slug),
        'rating_system': rating_system(slug),
        'profiles': profiles,
    }

    context.update(left_filter())
    context.update(total_price_items(request.user.id))

    return render(request, 'main/book_details.html', context)


# function to display all books of a specific category.
def category_books_list(request, slug):

    category_slug = models.Category.objects.filter(slug__iexact=slug)
    slug = check_on_slug(category_slug)
    if slug is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    category_books = models.Book.objects.filter(
        categories=slug)

    context = {
        'category_books': category_books,
        'category': category_slug[0],
        'books_paginator': paginate_view(request, category_books)
    }

    context.update(left_filter())
    context.update(total_price_items(request.user.id))
    return render(request, 'main/books_list.html', context)


# function to display all books of a specific language.
def language_books_list(request, slug):

    language_slug = models.Language.objects.filter(slug__iexact=slug)
    slug = check_on_slug(language_slug)
    if slug is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    language_books = models.Book.objects.filter(
        language=slug)

    context = {
        'language_books': language_books,
        'language': language_slug[0],
        'books_paginator': paginate_view(request, language_books)
    }

    context.update(left_filter())
    context.update(total_price_items(request.user.id))
    return render(request, 'main/books_list.html', context)


# function to display all books of a specific author.
def author_books_list(request, slug):

    author_slug = models.Author.objects.filter(slug__iexact=slug)
    slug = check_on_slug(author_slug)
    if slug is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    author_books = models.Book.objects.filter(
        authors=slug)

    context = {
        'author_books': author_books,
        'author': author_slug[0],
        'books_paginator': paginate_view(request, author_books)
    }
    context.update(left_filter())
    context.update(total_price_items(request.user.id))
    return render(request, 'main/books_list.html', context)


# function to display all books of a specific year.
def year_books_list(request, slug):

    year_slug = models.Year.objects.filter(slug__iexact=slug)
    slug = check_on_slug(year_slug)
    if slug is None:
        return HttpResponse('<h1>Post Not Found</h1>')

    year_books = models.Book.objects.filter(year=slug)

    context = {
        'year_books': year_books,
        'year': year_slug[0],
        'books_paginator': paginate_view(request, year_books)
    }

    context.update(left_filter())
    context.update(total_price_items(request.user.id))
    return render(request, 'main/books_list.html', context)


@login_required(login_url='/users/login', redirect_field_name='/')
# function to display all favourite books for a specific user.
def favourite_books_list(request, slug):

    favourite_books = models.Book.objects.filter(
        favourite=request.user.id)
    context = {
        'favourites': 'exist',
        "favourite_books": favourite_books,
        'books_paginator': paginate_view(request, favourite_books)
    }

    context.update(left_filter())
    context.update(total_price_items(request.user.id))
    return render(request, 'main/books_list.html', context)


@login_required(login_url='/users/login', redirect_field_name='/')
# function to display all comments for a specific user.
def user_comments_list(request):

    user_comments = models.Comment.objects.filter(
        user_id=request.user.id).order_by('-create_at')

    context = {
        'comments': 'exist',
        "user_comments": user_comments,
    }
    context.update(total_price_items(request.user.id))
    return render(request, 'main/comments.html', context)


# function to add a comment to a specific movie page.
@login_required(login_url='/users/login', redirect_field_name='/')
def comment_add(request, proid):

    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':

        form = models.CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = models.Comment()
            data.book_id = proid
            data.user_id = current_user.id
            data.message = form.cleaned_data['message']
            data.rating = form.cleaned_data['rating']
            data.save()
            messages.success(
                request, "Your review has been sent. Thank You for your interest.")
            return HttpResponseRedirect(url)
        else:
            messages.warning(
                request, "Your review has not been sent")
            return redirect(url)
    else:
        return HttpResponseRedirect(url)


# function to add a comment to a specific movie page.
@login_required(login_url='/users/login', redirect_field_name='/')
def delete_comment(request, proid):

    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    book_name = models.Comment.objects.filter(
        user_id=current_user.id, id=proid)[0]
    models.Comment.objects.filter(user_id=current_user.id, id=proid).delete()
    messages.success(
        request, f"Your comment on '{book_name}' has been deleted.")
    return HttpResponseRedirect(url)


# function to let the user add any book to thier favourites page.
@login_required(login_url='/users/login', redirect_field_name='/')
def favourite_book_add(request, proid):

    url = request.META.get('HTTP_REFERER')
    book = get_object_or_404(models.Book, id=proid)
    if book.favourite.filter(id=request.user.id).exists():
        book.favourite.remove(request.user)
        messages.warning(request, f'{book.name} removed from favourites.')
    else:
        book.favourite.add(request.user)
        messages.success(request, f'{book.name} added to favourites.')

    return HttpResponseRedirect(url)


# function to check if the slug is exist and return none if not.
def check_on_slug(slug):

    if slug.exists():
        slug = slug.first()
        return slug
    else:
        return None


# function returns (all categories, all authors, all languages, all years).
def left_filter():

    context = {}

    def category_books():
        dic_category = {}
        for category in models.Category.objects.all().order_by('name'):
            dic_category[category] = models.Book.objects.filter(
                categories=category).count()
        return dic_category

    def language_books():
        dic_language = {}
        for language in models.Language.objects.all().order_by('name'):
            dic_language[language] = models.Book.objects.filter(
                language=language).count()
        return dic_language

    def author_books():
        dic_author = {}
        for author in models.Author.objects.all().order_by('name'):
            dic_author[author] = models.Book.objects.filter(
                authors=author).count()
        return dic_author

    def year_books():
        dic_year = {}
        for year in models.Year.objects.all().order_by('-name'):
            dic_year[year] = models.Book.objects.filter(
                year=year).count()
        return dic_year

    context["categories"] = category_books()
    context["languages"] = language_books()
    context["authors"] = author_books()
    context['years'] = year_books()

    return context


# function for the autocomplete in the search bar.
def autoComplete_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        books = models.Book.objects.filter(name__icontains=q)
        authors = models.Author.objects.filter(name__icontains=q)
        categories = models.Category.objects.filter(name__icontains=q)
        languages = models.Language.objects.filter(name__icontains=q)
        years = models.Year.objects.filter(name__icontains=q)
        results = []
        for book in books:
            book_json = {}
            book_json = book.name + ' (Book)'
            results.append(book_json)
        for author in authors:
            author_json = {}
            author_json = author.name + ' (Author)'
            results.append(author_json)
        for category in categories:
            category_json = {}
            category_json = category.name + ' (Category)'
            results.append(category_json)
        for language in languages:
            language_json = {}
            language_json = language.name + ' (Language)'
            results.append(language_json)
        for year in years:
            year_json = {}
            year_json = year.name + ' (Year)'
            results.append(year_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# function return total price for the specific user and the numbers of the items.
def total_price_items(userid):

    shopcart = ShopCart.objects.filter(user_id=userid)
    context = {
        'shopcart': shopcart,
        'total_price': total_price(shopcart),
        'favourites_count': models.Book.objects.filter(
            favourite=userid).count()
    }
    return context


# function the paginate of the movies.
def paginate_view(request, books):

    page = request.GET.get('page', 1)
    paginator = Paginator(books, 1)
    try:
        books_paginator = paginator.page(page)
    except PageNotAnInteger:
        books_paginator = paginator.page(1)
    except EmptyPage:
        books_paginator = paginator.page(paginator.num_pages)

    return books_paginator
