from django.contrib import admin
from articles import models as articles_models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    list_filter = ('title',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','author','image','likes','views','publish_date',)
    list_filter = ('title','create_at','update_at')

admin.site.register(articles_models.Category,CategoryAdmin)
admin.site.register(articles_models.Article,ArticleAdmin)
   
    
