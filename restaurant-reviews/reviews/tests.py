from django.test import TestCase
from users.models import User
from restaurants.models import Restaurant
from reviews.models import Review


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpassword',
            nickname='testnickname',
        )
        self.restaurant = Restaurant.objects.create(
            name='테스트식당',
            address='서울시 강남구',
            contact='02-1234-5678',
        )

    def test_create_review(self):
        review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            title='테스트 리뷰',
            comment='맛있어요!',
        )
        self.assertEqual(review.title, '테스트 리뷰')
        self.assertEqual(review.comment, '맛있어요!')
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.restaurant, self.restaurant)