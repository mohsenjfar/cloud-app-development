from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    model_choices = (
        (SEDAN,'Sedan'),
        (SUV,'SUV'),
        (WAGON,'WAGON')
    )
    type = models.CharField(max_length=10, choices = model_choices)
    year = models.DateField()

class CarDealer:
    
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):

        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:

    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, purchase_date, review, sentiment=None):

        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment

    def __str__(self):
        return "Dealer name: " + self.name