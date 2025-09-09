
from django.db import models

class Promotion(models.Model):
    """Khuyến mãi cho sản phẩm"""
    name = models.CharField("Tên khuyến mãi", max_length=100)
    description = models.TextField("Mô tả", blank=True)
    discount_percent = models.PositiveIntegerField("Phần trăm giảm giá", default=0)
    start_date = models.DateTimeField("Ngày bắt đầu")
    end_date = models.DateTimeField("Ngày kết thúc")
    products = models.ManyToManyField('Product', related_name='promotions', blank=True)

    class Meta:
        verbose_name = "Khuyến mãi"
        verbose_name_plural = "Khuyến mãi"

    def __str__(self):
        return self.name

class Category(models.Model):
    """Danh mục sản phẩm mỹ phẩm"""
    name = models.CharField("Tên danh mục", max_length=100, unique=True)
    description = models.TextField("Mô tả", blank=True)

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"

    def __str__(self):
        return self.name

class Product(models.Model):
    """Sản phẩm mỹ phẩm"""
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField("Tên sản phẩm", max_length=200)
    brand = models.CharField("Thương hiệu", max_length=100, blank=True)
    description = models.TextField("Mô tả", blank=True)
    price = models.DecimalField("Giá bán", max_digits=12, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField("Tồn kho", default=0)
    created_at = models.DateTimeField("Ngày thêm", auto_now_add=True)
    updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)
    is_active = models.BooleanField("Còn kinh doanh", default=True)
    image = models.ImageField("Ảnh sản phẩm", upload_to="products/", blank=True, null=True)
    is_promotion = models.BooleanField("Khuyến mãi", default=False)
    is_flash_sale = models.BooleanField("Flash Sale", default=False)
class News(models.Model):
    """Tin tức làm đẹp, mỹ phẩm"""
    title = models.CharField("Tiêu đề", max_length=200)
    content = models.TextField("Nội dung")
    created_at = models.DateTimeField("Ngày đăng", auto_now_add=True)

    class Meta:
        verbose_name = "Tin tức"
        verbose_name_plural = "Tin tức"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Store(models.Model):
    """Cửa hàng hệ thống"""
    name = models.CharField("Tên cửa hàng", max_length=100)
    address = models.CharField("Địa chỉ", max_length=255)
    phone = models.CharField("Điện thoại", max_length=20, blank=True)

    class Meta:
        verbose_name = "Cửa hàng"
        verbose_name_plural = "Cửa hàng"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

    def __str__(self):
        return self.name

    @classmethod
    def search(cls, query=None, category=None):
        queryset = cls.objects.all()
        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) | 
                models.Q(brand__icontains=query)
            )
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

    def __str__(self):
        return self.name

class Customer(models.Model):
    """Thông tin khách hàng"""
    full_name = models.CharField("Họ tên", max_length=100)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Điện thoại", max_length=20, blank=True)
    address = models.CharField("Địa chỉ", max_length=255, blank=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)

    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"

    def __str__(self):
        return self.full_name

class Order(models.Model):
    """Đơn hàng"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name="orders")
    order_date = models.DateTimeField("Ngày đặt hàng", auto_now_add=True)
    shipped_date = models.DateTimeField("Ngày giao hàng", null=True, blank=True)
    status = models.CharField(
        "Trạng thái",
        max_length=20,
        choices=[
            ("pending", "Chờ xác nhận"),
            ("confirmed", "Đã xác nhận"),
            ("shipped", "Đã gửi hàng"),
            ("completed", "Hoàn thành"),
            ("canceled", "Đã hủy")
        ],
        default="pending"
    )
    shipping_address = models.CharField("Địa chỉ giao hàng", max_length=255, default="", blank=True)
    total_amount = models.DecimalField("Tổng tiền", max_digits=14, decimal_places=2, default=0)
    note = models.TextField("Ghi chú", blank=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ["-order_date"]

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.customer.full_name}"

    def calculate_total(self):
        """Tính tổng tiền đơn hàng từ các items"""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

class OrderItem(models.Model):
    """Chi tiết đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_items")
    product_name = models.CharField("Tên sản phẩm", max_length=200)  # Lưu tên sản phẩm tại thời điểm đặt hàng
    price = models.DecimalField("Đơn giá", max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField("Số lượng", default=1)

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.product_name} ({self.quantity})"

    @property
    def subtotal(self):
        """Tính thành tiền"""
        return self.price * self.quantity
