from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_emailtouser(name=name, email=email, message=message)

        messages.success(request, 'Your message has been sent successfully!')
    product = Products.objects.all()
    return render(request, 'home.html', {'product': product})


def register_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confrim_pass=request.POST.get('confirm-password')
        if confrim_pass==password:
            user=User.objects.create(username=username,email=email)
            user.set_password(password)
            user.save()
            return redirect('/login')
        else:
            messages.error(request ,'Password are not same please Try again!')
            return redirect('register_view')
    return render(request,'register.html')

def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.filter(username=username).first()
        if user:
            userauth=authenticate(username=username,password=password)
            if userauth:
                login(request,userauth)
                return redirect('/')
            else:
                messages.error(request,'wrong password!')
        else:
            messages.error(request,'username is not exist!')
    return render(request,'login.html')

def logout_view(request):  
    logout(request)  
    return redirect('/login_view') 

def about(request):
    return render(request,'about.html')



def add_product(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        uploaded_at = request.POST.get('uploaded_at')
        category = request.POST.get('category')
        print(category)
        cats = Category.objects.filter(id=category).first()
        print(cats)
        Products.objects.create(name=name,quantity=quantity,price=price,description=description,category=cats,image=image,uploaded_at=uploaded_at)  
        # return redirect('home') 
    category = Category.objects.all()
    print(category)
    for cat in category:
        print(cat.name)
    context = {
        'category' : category
    }
    return render(request,'add_product.html', context)

def detail(request, id):
    prod_detail = Products.objects.get(id=id)
    reviews = prod_detail.reviews.all()
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        if request.user.is_authenticated:
            Review.objects.create(
                product=prod_detail,
                user=request.user,
                comment=comment,
                rating=rating
            )
            return redirect('detail', id=id)  

    return render(request, 'prod_detail.html', {'prod_detail': prod_detail, 'reviews': reviews})


def add_to_cart(request,id):
    product =Products.objects.get(id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user, product=product.name,
        defaults={'price': product.price, 'quantity': 1}  
    )

    
    if not created:
        cart_item.quantity += 1
        cart_item.price = product.price  
        cart_item.save()

    
    return redirect('detail', id=id)

def carts(request):
    cart_items = Cart.objects.filter(user=request.user)  
    total_price = 0 

    for item in cart_items:
        item.total_price = item.price * item.quantity  
        total_price += item.total_price  

    return render(request, 'carts.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def delete_cart_item(request,id):
    item=Cart.objects.get(id=id)
    item.delete()
    return redirect('carts')


def update_product(request, id):
    product = Products.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image= request.POST.get('image')
        uploaded_at= request.POST.get('uploaded_at')
        
        product.name = name
        product.quantity = quantity
        product.price = price
        product.description = description
        product.uploaded_at =uploaded_at
        product.save()  
        
        return redirect('detail', id=id)  
    
    return render(request, 'update.html', {'product': product})       

def delete_product(request, id): 
        productt =Products.objects.get(id=id)
        productt.delete()
        return redirect('home')  

def send_emailtouser(name, email, message):
    subject = f"Message from {name}"
    email_message = (
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}"
    )
    return send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [email])

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_emailtouser(name=name, email=email, message=message)

        messages.success(request, 'Your message has been sent successfully!')

    return render(request, 'contact.html')


def productlist(request):
    cat = Category.objects.all()
    products = Products.objects.all()
    if request.method=="POST":
        prod = request.POST.get('prod')
        if prod=='all':
            products = Products.objects.all()
        else:
            products = Products.objects.filter(category__name=prod)
    print(products)
    context = {
        'products':products,
        'categories':cat,
    }
    return render(request, 'productlist.html', context)