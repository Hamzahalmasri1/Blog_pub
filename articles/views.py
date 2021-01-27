from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from articles import models as article_views
from django.urls import reverse, resolve
from django.http import JsonResponse
from django.db.models import Max, Min,Count
from django.contrib.auth.decorators import login_required

# Create your views here.




class IndexPageView(TemplateView):

    template_name = 'articles/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        most_viewed = article_views.Article.objects.order_by('-views')[:4]
        featured = article_views.Article.objects.order_by('-favorites')[:4]
        recent = article_views.Article.objects.order_by('-publish_date')[:4]
        most_recent = article_views.Article.objects.order_by('-update_at')[:4]
        context = {
    
        'most_viewed' : most_viewed,
        'featured' : featured,
        'recent' : recent,
        'most_recent':most_recent,
        }
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

        most_viewed = article_views.Article.objects.order_by('-views')[:4]
        featured = article_views.Article.objects.order_by('-favorites')[:4]
        recent = article_views.Article.objects.order_by('-publish_date')[:4]
        cate_list = article_views.Category.objects.values('title').annotate(count = Count('article'))
        category  = {cate['title']:cate['count'] for cate in cate_list}  

      

        paginator = Paginator(articles, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            articles_files = paginator.page(page)
        except PageNotAnInteger:
            articles_files = paginator.page(1)
        except EmptyPage:
            articles_files = paginator.page(paginator.num_pages)

      
       
        context = {
        'articles' :articles_files,
        'in_this_category' : article_views.Article.objects.filter(category__title__iexact=category_title)[:4],
        'most_viewed' : most_viewed,
        'featured' : featured,
        'recent' : recent,
        'category_title': category_title,
        'cate_list': category,}
        context.update(needed_everywhere())
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
        most_viewed = article_views.Article.objects.order_by('-views')[:4]
        featured = article_views.Article.objects.order_by('-favorites')[:4]
        recent = article_views.Article.objects.order_by('-publish_date')[:4]
        cate_list = article_views.Category.objects.values('title').annotate(count = Count('article'))
        category  = {cate['title']:cate['count'] for cate in cate_list}
      


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
            'in_this_category' : article_views.Article.objects.order_by('-update_at')[:6],
            'most_viewed' : most_viewed,
            'featured' : featured,
            'recent' : recent,
            'products_number': article_number,
            'search': search_term,
            'url_name': current_url,
            'search_exist': 'true',
            'cate_list': category,
        }
      
        context.update(needed_everywhere())
        return context


def details(request,cate_title,title):
    article =  article_views.Article.objects.get(title__iexact=title)
    article.views +=1
    article.save()
    most_viewed = article_views.Article.objects.order_by('-views')[:4]
    featured = article_views.Article.objects.order_by('-favorites')[:4]
    recent = article_views.Article.objects.order_by('-publish_date')[:4]
    cate_list = article_views.Category.objects.values('title').annotate(count = Count('article'))
    category  = {cate['title']:cate['count'] for cate in cate_list}
  
    context = {
        'article_title': article.title,
        'article_cate': article.category.title,
        'aricle_image' : article.image,
        'article_views': article.views,
        'artcile_likes': article.likes.count(),
        'description' : article.description,
        'author' : article.author,
        'date' : article.publish_date,
        'in_this_category' : article_views.Article.objects.filter(category__title__iexact=cate_title)[:4],
        'most_viewed' : most_viewed,
        'featured' : featured,
        'recent' : recent,
        'cate_list': category,
        'article': article,
        }
   
    context.update(needed_everywhere())
    return render (request, 'articles/single-page.html', context)




@ login_required(login_url='/accounts/login/')
def favourite_article(request,title):

    url = request.META.get('HTTP_REFERER')
    article = get_object_or_404(article_views.Article, title=title)
    if article.favorites.filter(id=request.user.id).exists():
        article.favorites.remove(request.user)
        messages.warning(
            request, f'"{article.title}" has been removed from your Favorites.')
    else:
        article.favorites.add(request.user)
        messages.success(
            request, f'"{article.title}" has been added to your Favorite.')
    return HttpResponseRedirect(url)



    
