# Generated by Django 3.2.14 on 2022-08-26 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20220826_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight_dependency',
            field=models.BooleanField(verbose_name='وابستگی محصول به جرم'),
        ),
    ]