from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User, AbstractUser
from django.utils.html import mark_safe
from django.utils.translation import ugettext as _
import random
from kavenegar import *
from django_jalali.db import models as jmodels



class User(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(_('آدرس'), max_length=600, null=True, blank=True)
    location = models.CharField(_('موقعبت مکانی'), max_length=600, null=True, blank=True)
    REQUIRED_FIELDS= ['first_name', 'last_name', 'password']

    def save(self, *args, **kwargs):
        self.name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربر')
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class FakeUser(models.Model):
    phone = models.CharField(max_length=11, unique=True) 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=11)
    otp= models.CharField(max_length=5, blank=True, null=True)

    def save(self, *args, **kwargs):
        code = random.randint(10000, 99999)
        self.otp = code
        super().save(*args, **kwargs)
        try:
            api = KavenegarAPI("652F41674B7458676A7A353777494D71636E36305958393532584F746D3364313835687A585839745639493D")
            params = {
            'receptor': f"{self.phone}",
            'template':'verify',
            'token': f"{self.otp}",
            'type': 'sms',
        }   
            response = api.verify_lookup(params)
            pass

        except APIException as e:
            pass

        except HTTPException as e:
            pass

class Category(models.Model):
    name = models.CharField(_("نام دسته "), max_length=100)
    picture = models.ImageField(_("عکس"), upload_to='')
    created_by =  models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ثبت کننده")
    created_at =  jmodels.jDateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_picture_url(self):
        return self.picture.url

    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی')

class ProductIdentity(models.Model):
    name = models.CharField(_('نام محصول'), max_length=100) 
    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name=_("دسته بندی")) 
    weight_dependency = models.BooleanField(_("عدم وابستگی محصول به وزن"), default=False)
    tag = models.CharField(_('برچسب محصول'), max_length=100) 
    price1 = models.IntegerField(_("قیمت اولیه محصول"), validators=[MinValueValidator(1)])
    price2 = models.IntegerField(_("قیمت تخفیف خورده محصول"), validators=[MinValueValidator(1)])
    discount_percent = models.FloatField(_("درصد تخفیف محصول"), blank=True, null=True)
    picture1 = models.ImageField(_("عکس محصول"), upload_to='')
    picture2 = models.ImageField(_("عکس محصول"), upload_to='')
    description = models.TextField(_("توضیحات محصول"), max_length=10000)
    sold = models.PositiveIntegerField(_("تعداد فروش"), null=True, blank=True)
    star = models.FloatField(_("میانگین امتیازات از 1 تا 5"), null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("ثبت کننده ی محصول"))
    created_at = jmodels.jDateField(auto_now_add = True)

    def image(self):
        return mark_safe('<img src="%s" width="220" height="70" />' % (self.picture1.url))
    image.allow_tags = True

    class Meta:
        verbose_name = _('شناسنامه محصول')
        verbose_name_plural = _('شناسنامه ی محصول')
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/{self.category}/{self.id}/'

    def get_picture1_url(self):
        return self.picture1.url

    def get_picture2_url(self):
        return self.picture2.url


class Product(models.Model):
    product = models.ForeignKey(ProductIdentity, on_delete=models.CASCADE, verbose_name=_("محصول"))
    CHOICES=[("0.1", "0.1"), ("0.2", "0.2"), ("0.3", "0.3"), ("0.4", "0.4"), ("0.5", "0.5"), 
    ("0.6", "0.6"), ("0.7", "0.7"), ("0.8", "0.8"), ("0.9", "0.9"), ("1.0", "1.0"), ("1.1", "1.1"), ("1.2", "1.2")
    , ("1.3", "1.3"), ("1.4", "1.4"), ("1.5", "1.5"), ("1.6", "1.6"), ("1.7", "1.7"), ("1.8", "1.8"), ("1.9", "1.9"),
    ("2.0", "2.0"), ("2.1", "2.1"), ("2.2", "2.2"), ("2.3", "2.3"), ("2.4", "2.4"), ("2.5", "2.5"), ("2.6", "2.6"),
    ("2.7", "2.7"), ("2.8", "2.8"), ("2.9", "2.9"), ("3.0", "3.0"), ("3.1", "3.1"), ("3.2", "3.2"), ("3.3", "3.3"), 
    ("3.4", "3.4"), ("3.5", "3.5"), ("3.6", "3.6"), ("3.7", "3.7"), ("3.8", "3.8"), ("3.9", "3.9"),
    ("4.0", "4.0"), ("4.1", "4.1"), ("4.2", "4.2"), ("4.3", "4.3"), 
    ("4.4", "4.4"), ("4.5", "4.5"), ("4.6", "4.6"), ("4.7", "4.7"), ("4.8", "4.8"), ("4.9", "4.9"),
    ("5.0", "5.0")
    ]
    ammount = models.CharField(_("وزن محصول بر حسب کیلوگرم"), max_length=4, choices=CHOICES, null=True, blank=True)
    stock = models.PositiveIntegerField(_("تعداد باقی مانده در انبار"), validators=[MinValueValidator(0)])
    sold = models.PositiveIntegerField(_("تعداد فروش"), null=True, blank=True)
    price = models.IntegerField(_("قیمت اولیه محصول"), blank=True, null=True)
    discounted_price = models.IntegerField(_("قیمت تخفیف خورده محصول"), blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("ثبت کننده ی محصول"))
    created_at = jmodels.jDateField(auto_now_add = True) 

    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصول')

    def __str__(self):
        return self.product.name


class ProductComment(models.Model): 
    productId = models.IntegerField(_("شناسه محصول"))
    product_name = models.CharField(_("نام محصول"), null=True, blank=True, max_length=100)
    star = models.IntegerField(_("امتیاز کاربر از 1 تا 5"))
    likes = models.IntegerField(_("تعداد لایک"), null=True, blank=True, default=0)
    comment = models.CharField(_("نظر کاربر "), max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("ثبت کننده ی نظر"))
    created_at = jmodels.jDateField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        self.product_name = ProductIdentity.objects.get(id=self.productId).name
        super().save(*args, **kwargs)

    def __str__(self):
        return f'دیدگاه شماره {self.id}'

    class Meta:
        verbose_name = _('دیدگاه')
        verbose_name_plural = _('دیدگاه')

class ProductCommentLikeCounter(models.Model):
    comment = models.ForeignKey(ProductComment, on_delete=models.CASCADE)
    ip = models.CharField(max_length=200)

class Article(models.Model):
    title = models.CharField(_("عنوان مقاله"), max_length=70)
    views = models.PositiveIntegerField(_("تعداد دانلود"), null=True, blank=True, default=0)
    picture = models.ImageField(_("عکس"), upload_to='')
    summary = models.CharField(_("خلاصه ی مقاله"), max_length=450)
    file = models.FileField(_("فایل مقاله"), upload_to='')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name=_("ثبت کننده ی مقاله"))
    created_at = jmodels.jDateField(auto_now_add = True) 

    class Meta:
        verbose_name = _('مقاله')
        verbose_name_plural = _('مقاله')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/article/{self.id}/'

    def get_picture_url(self):
        return self.picture.url

    def get_file_url(self):
        return self.file.url

class ArticleViewCounter(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip = models.CharField(max_length=200)
        
class Cooperation(models.Model):
    name = models.CharField(_("نام داوطلب "), max_length=100)
    phone = models.CharField(_("شماره همراه داوطلب "), max_length=11)
    description = models.CharField(_("توضیحات داوطلب"), max_length=1000)
    seen = models.BooleanField(_("دیده شده"), default=False)
    created_at = jmodels.jDateField(auto_now_add = True) 

    class Meta:
        ordering = ('seen',)
        verbose_name = _('همکاری')
        verbose_name_plural = _('همکاری')


class Banner(models.Model):
    picture = models.ImageField(_("عکس"), upload_to='')
    created_by =  models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ثبت کننده")
    created_at =  jmodels.jDateField(auto_now_add=True)

    def get_picture_url(self):
        return self.picture.url

    class Meta:
        verbose_name = _('بنر')
        verbose_name_plural = _('بنر')

    def __str__(self):
        return f"بنر شماره ی {self.id}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    previous_price = models.IntegerField(null=True, blank=True)
    previous_discounted_price = models.IntegerField(null=True, blank=True)
    selected_by =  models.ForeignKey(User, on_delete=models.CASCADE)
    created_at =  jmodels.jDateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        orders = OrderItem.objects.filter(selected_by=self.selected_by, product__product__name=self.product.product.name)
        if Basket.objects.filter(product_name=self.product.product.name, product_picture= self.product.product.picture1, product_discount_percent=self.product.product.discount_percent, selected_by=self.selected_by).exists():
            order = Basket.objects.get(product_name=self.product.product.name, product_picture= self.product.product.picture1, product_discount_percent=self.product.product.discount_percent, selected_by=self.selected_by)
            for item in orders:
                order.other_details.add(item.id)
                order.save()
        else:
            Basket.objects.create(product_name=self.product.product.name, product_picture= self.product.product.picture1, product_discount_percent=self.product.product.discount_percent, selected_by=self.selected_by)
            order = Basket.objects.get(product_name=self.product.product.name, product_picture= self.product.product.picture1, product_discount_percent=self.product.product.discount_percent, selected_by=self.selected_by)
            order.other_details.set(orders)



class Order(models.Model):
    orders = models.ManyToManyField(OrderItem, verbose_name="محصولات خریداری شده")
    total_quantity = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    total_discounted_price = models.IntegerField(null=True, blank=True)
    created_at =  jmodels.jDateField(auto_now_add=True)

    class Meta:
        verbose_name = _('سبد')
        verbose_name_plural = _('سبد')


class Basket(models.Model):
    product_name = models.CharField(max_length=100)
    product_picture = models.ImageField(_("عکس"), upload_to='')
    product_discount_percent = models.FloatField(_("درصد تخفیف محصول"))
    other_details = models.ManyToManyField(OrderItem, verbose_name="محصولات خریداری شده")
    selected_by =  models.ForeignKey(User, on_delete=models.CASCADE)
    created_at =  jmodels.jDateField(auto_now_add=True)

    def get_picture_url(self):
        return self.product_picture.url




