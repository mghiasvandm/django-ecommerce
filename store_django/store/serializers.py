from rest_framework import serializers
from .models import User, ProductIdentity, Product ,ProductComment, Article, Banner, Category, OrderItem, Basket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            "username",
            'name',
            'address',
            'location'
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=(
            'name',
            'picture',
            'get_picture_url',
        )

class ProductIdentitySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = ProductIdentity
        fields  = ('star', 'weight_dependency', 'sold', 'id', 'name', 'category', 'tag', 'discount_percent', 'picture1', 'picture2', 'description', 'created_at', 'get_absolute_url', 'get_picture1_url', 'get_picture2_url', 'price1', 'price2')

class ProductSerializer(serializers.ModelSerializer):
    product = ProductIdentitySerializer(many=False, read_only=True)
    class Meta:
        model = Product
        fields  = ('ammount', 'stock', 'price', 'discounted_price', 'product')  


class ProductCommentSerializer(serializers.ModelSerializer):
     created_by = UserSerializer(many=False, read_only=True)
     class Meta:
            model = ProductComment
            read_only_fields = ('star', 'likes')
            fields  = ('productId', 'star', 'comment','created_at', 'created_by', 'likes', 'id')

     def get_star(self, obj):
        product = ProductIdentitySerializer(ProductIdentity.objects.get(id=obj.id)).data
        return product["star"]



class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields  = ('id','title', "summary", 'picture', 'get_absolute_url', 'get_picture_url', 'file', 'get_file_url','views') 


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields=(
            'id',
            'picture',
            'get_picture_url',
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    class Meta:
        model = OrderItem
        fields=(
            'id',
            'product',
            'quantity',
            'previous_price',
            'previous_discounted_price',
        )

class BasketSerializer(serializers.ModelSerializer):
    other_details = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Basket
        fields=(
            'product_name',
            'product_discount_percent',
            'other_details',
            'get_picture_url',
        )
        
        