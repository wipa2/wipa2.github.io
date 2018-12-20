from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'works'
urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('exhibit', views.exhibit, name='exhibit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
