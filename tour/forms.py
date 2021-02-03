from django import forms
from tour.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_rate', 'review_content']