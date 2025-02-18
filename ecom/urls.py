from django.urls import path
from .views import ProductsList, ProductDetailsView, CategoryList, home, products_page, categories_page

urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductsList.as_view()),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('categories/', CategoryList.as_view()),
    path('products-page/', products_page, name='products-page'),
    path('categories-page/', categories_page, name='categories-page'),
]
