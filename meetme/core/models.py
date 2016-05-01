from django.db import models
from tinymce.models import HTMLField
# Create your models here.

class BaseMMModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True      # abstact class


class TinyMceModel(models.Model):
    text_area = HTMLField()