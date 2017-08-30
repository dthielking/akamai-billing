#!/usr/bin/env python3

import requests
import json
import datetime
import pymysql
import sys
from pprint import pprint
from akamai.edgegrid import EdgeGridAuth

currentYear = datetime.datetime.now().year
currentMonth = datetime.datetime.now().month
marketingProductIds = list()
# Get Credetials
with open('akamai_config.json') as config_file:
    config=json.load(config_file)

# Variables for akamai operations
apiUrl = config['akamai_credentials']['api_url']
apiClientToken = config['akamai_credentials']['client_token']
apiClientSecret = config['akamai_credentials']['client_secret']
apiAccessToken = config['akamai_credentials']['access_token']

# Variables for db instance
rdsHost = config['aws_rds_credentials']['rds_endpoint_url']
rdsPort = config['aws_rds_credentials']['rds_endpoint_port']
rdsDb = config['aws_rds_credentials']['rds_db']
rdsUser = config['aws_rds_credentials']['rds_username']
rdsPass = config['aws_rds_credentials']['rds_password']
# Opening Akamai http session
apiSession = requests.Session()
apiSession.auth = EdgeGridAuth(apiClientToken, apiClientSecret, apiAccessToken)
try:
    # Opening MySQL database connection
    mycon = pymysql.connect(host=rdsHost,
                            port=rdsPort,
                            db=rdsDb,
                            user=rdsUser,
                            password=rdsPass)
except:
    print(sys.exc_info())

# Get all Contracts
urlContracts = apiUrl
urlContracts += "/contract-api/v1/contracts/identifiers"

resContracts = apiSession.get(urlContracts).json()

# Insert Contracts into DB
try:
    with mycon.cursor() as cursor:
        selectRes = list()

        sqlSelect = "SELECT ContractId FROM tbl_Contracts"
        cursor.execute(sqlSelect)

        for row in cursor:
            selectRes += row

        for contract in resContracts:
            if contract not in selectRes:
                sql = "INSERT INTO tbl_Contracts(ContractId) VALUES(%s)"
                cursor.execute(sql, contract)

        mycon.commit()
        cursor.close()
except:
    print(sys.exc_info())

# Get all Reporting Group Ids
urlReportingGroupId = apiUrl
urlReportingGroupId += "/contract-api/v1/reportingGroups/identifiers"

resReportingGroupIds = apiSession.get(urlReportingGroupId).json()

try:
    with mycon.cursor() as cursor:
        selectRes = list()

        sqlSelect = "SELECT ReportingGroupId FROM tbl_ReportingGroups"
        cursor.execute(sqlSelect)

        for row in cursor:
            selectRes += row

        for reportingGroupId in resReportingGroupIds:
            if reportingGroupId not in selectRes:
                sql = "INSERT INTO tbl_ReportingGroups(ReportingGroupId) VALUES (%s)"
                cursor.execute(sql, reportingGroupId)

        mycon.commit()
        cursor.close()
except:
    print(sys.exc_info())

# Get All Products
listOfProducts = list()
for contract in resContracts:
    urlProducts = apiUrl
    urlProducts += "/contract-api/v1/contracts/"
    urlProducts += str(contract)
    urlProducts += "/products/summaries"
    resProducts = apiSession.get(urlProducts).json()

    listOfProducts += resProducts['products']['marketing-products']

try:
    with mycon.cursor() as cursor:
        dbProducts = list()

        cursor.execute("SELECT ProductId FROM tbl_Products")
        for row in cursor:
             dbProducts += row

        for product in listOfProducts:
            if product['marketingProductId'] not in dbProducts:
                insertProduct = 'INSERT INTO tbl_Products (ProductId, ProductName) '
                insertProduct += 'VALUES(%(marketingProductId)s, %(marketingProductName)s)'
                cursor.execute(insertProduct, product)

        mycon.commit()
        cursor.close()
except:
    print(sys.exc_info())

# Make ReportingGroup association with Contracts
for reportingGroupId in resReportingGroupIds:
    urlReportingGroupId = apiUrl
    urlReportingGroupId += "/contract-api/v1/reportingGroups/"
    urlReportingGroupId += str(reportingGroupId)
    urlReportingGroupId += "/products/summaries"
    resReportingGroupIds = apiSession.get(urlReportingGroupId)

    contractIds = list()
    if resReportingGroupIds.status_code == 200:
        contractIds.append(resReportingGroupIds.json()['products']['contractId'])
    elif resReportingGroupIds.status_code == 300:
        for ids in resReportingGroupIds.json()['contracts']:
            contractIds.append(ids['id'])

    try:
        with mycon.cursor() as cursor:
            dictSql = {}
            for contractId in contractIds:
                dictSql['contractId'] = contractId
                dictSql['reportingGroupId'] = reportingGroupId

                insertSql = 'INSERT INTO ztbl_ReportingContract(FK_ContractsKey, FK_ReportingGroupKey)'
                insertSql += 'VALUES((SELECT PK_ContractKey FROM tbl_Contracts WHERE ContractId = %(contractId)s),'
                insertSql += '(SELECT PK_ReportingGroupKey FROM tbl_ReportingGroups WHERE ReportingGroupId = %(reportingGroupId)s))'
                cursor.execute(insertSql, dictSql)
        mycon.commit()
        cursor.close()
    except:
        print(sys.exc_info())

try:
    mycon.close()
except:
    print(sys.exc_info())
