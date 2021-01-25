from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from articles import models as article_views
from django.urls import reverse, resolve
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

 
    

    return context

# def category_results(request,category_title):
#     return render(request,'articles/list_category.html')



class category_results(ListView):

    template_name = 'articles/list_category.html'
    model = article_views.Article
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(category_results, self).get_context_data(**kwargs)
        category_title = self.kwargs.get('title')
        articles = article_views.Article.objects.filter(category__title=  category_title) 
     
        context ['category_title'] = category_title

        paginator = Paginator(articles, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            articles_files = paginator.page(page)
        except PageNotAnInteger:
            articles_files = paginator.page(1)
        except EmptyPage:
            articles_files = paginator.page(paginator.num_pages)
            
        context['articles'] = articles_files
        return context



class SearchView(ListView):

    template_name = 'articles/list_category.html'
    model = article_views.Article
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        search_term = self.request.GET.get('q').strip(' */%^$#@!?')
        articles = article_views.Article.objects.filter(Q(title__icontains=search_term) | Q(
            author__icontains=search_term) | Q(category__title__icontains=search_term) | Q(description__icontains=search_term))
        article_number = articles.count()
        current_url = resolve(self.request.path_info).url_name


        paginator = Paginator(articles, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            articles_files = paginator.page(page)
        except PageNotAnInteger:
            articles_files = paginator.page(1)
        except EmptyPage:
            articles_files = paginator.page(paginator.num_pages)
            
        
        context = {
            'articles': articles_files,
            'products_number': article_number,
            'search': search_term,
            'url_name': current_url,
            'search_exist': 'true',
        }
      
       
        return context

    
   

    # def get_queryset(self,**kwargs):
       
        
    #     return context
