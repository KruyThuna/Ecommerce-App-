
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

#================================= API Model ==========================================

class TblBanner(models.Model):
    BannerName = models.CharField(max_length=200, null=True)
    BannerImage = models.ImageField(upload_to='images/Banners/',null=True,blank=True)
    BannerDate = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):          
        return f'{self.id} {self.BannerName}'

class ImageType(models.Model): 
    ImageTypeName = models.CharField(max_length=200, null=True) 
    ImageTypeDate = models.DateTimeField(auto_now_add=True, null=True) 
    def __str__(self):          
        return f'{self.id} {self.ImageTypeName}'
    
class Image(models.Model): 
    ImageName = models.CharField(max_length=200, null=True) 
    ImageURL = models.ImageField(upload_to='images/Dynamic/',null=True,blank=True) 
    ImageLink = models.CharField(max_length=200, null=True) 
    ImageTypeID = models.ForeignKey(ImageType, on_delete=models.CASCADE, null=True) 
    Active = models.CharField(max_length=200, null=True) 
    ImageDate = models.DateTimeField(auto_now_add=True, null=True) 
    def __str__(self):          
        return f'{self.ImageName}'
    
class Menu(models.Model):
    MenuNameKH = models.CharField(max_length=200, null=True)
    MenuNameEN = models.CharField(max_length=200, null=True)
    OrderBy = models.IntegerField(blank=True,null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.id} | {self.MenuNameKH} | {self.MenuNameEN} | {self.CreatedDate}'
    
class MenuDetail(models.Model):
    MenuID = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    Description =  RichTextUploadingField(null=True)
    MenuDetailDate = models.DateTimeField (auto_now_add=True, null=True)
    def __str__(self):         
        return self.MenuID.MenuNameEN

#================================= Main Model ==========================================

class BlogCategory(models.Model):
    blogCategoryName = models.CharField(max_length=200, null=True)
    blogCategoryImage = models.ImageField(upload_to='images/BlogCategories/',null=True,blank=True)
    def __str__(self):         
        return f'{self.id} - {self.blogCategoryName}'
    

class Blog(models.Model):
    blogName = models.CharField(max_length=200, null=True)
    blogCategoryID = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True) 
    blogDescript =  RichTextUploadingField(null=True)
    blogImage = models.ImageField(upload_to='images/Blogs/',null=True,blank=True)
    blogDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.id} - {self.blogName} '

class BlogDetail(models.Model):
    blogDetailName = models.CharField(max_length=200, null=True)
    blogID = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    Description =  RichTextUploadingField(null=True)
    Information = RichTextUploadingField(null=True)
    Reviews = RichTextUploadingField(null=True)
    blogDetailDate = models.DateTimeField (auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.blogID.blogName} - {self.blogDetailName}'
   
class BlogDetailImage(models.Model):
    blogDetailImageName = models.CharField(max_length=200, null=True)
    blogID = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    blogDetailImage = models.ImageField(upload_to='images/BlogDetail/',null=True,blank=True)
    imageDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.blogID.blogName} - {self.blogDetailImageName}'

#=--------------------


class Brand (models.Model):
    brandName = models.CharField(max_length=200, null=True)
    brandImage = models.ImageField(upload_to='images/Brands/',null=True,blank=True)
    def __str__(self):         
        return f'{self.id} - {self.brandName}'
    

class Category(models.Model):
    categoryName = models.CharField(max_length=200, null=True)
    categoryImage = models.ImageField(upload_to='images/Categories/',null=True,blank=True)
    def __str__(self):         
        return f'{self.id} - {self.categoryName}'
    
class ProductStock(models.Model):
    productStockName = models.CharField(max_length=200, null=True)
    
    def __str__(self):         
        return f'{self.id} - {self.productStockName}'
    
class Product(models.Model):
    productName = models.CharField(max_length=200, null=True)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE, null=True) 
    brandid = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    productStockID = models.ForeignKey(ProductStock, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=200, null=True)
    productDescript =  RichTextUploadingField(null=True)
    weight = models.CharField(max_length=200, null=True)
    availability = models.CharField(max_length=200, null=True)
    shipping = models.CharField(max_length=200, null=True)
    productImage = models.ImageField(upload_to='images/Products/',null=True,blank=True)
    productDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.id} - {self.productName} '

class ProductDetail(models.Model):
    productDetailName = models.CharField(max_length=200, null=True)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    Description =  RichTextUploadingField(null=True)
    Information = RichTextUploadingField(null=True)
    Reviews = RichTextUploadingField(null=True)
    productDetailDate = models.DateTimeField (auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.productID.productName} - {self.productDetailName}'
    
class ProductDetailImage(models.Model):
    productDetailImageName = models.CharField(max_length=200, null=True)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    productDetailImage = models.ImageField(upload_to='images/productDetail/',null=True,blank=True)
    imageDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.productID.productName} - {self.productDetailImageName}'


class QRCode(models.Model):
    qrName = models.CharField(max_length=100)
    qrImage = models.ImageField(upload_to='images/qrcodes/')
    def __str__(self): 
        return f'{self.qrName}'

class Order(models.Model):
    customerName = models.CharField(max_length=100)
    customerPhone = models.CharField(max_length=20)
    orderDate = models.DateTimeField(auto_now_add=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    QRCodeInvoice = models.ImageField(upload_to='images/QRCodeInvoice/',null=True,blank=True)
    def __str__(self):
        return f'Order {self.id} by {self.customerName} on {self.orderDate}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    productName = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    def __str__(self):
        return f'{self.productName} - {self.qty} pcs'
    
# ================================= Token Model ==========================================

class AccessToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.token