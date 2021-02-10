from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 메인 페이지
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('signupProcess/', views.signup_process, name='signup_process'),
    path('loginProcess/', views.login_process, name='login_process'),
    path('logoutProcess/', views.logout_process, name='logout_process'),
    path('tour/', include('tour.urls')),
    path('account/', include('account.urls')),
]

# Debug Mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
