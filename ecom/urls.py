from django.urls import path
from .views import ProductsList, ProductDetailsView, CategoryList, home, products_page, categories_page, CartList, WishList, OrderList, ReviewList, add_to_cart, add_to_wishlist, view_cart, view_wishlist, remove_item_from_cart, remove_from_wishlist
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductsList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category-details'),
    path('wishlist/<int:pk>/', WishList.as_view(), name='wishlist-detail'),
    path('Cart/', CartList.as_view(), name='cart'),
    path('orders/', OrderList.as_view(), name='orders'),
    path('reviews/', ReviewList.as_view(), name='reviews'),
    path('products-page/', products_page, name='products-page'),
    path('categories-page/', categories_page, name='categories-page'),
    # //prettier-ignore
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/',
         remove_item_from_cart, name='remove-from-cart'),
    path('add-to-wishlist/<int:pk>/', add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/<int:product_id>/',
         remove_from_wishlist, name='remove-from-wishlist'),
    path('cart/', view_cart, name='view-cart'),
    path('wishlist/', view_wishlist, name='view-wishlist'),
    path('api/wishlist/', WishList.as_view(), name='wishlist-api'),
    # Add explicit logout path with next parameter
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
