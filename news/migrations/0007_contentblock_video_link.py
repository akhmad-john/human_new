# Generated by Django 2.2.19 on 2021-03-28 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_article_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentblock',
            name='video_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
