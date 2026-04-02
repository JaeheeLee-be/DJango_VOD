from django.db import models
from config.models import BaseModel
from users.models import User
from restaurants.models import Restaurant


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    comment = models.TextField()