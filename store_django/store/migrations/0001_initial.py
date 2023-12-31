# Generated by Django 3.2.14 on 2022-08-26 06:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=600, null=True)),
                ('location', models.CharField(blank=True, max_length=600, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربر',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='عنوان مقاله')),
                ('views', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='تعداد دانلود')),
                ('picture', models.ImageField(upload_to='', verbose_name='عکس')),
                ('summary', models.CharField(max_length=450, verbose_name='خلاصه ی مقاله')),
                ('file', models.FileField(upload_to='', verbose_name='فایل مقاله')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ثبت کننده ی مقاله')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقاله',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام دسته ')),
                ('picture', models.ImageField(upload_to='', verbose_name='عکس')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ثبت کننده')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی',
            },
        ),
        migrations.CreateModel(
            name='Cooperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام داوطلب ')),
                ('phone', models.CharField(max_length=11, verbose_name='شماره همراه داوطلب ')),
                ('description', models.CharField(max_length=1000, verbose_name='توضیحات داوطلب')),
                ('seen', models.BooleanField(default=False, verbose_name='دیده شده')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'همکاری',
                'verbose_name_plural': 'همکاری',
                'ordering': ('seen',),
            },
        ),
        migrations.CreateModel(
            name='FakeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=11)),
                ('otp', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productId', models.IntegerField(verbose_name='شناسه محصول')),
                ('star', models.IntegerField(verbose_name='امتیاز کاربر از 1 تا 5')),
                ('likes', models.IntegerField(blank=True, default=0, null=True, verbose_name='تعداد لایک')),
                ('comment', models.CharField(max_length=1000, verbose_name='نظر کاربر ')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ثبت کننده ی نظر')),
            ],
            options={
                'verbose_name': 'دیدگاه',
                'verbose_name_plural': 'دیدگاه',
            },
        ),
        migrations.CreateModel(
            name='ProductIdentity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام محصول')),
                ('tag', models.CharField(max_length=100, verbose_name='برچسب محصول')),
                ('price1', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='قیمت اولیه محصول')),
                ('price2', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='قیمت تخفیف خورده محصول')),
                ('discount_percent', models.FloatField(blank=True, null=True, verbose_name='درصد تخفیف محصول')),
                ('picture1', models.ImageField(upload_to='', verbose_name='عکس محصول')),
                ('picture2', models.ImageField(upload_to='', verbose_name='عکس محصول')),
                ('description', models.TextField(max_length=10000, verbose_name='توضیحات محصول')),
                ('sold', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد فروش')),
                ('star', models.FloatField(blank=True, null=True, verbose_name='میانگین امتیازات از 1 تا 5')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category', verbose_name='دسته بندی')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ثبت کننده ی محصول')),
            ],
            options={
                'verbose_name': 'شناسنامه محصول',
                'verbose_name_plural': 'شناسنامه ی محصول',
            },
        ),
        migrations.CreateModel(
            name='ProductCommentLikeCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=200)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productcomment')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.CharField(choices=[('0.1', '0.1'), ('0.2', '0.2'), ('0.3', '0.3'), ('0.4', '0.4'), ('0.5', '0.5'), ('0.6', '0.6'), ('0.7', '0.7'), ('0.8', '0.8'), ('0.9', '0.9'), ('1.0', '1.0'), ('1.1', '1.1'), ('1.2', '1.2'), ('1.3', '1.3'), ('1.4', '1.4'), ('1.5', '1.5'), ('1.6', '1.6'), ('1.7', '1.7'), ('1.8', '1.8'), ('1.9', '1.9'), ('2.0', '2.0'), ('2.1', '2.1'), ('2.2', '2.2'), ('2.3', '2.3'), ('2.4', '2.4'), ('2.5', '2.5'), ('2.6', '2.6'), ('2.7', '2.7'), ('2.8', '2.8'), ('2.9', '2.9'), ('3.0', '3.0'), ('3.1', '3.1'), ('3.2', '3.2'), ('3.3', '3.3'), ('3.4', '3.4'), ('3.5', '3.5'), ('3.5', '3.5'), ('3.6', '3.6'), ('3.7', '3.7'), ('3.8', '3.8'), ('3.9', '3.9'), ('4.0', '4.0')], max_length=4, verbose_name='وزن محصول بر حسب کیلوگرم')),
                ('stock', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='تعداد باقی مانده در انبار')),
                ('sold', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد فروش')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='قیمت اولیه محصول')),
                ('discounted_price', models.IntegerField(blank=True, null=True, verbose_name='قیمت تخفیف خورده محصول')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ثبت کننده ی محصول')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productidentity', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصول',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('previous_price', models.IntegerField()),
                ('previous_discounted_price', models.IntegerField()),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('selected_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_quantity', models.IntegerField(blank=True, null=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('total_discounted_price', models.IntegerField(blank=True, null=True)),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('orders', models.ManyToManyField(to='store.OrderItem', verbose_name='محصولات خریداری شده')),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_picture', models.ImageField(upload_to='', verbose_name='عکس')),
                ('product_discount_percent', models.FloatField(verbose_name='درصد تخفیف محصول')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('other_details', models.ManyToManyField(to='store.OrderItem', verbose_name='محصولات خریداری شده')),
                ('selected_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='', verbose_name='عکس')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ثبت کننده')),
            ],
            options={
                'verbose_name': 'بنر',
                'verbose_name_plural': 'بنر',
            },
        ),
        migrations.CreateModel(
            name='ArticleViewCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=200)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.article')),
            ],
        ),
    ]
