from django.db import models
from django.contrib.auth.models import User
# Remove AbstractUser import since we won't use it


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shipping_address')
    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=200)


class Orders(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, related_name='shipping_address')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product')
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='PENDING', choices=[
        ('PENDING', 'PENDING'),
        ('SHIPPED', 'SHIPPED'),
        ('DELIVERED', 'DELIVERED'),
        ('CANCELLED', 'CANCELLED')
    ])


class Payments(models.Model):
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=100, choices=[
        ('M-PESA', 'M-PESA'),
        ('Paypal', 'Paypal'),
    ])
    transaction_id = models.CharField(max_length=100)

    @property
    def amount(self):
        return self.order.amount


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating} by {self.user.username}"


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def quantity(self):
        return self.product.stock

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"
