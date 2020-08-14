from django.db import models
from django.utils.translation import ugettext_lazy as _

STATUS_CHOICES = (
    ("v", "Visible"),
    ("i", "Invisible")
)


class Phone(models.Model):
    name = models.CharField(max_length=128, verbose_name="Phone name")
    description = models.TextField(verbose_name="Description")
    staticpath = models.CharField(max_length=256, verbose_name="Path to static file")
    visible_status = models.CharField(max_length=1, default="v", verbose_name="Visible status", choices=STATUS_CHOICES)
