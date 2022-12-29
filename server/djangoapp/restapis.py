import requests
import json
from .models import CarDealer, DealerView
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):    
    print(kwargs)    
    print(f"GET from {url} ")
    try:  
        # Call get method of requests library with URL and parameters        
        response = requests.get(url, headers={'Content-Type': 'application/json'},params=kwargs)
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
def get_dealer_by_id_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as review
        reviews = json_result["docs"]
        # For each review object
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerView(
                car_make = review['car_make'], car_model = review['car_model'], car_year = review['car_year'],
                dealership = review['dealership'], id = review['id'], name = review['name'], purchase = review['purchase'], 
                purchasedate = review['purchasedate'], review = review['review']
            )
            results.append(review_obj)
        print(results)
        return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



