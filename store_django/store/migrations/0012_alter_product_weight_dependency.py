# Generated by Django 3.2.14 on 2022-08-26 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20220827_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight_dependency',
            field=models.BooleanField(verbose_name='عدم وابستگی محصول به وزن'),
        ),
    ]