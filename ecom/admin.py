from django.contrib import admin
from .models import Product, Cart, Wishlist, Review, Orders, Category, Payments, UserProfile

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Payments)
admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(Orders)
admin.site.register(UserProfile)
