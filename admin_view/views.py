from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from main import views as main_views
from main import models as main_models
from admin_view import forms as admin_forms


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Book.
def add_book(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.BookForm(request.POST, request.FILES)
        if form.is_valid():
            add_book_form = form.save(commit=False)
            book_name = form.cleaned_data.get("name")
            add_book_form.save()
            form.save_m2m()
            messages.success(
                request, f"({book_name}) Has Been Added to the Books table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.BookForm()
        context = {
            'form': form,
            'admin_book': 'exist',
            'add_book': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Category.
def add_category(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({category_name}) Has Been Added to the Categories table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.CategoryForm()
        context = {
            'form': form,
            'admin_category': 'exist',
            'add_category': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Author.
def add_author(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            author_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({author_name}) Has Been Added to the Authors table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.AuthorForm()
        context = {
            'form': form,
            'admin_author': 'exist',
            'add_author': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Language.
def add_language(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.LanguageForm(request.POST, request.FILES)
        if form.is_valid():
            language_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({language_name}) Has Been Added to the Languages table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.LanguageForm()
        context = {
            'form': form,
            'admin_language': 'exist',
            'add_language': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to add Year.
def add_year(request):

    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = admin_forms.YearForm(request.POST, request.FILES)
        if form.is_valid():
            year_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({year_name}) Has Been Added to the Years table.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.YearForm()
        context = {
            'form': form,
            'admin_year': 'exist',
            'add_year': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to update book.
def update_book(request, slug):

    url = request.META.get('HTTP_REFERER')
    book = main_models.Book.objects.get(slug=slug)
    if request.method == "POST":
        form = admin_forms.BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({book_name}) Has Been updated.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.BookForm(instance=book)
        context = {
            'form': form,
            'admin_book': 'exist',
            'book_name': book.name,
            'update_book': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to update Category.
def update_category(request, slug):

    url = request.META.get('HTTP_REFERER')
    category = main_models.Category.objects.get(slug=slug)
    if request.method == "POST":
        form = admin_forms.CategoryForm(
            request.POST, request.FILES, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({category_name}) Has Been updated.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.CategoryForm(instance=category)
        context = {
            'form': form,
            'admin_category': 'exist',
            'category_name': category.name,
            'update_category': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to update Author.
def update_author(request, slug):

    url = request.META.get('HTTP_REFERER')
    author = main_models.Author.objects.get(slug=slug)
    if request.method == "POST":
        form = admin_forms.AuthorForm(
            request.POST, request.FILES, instance=author)
        if form.is_valid():
            author_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({author_name}) Has Been updated.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.AuthorForm(instance=author)
        context = {
            'form': form,
            'admin_author': 'exist',
            'author_name': author.name,
            'update_author': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to update Language.
def update_language(request, slug):

    url = request.META.get('HTTP_REFERER')
    language = main_models.Language.objects.get(slug=slug)
    if request.method == "POST":
        form = admin_forms.LanguageForm(
            request.POST, request.FILES, instance=language)
        if form.is_valid():
            language_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({language_name}) Has Been updated.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.LanguageForm(instance=language)
        context = {
            'form': form,
            'admin_language': 'exist',
            'language_name': language.name,
            'update_language': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to update Year.
def update_year(request, slug):

    url = request.META.get('HTTP_REFERER')
    year = main_models.Year.objects.get(slug=slug)
    if request.method == "POST":
        form = admin_forms.YearForm(
            request.POST, request.FILES, instance=year)
        if form.is_valid():
            year_name = form.cleaned_data.get("name")
            form.save()
            messages.success(
                request, f"({year_name}) Has Been updated.")
            return HttpResponseRedirect(url)
    else:
        form = admin_forms.YearForm(instance=year)
        context = {
            'form': form,
            'admin_year': 'exist',
            'year_name': year.name,
            'update_year': 'exist',
        }
        context.update(main_views.total_price_items(request.user.id))
        return render(request, "admin/add_record.html", context)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to delete Book.
def delete_book(request, slug):
    url = request.META.get('HTTP_REFERER')
    book_name = main_models.Book.objects.filter(
        slug=slug)[0]
    main_models.Book.objects.filter(slug=slug).delete()
    messages.warning(
        request, f"'{book_name}' has been deleted.")
    return HttpResponseRedirect(url)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to delete Category.
def delete_category(request, slug):
    url = request.META.get('HTTP_REFERER')
    category_name = main_models.Category.objects.filter(
        slug=slug)[0]
    main_models.Category.objects.filter(slug=slug).delete()
    messages.warning(
        request, f"'{category_name}' has been deleted.")
    return HttpResponseRedirect(url)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to delete Author.
def delete_author(request, slug):
    url = request.META.get('HTTP_REFERER')
    author_name = main_models.Author.objects.filter(
        slug=slug)[0]
    main_models.Author.objects.filter(slug=slug).delete()
    messages.warning(
        request, f"'{author_name}' has been deleted.")
    return HttpResponseRedirect(url)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to delete Language.
def delete_language(request, slug):
    url = request.META.get('HTTP_REFERER')
    language_name = main_models.Language.objects.filter(
        slug=slug)[0]
    main_models.Language.objects.filter(slug=slug).delete()
    messages.warning(
        request, f"'{language_name}' has been deleted.")
    return HttpResponseRedirect(url)


@user_passes_test(lambda u: u.is_superuser)
# forms for the admin, if he want to delete year.
def delete_year(request, slug):
    url = request.META.get('HTTP_REFERER')
    year_name = main_models.Year.objects.filter(slug=slug)[0]
    main_models.Year.objects.filter(slug=slug).delete()
    messages.warning(
        request, f"'{year_name}' has been deleted.")
    return HttpResponseRedirect(url)
