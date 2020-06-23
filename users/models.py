from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

from eCommerce.utils import unique_profile_slug_generator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=150, blank=True)
    zip_code = models.CharField(max_length=8, blank=True)
    city = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    image = models.ImageField(upload_to='profile_img', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def name(self):
        return self.user.username


def create_profile_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_profile_slug_generator(instance)


pre_save.connect(create_profile_slug, sender=Profile)
