from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext as _

from core.models import TimeStampMixin
# Create your models here.


class Category(TimeStampMixin):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class SubCategory(TimeStampMixin):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    def __str__(self):
        return self.category.name + ' - ' + self.name

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

    def __str__(self):
        return self.ru_heading

class ContentBlock(TimeStampMixin):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='content_blocks')
    
    ru_content =  HTMLField()
    oz_content =  HTMLField()
    uz_content =  HTMLField()

    block_image = models.ImageField(upload_to='in_content_images/')

    # def __str__(self):
    #     return "Block #"
