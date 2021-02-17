from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tour.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_rate', 'review_content']


class UserSignupForm(UserCreationForm):
    email = forms.EmailField() # required

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


