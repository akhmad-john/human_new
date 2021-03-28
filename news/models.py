from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext as _

from core.models import TimeStampMixin
# Create your models here.


class Category(TimeStampMixin):
    ru_name = models.CharField(max_length=20)
    oz_name = models.CharField(max_length=20, null=True)
    uz_name = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.ru_name


class SubCategory(TimeStampMixin):
    ru_name = models.CharField(max_length=20)
    oz_name = models.CharField(max_length=20, null=True)
    uz_name = models.CharField(max_length=20, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    def __str__(self):
        return self.category.ru_name + ' - ' + self.ru_name

    class Meta:
        verbose_name_plural = 'subcategories'


class Tag(TimeStampMixin):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Article(TimeStampMixin):
    main_image = models.ImageField(upload_to='main_images/')
    tag = models.ManyToManyField(Tag, related_name="article")

    ru_heading = models.CharField(max_length=50)
    oz_heading = models.CharField(max_length=50)
    uz_heading = models.CharField(max_length=50)

    ru_subheading = models.TextField()
    oz_subheading = models.TextField()
    uz_subheading = models.TextField()

    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)

    display = models.BooleanField(default=True)

    def __str__(self):
        return self.ru_heading

class ContentBlock(TimeStampMixin):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='content_blocks')
    
    ru_content = HTMLField(null=True, blank=True)
    oz_content = HTMLField(null=True, blank=True)
    uz_content = HTMLField(null=True, blank=True)

    block_image = models.ImageField(upload_to='in_content_images/', null=True, blank=True)
    video_link = models.CharField(max_length=255,null=True, blank=True)

    # def __str__(self):
    #     return "Block #"
