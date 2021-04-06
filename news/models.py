from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
import datetime
from core.models import TimeStampMixin
# Create your models here.


class Category(TimeStampMixin):
    ru_name = models.CharField(max_length=20)
    oz_name = models.CharField(max_length=20, null=True)
    uz_name = models.CharField(max_length=20, null=True)

    home_display = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.ru_name


class SubCategory(TimeStampMixin):
    ru_name = models.CharField(max_length=20)
    oz_name = models.CharField(max_length=20, null=True)
    uz_name = models.CharField(max_length=20, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    home_display = models.BooleanField(default=False)

    def __str__(self):
        return self.category.ru_name + ' - ' + self.ru_name

    class Meta:
        verbose_name_plural = 'subcategories'


class Tag(TimeStampMixin):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Article(models.Model):
    main_image = models.ImageField(upload_to='main_images/')
    tag = models.ManyToManyField(Tag, related_name="article")

    ru_heading = models.CharField(max_length=50, null=True, blank=True)
    oz_heading = models.CharField(max_length=50, null=True, blank=True)
    uz_heading = models.CharField(max_length=50, null=True, blank=True)

    ru_subheading = models.TextField(null=True, blank=True)
    oz_subheading = models.TextField(null=True, blank=True)
    uz_subheading = models.TextField(null=True, blank=True)

    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)

    display = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.ru_heading is not None:
            return self.ru_heading
        elif self.oz_heading is not None:
            return self.oz_heading
        elif self.oz_heading is not None:
            return self.uz_heading
        else:
            return "There is no title"

    def create(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()
        super().save(*args, **kwargs)

class ContentBlock(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='content_blocks')
    
    ru_content = HTMLField(null=True, blank=True)
    oz_content = HTMLField(null=True, blank=True)
    uz_content = HTMLField(null=True, blank=True)

    block_image = models.ImageField(upload_to='in_content_images/', null=True, blank=True)
    video_link = models.CharField(max_length=255,null=True, blank=True)

    # def __str__(self):
    #     return "Block #"
