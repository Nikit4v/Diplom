from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ("v", "Visible"),
    ("i", "Invisible")
)


class Phone(models.Model):
    name = models.CharField(max_length=128, verbose_name="Phone name")
    description = models.TextField(verbose_name="Description")
    staticpath = models.CharField(max_length=256, verbose_name="Path to static file")
    visible_status = models.CharField(max_length=1, default="v", verbose_name="Visible status", choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class CartCompanion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Phone, related_name="carts")


class Article(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    phones = models.ManyToManyField(Phone)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Publish date")
    visible_status = models.CharField(max_length=1, default="v", verbose_name="Visible status", choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.title}({self.visible_status})"
