from django.urls import path
from .views import ProductsList, ProductDetailsView, CategoryList, home, products_page, categories_page, CartList, WishList, OrderList, ReviewList

urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductsList.as_view()),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category-details'),
    path('wishlist/', WishList.as_view(), name='wishlist'),
    path('cart/', CartList.as_view(), name='cart'),
    path('orders/', OrderList.as_view(), name='orders'),
    path('reviews/', ReviewList.as_view(), name='reviews'),
    path('products-page/', products_page, name='products-page'),
    path('categories-page/', categories_page, name='categories-page'),
]
