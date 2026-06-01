from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

from . import views

from .views import show_api_data


router = DefaultRouter()
router.register(r'banners', TblBannerView)
router.register(r'imagetypes', ImageTypeView)
router.register(r'images', ImageView)
router.register(r'menus', MenuView)
router.register(r'menudetails', MenuDetailView)

#================================
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'productdetails', ProductDetailViewSet)
router.register(r'productdetailimages', ProductDetailImageViewSet)

router.register(r'qrcodes', QRCodeViewSet)
router.register(r'orders', OrderViewSet)
    

urlpatterns = [
    path("",views.index, name="index"),
    path("category/",views.category, name="category"),
    # path("product_detail/",views.productDetail, name="product_detail"),
    
    path('product_detail/<int:pk>/', views.productDetail, name='product_detail'),
    
    path("blog/",views.blog, name="blog"),
    path("blog_detail/<int:blog_id>/",views.blogDetail, name="blog_detail"),
    
    path("contact/",views.contact, name="contact"),
    
    
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),  # <-- Confirm this is here
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    
    
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:pk>/', views.confirmation, name='confirmation'),
    
    path("login/",views.login, name="login"),
    path("elements/",views.elements, name="elements"),
    path("tracking/",views.tracking, name="tracking"),
    path("login/",views.login, name="login"),
    
    path('', include(router.urls)),
    path('api/show/', show_api_data, name='show_data'),
    path('api/banner_crud/', show_banner_crud, name='banner_crud'),
    path('api/image_menu_crud/', show_image_menu_crud, name='image_menu_crud'),
    path('api/show_menu_detail_crud/', show_menu_detail_crud, name='show_menu_detail_crud'),
    path('api/CarouselImageAPI/', CarouselImageAPI, name='CarouselImageAPI'),
    path('api/MenuClickToLoadMenuDetail/', MenuClickToLoadMenuDetail, name='MenuClickToLoadMenuDetail'),
    
    #==================================
    
    path('api/ListProductWithAddToCartCheckoutOrder/', ListProductWithAddToCartCheckoutOrder, name='ListProductWithAddToCartCheckoutOrder'),
    
    path('api/protected_product_api/', protected_product_api, name='protected_product_api'),

]

