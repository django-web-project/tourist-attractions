from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    # localhost:8000/account
    path('', views.check_login, name='check_login'),
    path('setting/', views.profile, name='profile'),
    path('profileUpdate/', views.profile_update, name='profile_update'),
    path('my-list/', views.my_list, name='my_list'),
    path('myReviewEdit/', views.my_review_edit, name='my_review_edit'),
    path('myRatingEdit/', views.my_rating_edit, name='my_rating_edit'),
    path('myListDelete/', views.my_list_delete, name='my_list_delete'),
    path('deleteAll/', views.delete_all, name='delete_all')
]

# Debug Mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

