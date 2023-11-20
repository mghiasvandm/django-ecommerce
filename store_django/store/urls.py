from django.urls import path, include
from .views import ArticleViewSet, index, fake, otp, forgetPassword, getPosition, productDetail, relatedProducts, productComments, cooperation, UserViewSet, editProfile, productAmmounts, countArticleDownloads, countCommentLikes, getFreeSpecialProducts, productStockAndQuantityAndPrices, addToCart, showCart, checkProfile, editBasket, totalPrices, deleteOrder, basketLength, deleteComment

from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()

app_name= "store"

router.register('articles', ArticleViewSet, basename='articles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('index', index),
    path('fake', fake),
    path('otp', otp),
    path('forget_password', forgetPassword),
    path('get_position', getPosition),
    path('products', relatedProducts),
    path('product/<str:category>/<int:id>', productDetail),
    path('product_comments/<str:category>/<int:id>', productComments),
    path('cooperation', cooperation),
    path('edit_profile', editProfile),
    path('product_ammounts/<int:id>', productAmmounts),
    path('product_stock_and_quantity_and_prices/<int:id>/<str:ammount>', productStockAndQuantityAndPrices),
    path('count_article_downloads', countArticleDownloads),
    path('count_comment_likes', countCommentLikes),
    path('few_special_products', getFreeSpecialProducts),
    path('add_to_cart/<int:id>', addToCart),
    path('show_cart', showCart),
    path('check_profile', checkProfile),
    path('edit_basket', editBasket),
    path('total_prices', totalPrices),
    path('delete_order', deleteOrder),
    path('basket_length', basketLength),
    path('delete_comment/<str:category>/<int:id>', deleteComment),
]



