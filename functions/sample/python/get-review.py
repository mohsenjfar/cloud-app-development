from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(params):
    authenticator = IAMAuthenticator(params['apikey'])
    
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(params['url'])
    
    response = client.post_all_docs(
      db='dealerships',
      include_docs=True
    ).get_result()

    return response
