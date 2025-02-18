from django.contrib.auth.models import User
from .models import Product, Category, Orders, Payments, Review, Cart, Wishlist, UserProfile
from rest_framework import serializers
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone_number',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create(**validated_data)
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data and instance.profile:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # product = ProductSerializer()
    # payments = serializers.StringRelatedField()

    class Meta:
        model = Orders
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # product = ProductSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # product = ProductSerializer()

    class Meta:
        model = Wishlist
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Payments
        fields = '__all__'
