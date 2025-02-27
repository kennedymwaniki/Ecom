from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import generics
from .models import Product, Category, Wishlist, Orders, Payments, Review, Cart, UserProfile
from .serializers import ProductSerializer, CategorySerializer, WishListSerializer, CartSerializer, OrderSerializer, PaymentSerializer, ReviewSerializer
from .forms import RegistrationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductDetailsView(generics.RetrieveUpdateDestroyAPIView):
    # het the product by id
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # get the object by id
        return Product.objects.get(id=self.kwargs.get('pk'))


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class WishList(generics.ListAPIView):  # Changed from RetrieveAPIView to ListAPIView
    serializer_class = WishListSerializer

    def get_queryset(self):
        # Return only the current user's wishlist items
        return Wishlist.objects.filter(user=self.request.user)


class WishListDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishListSerializer
    queryset = Wishlist.objects.all()

    def get_object(self):
        return Wishlist.objects.get(id=self.request.kwargs.get('pk'))


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


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


# get reviews of a particular product
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_object(self):
        return Review.objects.get(id=self.kwargs.get('pk'))


# registration
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()

            # Update the existing profile instead of creating a new one
            phone_number = form.cleaned_data.get("phone_number")
            # Access the profile created by signal
            user.profile.phone_number = phone_number
            user.profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add a product to the user's cart"""
    try:
        product = Product.objects.get(id=product_id)

        # Check if product is already in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product
        )

        if created:
            message = "Product added to cart successfully!"
        else:
            message = "Product is already in your cart!"

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': message})
        else:
            return redirect('products-page')

    except Product.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        else:
            return redirect('products-page')


@login_required
@require_POST
def add_to_wishlist(request, pk):
    """Add a product to the user's wishlist"""
    try:
        product = Product.objects.get(id=pk)

        # Check if product is already in wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        if created:
            message = "Product added to wishlist successfully!"
        else:
            message = "Product is already in your wishlist!"

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': message})
        else:
            return redirect('products-page')

    except Product.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        else:
            return redirect('products-page')


# Views to display user's cart and wishlist
@login_required
def view_cart(request):
    """View the user's cart"""
    cart_items = Cart.objects.filter(
        user=request.user).select_related('product')

    # Calculate the total price of all cart items
    cart_total = sum(item.product.price for item in cart_items)

    return render(request, 'ecom/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })


@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user).select_related('product')
    return render(request, 'ecom/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
@require_POST
def remove_item_from_cart(request, product_id):
    """Remove a product from the user's cart"""
    try:
        cart_item = Cart.objects.get(
            user=request.user,
            product_id=product_id
        )

        cart_item.delete()
        message = "Product removed from cart successfully!"

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': message})
        else:
            return redirect('view-cart')
    except Cart.DoesNotExist:
        message = "Product not found in your cart."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': message}, status=404)
        else:
            return redirect('view-cart')


@login_required
@require_POST
def remove_from_wishlist(request, product_id):
    try:
        wishlist_item = Wishlist.objects.get(
            user=request.user,
            product_id=product_id
        )

        wishlist_item.delete()
        message = "Product removed from wishlist successfully"
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({'status': 'success', 'message': 'Product removed from wishlist successfully'}, status=200)
        else:
            return redirect('view-wishlist')

    except Wishlist.DoesNotExist:  # Fixed typo here
        message = "Product not found in your wishlist"
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': message}, status=404)
        else:
            return redirect('view-wishlist')
