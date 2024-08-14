from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from cart.cart import Cart
from order_process.forms import ShippingForm
from order_process.models import ShippingAddress
from .models import Product, Category, Subcategory, Profile, Review, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUser, UpdatePasswordForm, UserInfoForm, ReviewForm
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
            current_user = Profile.objects.get(user_id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, 'You have been logged in.')
            send_mail(User.objects.get(username=username).email)

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
        current_user = Profile.objects.get(user_id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('update_info')
        return render(request, 'update_info.html', {'form': form, 'shipping_form':shipping_form})
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
    comments = Review.objects.filter(product=product)
    if comments:
        avg_rate = f'{sum(comment.rate for comment in comments) / len(comments):.2f}'
    else:
        avg_rate = 0
    return render(request, 'product.html', {'product': product, 'comments': comments, 'avg_rate':avg_rate})


def category(request, cat_name):
    # to figure how to get all subcategories and their products
    category = Category.objects.get(name=cat_name)
    subcategories = Subcategory.objects.filter(category=category, parent__isnull=True)
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


def submit_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_id
            review.save()
            messages.success(request, 'Thank you, your review has been submitted!')
        else:
            messages.error(request, 'There was error.')
        return redirect('product', pk=product_id)
    return redirect('product')

def send_mail(email):
    subject = 'Test Mail'
    sender = 'aleks.dimova96@gmail.com'
    receipient = email
    html_content = render_to_string('emails/test_email.html')
    plain_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, plain_content, sender, [receipient])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
