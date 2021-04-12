from django.db import models
# Create your models here.

AD_TYPES = (
    (1, "Верх"),
    (2, "Сбоку"),
    (3, "Снизу"),
)


class Advertisement(models.Model):
    company_name = models.CharField(max_length=50)
    banner = models.ImageField(upload_to="ad_images", verbose_name="Рекламное фото")
    ad_type = models.IntegerField(choices=AD_TYPES)
    click_count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Реклама"
        verbose_name_plural = "Реклама"

    def __str__(self):
        return self.company_name
