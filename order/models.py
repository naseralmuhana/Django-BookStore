from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput

from main.models import Book


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.book.name

    @property
    def amount(self):
        if self.book.discount_price:
            return round((self.quantity * self.book.discount_price), 2)
        return round((self.quantity * self.book.price), 2)


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=8, blank=True)
    total = models.FloatField()
    note = models.TextField(null=True, default="", blank=True)
    status = models.CharField(choices=STATUS, default='New', max_length=15)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class OrderForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['note'].required = False

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'address', 'city', 'country', 'zip_code', 'note']
        widgets = {
            'first_name': TextInput(attrs={'class': 'input'}),
            'last_name': TextInput(attrs={'class': 'input'}),
            'email': TextInput(attrs={'class': 'input'}),
            'phone': TextInput(attrs={'class': 'input'}),
            'address': TextInput(attrs={'class': 'input'}),
            'city': TextInput(attrs={'class': 'input'}),
            'country': TextInput(attrs={'class': 'input'}),
            'zip_code': TextInput(attrs={'class': 'input'}),
            'note': TextInput(attrs={'class': 'input'}),
        }


class OrderDetail(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book.name
