from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(to= 'Category', on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="Articles-Images", null=True, blank=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    publish_date = models.DateField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



