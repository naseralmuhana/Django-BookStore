from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('add-to-cart/<int:id>', views.shop_cart_add, name='add_to_cart'),
    path('shoping-cart', views.shoping_cart, name='shoping_cart'),
    path('delete-from-cart/<int:id>', views.shop_cart_delete, name='delete_from_cart'),
    path('update-quantity/<int:id>', views.update_quantity, name='update_quantity'),
    path('checkout', views.checkout, name='checkout'),
    path('checkout-complete/<int:id>', views.checkout_complete, name='checkout_complete'),
    path('orders-list', views.orders_list, name='orders_list'),
    ]