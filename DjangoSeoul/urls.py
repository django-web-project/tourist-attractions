from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView

urlpatterns = [
    # 메인 페이지
    url(r'^$', TemplateView.as_view(template_name='main.html')),
    path('admin/', admin.site.urls),
    path('tour/', include('tour.urls'))
]
