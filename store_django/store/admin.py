from . import models
from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from .models import User, ProductIdentity, Product, Article, ProductComment, Cooperation, Category, Banner, Order, Basket
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'showPhone', 'is_staff']
    search_fields = ('name',)
    list_filter = ('is_staff', 'groups')
    exclude = ('name', 'user_permissions', 'email')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


    def showPhone(self, obj):
        return obj.username
    showPhone.short_description = 'شماره همراه'

class DiscountPercentFilter(admin.SimpleListFilter):
    title = "درصد تخفیف"
    parameter_name = "discount_percent"
    def lookups(self, request, model_admin):
        return(
            ('0% تا 10%', '0% تا 10%'),
            ('11% تا 20%', '11% تا 20%'),
            ('21% تا 30%', '21% تا 30%'),
            ('31% تا 40%', '31% تا 40%'),
            ('41% تا 50%', '41% تا 50%'),
            ('51% تا 60%', '51% تا 60%'),
            ('61% تا 70%', '61% تا 70%'),
            ('71% تا 80%', '71% تا 80%'),
        )

    def queryset(self, request, queryset):
        if self.value() ==('0% تا 10%'):
            return queryset.filter(discount_percent__gte=0, discount_percent__lte=10)
        elif self.value() ==('11% تا 20%'):
            return queryset.filter(discount_percent__gte=11, discount_percent__lte=20)
        elif self.value() ==('21% تا 30%'):
           return queryset.filter(discount_percent__gte=21, discount_percent__lte=30)
        elif self.value() ==('31% تا 40%'):
           return queryset.filter(discount_percent__gte=31, discount_percent__lte=40)
        elif self.value() ==('41% تا 50%'):
            return queryset.filter(discount_percent__gte=41, discount_percent__lte=50)
        elif self.value() ==('51% تا 60%'):
            return queryset.filter(discount_percent__gte=51, discount_percent__lte=60) 
        elif self.value() ==('61% تا 70%'):
            return queryset.filter(discount_percent__gte=61, discount_percent__lte=70)
        elif self.value() ==('71% تا 80%'):
            return queryset.filter(discount_percent__gte=71, discount_percent__lte=80)

@admin.register(ProductIdentity)
class ProductIdentityAdmin(admin.ModelAdmin):
    list_display = ["name", "category", 'weight_dependency', "image", "price1", "price2", 'discount_percent', "created_by", 'star']
    search_fields = ["name"]
    list_filter = ["category", DiscountPercentFilter]
    readonly_fields = ['sold',  'star',"discount_percent", "created_by"]

    def save_model(self, request, obj, form, change):
        if obj.sold == None:
            obj.sold = 0
        else:
            obj.sold = obj.sold
        obj.created_by = request.user
        obj.discount_percent = round((((obj.price1-obj.price2)/obj.price1)*100), 0)
        productName = obj.name
        if Basket.objects.filter(product_name = productName).exists():
            basketSimilarItems = Basket.objects.filter(product_name = productName)
            for item in basketSimilarItems:
                item.product_name = productName
                item.product_picture = obj.picture1
                item.discount_percent = obj.discount_percent
                item.save()
        else:
            pass
        super().save_model(request, obj, form, change)
    
    def delete_queryset(self, request, queryset):
        for query in queryset:
            comments = models.ProductComment.objects.filter(productId = query.id)
            comments.delete()
        queryset.delete()

class StockFilter(admin.SimpleListFilter):
    title = "تعداد موجود در انبار"
    parameter_name = "stock"
    def lookups(self, request, model_admin):
        return(
            ('0 تا 10', '0 تا 10'),
            ('11 تا 20', '11 تا 20'),
            ('21 تا 30', '21 تا 30'),
            ('31 تا 40', '31 تا 40'),
            ('41 تا 50', '41 تا 50'),
            ('بیش از 51', 'بیش از 51'),
        )

    def queryset(self, request, queryset):
        if self.value() ==('0 تا 10'):
            return queryset.filter(stock__gte=0, stock__lte=10)
        elif self.value() ==('11 تا 20'):
            return queryset.filter(stock__gte=11, stock__lte=20)
        elif self.value() ==('21 تا 30'):
            return queryset.filter(stock__gte=21, stock__lte=30)
        elif self.value() ==('31 تا 40'):
            return queryset.filter(stock__gte=31, stock__lte=40)
        elif self.value() ==('41 تا 50'):
            return queryset.filter(stock__gte=41, stock__lte=50)
        elif self.value() ==('بیش از 51'):
            return queryset.filter(stock__gte=51)
        



class SoldFilter(admin.SimpleListFilter):
    title = "تعداد فروش"
    parameter_name = "sold"
    def lookups(self, request, model_admin):
        return(
            ('0 تا 20', '0 تا 20'),
            ('21 تا 40', '21 تا 40'),
            ('41 تا 60', '41 تا 60'),
            ('61 تا 80', '81 تا 100'),
            ('بیش از 101', 'بیش از 101'),
        )

    def queryset(self, request, queryset):
        if self.value() ==('0 تا 20'):
            return queryset.filter(stock__gte=0, stock__lte=20)
        elif self.value() ==('21 تا 40'):
            return queryset.filter(stock__gte=21, stock__lte=40)
        elif self.value() ==('41 تا 60'):
            return queryset.filter(stock__gte=41, stock__lte=60)
        elif self.value() ==('61 تا 80'):
            return queryset.filter(stock__gte=61, stock__lte=80)
        elif self.value() ==('بیش از 100'):
            return queryset.filter(stock__gte=101)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display= ["product", 'ammount', 'sold', 'stock','created_by']
    search_fields = ["product__name",]
    list_filter = [StockFilter, SoldFilter]
    readonly_fields = ["sold","created_by"]
    autocomplete_fields = ('product',)
    exclude = ('price', 'discounted_price')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        if obj.sold == None:
            obj.sold = 0
        else:
            obj.sold = obj.sold
        if obj.ammount != None and obj.product.weight_dependency == False:
            obj.price = (ProductIdentity.objects.get(name=obj.product.name).price1) * float(obj.ammount)
            obj.discounted_price = (ProductIdentity.objects.get(name=obj.product.name).price2) * float(obj.ammount)
            obj.save()
        if obj.ammount == None and obj.product.weight_dependency == True:
            obj.price = obj.product.price1
            obj.discounted_price = obj.product.price2
            obj.save()

        i
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display= ["__str__", 'views']
    readonly_fields = ["views", "created_by"]
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Cooperation)
class CooperationAdmin(admin.ModelAdmin):
    list_display= ["name", 'phone', 'seen']
    readonly_fields = ["name", "phone", "description", 'seen']

    def save_model(self, request, obj, form, change):
        obj.seen = True
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(ProductComment)
class ProductComment(admin.ModelAdmin):
    list_display= ["product_name", 'star', 'likes', 'created_by']
    list_filter= ['star',]
    exclude= ('productId',)

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def delete_queryset(self, request, queryset):
        for query in queryset:
            comments = models.ProductComment.objects.all()
            totalStars = 0
            commentsNumber = 0
            for comment in comments:
                if comment.productId == query.productId and comment.id != query.id:
                    commentsNumber += 1
                    totalStars += int(comment.star)
            product=ProductIdentity.objects.get(id=query.productId)
            product.star = round(totalStars/commentsNumber, 1)
            product.save()
        queryset.delete()


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    readonly_fields = ["created_by"]
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ["created_by"]
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

admin.site.unregister(TokenProxy)
