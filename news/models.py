from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
import datetime
from core.models import TimeStampMixin
# Create your models here.


class Category(TimeStampMixin):
    ru_name = models.CharField(max_length=20, verbose_name="Название(на русском)")
    oz_name = models.CharField(max_length=20, null=True, verbose_name="Название(на латинице)")
    uz_name = models.CharField(max_length=20, null=True, verbose_name="Название(на кирилице)")

    home_display = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.ru_name

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"


class SubCategory(TimeStampMixin):
    ru_name = models.CharField(max_length=20, verbose_name="Название(на русском)")
    oz_name = models.CharField(max_length=20, null=True, verbose_name="Название(на латинице)")
    uz_name = models.CharField(max_length=20, null=True, verbose_name="Название(на кирилице)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    home_display = models.BooleanField(default=False)

    def __str__(self):
        return self.category.ru_name + ' - ' + self.ru_name

    class Meta:
        verbose_name_plural = 'subcategories'

    class Meta:
        verbose_name = "Подкатегории"
        verbose_name_plural = "Подкатегории"


class Tag(TimeStampMixin):
    ru_name = models.CharField(max_length=30, verbose_name="Название(на русском)")
    oz_name = models.CharField(max_length=30, null=True, verbose_name="Название(на латинице)")
    uz_name = models.CharField(max_length=30, null=True, verbose_name="Название(на кирилице)")

    def __str__(self):
        return self.ru_name

    class Meta:
        verbose_name = "Теги"
        verbose_name_plural = "Теги"

class Article(models.Model):
    main_image = models.ImageField(upload_to='main_images/', verbose_name="Главное фото")
    tag = models.ManyToManyField(Tag, related_name="article")

    ru_heading = models.CharField(max_length=50, null=True, blank=True, verbose_name="Оглавление(на русском)")
    oz_heading = models.CharField(max_length=50, null=True, blank=True, verbose_name="Оглавление(на латинице)")
    uz_heading = models.CharField(max_length=50, null=True, blank=True, verbose_name="Оглавление(на кирилице)")

    ru_subheading = models.TextField(null=True, blank=True, verbose_name="Описание(на русском)")
    oz_subheading = models.TextField(null=True, blank=True, verbose_name="Описание(на латинице)")
    uz_subheading = models.TextField(null=True, blank=True, verbose_name="Описание(на кирилице)")

    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, verbose_name="Подкатегория")

    display = models.BooleanField(default=True)

    view_count = models.IntegerField(default=0, verbose_name="Количество просмотров")

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

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = "Статьи"

class ContentBlock(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='content_blocks')
    
    ru_content = HTMLField(null=True, blank=True, verbose_name="Блок (на русском)")
    oz_content = HTMLField(null=True, blank=True, verbose_name="Блок (на латинице)")
    uz_content = HTMLField(null=True, blank=True, verbose_name="Блок (на кирилице)")

    block_image = models.ImageField(upload_to='in_content_images/', null=True, blank=True, verbose_name="Фото для блока")
    video_link = models.CharField(max_length=255,null=True, blank=True, verbose_name="Ссылка для видео")

    class Meta:
        ordering = ['id']
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"


    # def __str__(self):
    #     return "Block #"
