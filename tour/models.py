from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Gu(models.Model):
    gu_name = models.CharField(max_length=100)

    def __str__(self):
        return self.gu_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Toursite(models.Model):
    toursite_name = models.CharField(max_length=100)
    toursite_address = models.CharField(max_length=100)
    toursite_img = models.CharField(max_length=1000)
    toursite_detail = models.TextField()

    gu = models.ForeignKey(Gu, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.toursite_name

class Tuser(models.Model):
    user_img = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    review_rate = models.IntegerField(default=0)
    review_date = models.DateTimeField(default=timezone.now)
    review_content = models.CharField(max_length=100)

    toursite = models.ForeignKey(Toursite, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.review_content

