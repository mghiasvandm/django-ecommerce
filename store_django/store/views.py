from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, FakeUser, ProductIdentity, Product, ProductComment, Article, ArticleViewCounter, ProductCommentLikeCounter, Cooperation, Category, Banner, OrderItem, Basket
from .serializers import ProductIdentitySerializer, ProductCommentSerializer, ArticleSerializer, CategorySerializer, BannerSerializer, UserSerializer, BasketSerializer
from django.http import Http404
from rest_framework.authtoken.models import Token


@api_view(['GET'])
def basketLength(request):
    basketLength = 0
    orders = OrderItem.objects.filter(selected_by=request.user)
    for order in orders:
        basketLength += order.quantity

    return Response({
        "basketLength": basketLength
    })


@api_view(['POST'])
def deleteOrder(request):
    order = OrderItem.objects.get(id=request.data["id"])
    order.delete()
    basket = Basket.objects.get(product_name = order.product.product.name)
    if not basket.other_details.exists():
        basket.delete()
    else:
        pass
    return Response()



@api_view(['GET'])
def totalPrices(request):
    other_details = []
    details = []
    totalPrice = 0
    discountAmmount = 0
    finalPrice = 0
    items = Basket.objects.filter(selected_by=request.user)

    for item in items:
        other_details.append(item.other_details)

    for other_detail in other_details:
        details.append(other_detail.all())

    for options in details:
        for option in options:
            totalPrice += option.previous_price
            finalPrice += option.previous_discounted_price
            discountAmmount += totalPrice - finalPrice

    return Response({
        "totalPrice": totalPrice,
        "discountAmmount": discountAmmount,
        "finalPrice": finalPrice,
    })

@api_view(['POST'])
def editBasket(request):
    orders = request.data["orders"]
    for order in orders:
        item = OrderItem.objects.get(id=int(order[0].split(',')[0]))
        item.quantity = int(order[0].split(',')[1])
        item.previous_price = int(order[0].split(',')[1]) * item.product.price
        item.previous_discounted_price = int(order[0].split(',')[1]) * item.product.discounted_price
        item.save()
    return Response()


@api_view(['GET'])
def checkProfile(request):
    completed = None
    user = User.objects.get(username=request.user.username)
    if user.first_name is None or user.last_name is None or user.username is None or user.address is None or user.location is None:
        completed = False
    else:
        completed = True
    return Response({
        "completed": completed
    })
        

@api_view(['POST'])
def addToCart(request, id):
    if 'ammount' in request.data:
        product = Product.objects.get(product = ProductIdentity.objects.get(id=id), ammount=request.data    ["ammount"])
    else:
        product = Product.objects.get(product = ProductIdentity.objects.get(id=id))
    if OrderItem.objects.filter(product=product, selected_by=request.user).exists():
        item = OrderItem.objects.get(product=product)
        item.quantity = int(request.data["quantity"])
        item.previous_price = int(request.data["quantity"]) * item.product.price
        item.previous_discounted_price = int(request.data["quantity"]) * item.product.discounted_price
        item.save()
    else:
        OrderItem.objects.create(product=product, quantity=int(request.data["quantity"]), selected_by=request.user)
        item = OrderItem.objects.get(product=product, quantity=int(request.data["quantity"]), selected_by=request.user)
        item.previous_price = item.quantity * item.product.price
        item.previous_discounted_price = item.quantity* item.product.discounted_price
        item.save()
    orders = OrderItem.objects.filter(selected_by=request.user, product__product__name=product.product.name)    
    if Basket.objects.filter(product_name=product.product.name, product_picture= product.product.picture1, product_discount_percent=product.product.discount_percent, selected_by=request.user).exists():
        order = Basket.objects.get(product_name=product.product.name, product_picture= product.product.picture1, product_discount_percent=product.product.discount_percent, selected_by=request.user)
        for item in orders:
            order.other_details.add(item.id)
            order.save()
    else:
        Basket.objects.create(product_name=product.product.name, product_picture= product.product.picture1, product_discount_percent=product.product.discount_percent, selected_by=request.user)
        order = Basket.objects.get(product_name=product.product.name, product_picture= product.product.picture1, product_discount_percent=product.product.discount_percent, selected_by=request.user)
        order.other_details.set(orders)

    basketLength = 0
    orders = OrderItem.objects.filter(selected_by=request.user)
    for order in orders:
        basketLength += order.quantity

    return Response({
        "basketLength": basketLength
    })


@api_view(['GET'])
def showCart(request):
    orders = Basket.objects.filter(selected_by=request.user.id)
    ordersSerializer = BasketSerializer(orders, many=True)
    return Response({
        "orders": ordersSerializer.data
    })


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        return self.queryset.all().order_by('-views')


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset.all().filter(username=self.request.user.username)

@api_view(['POST'])
def deleteComment(request, category, id):
    ProductComment.objects.get(id=request.data['commentId']).delete()
    comments = ProductComment.objects.all()
    totalStars = 0
    commentsNumber = 0
    for comment in comments:
        if comment.productId == id:
            commentsNumber += 1
            totalStars += int(comment.star)
    product=ProductIdentity.objects.get(id=id)
    
    if commentsNumber == 0:
        product.star = None
    else:
        product.star = round(totalStars/commentsNumber, 1)
    product.save()
    return Response()

@api_view(['POST'])
def editProfile(request):
    user = User.objects.get(username=request.user.username)
    user.first_name = request.data["first_name"]
    user.last_name = request.data["last_name"]
    user.username = request.data["username"]
    user.address = request.data["address"]
    user.location = request.data["location"]
    user.save()
    return Response()


@api_view(['GET'])
def productAmmounts(request, id):
    productAmmounts=[]
    products = Product.objects.filter(product=ProductIdentity.objects.get(id=id))
    for product in products:
        productAmmounts.append(product.ammount)
    return Response({
        "productAmmounts": productAmmounts,
    })

@api_view(['GET'])    
def productStockAndQuantityAndPrices(request, id, ammount):
    product = Product.objects.get(product=ProductIdentity.objects.get(id=id), ammount=float(ammount))
    if request.user.is_authenticated:
        if OrderItem.objects.filter(product=product, selected_by=request.user).exists():
            quantity = OrderItem.objects.get(product=product, selected_by=request.user).quantity
        else:
            quantity=1
        if product.stock < quantity:
            quantity = product.stock
        else:
            pass
        return Response({
            "productQuantity": quantity,
            "productStock": product.stock,
            "productPrice": product.price * quantity,
            "productDiscountedPrice": product.discounted_price* quantity,
            "pureProductPrice": product.price,
            "pureProductDiscountedPrice": product.discounted_price,
        })
    else:
        return Response({
            "productQuantity": 1,
            "productStock": product.stock,
            "productPrice": product.price,
            "productDiscountedPrice": product.discounted_price,
            "pureProductPrice": product.price,
            "pureProductDiscountedPrice": product.discounted_price,
        })

@api_view(['GET'])
def getFreeSpecialProducts(request):
    specialProducts = []
    products = ProductIdentity.objects.all().order_by('-discount_percent')[:3]
    for product in products:
        if Product.objects.filter(product=product).exists():
            specialProducts.append(product)
        else:
            pass
    specialProductsSerializer = ProductIdentitySerializer(specialProducts, many=True)
    return Response({
        "fewSpecialProducts": specialProductsSerializer.data,
    })


@api_view(['POST'])
def countCommentLikes(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ProductCommentLikeCounter.objects.filter(comment__id=request.data["commentId"], ip=ip).exists():
        pass
    else:
        comment = ProductComment.objects.get(id=request.data["commentId"])
        comment.likes = int(comment.likes)+1
        comment.save()
        ProductCommentLikeCounter.objects.create(comment=comment, ip=ip)
    return Response()

@api_view(['POST'])
def countArticleDownloads(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ArticleViewCounter.objects.filter(article__id=request.data["articleId"], ip=ip).exists():
        pass
    else:
        article = Article.objects.get(id=request.data["articleId"])
        article.views = int(article.views)+1
        article.save()
        ArticleViewCounter.objects.create(article=article, ip=ip)
    return Response()


@api_view(['GET'])
def index(request):
    categories = Category.objects.all()
    categoriesSerializer = CategorySerializer(categories, many=True)
    banners = reversed(Banner.objects.all())
    bannersSerializer = BannerSerializer(banners, many=True)
    specialProducts = []
    products = ProductIdentity.objects.all().order_by('-discount_percent')[:7]
    for product in products:
        if Product.objects.filter(product=product).exists():
            specialProducts.append(product)
        else:
            pass
    specialProductsSerializer = ProductIdentitySerializer(specialProducts, many=True)
    newProducts = []
    products = ProductIdentity.objects.all().order_by('-created_at')[:7]
    for product in products:
        if Product.objects.filter(product=product).exists():
            newProducts.append(product)
        else:
            pass
    newProductsSerializer = ProductIdentitySerializer(reversed(newProducts), many=True)
    bestSellerProducts = []
    products = ProductIdentity.objects.all().order_by('-sold')[:7]
    for product in products:
        if Product.objects.filter(product=product).exists():
            bestSellerProducts.append(product)
        else:
            pass
    bestSellerProductsSerializer = ProductIdentitySerializer(bestSellerProducts, many=True)
    articles = Article.objects.all().order_by('-views')[:3]
    articlesSerializer = ArticleSerializer(articles, many=True)
    serializerDatas = [
        specialProductsSerializer.data, newProductsSerializer.data, bestSellerProductsSerializer.data, articlesSerializer.data, categoriesSerializer.data, bannersSerializer.data
    ]
    return Response({
        "specialProducts": serializerDatas[0],
        "newProducts": serializerDatas[1],
        "bestSellerProducts": serializerDatas[2],
        "articles": serializerDatas[3],
        "categories": serializerDatas[4],
        "banners": serializerDatas[5],
    })


@api_view(['POST'])
def otp(request):
    phone = request.data["phone"]
    otp = request.data["otp"]
    if FakeUser.objects.filter(phone=phone, otp=otp).exists():
        fakeUser = FakeUser.objects.get(phone=phone, otp=otp)
        User.objects.create(username=fakeUser.phone, first_name=fakeUser.first_name, last_name=fakeUser.last_name, password=fakeUser.password)
        return Response(200)
    else:
        return Response("رمز یکبار مصرف وارد شده اشتباه است.")


@api_view(['POST'])
def fake(request):
    if FakeUser.objects.filter(phone=request.data["phone"]).exists():
        return Response('این حساب کاربری از پیش ثبت شده است لطفا وارد حساب تان شوید.')
    else:
        FakeUser.objects.create(phone=request.data["phone"], first_name=request.data["first_name"], last_name=request.data["last_name"], password=request.data["password"])
        return Response(200)



@api_view(['POST'])
def forgetPassword(request):
    user = User.objects.get(username=request.data["username"])
    user.set_password(request.data["password"])
    user.save()
    return Response()


@api_view(['GET'])
def getPosition(request):
    staff = False
    user = User.objects.get(name=request.user)
    if user.is_staff == True:
        staff = True
    else:
        staff = False
    name = user.name
    return Response({
        "staff": staff ,
        "name": name ,
    })


@api_view(['GET'])
def productDetail(request, category, id):
    if ProductIdentity.objects.filter(id=id).exists():
        if ProductIdentity.objects.get(id=id).weight_dependency == False:
            intendedProduct = ProductIdentity.objects.filter(id=id).first()
            productSerializer = ProductIdentitySerializer(intendedProduct)
            return Response({
                "product": productSerializer.data
            })
        else:
            intendedProduct = ProductIdentity.objects.filter(id=id).first()
            productSerializer = ProductIdentitySerializer(intendedProduct)
            productStock = Product.objects.get(product=intendedProduct).stock
            if request.user.is_authenticated:
                if OrderItem.objects.filter(product__product__name=ProductIdentity.objects.get(id=id).name,selected_by=request.user).exists():
                    quantity = OrderItem.objects.get(product__product__name=ProductIdentity.objects.get(id=id). name, selected_by=request.user).quantity
                    previousPrice = ProductIdentity.objects.get(id=id).price1 * quantity
                    previousDiscountedPrice = ProductIdentity.objects.get(id=id).price2 * quantity
                    return Response({
                        "product": productSerializer.data,
                        "quantity": quantity,
                        'previousPrice': previousPrice,
                        'previousDiscountedPrice': previousDiscountedPrice,
                        'productStock': productStock
                    })
                else:
                    previousPrice = ProductIdentity.objects.get(id=id).price1
                    previousDiscountedPrice = ProductIdentity.objects.get(id=id).price2
                    return Response({
                        "product": productSerializer.data,
                        "quantity": 1,
                        'previousPrice': previousPrice,
                        'previousDiscountedPrice': previousDiscountedPrice,
                        'productStock': productStock
                    })
            else:
                previousPrice = ProductIdentity.objects.get(id=id).price1 
                previousDiscountedPrice = ProductIdentity.objects.get(id=id).price2
                return Response({
                        "product": productSerializer.data,
                        "quantity": 1,
                        'previousPrice': previousPrice,
                        'previousDiscountedPrice': previousDiscountedPrice,
                        'productStock': productStock
                    })
    else:
        raise Http404


@api_view(['POST'])
def relatedProducts(request):
    if ProductIdentity.objects.filter(category__name = request.data['category']).exists():
        relatedProducts = ProductIdentity.objects.filter(category__name = request.data['category'])
        products = []
        for relatedProduct in relatedProducts:
            if Product.objects.filter(product=relatedProduct).exists():
                products.append(relatedProduct)
            else:
                pass
        productsSerializer = ProductIdentitySerializer(products, many=True)
        return Response({
            "products": productsSerializer.data
        })
    else:
        raise Http404


@api_view(['GET', 'POST'])
def productComments(request, category, id):
    if request.method == 'GET':
        if ProductComment.objects.filter(productId = id).exists():
            comments = reversed(ProductComment.objects.filter(productId = id))
            commentsSerializer = ProductCommentSerializer(comments, many=True)
            return Response({
            "comments": commentsSerializer.data
            })
        else:
            return Response()
    if request.method == "POST":
        token = Token.objects.get(key=request.data['token'])
        ProductComment.objects.create(productId=id, star=request.data["star"] , comment=request.data["comment"], created_by=token.user)
        comments = ProductComment.objects.all()
        totalStars = 0
        commentsNumber = 0
        for comment in comments:
            if comment.productId == id:
                commentsNumber += 1
                totalStars += int(comment.star)
        product=ProductIdentity.objects.get(id=id)
        product.star = round(totalStars/commentsNumber, 1)
        product.save()
        return Response()

@api_view(['POST'])
def cooperation(request):
    Cooperation.objects.create(name=request.data["name"], phone=request.data["phone"], description=request.data["description"], seen=False)
    return Response()