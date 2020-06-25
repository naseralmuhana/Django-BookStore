from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from django.forms import ModelForm, Textarea
import datetime
from eCommerce.utils import unique_slug_generator


class Category(models.Model):

    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(
        upload_to="categories-img", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Language(models.Model):

    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to="languages-img", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Author(models.Model):

    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to="authors-img", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Year(models.Model):

    name = models.CharField(max_length=4, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to="books-img", blank=True)
    description = models.TextField(null=True, blank=True)
    Publication_date = models.DateField(default='2020-12-31')
    page = models.IntegerField('Pages number', default=100)
    for_age = models.IntegerField('For ages', default=15)
    price = models.FloatField(default=0.0)
    discount_price = models.FloatField(blank=True, null=True)
    authors = models.ManyToManyField(to='Author')
    language = models.ForeignKey(to='Language', on_delete=models.DO_NOTHING)
    categories = models.ManyToManyField(to='Category')
    year = models.ForeignKey(to='Year', on_delete=models.DO_NOTHING)
    favourite = models.ManyToManyField(
        User, related_name='favourite', blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def discount_percent(self):
        discount_precent = int(100 - (self.discount_price / self.price)*100)
        return discount_precent

    def price_difference(self):
        difference = ((self.price - self.discount_price)-1.00)+0.99
        return round(difference, 2)


# function to create a slug using the function (unique_slug_generator) that exist in the module (utils.py)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(create_slug, sender=Category)
pre_save.connect(create_slug, sender=Language)
pre_save.connect(create_slug, sender=Author)
pre_save.connect(create_slug, sender=Book)
pre_save.connect(create_slug, sender=Year)


class Comment(models.Model):

    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    rating = models.IntegerField(choices=RATING, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book.name



# class for the form of the comment section. we can write it in the forms.py or here.
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message', 'rating']
        widgets = {
            'message': Textarea(attrs={'class': 'input'}),
            'rating': Textarea(attrs={'class': 'input'}),
        }
