from django.shortcuts import render, redirect, HttpResponse
from time import localtime, strftime
import random
from .models import *
import bcrypt
from django.contrib import messages

def index(request):

    return render(request, 'index.html')


#============================================
#Login Route
#============================================

def login_page(request):
    return render(request, 'login_page.html')

#============================================
#Registration Processing Route
#============================================

def register(request):
    #validate your info
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else: 
    #create User   
        hashed = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name =request.POST['fname'],
            last_name=request.POST['lname'],
            email=request.POST['email'],
            address = request.POST['address'],
            password=hashed,
            # isManager = True
        )
    # Once created, log them in
        request.session['userid'] = new_user.id
    #redirect to the main page
        return redirect('/dashboard')


#============================================
#Login Processing Route
#============================================
def login(request):
    #validate that user exists
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        user = User.objects.filter(email = request.POST['log_email']) 
        request.session['userid'] = user[0].id
        #log User in
        #redirect to home page

    return redirect('/dashboard')

#=================LOGOUT====================
def logout(request):
    request.session.clear()
    return redirect('/index')
#============================================
#Dashboard/Service  Route
#============================================

def dashboard(request):
    if 'userid' not in request.session:
        messages.error(request,'Please log in before continuing!')
        return redirect('/')

    user= User.objects.get(id=request.session['userid'])
    client =user.orders.all()
    context = {
        'logged_in' : User.objects.get(id=request.session['userid']),
        'services' : Service.objects.all(),
        'the_order' : Order.objects.all(),

        'client_orders' : client

    }
    return render(request, 'dashboard.html',context)

#============================================
#services page / form
#============================================
def services(request):

    context = {
        'logged_in' : User.objects.get(id=request.session['userid']),
        'user_id': request.session['userid']
    }
    return render(request, 'services.html',context)

def services_form(request):

    Service.objects.create(
        service = request.POST['service'],
        price = request.POST['num'],
        description = request.POST['description'],
        client = User.objects.get(id=request.session['userid']),
    )

    return redirect('/dashboard')

#============================================
#services & quote Display page
#============================================
def services_quotes(request):

        return render(request, 'service_quote.html')

#============================================
#Review Order page
#============================================

def review_order(request, id):
        if 'userid' not in request.session:
            messages.error(request,'Please log in before continuing!')
            return redirect('/')

        context = {
            'logged_in' : User.objects.get(id=request.session['userid']),
            'the_order': Order.objects.get(id=id),
        }

        return render(request, 'review_order.html',context)

#============================================
# Process Review Order page
#============================================

def process_order(request):

    Order.objects.create(
        service = Service.objects.get(id=request.POST["service_id"]),
        client = User.objects.get(id=request.session['userid'])
    ) 
    id = request.POST['service_id']

    return redirect(f'/review_order/{id}')

#============================================
# Cancel order
#============================================  

def cancel(request):

    return redirect('dashboard')