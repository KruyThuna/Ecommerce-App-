from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(TblBanner)
admin.site.register(Image)
admin.site.register(ImageType)
admin.site.register(Menu)
admin.site.register(MenuDetail)

#=================================

admin.site.register(Brand)
admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(ProductStock)
# admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(ProductDetailImage)
admin.site.register(QRCode)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(AccessToken)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoryName')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'productName', 'categoryID', 'price', 'productStockID', 'productDate')
