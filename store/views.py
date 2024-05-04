from django.shortcuts import render, redirect
from .models import Product, Category, Subcategory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm


# Create your views here.
def home(request):
    products = Product.objects.all()[:5]
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in.')
            return redirect('home')
        else:
            messages.error(request, 'There was an error. Please try again.')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logout.')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered successfully.')
            return redirect('home')
        else:
            messages.error(request, 'There was a problem registering. Please try again.')
            return redirect('register')

    else:
        return render(request, 'register.html', {'form': form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def category(request, cat_name):
    cat_name = cat_name.replace('-', ' ')

    # to figure how to get all subcategories and their products
    category = Category.objects.get(name=cat_name)
    subcategories = Subcategory.objects.filter(category=category)
    products = Product.objects.filter(subcategory__in=subcategories)
    return render(request, 'category.html', {'category': category, 'subcategories': subcategories, 'products': products})
    # except:
    #     messages.error(request, 'That category does not exist.')
    #     return redirect('home')


