# Generated by Django 3.2.14 on 2022-08-27 05:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20220827_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='productidentity',
            name='stock',
            field=models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='تعداد باقی مانده در انبار'),
        ),
    ]
