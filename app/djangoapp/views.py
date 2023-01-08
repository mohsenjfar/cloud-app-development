from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_name
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def get_dealerships(request):    
    if request.method == "GET":        
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/e7d8f3db-0cc6-4f5c-80ef-d9860b3f8248/dealership-package/get-dealership-sequence.json"
        dealerships = get_dealers_from_cf(url)
        context = dict()
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):    
    if request.method == "GET":        
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/e7d8f3db-0cc6-4f5c-80ef-d9860b3f8248/dealership-package/get-review.json"
        # Get reviews from the URL        
        reviews = get_dealer_reviews_from_cf(url, **{'dealerId':dealer_id})
        context = dict()
        context['review_list'] = reviews
        context['dealer_id'] = dealer_id
        context['dealer_name'] = get_dealer_name(dealer_id)
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request,dealer_id):
    if request.method == 'GET':
        context = dict()
        context['cars'] = [
            {
                'id':car.id,
                'make':car.make.name,
                'model':car.name,
                'year':car.year,
            } for car in CarModel.objects.filter(dealer_id = dealer_id)
        ]
        context['dealer_id'] = dealer_id
        context['dealer_name'] = get_dealer_name(dealer_id)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/e7d8f3db-0cc6-4f5c-80ef-d9860b3f8248/dealership-package/post-review-sequence"
        car = CarModel.objects.get(pk = int(request.POST['car']))
        payload = dict()
        payload['review'] = {
            "id" : int(request.POST['car']),
            "time" : datetime.utcnow().isoformat(),
            "name" : request.user.username,
            "dealership" : int(dealer_id),
            "purchase" : True if 'purchasecheck' in request.POST else False,
            "purchase_date" : request.POST['purchasedate'],
            "car_make" : car.make.name,
            "car_model" : car.name,
            "car_year" : car.year.strftime("%Y"),
            "review" : request.POST['content'],
        }
        post_request(url, payload)
        return redirect('djangoapp:dealer_details' , dealer_id = dealer_id)