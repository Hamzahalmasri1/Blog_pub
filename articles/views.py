from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from articles import models as article_views
# Create your views here.




class IndexPageView(TemplateView):

    template_name = 'articles/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context.update(needed_everywhere())
        return context


def needed_everywhere():
    context = {}
    all_articles = {}
    all_categories = article_views.Category.objects.all()
 

    for category in all_categories:
        all_articles[category.title] = article_views.Article.objects.filter(
            category__title=category.title).order_by('-create_at')[:12]

  
    context['all_category'] = all_categories
    context['all_articles'] = all_articles

    print(all_categories)
    print(all_articles)
    

    return context