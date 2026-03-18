from django.db import models

# Create your models here.

# Model = DB의 테이블
# Field = DB의 컬럼

# 북마크
# 이름 => varchar
# URL 주소 => varchar

# google search => django model field

class Bookmark(models.Model):
    name = models.CharField('이름', max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('생성일식', auto_now_add=True)
    updated_at = models.DateTimeField('수정일식', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'

# makemigrations => migration.py 파일을 생성
# 실제 DB에는 영향 X => 실제 DB에 넣기 위한 정의를 하는 파일을 생성

# migrate => migrations / 폴더 안에 migration 파일들을 실제 DB에 적용을 함

# makemigrations => Git의 commit => GitHub에 적용 X => DB에 적용 X, 적용할 파일 생성
# migrate => Git의 push => GitHub에 적용 o, 로컬에 있는 커밋 기록 => DB 적용 o, migrations 파일을 가지고 적용


