import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):    
    print(kwargs)    
    print(f"GET from {url} ")
    try:  
        # Call get method of requests library with URL and parameters        
        response = requests.get(url, headers={'Content-Type': 'application/json'},                                    
        params=kwargs)    
    except:
        # If any error occurs
        print("Network exception occurred") 
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, payload, **kwargs):    
    print(kwargs)    
    print(f"POST to {url} ")
    try:  
        # Call get method of requests library with URL and parameters        
        response = requests.post(url, params=kwargs, json=payload)
    except:
        # If any error occurs
        print("Network exception occurred") 
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



