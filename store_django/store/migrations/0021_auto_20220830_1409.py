# Generated by Django 3.2.14 on 2022-08-30 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_productcomment_product_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'سبد', 'verbose_name_plural': 'سبد'},
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='productId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productidentity'),
        ),
    ]
