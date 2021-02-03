from django.db import models


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
    toursite_img = models.CharField(max_length=500)
    toursite_detail = models.CharField(max_length=500)

    gu = models.ForeignKey(Gu, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.toursite_name

class User(models.Model):
    user_email = models.CharField(max_length=100)
    user_pw = models.CharField(max_length=100)
    user_nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.user_email

class Review(models.Model):
    review_rate = models.IntegerField(default=0)
    review_date = models.DateTimeField('published date')
    review_content = models.CharField(max_length=100)

    toursite = models.ForeignKey(Toursite, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.review_content

