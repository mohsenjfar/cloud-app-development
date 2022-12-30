import requests
import json
from .models import CarDealer, DealerView
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, api_key, **params):
    headers={'Content-Type': 'application/json'}
    request.get(url, params=params, headers = headers)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, payload, **kwargs):    
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], 
                                   short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
        print(results)
        return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **params):
    results = []
    json_result = get_request(url, **params)
    if json_result:
        # Get the row list in JSON as review
        reviews = json_result["docs"]
        # For each review object
        for review in reviews:
            # Create a DealerView object with values in `doc` object
            review_obj = DealerView(
                car_make = review['car_make'], car_model = review['car_model'], car_year = review['car_year'],
                dealership = review['dealership'], id = review['id'], name = review['name'], purchase = review['purchase'], 
                purchase_date = review['purchase_date'], review = review['review']
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
        print(results)
        return results

def analyze_review_sentiments(text):
    api_key = 'S-vguDraKch-lQFBkzzVxO3hZd-sUHEwd8LPdlk59S_o'
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/ca69e882-e6c8-40df-be35-c26f9d4cf63c"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text = text,
        features=Features(sentiment = SentimentOptions(document=True))
        ).get_result()
    return response['sentiment']['document']['label']