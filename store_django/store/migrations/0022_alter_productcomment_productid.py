# Generated by Django 3.2.14 on 2022-08-30 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20220830_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='productId',
            field=models.IntegerField(verbose_name='شناسه محصول'),
        ),
    ]
