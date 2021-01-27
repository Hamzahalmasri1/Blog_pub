
from django.conf.urls.static import static
from blogs import settings
from django.urls import path, include
from articles import views as article_views


app_name = 'articles'
urlpatterns = [
    path('', article_views.IndexPageView.as_view(), name='index'),
    path('category_results/<str:title>/', article_views.category_results.as_view(), name='category_results'),
    path('search', article_views.SearchView.as_view(), name='search_result'),
    path('Quick_view/', article_views.Quick_View, name='Quick_View'),
    path('read_more/<str:cate_title>/<str:title>', article_views.details, name='details'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
