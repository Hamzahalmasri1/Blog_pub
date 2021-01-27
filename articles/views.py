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

def details(request,cate_title,title):
    article =  article_views.Article.objects.get(title__iexact=title)
    article.views +=1
    article.save()
    most_viewed = article_views.Article.objects.order_by('-views')[:4]
    featured = article_views.Article.objects.order_by('-favorites')[:4]
    recent = article_views.Article.objects.order_by('-publish_date')[:4]
    cate_list = article_views.Category.objects.values('title').annotate(Count('article'))
    for i in cate_list:
        for k1,v1 in i.items():
            print (k1,v1)

    print(cate_list)
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
        'cate_list': cate_list,
        }
   

    return render (request, 'articles/single-page.html', context)




    
def Quick_View (request):
    current_user = request.user
    
    if request.is_ajax():
        
        name_product = request.GET.get("product_name")
        
        product = core_models.Product.objects.filter(name = name_product)
        product_id = product[0].id

        product_name = product[0].name
        image =product[0].image
        description = product[0].description
        price = product[0].price
        discount_price=product[0].discount_price
        color = product[0].color
        size = product[0].size
        c_store_type = product[0].category.store.storetype.slug
        category_slug = product[0].category.slug
        slug=product[0].slug
        store_slug = product[0].category.store.slug
        fav = product[0].favourite.all()

        if  current_user in fav:
           favourite =True
        else:
            favourite = False   

        slug_product = ("/{c_store_type}-type/{store_slug}/{category_slug}/{slug}/").format(c_store_type=c_store_type, store_slug=store_slug, category_slug=category_slug, slug=slug)

        favourite_slag = ('/favourite-product/{slug}/').format(slug = slug)
        add_product_herf = ('/order/addtoshpcart/{id}/').format(id = product_id )
        image = str(image)
        slug_product = str(slug_product)
        
        context = {
                'product_name': product_name,
                'image': image,
                'description':description,
                'price': price,
                'discount_price': discount_price,
                'color': color,
                'size': size,
                'slug':slug_product,
                'id':product_id,
                'favourite': favourite,
                'favourite_slag':favourite_slag,
                'add':add_product_herf,


            }
        return JsonResponse(context)
