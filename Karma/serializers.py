from rest_framework import serializers
from .models import TblBanner, ImageType, Image, Menu, MenuDetail, Category, Product, ProductDetail, ProductDetailImage, QRCode, OrderItem, Order

import json 


class TblBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblBanner
        fields = '__all__'

class ImageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageType
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDetail
        fields = '__all__'
             
#==================================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    categoryID = CategorySerializer(read_only=True)
    categoryID_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='categoryID', write_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    productID = ProductSerializer(read_only=True)
    productID_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='productID', write_only=True)
    class Meta:
        model = ProductDetail
        fields = '__all__'

class ProductDetailImageSerializer(serializers.ModelSerializer):
    productID = ProductSerializer(read_only=True)
    productID_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='productID', write_only=True)

    class Meta:
        model = ProductDetailImage
        fields = '__all__'

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_items(self, obj):
        items = obj.items.all()
        return OrderItemSerializer(items, many=True).data

    def create(self, validated_data):
        request = self.context['request']
        items_json = request.data.get('items')
        items_data = json.loads(items_json) if items_json else []

        # Pop items key out, rest is for Order creation (QRCodeInvoice will be in validated_data as file)
        validated_data.pop('items', None)

        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order

