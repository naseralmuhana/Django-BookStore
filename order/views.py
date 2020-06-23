from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from order import models
from main import views
from users import models as users_models


@login_required(login_url='/users/login')
def shoping_cart(request):

    context = {
        'shopcart_page': 'exist',
    }
    context.update(views.total_price_items(request.user.id))
    return render(request, 'order/shoping_cart.html', context)


def total_price(shopcart):

    total_price = 0
    for book_in_cart in shopcart:
        if book_in_cart.book.discount_price:
            total_price += book_in_cart.quantity * book_in_cart.book.discount_price
        else:
            total_price += book_in_cart.quantity * book_in_cart.book.price
    return round(total_price, 2)


@login_required(login_url='/users/login', redirect_field_name='/')
def shop_cart_add(request, id):

    # if this is a POST request we need to process the form data
    url = request.META.get('HTTP_REFERER')
    current_user = request.user  # Get User id
    # Checking product in ShopCart
    try:
        q1 = models.ShopCart.objects.get(
            user_id=current_user.id, book_id=id)
    except models.ShopCart.DoesNotExist:
        q1 = None

    if request.method == 'POST':
        form = models.ShopCartForm(request.POST)
        if form.is_valid():  # check whether it's valid:

            # get product quantity from form
            quantity = form.cleaned_data['quantity']

            if q1 != None:  # Update  quantity to exist product quantity
                q1.quantity = q1.quantity + quantity
                q1.save()
                messages.success(
                    request, f'{q1.book.name} added to cart. (quantities = {quantity})')

            else:  # Add new item to shop cart
                data = models.ShopCart(
                    user_id=current_user.id, book_id=id, quantity=quantity)
                data.save()
                messages.success(
                    request, f'{data.book.name} added to cart. (quantities = {quantity})')

            # request.session['cart_items'] = models.ShopCart.objects.filter(user_id=current_user.id).count() #Count item in shop cart

    else:
        if q1 != None:  # Update  quantity to exist product quantity
            q1.quantity += 1
            q1.save()
            messages.success(request, f'{q1.book.name} added to cart.')
        else:  # Add new item to shop cart
            data = models.ShopCart(
                user_id=current_user.id, book_id=id, quantity=1)
            data.save()
            messages.success(request, f'{data.book.name} added to cart.')

    return HttpResponseRedirect(url)


@login_required(login_url='/users/login')
def update_quantity(request, id):

    # if this is a POST request we need to process the form data
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = models.ShopCartForm(request.POST)
        if form.is_valid():  # check whether it's valid:

            # get product quantity from form
            quantity = form.cleaned_data['quantity']
            current_user = request.user  # Get User id
            q1 = models.ShopCart.objects.get(
                user_id=current_user.id, book_id=id)
            if q1 != None:  # Update  quantity to exist product quantity
                new_quantity = quantity - q1.quantity
                q1.quantity = q1.quantity + new_quantity
                q1.save()
            # request.session['cart_items'] = models.ShopCart.objects.filter(user_id=current_user.id).count() #Count item in shop cart
            messages.success(
                request, f"{q1.book.name} quantity has been updated.")
    return HttpResponseRedirect(url)


@login_required(login_url='/users/login')
def shop_cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')
    book_name = models.ShopCart.objects.filter(id=id)[0]
    models.ShopCart.objects.filter(id=id).delete()
    messages.success(request, f"{book_name} has been deleted from cart. ")
    return HttpResponseRedirect(url)


@login_required(login_url='/users/login')
def checkout(request):

    current_user = request.user
    shopcart = models.ShopCart.objects.all().filter(user_id=current_user.id)
    profiles = users_models.Profile.objects.filter(user_id=request.user.id)
    total_cart = 0

    for bk_cart in shopcart:
        if bk_cart.book.discount_price:
            total_cart += bk_cart.quantity * bk_cart.book.discount_price
        else:
            total_cart += bk_cart.quantity * bk_cart.book.price
    total_cart = round(total_cart, 2)

    if request.method == 'POST':
        form = models.OrderForm(request.POST or None)

        # check whether it's valid:
        if form.is_valid():

            data = models.Order()
            # get product quantity from form
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.zip_code = form.cleaned_data['zip_code']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.note = form.cleaned_data['note']

            data.user_id = current_user.id
            data.total = total_cart
            data.save()

            # Save Shopcart items to Order detail items
            for bk_cart in shopcart:
                detail = models.OrderDetail()
                detail.order_id = data.id  # Order Id
                detail.book_id = bk_cart.book_id
                detail.user_id = current_user.id
                detail.quantity = bk_cart.quantity
                if bk_cart.book.discount_price:
                    detail.price = bk_cart.book.discount_price
                else:
                    detail.price = bk_cart.book.price
                detail.total = bk_cart.amount
                detail.save()
            # Clear & Delete shopcart
            models.ShopCart.objects.filter(user_id=current_user.id).delete()
            messages.success(
                request, f"Thank for Providing Your Info, Mr.{request.user.username}. Your order has been completed. We will contact with you based on your info below.")
            return redirect("order:checkout_complete", id=data.id)

    context = {
        'profiles': profiles,
        'checkout_page': 'exist',
    }
    context.update(views.total_price_items(request.user.id))
    return render(request, 'order/checkout.html', context)


@login_required(login_url='/users/login')
def checkout_complete(request, id):
    order_details = models.Order.objects.filter(id=id)[0]
    order_book_details = models.OrderDetail.objects.filter(order_id=id)
    profiles = users_models.Profile.objects.filter(user_id=request.user.id)
    context = {
        'order_details': order_details,
        'order_book_details': order_book_details,
        'profiles': profiles,
        'checkout_complete_page': 'exist',
    }
    context.update(views.total_price_items(request.user.id))
    return render(request, 'order/checkout_complete.html', context)


@login_required(login_url='/login')
def orders_list(request):

    orders = models.Order.objects.filter(
        user_id=request.user.id).order_by('-create_at')

    context = {
        'orders': orders,
    }
    context.update(views.total_price_items(request.user.id))
    return render(request, 'order/orders_list.html', context)
