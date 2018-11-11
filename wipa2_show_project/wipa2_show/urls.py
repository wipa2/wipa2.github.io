from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'works'
urlpatterns = [
    path('', views.index, name='index'),
    path('works_list', views.WorksListView.as_view(), name='works_list'),
    path('submit', views.submit, name='submit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
