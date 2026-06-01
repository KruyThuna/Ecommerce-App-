from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from django.core.paginator import Paginator

from decimal import Decimal, InvalidOperation

from django import forms

from .forms import CheckoutForm
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
from Karma.authentication import QueryParamAccessTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.
from rest_framework import viewsets
from .models import *
from .serializers import *

# ========================================================

def index(request):
    latest_products = Product.objects.filter(
        productStockID__productStockName__iexact='Latest Products'
    )[:8]
    
    coming_products = Product.objects.filter(
        productStockID__productStockName__iexact='Coming Products'
    )[:8]
    
    context = {
        'latest_products': latest_products, 
        'coming_products': coming_products 
    }

    return render(request, 'main-file/index.html', context)

def productDetail(request, pk):  # <-- receives product ID
    product = get_object_or_404(Product, pk=pk)
    detail_images = ProductDetailImage.objects.filter(productID=product)
    product_detail = ProductDetail.objects.filter(productID=product).first()

    context = {
        'product': product,
        'detail_images': detail_images,
        'product_detail': product_detail, 
    }
    return render(request, 'main-file/product-detail.html', context)




def blog(request):
    blogs = Blog.objects.all().order_by('-blogDate')
    categories = BlogCategory.objects.all()

    paginator = Paginator(blogs, 4)  # Show 4 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'main-file/blog.html', context)

# Blog detail view
def blogDetail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    context = {
        'blog': blog
    }
    return render(request, 'main-file/blog-detail.html',context)



def category(request):
    stock_filter = request.GET.get('stock')
    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')

    products = Product.objects.all()

    # Apply filters
    if stock_filter:
        products = products.filter(productStockID__productStockName__iexact=stock_filter)

    if brand_filter:
        products = products.filter(brandid_id=brand_filter)

    if category_filter:
        products = products.filter(categoryID_id=category_filter)

    # Paginate products: 6 per page
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Create page range list for dropdown
    page_range = list(paginator.page_range)

    context = {
        'products': page_obj,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'stock_filter': stock_filter,
        'brand_filter': brand_filter,
        'category_filter': category_filter,
        'page_range': page_range,  # For your second dropdown
    }

    return render(request, 'main-file/category.html', context)


from django.shortcuts import render, get_object_or_404

def cart(request):
    cart = request.session.get('cart', {})  # {product_id: quantity (string)}
    items = []
    total = 0.0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid))

        # Parse quantity
        try:
            qty = int(qty)
        except (ValueError, TypeError):
            qty = 1

        # Parse price
        try:
            price = float(product.price)
        except (ValueError, TypeError):
            price = 0.0

        item_total = price * qty

        items.append({
            'product': product,
            'quantity': qty,
            'item_total': item_total,
        })

        total += item_total

    # Parse shipping from the first product (or default to 0)
    try:
        shipping_str = items[0]['product'].shipping if items else "0"
        shipping = float(shipping_str)
    except (ValueError, TypeError):
        shipping = 0.0

    context = {
        'items': items,
        'subtotal': total,
        'shipping': shipping,
        'grand_total': total + shipping,
    }

    return render(request, 'main-file/cart.html', context)


@require_POST
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    pid = str(pk)
    cart[pid] = cart.get(pid, 0)
    cart[pid] = int(cart[pid]) + quantity

    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def update_cart(request, pk):
    cart = request.session.get('cart', {})
    quantity = request.POST.get('quantity')

    try:
        quantity = int(quantity)
        if quantity < 1:
            cart.pop(str(pk), None)
        else:
            cart[str(pk)] = quantity
    except (ValueError, TypeError):
        pass  # skip invalid input

    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart')



# ===========================================================

@csrf_exempt
def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0.0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        try:
            qty = int(qty)
        except (ValueError, TypeError):
            qty = 1

        try:
            price = float(product.price)
        except (ValueError, TypeError):
            price = 0.0

        item_total = price * qty
        total += item_total

        items.append({
            'product': product,
            'quantity': qty,
            'price': price,
            'item_total': item_total
        })

    if request.method == 'POST':
        form = CheckoutForm(request.POST, request.FILES)
        if form.is_valid():
            # Save order with uploaded image
            order = Order.objects.create(
                customerName=form.cleaned_data['name'],
                customerPhone=form.cleaned_data['phone'],
                totalAmount=Decimal(total),
                QRCodeInvoice=form.cleaned_data.get('payment_proof')  # Save image
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    productName=item['product'].productName,
                    price=item['price'],
                    qty=item['quantity']
                )

            request.session['cart'] = {}
            return redirect('confirmation', pk=order.pk)
    else:
        form = CheckoutForm()

    qrcodes = QRCode.objects.all()

    context = {
        'form': form,
        'items': items,
        'total': total,
        'qrcodes': qrcodes,
    }
    return render(request, 'main-file/checkout.html', context)


def confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = OrderItem.objects.filter(order=order)

    def to_decimal(value):
        try:
            return Decimal(value)
        except (InvalidOperation, TypeError):
            return Decimal('0.00')

    subtotal = sum(to_decimal(item.price) * item.qty for item in items)
    shipping = to_decimal('50.00')
    grand_total = subtotal + shipping

    context = {
        'order': order,
        'products': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'main-file/confirmation.html', context)

def contact(request):
    return render(request, 'main-file/contact.html') 


# ===========================================================

def elements(request):
    return render(request, 'main-file/elements.html') 

def login(request):
    return render(request, 'main-file/login.html') 

def tracking(request):
    return render(request, 'main-file/tracking.html') 


# =========================================================


class TblBannerView(viewsets.ModelViewSet):
    queryset = TblBanner.objects.all()
    serializer_class = TblBannerSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        return queryset

class ImageTypeView(viewsets.ModelViewSet):
    queryset = ImageType.objects.all()
    serializer_class = ImageTypeSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        return queryset

class ImageView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        return queryset

class MenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        return queryset

class MenuDetailView(viewsets.ModelViewSet):
    queryset = MenuDetail.objects.all()
    serializer_class = MenuDetailSerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        return queryset

    
def show_api_data(request):
    return render(request, 'api-files/show_data.html')

def show_banner_crud(request):
    return render(request, 'api-files/show_banner_crud.html')

def show_image_menu_crud(request):
    return render(request, 'api-files/show_image_menu_crud.html')

def show_menu_detail_crud(request):
    return render(request, 'api-files/show_menu_detail_crud.html')

def CarouselImageAPI(request):
    return render(request, 'api-files/CarouselImageAPI.html')

def MenuClickToLoadMenuDetail(request):
    return render(request, 'api-files/MenuClickToLoadMenuDetail.html')

#================================

def ListProductWithAddToCartCheckoutOrder(request):
    return render(request, 'api-files/ListProductWithAddToCartCheckoutOrder.html')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        return queryset

    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset
    
    
class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    
    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        product_id = self.request.query_params.get('productID')
        if product_id:
            return ProductDetail.objects.filter(productID=product_id)
        return ProductDetail.objects.all()
    
class ProductDetailImageViewSet(viewsets.ModelViewSet):
    queryset = ProductDetailImage.objects.all()
    serializer_class = ProductDetailImageSerializer
    
    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")

        product_id = self.request.query_params.get('productID')
        if product_id:
            return self.queryset.filter(productID__id=product_id)
        return self.queryset



class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
    
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        return queryset


# ===================================

def protected_product_api(request):
    token = request.GET.get('token')
    if not token:
        return JsonResponse({'error': 'Token is required'}, status=400)

    if not AccessToken.objects.filter(token=token, is_active=True).exists():
        return JsonResponse({'error': 'Invalid or inactive token'}, status=403)
    
    # Query all items
    products = Product.objects.all().values('id', 'categoryID', 'productName', 'price', 'productDescript','weight', 'availability', 'shipping', 'productImage', 'productDate')
    return JsonResponse({'products': list(products)})