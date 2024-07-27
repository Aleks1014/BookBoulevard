import datetime
import time

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=70)
    picture = models.ImageField(upload_to='author/', blank=True)
    social_media = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Publisher(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Product(models.Model):
    formats = {
        'PB': 'Paperback',
        'HC': 'Hardcover',
        'EB': 'E-book'
    }
    title = models.CharField(max_length=150)
    description = models.TextField()
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField()
    cover = models.ImageField(upload_to='cover/')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    format = models.CharField(max_length=2, choices=formats)
    pages = models.IntegerField()
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name_plural = 'products Inventory'



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rate = models.FloatField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} - {self.rate} - {self.name}"

