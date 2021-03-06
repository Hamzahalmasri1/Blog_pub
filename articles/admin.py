from django.contrib import admin
from articles import models as articles_models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    list_filter = ('title',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','author','image','views','publish_date',)
    list_filter = ('title','category','create_at','update_at')

admin.site.register(articles_models.Category,CategoryAdmin)
admin.site.register(articles_models.Article,ArticleAdmin)
   
    
