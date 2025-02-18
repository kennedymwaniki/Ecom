from django.shortcuts import render
from rest_framework import generics
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


def home(request):
    routes = [
        {
            'name': 'Products',
            'description': 'View and manage products in the store',
            'api_url': '/api/products/',
            'page_url': '/products-page/'
        },
        {
            'name': 'Categories',
            'description': 'Browse products by categories',
            'api_url': '/api/categories/',
            'page_url': '/categories-page/'
        },
    ]
    return render(request, 'ecom/home.html', {'routes': routes})


def products_page(request):
    products = Product.objects.all()
    return render(request, 'ecom/products.html', {'products': products})


def categories_page(request):
    categories = Category.objects.all()
    return render(request, 'ecom/categories.html', {'categories': categories})


class ProductsList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailsView(generics.RetrieveUpdateDestroyAPIView):
    # het the product by id
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        # get the object by id
        return Product.objects.get(id=self.kwargs.get('pk'))


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
