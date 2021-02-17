from django.urls import path
from . import views

# localhost:8000/tour
app_name = 'tour'

urlpatterns = [
    path('detail/<str:toursite_id>', views.detail, name='detail'),
    path('search/', views.search, name='search')
]

