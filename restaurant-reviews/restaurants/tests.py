from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from users.models import User
from restaurants.models import Restaurant

class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant_data = {
            'name': '오즈식당',
            'address': '서울시 서초구',
            'contact': '02-1234-5678',
        }

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(**self.restaurant_data)
        self.assertEqual(restaurant.name, self.restaurant_data['name'])
        self.assertEqual(restaurant.address, self.restaurant_data['address'])
        self.assertEqual(restaurant.contact, self.restaurant_data['contact'])


class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpassword',
            nickname='testuser',
        )
        self.restaurant = Restaurant.objects.create(
            name='오즈식당',
            address='서울시 서초구',
            contact='02-1234-5678',
        )
        self.restaurant_data = {
            'name': '새로운식당',
            'address': '서울시 강남구',
            'contact': '02-2345-6789',
        }

    def test_restaurant_list_view(self):
        url = reverse('restaurant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_post_view(self):
        url = reverse('restaurant-list')
        response = self.client.post(url, self.restaurant_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurant_detail_view(self):
        url = reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_update_view(self):
        url = reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})
        response = self.client.patch(url, {'name': '수정된식당'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_delete_view(self):
        url = reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)