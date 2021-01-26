from django.db import models
from account import models as account_models

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
    likes =models.ManyToManyField(account_models.UserRegistration, related_name='like', blank=True)

    views = models.IntegerField(default=0)
    favorites = models.ManyToManyField(
        account_models.UserRegistration, related_name='favourite', blank=True)
    publish_date = models.DateField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



