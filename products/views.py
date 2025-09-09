from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Product, Category, Customer, Order, OrderItem
from .forms import ProductForm, ProductSearchForm, CartAddProductForm, CustomerForm, OrderForm
from .cart import Cart
from django.contrib.auth.decorators import login_required

# Trang mở rộng
def promotions(request):
    promotions = [
        {'title': 'Giảm giá 50%', 'desc': 'Áp dụng cho đơn từ 500k'},
        {'title': 'Mua 1 tặng 1', 'desc': 'Chỉ áp dụng cho sản phẩm dưỡng da'},
    ]
    return render(request, 'products/promotions.html', {'promotions': promotions})

def flash_sale(request):
    flash_sales = [
        {'name': 'Son lì', 'price': 100000, 'old_price': 200000},
    ]
    return render(request, 'products/flash_sale.html', {'flash_sales': flash_sales})

def news(request):
    news_list = [
        {'title': 'Ra mắt sản phẩm mới', 'content': 'Chi tiết về sản phẩm mới...'},
    ]
    return render(request, 'products/news.html', {'news_list': news_list})

def brands(request):
    brands = [
        {'name': 'Maybelline'},
        {'name': 'L\'Oreal'},
    ]
    return render(request, 'products/brands.html', {'brands': brands})

def stores(request):
    stores = [
        {'name': 'Cửa hàng 1', 'address': '123 Đường A'},
        {'name': 'Cửa hàng 2', 'address': '456 Đường B'},
    ]
    return render(request, 'products/stores.html', {'stores': stores})

def order_lookup(request):
    orders = None
    if request.method == 'POST':
        code = request.POST.get('order_code')
        if code == '123':
            orders = [{'code': '123', 'status': 'Đang giao'}]
        else:
            orders = []
    return render(request, 'products/order_lookup.html', {'orders': orders})

# Trang giới thiệu
def about(request):
    return render(request, 'products/about.html')

# Trang liên hệ
def contact(request):
    return render(request, 'products/contact.html')

# Trang chính sách
def policy(request):
    return render(request, 'products/policy.html')
# Quản lý đơn hàng cho admin/người bán
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/login/')
def admin_order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'products/admin_order_list.html', {'orders': orders})

@staff_member_required(login_url='/login/')
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products/admin_order_detail.html', {'order': order})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Product, Category, Customer, Order, OrderItem
from .forms import ProductForm, ProductSearchForm, CartAddProductForm, CustomerForm, OrderForm
from .cart import Cart
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def home(request):
    products = Product.objects.all().order_by('-created_at')[:9]
    categories = Category.objects.all()
    # promotions = Promotion.objects.all().order_by('-start_date')[:3]  # Xóa nếu Promotion chưa có
    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
        # 'promotions': promotions,
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    form = CartAddProductForm()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'form': form,
        # 'recommended_products': [],
    })

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Sản phẩm "{product.name}" đã được tạo thành công!')
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Thêm sản phẩm mới'
    })

def product_edit(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sản phẩm "{product.name}" đã được cập nhật!')
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'product': product,
        'title': 'Chỉnh sửa sản phẩm'
    })

def product_delete(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Sản phẩm "{product_name}" đã được xóa!')
        return redirect('product_list')

    return render(request, 'products/product_confirm_delete.html', {'product': product})

# Chức năng giỏ hàng
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'products/cart/detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

# Chức năng đặt hàng
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('product_list')

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        order_form = OrderForm(request.POST)

        if customer_form.is_valid() and order_form.is_valid():
            try:
                customer = Customer.objects.get(email=customer_form.cleaned_data['email'])
                customer_form = CustomerForm(request.POST, instance=customer)
                customer = customer_form.save()
            except Customer.DoesNotExist:
                customer = customer_form.save()

            order = order_form.save(commit=False)
            order.customer = customer
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    price=item['price'],
                    quantity=item['quantity']
                )

            order.calculate_total()

            # Gửi email xác nhận đơn hàng (có thể bỏ qua nếu chưa cấu hình)
            # from django.core.mail import send_mail
            # subject = f'Xác nhận đơn hàng #{order.id} tại Cosmetic Shop'
            # message = f'Cảm ơn bạn đã đặt hàng tại Cosmetic Shop!\n\nMã đơn hàng: #{order.id}\nTổng tiền: {order.total_amount}₫\nTrạng thái: {order.get_status_display()}\n\nChúng tôi sẽ liên hệ và giao hàng sớm nhất.'
            # recipient = customer.email
            # send_mail(subject, message, None, [recipient], fail_silently=True)

            cart.clear()

            messages.success(request, f'Đơn hàng của bạn đã được tạo thành công! Mã đơn hàng: #{order.id}')
            return render(request, 'products/orders/created.html', {'order': order})
    else:
        customer_form = CustomerForm()
        order_form = OrderForm()

    return render(request, 'products/orders/create.html', {
        'cart': cart,
        'customer_form': customer_form,
        'order_form': order_form
    })

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products/orders/detail.html', {'order': order})

# Chức năng người dùng
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'products/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_dashboard(request):
    return render(request, 'products/user_dashboard.html')

@login_required
def user_orders(request):
    try:
        customer = Customer.objects.get(email=request.user.email)
        orders = Order.objects.filter(customer=customer).order_by('-order_date')
    except Customer.DoesNotExist:
        orders = []
    return render(request, 'products/user_orders.html', {'orders': orders})