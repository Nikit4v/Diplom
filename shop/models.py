from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import json

STATUS_CHOICES = (
    ("v", "Visible"),
    ("i", "Invisible")
)

RatioChoices = (
    ("a", "★★★★★"),
    ("b", "★★★★"),
    ("c", "★★★"),
    ("d", "★★"),
    ("e", "★")
)

class Phone(models.Model):
    name = models.CharField(max_length=128, verbose_name="Phone name")
    description = models.TextField(verbose_name="Description")
    staticpath = models.CharField(max_length=256, verbose_name="Path to static file")
    visible_status = models.CharField(max_length=1, default="v", verbose_name="Visible status", choices=STATUS_CHOICES)
    type = models.CharField(max_length=32, default="p", verbose_name="Type")

    def __str__(self):
        return self.name


class CartCompanion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    cart = models.ManyToManyField(Phone, related_name="carts", through="CartCompanionSupport")

    def __str__(self):
        return str(self.user)


class Article(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    phones = models.ManyToManyField(Phone)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Publish date")
    visible_status = models.CharField(max_length=1, default="v", verbose_name="Visible status", choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.title}({self.visible_status})"


class Comment(models.Model):

    author = models.CharField(max_length=128, verbose_name="Author")
    content = models.TextField()
    ratio = models.CharField(max_length=1, verbose_name="Ratio", choices=RatioChoices)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name="comments")
    visible_status = models.CharField(max_length=1, default="v", verbose_name="Visible status", choices=STATUS_CHOICES)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Publish date")

    def __str__(self):
        return f"{self.author}({self.phone.name})"


class SiteField(models.Model):
    name = models.CharField(max_length=128, verbose_name="Field name")
    is_dropdown = models.BooleanField()
    handler = models.CharField(max_length=128, default="#", blank=True, null=True)
    exclude = models.BooleanField()
    view = models.CharField(max_length=128, blank=True, null=True)
    dropdown_fields = models.ManyToManyField("SiteField", blank=True)
    main = models.BooleanField(default=True)
    visible_status = models.CharField(max_length=1, default="v", verbose_name="Visible status", choices=STATUS_CHOICES)
    phone_type = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    phones = models.ManyToManyField(Phone, through="OrderSupport")

    def __str__(self):
        return str(self.user)


class CartCompanionSupport(models.Model):
    cart = models.ForeignKey(CartCompanion, on_delete=models.CASCADE)
    phones = models.ForeignKey(Phone, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username}-{self.phones.name}"


class OrderSupport(models.Model):
    cart = models.ForeignKey(Order, on_delete=models.CASCADE)
    phones = models.ForeignKey(Phone, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username}-{self.phones.name}"
