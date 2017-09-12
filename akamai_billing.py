#!/usr/bin/env python3
""" This Module gets statistics from
the akamai api espacially the contracts and
billing api
 """
import sys
import json
import datetime
import requests
import pymysql
from akamai.edgegrid import EdgeGridAuth

def get_product_statitics(reporting_group_id, product_ids, requests_session, api_url, datetime_now = None):
    if not datetime_now:
        try:
            import datetime
            date = datetime.datetime.now()
            current_year = date.year
            current_month = date.month
        except ImportError:
            print("Module not loadable.")
            print(sys.exc_info())
            sys.exit()
    else:
        current_year = datetime_now.year
        current_month = datetime_now.month

    for product in product_ids:
        # Get statistics from API and write them into DB
        query = '?fromYear={}&fromMonth={}&toYear={}&toMonth={}'
        query = query.format(current_year, current_month-1, current_year, current_month)
        url = '/billing-center-api/v2/reporting-groups/{}/products/{}/measures{}'
        url = url.format(reporting_group_id, product_ids, query)

        response_stats = requests_session.get(api_url + url)
        return response_stats

def assoc_repgrp_product(reporting_group_id, product_ids, sql_con):
    """ Makes the association between ReportingGroups and Products """

    # Association between Reporting Group and Product
    for product in product_ids:
        reporting_product = {'reportingGroupId': reporting_group_id,
                             'productId': product['marketingProductId']}

        sql_insert = 'INSERT INTO ztbl_ReportingProduct(ProductsKey, ReportingGroupKey) '
        sql_insert += 'Values(%(productId)s, %(reportingGroupId)s) '
        sql_insert += 'ON DUPLICATE KEY UPDATE ProductsKey = %(productId)s, '
        sql_insert += 'ReportingGroupKey = %(reportingGroupId)s'

        with sql_con.cursor() as cursor:
            cursor.execute(sql_insert, reporting_product)
            sql_con.commit()

def assoc_repgrp_contract(reporting_group_id, contract_id, sql_con):
    """ Makes the association between ReportingGroups and Contracts """
    # Association between Reporting Group and Contract
    sql_insert = 'INSERT INTO ztbl_ReportingContract(ReportingGroupKey, ContractsKey) '
    sql_insert += 'Values(%(reportingGroupId)s, %(contractId)s) '
    sql_insert += 'ON DUPLICATE KEY UPDATE ReportingGroupKey = '
    sql_insert += '%(reportingGroupId)s, ContractsKey = %(contractId)s'

    sql_data = dict()
    sql_data['reportingGroupId'] = reporting_group_id
    sql_data['contractId'] = contract_id

    with sql_con.cursor() as cursor:
        cursor.execute(sql_insert, sql_data)
        sql_con.commit()

def insert_statistics_db(statistics, reporting_group_id, sql_connection):
    """ Writes list of statistics into database """

    for statistic in statistics:
        if statistic:
            insert_data = dict()
            insert_data['value'] = statistic['value']
            insert_data['date'] = statistic['date']
            insert_data['final'] = statistic['final']
            insert_data['unit'] = statistic['statistic']['unit']
            insert_data['statistictype'] = statistic['statistic']['name']
            insert_data['productsid'] = statistic['productId']
            insert_data['reportinggroupid'] = reporting_group_id

            sql_insert = 'INSERT INTO tbl_ReportingGroupStatistics('
            sql_insert += 'Value, Date, Final, Productsid, '
            sql_insert += 'ReportingGroupId, Unit, StatisticType) '
            sql_insert += 'VALUES(%(value)s, %(date)s, %(final)s, %(productsid)s, '
            sql_insert += '%(reportinggroupid)s, %(unit)s, %(statistictype)s)'
            sql_insert += 'ON DUPLICATE KEY UPDATE Value= %(value)s'

            with sql_connection.cursor() as cursor:
                cursor.execute(sql_insert, insert_data)
                sql_connection.commit()


def main():
    """ Main function """
    # Initializing global Variables
    date = datetime.datetime.now()

    # Load configuration file
    try:
        file = open('./akamai_config.json', 'r')
        config = json.load(file)
    except IOError as err:
        print('I/O errno({}): {}'.format(err.errno, err.strerror))
        print(sys.exc_info())
    except json.JSONDecodeError as jerr:
        print('JSON errno({}): {}'.format(jerr.pos, jerr.msg))
        print(sys.exc_info())

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
        print(sys.exc_info())

    # Akamain API Url
    api_url = config['akamai']['api_url']

    # Make API Calls to get contracts ids
    resp_contr = session.get(api_url + '/contract-api/v1/contracts/identifiers?depth=TOP')

    # Insert Contracts to DB without duplicates
    if resp_contr.status_code == 200:
        try:
            for contract_id in resp_contr.json():
                sql_insert = 'INSERT INTO tbl_contracts(ContractId) VALUES(%s) '
                sql_insert += 'ON DUPLICATE KEY UPDATE ContractId = %s'
 
                with sql_con.cursor() as cursor:
                    cursor.execute(sql_insert, (contract_id, contract_id))
                    sql_con.commit()

        except pymysql.DatabaseError as dberr:
            print('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))
            print(sys.exc_info())
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
                    print(sys.exc_info())
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
                sql_insert = 'INSERT INTO tbl_reportinggroups (ReportingGroupId) VALUES (%s) '
                sql_insert += 'ON DUPLICATE KEY UPDATE ReportingGroupId = %s'

                with sql_con.cursor() as cursor:
                    # Insert reporting groups to DB without duplicates
                    cursor.execute(sql_insert, (repgrp, repgrp))
                    sql_con.commit()

                # Generating ReportingGroup URLs to get Products per ReportingGroup
                resp = session.get(api_url +
                                   '/contract-api/v1/reportingGroups/{}/products/summaries'
                                   .format(repgrp))

                if resp.status_code == 200:
                    assoc_repgrp_contract(repgrp, resp.json()['products']['contractId'], sql_con)
                    assoc_repgrp_product(repgrp, resp.json()['products']['marketing-products'], sql_con)

                    response_stats = get_product_statitics(repgrp, resp.json()['products']['marketing-products'], session, api_url, date)
                    if response_stats.status_code == 200:
                        insert_statistics_db(response_stats, repgrp, sql_con)

                elif resp.status_code == 300:
                    for contract_link in resp.json()['contracts']:
                        # Dirty ugly hack to call API when multiple Contracts
                        # are associated to ReportingGroups
                        # If Akamai fixes the href we can remove .replace()
                        response = session.get(api_url + contract_link['href'].replace(
                            'v1.0', 'v1'
                        ))

                        assoc_repgrp_contract(repgrp, response.json()['products']['contractId'], sql_con)
                        assoc_repgrp_product(repgrp, response.json()['products']['marketing-products'], sql_con)
                        response_stats = get_product_statitics(repgrp, response.json()['products']['marketing-products'], session, api_url, date)
                        if response_stats.status_code == 200:
                            insert_statistics_db(response_stats, repgrp, sql_con)

        except pymysql.DatabaseError as dberr:
            print('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))
            print(sys.exc_info())
        finally:
            cursor.close()

    try:
        sql_con.close()
    except pymysql.DatabaseError as dberr:
        print('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))
        print(sys.exc_info())

if __name__ == '__main__':
    # Call main()
    main()
