from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)  # 현재 이미지
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)  # 최대 이미지 크기
            img.thumbnail(output_size)
            img = img.convert('RGB')  # OSError: cannot write mode RGBA as JPEG
            img.save(self.image.path)
