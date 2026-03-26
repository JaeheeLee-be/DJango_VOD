from io import BytesIO
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    completed_image = models.ImageField(upload_to='completed_images/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True, default='thumbnails/default.png')

    def save(self, *args, **kwargs):
        if self.completed_image:

            path = Path(self.completed_image.name)
            stem = path.stem
            suffix = path.suffix.lower()

            if suffix in ['.jpg', '.jpeg']:
                file_type = 'JPEG'
            elif suffix == '.png':
                file_type = 'PNG'
            elif suffix == '.gif':
                file_type = 'GIF'
            else:
                return super().save(*args, **kwargs)

            img = Image.open(self.completed_image)
            img.thumbnail((300, 300))

            thumbnail_name = f'{stem}_thumbnail{suffix}'

            temp_file = BytesIO()
            img.save(temp_file, format=file_type)

            self.thumbnail.save(thumbnail_name, ContentFile(temp_file.getvalue()), save=False)

            temp_file.close()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.message[:20]}'