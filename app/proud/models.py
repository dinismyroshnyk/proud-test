import uuid

from django.db import models
from django.contrib.auth.hashers import make_password
from django import forms


class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    type = models.IntegerField(choices=[
        (1, 'admin'),
        (2, 'cliente'),
        (3, 'membro')
    ], default=2)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    nationality = models.CharField(max_length=100, null=True)
    request_membership = models.BooleanField(default=False)
    phone = models.CharField(max_length=9, null=True)
    state = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.email


class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    payment_method = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Compra de {self.buyer} no valor de {self.price} em {self.date}"


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Newsletter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    status = models.BooleanField(default=True)


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField()
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Product(models.Model):

    PRODUCT_TYPES = [
        (1, 'CLOTHES'),
        (2, 'ACCESSORIES')
    ]

    PRODUCT_SIZES = [
        (1, 'XS'),
        (2, 'S'),
        (3, 'M'),
        (4, 'L'),
        (5, 'XL'),
        (6, '2XL')
    ]

    id = models.AutoField(primary_key=True, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    name = models.TextField(null=False)
    type = models.IntegerField(choices=PRODUCT_TYPES, null=False)
    stock = models.IntegerField(null=False, default=0)
    description = models.TextField(null=False)
    exclusivity = models.BooleanField(null=False, default=False)
    size = models.IntegerField(choices=PRODUCT_SIZES, null=False)


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.TextField(null=False)
    image = models.ImageField(upload_to='images/')


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    product_array = models.ManyToManyField(Product)