/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
  const client = CloudantV1.newInstance({
    authenticator: authenticator
  });
  client.setServiceUrl(params.COUCH_URL);
  try {
    let dbList = await client.postAllDocs({
      db: 'dealerships',
      includeDocs: true,
    });
    return { "dbs": dbList.result };
  } catch (error) {
    return { error: error.description };
  }
}