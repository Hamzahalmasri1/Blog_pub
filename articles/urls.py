
from django.conf.urls.static import static
from blogs import settings
from django.urls import path, include
from articles import views as article_views

urlpatterns = [
    path('', article_views.IndexPageView.as_view(), name='index'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
