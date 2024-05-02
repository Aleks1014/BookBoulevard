import time

from django.db import models
from django.utils import timezone

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
    STAR_RATING = {
        '1': 'One star',
        '1.5': 'One and a half star',
        '2': 'Two stars',
        '2.5': 'Two and a half stars',
        '3': 'Three stars',
        '3.5': 'Three and a half stars',
        '4': 'Four stars',
        '4.5': 'Four and a half stars',
        '5': 'Five stars',
        '5.5': 'Five and a half stars',
    }
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stars = models.DecimalField(choices=STAR_RATING, decimal_places=1, max_digits=2)
    review = models.CharField(max_length=350)
    date = models.DateTimeField(timezone.now())





