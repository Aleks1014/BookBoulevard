from django.db.models import Q
from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Product, Category, Subcategory, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUser, UpdatePasswordForm, UserInfoForm
import json


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
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

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
            messages.success(request, 'You have registered successfully. Please fill out your additional information.')
            return redirect('update_info')
        else:
            messages.error(request, 'There was a problem registering. Please try again.')
            return redirect('register')

    else:
        return render(request, 'register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUser(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'Your account has been updated.')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.error(request, 'You must log in to access this page.')
        return redirect('home')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.error(request, 'You must log in to access this page.')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully updated your password.')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to access the page.')
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def category(request, cat_name):
    cat_name = cat_name.replace('-', ' ')

    # to figure how to get all subcategories and their products
    category = Category.objects.get(name=cat_name)
    subcategories = Subcategory.objects.filter(category=category)
    products = Product.objects.filter(subcategory__in=subcategories)
    return render(request, 'category.html',
                  {'category': category, 'subcategories': subcategories, 'products': products})
    # except:
    #     messages.error(request, 'That category does not exist.')
    #     return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, 'category_summary.html', {'categories': categories, 'subcategories': subcategories})


def search_result(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        results = Product.objects.filter(
            Q(author__first_name__icontains=searched) | Q(author__last_name__icontains=searched) | Q(
            title__icontains=searched))
        if not results:
            messages.error(request, 'No books found. '
                                    'Please double check your spelling or try with less specific keywords.')
        return render(request, 'search_result.html', {'searched': searched, 'results': results})
    else:
        return render(request, 'search_result.html', {})
