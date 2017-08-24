#!/usr/bin/env python3

import requests
import json
import itertools
import datetime
from pprint import pprint
from urllib.parse import urljoin
from akamai.edgegrid import EdgeGridAuth

currentYear = datetime.datetime.now().year
currentMonth = datetime.datetime.now().month
marketingProductIds = list()

# Get Credetials
with open('akamai_credentials.json') as credentials_file:
    credentials=json.load(credentials_file)

# Variables for akamai operations
apiUrl = credentials['akamai_credentials']['api_url']
apiClientToken = credentials['akamai_credentials']['client_token']
apiClientSecret = credentials['akamai_credentials']['client_secret']
apiAccessToken = credentials['akamai_credentials']['access_token']

# Opening Akamai http session
apiSession = requests.Session()
apiSession.auth = EdgeGridAuth(apiClientToken, apiClientSecret, apiAccessToken)

# Get all Reporting Group Ids
urlReportingGroupId = apiUrl
urlReportingGroupId += "/contract-api/v1/reportingGroups/identifiers"

reportingGroupIds = apiSession.get(urlReportingGroupId).json()


#usageDataFilter = {
#        "statisticTypes": [
#            "Total MB",
#            ],
#        "month": currentMonth,
#        "year": currentYear,
#        "productIds": reportingGroupIds[0]
#        }
usageDataFilter ={
    "statisticTypes": [
        "Total MB"
    ],
    "contractIds": [
        "3-O5GPDD"
    ],
    "month": 7,
    "year": 2017,
    "reportingGroupIds": [
        121692,
        121693,
        121694
    ]
}

print(usageDataFilter)
usageDataUrl = apiUrl + "/billing-center-api/v2/measures/find"
usageDataRes = apiSession.post(usageDataUrl, data=usageDataFilter)
pprint(usageDataRes.json())

# Gather all products per reporting group
#for reportingGroupId in reportingGroupIds:
#    urlProductsPerReportingGroup = apiUrl
#    urlProductsPerReportingGroup += "/contract-api/v1/reportingGroups/"
#    urlProductsPerReportingGroup += str(reportingGroupId)
#    urlProductsPerReportingGroup += "/products/summaries"
#
#    # Delete following if when it goes productive
#    if reportingGroupId == 72077:
#        productsPerReportingGroup = apiSession.get(urlProductsPerReportingGroup).json()
#        pprint(productsPerReportingGroup)
#        # Getting status_code of request,
#        # if status_code is 300 there are more contracts
#        # associated with ReportingGroup
#        statusCodeProductsPerReportingGroup = apiSession.get(urlProductsPerReportingGroup).status_code
#
#        if statusCodeProductsPerReportingGroup == 200:
#            for marketingProduct in productsPerReportingGroup['products']['marketing-products']:
#                urlUsagePerReportingGroup = apiUrl
#                urlUsagePerReportingGroup += "/billing-center-api/v2/reporting-groups/{}/products/{}/measures"
#                urlUsagePerReportingGroup += "?year={}&month={}&statisticName=Total%20MB"
#                urlUsagePerReportingGroup = urlUsagePerReportingGroup.format(reportingGroupId,
#                                            marketingProduct['marketingProductId'], currentYear, currentMonth)
#
#                #usagePerReportingGroup = apiSession.get(urlUsagePerReportingGroup).json()
#                #print("Marketing Productname: " + marketingProduct['marketingProductName'])
#                #print("Marketing Product Id: " + marketingProduct['marketingProductId'])
#                #print("Usage per Product and Reporting Group")
#                #pprint(usagePerReportingGroup)
#        elif statusCodeProductsPerReportingGroup == 300:
#            for productsPerContract in productsPerReportingGroup['contracts']:
#                productsPerReportingGroup = apiSession.get(apiUrl + productsPerContract['href'])
#
