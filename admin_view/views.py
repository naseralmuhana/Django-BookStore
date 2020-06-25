from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from main import views as main_views
from admin_view import forms as admin_forms


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Book.
def add_book(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            add_book_form = form.save(commit=False)
            book_name = form.cleaned_data.get("name")
            add_book_form.save()
            form.save_m2m()
            messages.success(
                request, f"({book_name}) Has Been Added to the Books table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.AddBookForm()
        context = {
            'form': form,
            'add_book': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Category.
def add_category(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.AddCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({category_name}) Has Been Added to the Categories table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.AddCategoryForm()
        context = {
            'form': form,
            'add_category': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Author.
def add_author(request):
    
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.AddAuthorForm(request.POST, request.FILES)
        if form.is_valid():
            author_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({author_name}) Has Been Added to the Authors table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.AddAuthorForm()
        context = {
            'form': form,
            'add_author': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Language.
def add_language(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.AddLanguageForm(request.POST, request.FILES)
        if form.is_valid():
            language_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({language_name}) Has Been Added to the Languages table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.AddLanguageForm()
        context = {
            'form': form,
            'add_language': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Year.
def add_year(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.AddYearForm(request.POST, request.FILES)
        if form.is_valid():
            year_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({year_name}) Has Been Added to the Years table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.AddYearForm()
        context = {
            'form': form,
            'add_year': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)
