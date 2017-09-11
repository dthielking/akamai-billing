#!/usr/bin/env python3
""" blub """
import sys
import json
import datetime
import requests
import pymysql
from akamai.edgegrid import EdgeGridAuth

from pprint import pprint

def main():
    """ Main function """
    # Load configuration file
    try:
        file = open('./akamai_config.json', 'r')
        config = json.load(file)
    except IOError as err:
        print('I/O errno({}): {}'.format(err.errno, err.strerror))
    except json.JSONDecodeError as jerr:
        print('JSON errno({}): {}'.format(jerr.pos, jerr.msg))

    # Authenticate against Akamai API
    session = requests.session()
    session.auth = EdgeGridAuth(
        config['akamai']['client_token'],
        config['akamai']['client_secret'],
        config['akamai']['access_token']
    )

    # Open SQL Connection to database
    try:
        sql_con = pymysql.connect(
            host=config['sql']['host'],
            port=config['sql']['port'],
            db=config['sql']['db'],
            user=config['sql']['user'],
            password=config['sql']['password']
        )
    except pymysql.DatabaseError as dberr:
        print('DB errno({}): {}'.format(dberr.args[0], dberr.args[1]))

    # Akamain API Url
    api_url = config['akamai']['api_url']

    # Make API Calls to get contracts ids
    resp_contr = session.get(api_url + '/contract-api/v1/contracts/identifiers?depth=TOP')

    # Insert Contracts to DB without duplicates
    if resp_contr.status_code == 200:
        try:
            for contract_id in resp_contr.json():
                sql_insert = 'INSERT INTO tbl_contracts(ContractId) VALUES("{0}") '
                sql_insert += 'ON DUPLICATE KEY UPDATE ContractId = "{0}"'
                sql_insert = sql_insert.format(contract_id)

                with sql_con.cursor() as cursor:
                    cursor.execute(sql_insert)
                    sql_con.commit()

        except pymysql.DatabaseError as dberr:
            print('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))
        finally:
            cursor.close()

        # Generate list of products uri
        for contract_id in resp_contr.json():
            product_uri = '/contract-api/v1/contracts/{}/products/summaries'.format(contract_id)
            # Call API with products_uri
            for product in session.get(api_url + product_uri).json()['products']['marketing-products']:
                # Insert products into db without duplicates
                try:
                    sql_insert = 'INSERT INTO tbl_products(ProductId, ProductName) '
                    sql_insert += 'VALUES (%(marketingProductId)s, %(marketingProductName)s) '
                    sql_insert += 'ON DUPLICATE KEY UPDATE ProductId = %(marketingProductId)s'

                    with sql_con.cursor() as cursor:
                        cursor.execute(sql_insert, product)
                        sql_con.commit()

                except pymysql.DatabaseError as dberr:
                    print('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))
                finally:
                    cursor.close()
    else:
        sys.exit('Contract:HTTP Status not 200. HTTP status: {}'.format(resp_contr.status_code))

    # Make API Call to get reporting groups ids
    res_repgrp = session.get(api_url + '/contract-api/v1/reportingGroups/identifiers')

    if res_repgrp.status_code == 200:
        try:
            for repgrp in res_repgrp.json():
                # Insert Reporting Groups into DB
                sql_insert = 'INSERT INTO tbl_reportinggroups (ReportingGroupId) VALUES ("{0}") '
                sql_insert += 'ON DUPLICATE KEY UPDATE ReportingGroupId = "{0}"'
                sql_insert = sql_insert.format(repgrp)

                with sql_con.cursor() as cursor:
                    # Insert reporting groups to DB without duplicates
                    cursor.execute(sql_insert)
                    sql_con.commit()

                # Generating ReportingGroup URLs to get Products per ReportingGroup
                resp = session.get(api_url +
                                   '/contract-api/v1/reportingGroups/{}/products/summaries'
                                   .format(repgrp))

                # Get current year and month for querying
                current_year = datetime.datetime.now().year
                current_month = datetime.datetime.now().month

                if resp.status_code == 200:

                    # Association between Reporting Group and Contract
                    sql_insert = 'INSERT INTO ztbl_ReportingContract(ReportingGroupKey, ContractsKey) '
                    sql_insert += 'Values(%(reportingGroupId)s, %(contractId)s) '
                    sql_insert += 'ON DUPLICATE KEY UPDATE ReportingGroupKey = '
                    sql_insert += '%(reportingGroupId)s, ContractsKey = %(contractId)s'

                    sql_data = dict()
                    sql_data['reportingGroupId'] = repgrp
                    sql_data['contractId'] = resp.json()['products']['contractId']

                    with sql_con.cursor() as cursor:
                        cursor.execute(sql_insert, sql_data)
                        sql_con.commit()

                    # Association between Reporting Group and Product
                    for product in resp.json()['products']['marketing-products']:
                        reporting_product = {'reportingGroupId': repgrp,
                                              'productId': product['marketingProductId']}

                        sql_insert = 'INSERT INTO ztbl_ReportingProduct(ProductsKey, ReportingGroupKey) '
                        sql_insert += 'Values(%(productId)s, %(reportingGroupId)s) '
                        sql_insert += 'ON DUPLICATE KEY UPDATE ProductsKey = %(productId)s, '
                        sql_insert += 'ReportingGroupKey = %(reportingGroupId)s'

                        with sql_con.cursor() as cursor:
                            cursor.execute(sql_insert, reporting_product)
                            sql_con.commit()

                        # Get statistics from API and write them into DB
                        query = '?fromYear={}&fromMonth={}&toYear={}&toMonth={}'
                        query = query.format(current_year, current_month-1, current_year, current_month)
                        url = '/billing-center-api/v2/reporting-groups/{}/products/{}/measures{}'
                        url = url.format(repgrp, reporting_product['productId'], query)
        
                        response_stats = session.get(api_url + url)
                        for response_stat in response_stats.json():
                            if response_stat:
                                insert_data = dict()
                                insert_data['value'] = response_stat['value']
                                insert_data['date'] = response_stat['date']
                                insert_data['final'] = response_stat['final']
                                insert_data['unit'] = response_stat['statistic']['unit']
                                insert_data['statistictype'] = response_stat['statistic']['name']
                                insert_data['productsid'] = reporting_product['productId']
                                insert_data['reportinggroupid'] = repgrp

                                sql_insert = 'INSERT INTO tbl_ReportingGroupStatistics('
                                sql_insert += 'Value, Date, Final, Productsid, '
                                sql_insert += 'ReportingGroupId, Unit, StatisticType) '
                                sql_insert += 'VALUES(%(value)s, %(date)s, %(final)s, %(productsid)s, '
                                sql_insert += '%(reportinggroupid)s, %(unit)s, %(statistictype)s)'
                                sql_insert += 'ON DUPLICATE KEY UPDATE Value= %(value)s'

                                with sql_con.cursor() as cursor:
                                    cursor.execute(sql_insert, insert_data)
                                    sql_con.commit()

                elif resp.status_code == 300:
                    for contract_link in resp.json()['contracts']:
                        # Dirty ugly hack to call API when multiple Contracts
                        # are associated to ReportingGroups
                        # If Akamai fixes the href we can remove .replace()
                        response = session.get(api_url + contract_link['href'].replace(
                            'v1.0', 'v1'
                        ))

                        sql_insert = 'INSERT INTO ztbl_ReportingContract(ReportingGroupKey, ContractsKey) '
                        sql_insert += 'Values(%(reportingGroupId)s, %(contractId)s) '
                        sql_insert += 'ON DUPLICATE KEY UPDATE ReportingGroupKey = '
                        sql_insert += '%(reportingGroupId)s, ContractsKey = %(contractId)s'
                        sql_data = dict()
                        sql_data['reportingGroupId'] = repgrp
                        sql_data['contractId'] = response.json()['products']['contractId']

                        with sql_con.cursor() as cursor:
                            cursor.execute(sql_insert, sql_data)
                            sql_con.commit()

                        # Association between Reporting Group and Product
                        for product in response.json()['products']['marketing-products']:

                            reporting_product = {'reportingGroupId': repgrp,
                                                 'productId': product['marketingProductId']}
                            
                            sql_insert = 'INSERT INTO ztbl_ReportingProduct(ProductsKey, ReportingGroupKey) '
                            sql_insert += 'Values(%(productId)s, %(reportingGroupId)s) '
                            sql_insert += 'ON DUPLICATE KEY UPDATE ProductsKey = %(productId)s, '
                            sql_insert += 'ReportingGroupKey = %(reportingGroupId)s'

                            with sql_con.cursor() as cursor:
                                cursor.execute(sql_insert, reporting_product)
                                sql_con.commit()

                            # Get statistics from API and write them into DB
                            query = '?fromYear={}&fromMonth={}&toYear={}&toMonth={}'
                            query = query.format(current_year, current_month-1, current_year, current_month)
                            url = '/billing-center-api/v2/reporting-groups/{}/products/{}/measures{}'
                            url = url.format(repgrp, reporting_product['productId'], query)
            
                            response_stats = session.get(api_url + url)
                            for response_stat in response_stats.json():
                                if response_stat:
                                    insert_data = dict()
                                    insert_data['value'] = response_stat['value']
                                    insert_data['date'] = response_stat['date']
                                    insert_data['final'] = response_stat['final']
                                    insert_data['unit'] = response_stat['statistic']['unit']
                                    insert_data['statistictype'] = response_stat['statistic']['name']
                                    insert_data['productsid'] = reporting_product['productId']
                                    insert_data['reportinggroupid'] = repgrp

                                    sql_insert = 'INSERT INTO tbl_ReportingGroupStatistics('
                                    sql_insert += 'Value, Date, Final, Productsid, '
                                    sql_insert += 'ReportingGroupId, Unit, StatisticType) '
                                    sql_insert += 'VALUES(%(value)s, %(date)s, %(final)s, %(productsid)s, '
                                    sql_insert += '%(reportinggroupid)s, %(unit)s, %(statistictype)s)'
                                    sql_insert += 'ON DUPLICATE KEY UPDATE Value= %(value)s'

                                    with sql_con.cursor() as cursor:
                                        cursor.execute(sql_insert, insert_data)
                                        sql_con.commit()

        except pymysql.DatabaseError as dberr:
            print('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))
            print(sys.exc_info)
        finally:
            cursor.close()

    try:
        sql_con.close()
    except pymysql.DatabaseError as dberr:
        print('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))

if __name__ == '__main__':
    # Call main()
    main()
