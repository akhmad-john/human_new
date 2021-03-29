from django.db import models
import datetime
# Create your models here.


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        abstract = True