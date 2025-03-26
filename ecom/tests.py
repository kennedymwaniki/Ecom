from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, Category, Cart, Wishlist
from decimal import Decimal


class ApiTests(TestCase):
    def setUp(self):
        # Create test client
        self.client = Client()
        self.api_client = APIClient()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Category Description'
        )

        # Create test product
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=99.99,
            stock=10,
            category=self.category
        )

    def test_product_list(self):
        """Test retrieving product list"""
        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Product')

    def test_product_detail(self):
        """Test retrieving product detail"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('product-details', args=[self.product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_category_list(self):
        """Test retrieving category list"""
        url = reverse('category-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Category')

    def test_add_to_cart(self):
        """Test adding product to cart"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('add-to-cart', args=[self.product.id])

        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_REFERER='/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.first().product, self.product)

    def test_add_to_wishlist(self):
        """Test adding product to wishlist"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('add-to-wishlist', args=[self.product.id])

        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_REFERER='/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wishlist.objects.count(), 1)
        self.assertEqual(Wishlist.objects.first().product, self.product)

    def test_view_cart(self):
        """Test viewing cart"""
        self.client.login(username='testuser', password='testpass123')
        Cart.objects.create(user=self.user, product=self.product)
        url = reverse('view-cart')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'ecom/cart.html')

    def test_view_wishlist(self):
        """Test viewing wishlist"""
        self.client.login(username='testuser', password='testpass123')
        Wishlist.objects.create(user=self.user, product=self.product)
        url = reverse('view-wishlist')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'ecom/wishlist.html')

    def test_unauthenticated_access(self):
        """Test accessing protected endpoints without authentication"""
        urls = [
            reverse('view-cart'),
            reverse('view-wishlist'),
            reverse('product-details', args=[self.product.id]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertIn(response.status_code,
                          [status.HTTP_302_FOUND, status.HTTP_403_FORBIDDEN])

    def test_remove_from_cart(self):
        """Test removing product from cart"""
        self.client.login(username='testuser', password='testpass123')
        cart_item = Cart.objects.create(user=self.user, product=self.product)
        url = reverse('remove-from-cart', args=[self.product.id])

        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_REFERER='/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.count(), 0)

    def test_remove_from_wishlist(self):
        """Test removing product from wishlist"""
        self.client.login(username='testuser', password='testpass123')
        wishlist_item = Wishlist.objects.create(
            user=self.user, product=self.product)
        url = reverse('remove-from-wishlist', args=[self.product.id])

        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_REFERER='/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wishlist.objects.count(), 0)
