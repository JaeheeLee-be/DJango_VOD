from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from utils.models import TimeStampModel

User = get_user_model()

class Blog(TimeStampModel):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )

    # CHOICES: 정해진 값, 항목에서만 고를 수 있게 하는 Django 필드에 넘겨주는 옵션(매개변수)

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # models.CASCADE: 같이 삭제
    # models.PROTECT: 삭제가 불가능함 (유저를 삭제하려고 할 때 블로그가 있으면 유저 삭제가 불가능)
    # models.SET_NULL: NULL값을 넣습니다. 유저 삭제시 블로그의 author가 null이 됨
    # makemigrations: 기본값이 안정해져 있으면 선택지를 준다. (1.디폴트값, 2.종료)


    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'


     # category update
     # Blog.objects.filter(category='').update(category='free')


class Comment(TimeStampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'