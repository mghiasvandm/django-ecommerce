# Generated by Django 3.2.14 on 2022-08-26 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_weight_dependency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight_dependency',
            field=models.BooleanField(verbose_name='عدم وابستگی محصول به جرم'),
        ),
    ]
