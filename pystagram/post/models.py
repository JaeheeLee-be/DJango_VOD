from django.contrib.auth import get_user_model
from django.db import models

from utils.models import TimeStampedModel


User = get_user_model()

class Post(TimeStampedModel):
    content = models.TextField('본문')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} post'

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = '포스트 목록'

class PostImage(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('이미지', upload_to='post/%Y/%m/%d')

    def __str__(self):
        return f'{self.post} image'

    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = '이미지 목록'
