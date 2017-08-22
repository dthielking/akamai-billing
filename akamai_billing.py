#!/usr/bin/env python3

import requests
import json
from pprint import pprint
from urllib.parse import urljoin
from akamai.edgegrid import EdgeGridAuth

# Get Credetials
with open('akamai_credentials.json') as credentials_file:
    credentials=json.load(credentials_file)

apiUrl = "https://" + credentials['api_url']

apiSession = requests.Session()
apiSession.auth = EdgeGridAuth(credentials['client_token'], credentials['client_secret'], credentials['access_token'])

reportingUrl= apiUrl + "/contract-api/v1/reportingGroups/identifiers"
print(reportingUrl)
reportingGroupIds = apiSession.get(reportingUrl)

pprint(reportingGroupIds)

#pprint(apiSession.get(urljoin(credentials['api_url'], "/diagnostic-tools/v1/locations")))

#reporting_groupids={"rtl":72076}
res_contract_ids = apiSession.get(urljoin(apiUrl, '/contract-api/v1/contracts/identifiers'))
pprint(res_contract_ids.json())
#res_product_ids = session.get(urljoin(api_url, '/contract-api/v1/reportingGroups/' + str(reporting_groupids['rtl']) + '/products/summaries'))
#res_reporting_group_ids = session.get(urljoin(api_url, '/contract-api/v1/reportingGroups/identifiers'))
#res_reporting_group_id = session.get()





#count=0
#for product_id in product_ids:
#    path_url = '/billing-center-api/v2/reporting-groups/'
#    path_url += str(reporting_groupids['rtl'])
#    path_url += '/products/'
#    path_url += str(product_id)
#    path_url += '/measures?year=2017&month=5'
#    pprint(path_url)
#    count+=1
#    usage_reporting_group = session.get(urljoin(api_url, path_url)).json()
#    pprint(usage_reporting_group)
#
#print(count)

