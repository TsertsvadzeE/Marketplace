from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class ProductCreateTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('product-list')

    def test_create_product(self):
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 10.99,
            'category': 'Electronics',
        }


        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        product = Product.objects.get(name='Test Product')
        self.assertEqual(product.description, 'Test Description')
        self.assertEqual(product.price, 10.99)


class ProductListTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.product1 = Product.objects.create(
            name='Product One', description='Description One', price=5.99, category='Toys', user=self.user
        )
        self.product2 = Product.objects.create(
            name='Product Two', description='Description Two', price=15.99, category='Electronics', user=self.user
        )
        self.url = reverse('product-list')

    def test_product_list(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Product One')
        self.assertEqual(response.data[1]['name'], 'Product Two')
