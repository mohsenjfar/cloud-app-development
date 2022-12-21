from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('{apikey}')

client = CloudantV1.new_instance(
    authenticator=authenticator
)
client.set_service_url('{url}')

response = client.post_all_docs(
  db='dealerships',
  include_docs=True
).get_result()

print(response)