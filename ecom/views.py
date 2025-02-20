from django.shortcuts import render
from rest_framework import generics
from .models import Product, Category, Wishlist, Orders, Payments, Review, Cart, UserProfile
from .serializers import ProductSerializer, CategorySerializer, WishListSerializer, CartSerializer, OrderSerializer, PaymentSerializer, ReviewSerializer


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


class WishList(generics.RetrieveAPIView):
    serializer_class = WishListSerializer
    queryset = Wishlist.objects.all()


class WishListDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishListSerializer
    queryset = Wishlist.objects.all()


class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class PaymentList(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailsList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()


# get reviews of a particular
