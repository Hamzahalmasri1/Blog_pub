from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from account import forms as account_forms
from account import models as account_models
from articles import views as article_view
from articles import models as article_models


def register_view(request):

    if request.method == 'POST':
        form = account_forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            user = authenticate(username=username, password=password1)
            login(request, user)
            messages.success(
                request, f"Welcome Mr.{username}.")
            return redirect('articles:index')
    else:
        form = account_forms.UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
        if 'next' in request.POST:
            return HttpResponseRedirect(request.POST.get('next'))
        else:
            return redirect('articles:index')
    else:
        return render(request, 'account/login.html')

@login_required(login_url='/accounts/login/')
def profile(request):
    if request.method == 'POST':
        form = account_forms.ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = account_forms.ProfileUpdateForm(instance=request.user)

    profile = account_models.UserRegistration.objects.filter(
        username=request.user.username)[0]
    wishlist_count = article_models.Article.objects.filter(
        favorites=request.user.id).count()
  
    context = {
        'profile_exist': True,
        'profile': profile,
        'wishlist_count': wishlist_count,
        'form': form,
        
    }
    context.update(article_view.needed_everywhere())
    return render(request, 'account/profile.html', context)


@login_required(login_url='/accounts/login/')
def wishlist_view(request):
    profile = account_models.UserRegistration.objects.filter(
        username=request.user.username)[0]
    wishlist_list = article_models.Article.objects.filter(
        favorites=request.user.id).order_by('title')
    wishlist_count = wishlist_list.count()
 
    context = {
        'wishlist_exist': True,
        'profile': profile,
        'wishlist_list': wishlist_list,
        'wishlist_count': wishlist_count,
      
    }
    context.update(article_view.needed_everywhere())
    return render(request, 'account/profile.html', context)


