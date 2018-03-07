#!/usr/bin/env python36
"""This Module gets statistics from
the akamai api espacially the contracts and
billing api
"""

import argparse
import datetime
import json
import logging
import os
import pymysql
import requests
import sys
from akamai.edgegrid import EdgeGridAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def add_argument_parser():
    """Implementing commandline argument parser

    Returns:
        dictionary -- Returns values of given commandline arguments
    """

    # Initialize parser
    parser = argparse.ArgumentParser(description='This program gets Akamai API statistics')

    # Adding general group to parser
    general_group = parser.add_argument_group(title='General', description='General parameters not specific to any component')
    general_group.add_argument('--verbose', '-v', action='count', help='Increases verbosity')
    general_group.add_argument('--configuration-file', '-c', help='Path to configuration file')
    general_group.add_argument('--log-file-path', '-l', help='Path where to store logfiles')

    # Adding Data group
    data_group = parser.add_argument_group(title='Data', description='Time range to get data from')
    data_group.add_argument('--from-year', help='Must be in numeric format like 1990')
    data_group.add_argument('--to-year', help='Must be in numeric format like 1990')
    data_group.add_argument('--from-month', help='Must be in numeric format with leading 0 if month smaler than ten')
    data_group.add_argument('--to-month', help='Must be in numeric format with leading 0 if month smaler than ten')

    # Adding database group to parser
    db_group = parser.add_argument_group(title='Database configuration parameters', description='This parameters are used to configure the database')
    db_group.add_argument('--database-host', help='Database host endpoint')
    db_group.add_argument('--database-port', help='Database port to connect to')
    db_group.add_argument('--database', help='Database on Host')
    db_group.add_argument('--database-user', help='Database user')
    db_group.add_argument('--database-password', help='Database password.')

    # Adding akamai group to parser
    akamai_group = parser.add_argument_group(
        title='Akamai configuration parameters',
        description='This parameters are used to configure the credentials for Akamai API'
    )
    akamai_group.add_argument('--api-url', help='Akamai API URL provided by Akamai')
    akamai_group.add_argument('--access-token', help='Akamai API access token')
    akamai_group.add_argument('--client-token', help='Akamai API client token')
    akamai_group.add_argument('--client-secret', help='Akamai API client secret')

    return parser.parse_args()


def get_logger(log_level=None, akamai_log_level=None, urllib3_log_level=None, log_file_path=None):
    """Initialize logging engine.

    Internal function to initialize logging engine to receive output specified by logging level.

    Keyword Arguments:
        logger {logger} -- logging engine (default: {None})

    Returns:
        logger -- Initialized logger with it's logging facility.
    """

    logging.basicConfig(
        level=logging.ERROR,
        format='%(levelname)s: %(asctime)s - %(funcName)s at %(lineno)d %(message)s'
    )

    logger = logging.getLogger()

    if log_file_path:
        log_file_handler = logging.FileHandler(log_file_path)
        log_stream_handler = logging.StreamHandler()
        logger.addHandler(log_file_handler)
        logger.addHandler(log_stream_handler)

    if log_level:
        logger.setLevel(log_level)

        if log_level == 'DEBUG':
            logger.debug('Setting loglevel to DEBUG')
            try:
                from pprint import pprint
                logger.debug('Loading pprint module.')
            except ImportError as e:
                logger.error('Module pprint not found!')
                logger.debug('', exc_info=True)
        if log_level == 'INFO':
            logger.info('Set loglevel to INFO')

    if akamai_log_level:
        akamai_log_level = akamai_log_level
    else:
        akamai_log_level = logging.ERROR

    if urllib3_log_level:
        urllib3_log_level = urllib3_log_level
    else:
        urllib3_log_level = logging.ERROR

    loggers = logging.Logger.manager.loggerDict
    if 'lib.akamai' in loggers or 'akamai' in loggers:
        logging.getLogger('akamai').setLevel(akamai_log_level)

    if 'urllib3' in loggers:
        logging.getLogger('urllib3').setLevel(urllib3_log_level)

    return logger


def get_configuration(logger, config_file_path=None):
    """Loads and parses configuration file

    Tries to load configuration file. If no config_file_path is provided,
    this module will test if configuration.json file exists in modules directory,
    f so it will load and parse it. If config_file_path is provided module will load
    and parse it.
    If either of both is provided and existent return value is False.

    Arguments:
        logger {logger} -- Logging engine

    Keyword Arguments:
        config_file_path {string} -- Path to configuration.json file (default: {None})

    Returns:
        dictionary -- dictionary with configuration parameters
    """

    try:
        if config_file_path:
            file = open(config_file_path, 'r')
            logger.debug('Configuration file path: {}'.format(config_file_path))
            config = json.load(file)
        elif os.path.exists(os.path.join(os.path.abspath(__file__), 'configuration.json')):
            config_file_path = os.path.join(os.path.abspath(__file__), 'configuration.json')
            logger.debug('Configuration file path: {}'.format(config_file_path))
            file = open(config_file_path, 'r')
            config = json.load(file)
        else:
            config = False
        logger.debug('Configuration Content: {}'.format(config))
        return config
    except IOError as e:
        logger.error('I/O errno({})'.format(e.errno))
        logger.debug('', exc_info=True)
        sys.exit(127)
    except json.JSONDecodeError as e:
        logger.error('JSON errno({})'.format(e.pos))
        logger.debug('', exc_info=True)
        sys.exit(127)


def get_akamai_credentials(logger, cmd_args=None, akamai_api_config=None):
    """Returns akamai credentials

    This function returns akamai credentials either form environment variables,
    commandline arguments or configuration file.
    The precendence of overwritting arguments provided is as followed:
    Arguments provided by configuration file will be overridden by commandline arguments
    those are possible to override with os environment variables.

    Arguments:
        logger {logger} -- logging engine

    Keyword Arguments:
        cmd_args {argpase arguments} -- Arguments returned by argparse parser. (default: {None})
        akamai_api_config {dictionary} -- Contains dictionary with akamai credentials. (default: {None})

    Returns:
        dictionary -- dictionary with database configuration arguments.
    """

    akamai_conf = dict()

    if akamai_api_config:
        akamai_conf['AKAMAI_CLIENT_TOKEN'] = akamai_api_config['akamai']['client_token']
        akamai_conf['AKAMAI_ACCESS_TOKEN'] = akamai_api_config['akamai']['access_token']
        akamai_conf['AKAMAI_CLIENT_SECRET'] = akamai_api_config['akamai']['client_secret']
        akamai_conf['AKAMAI_API_URL'] = akamai_api_config['akamai']['api_url']

    if 'AKAMAI_CLIENT_TOKEN' in os.environ:
        akamai_conf['AKAMAI_CLIENT_TOKEN'] = os.environ.get('AKAMAI_CLIENT_TOKEN')
    elif cmd_args.client_token:
        akamai_conf['AKAMAI_CLIENT_TOKEN'] = cmd_args.client_token
    if 'AKAMAI_ACCESS_TOKEN' in os.environ:
        akamai_conf['AKAMAI_ACCESS_TOKEN'] = os.environ.get('AKAMAI_ACCESS_TOKEN')
    elif cmd_args.access_token:
        akamai_conf['AKAMAI_ACCESS_TOKEN'] = cmd_args.access_token
    if 'AKAMAI_CLIENT_SECRET' in os.environ:
        akamai_conf['AKAMAI_CLIENT_SECRET'] = os.environ.get('AKAMAI_CLIENT_SECRET')
    elif cmd_args.client_secret:
        akamai_conf['AKAMAI_CLIENT_SECRET'] = cmd_args.client_secret
    if 'AKAMAI_API_URL' in os.environ:
        akamai_conf['AKAMAI_API_URL'] = os.environ.get('AKAMAI_API_URL')
    elif cmd_args.api_url:
        akamai_conf['AKAMAI_API_URL'] = cmd_args.api_url

    debug_output = 'Configuration for Akamai API URL\n'
    debug_output += '\tAkamai Client Token: {}\n'
    debug_output += '\tAkamai Access Token: {}\n'
    debug_output += '\tAkamai Client Secret: {}\n'
    debug_output += '\tAkamai API URL: {}\n'
    debug_output = debug_output.format(
        akamai_conf['AKAMAI_CLIENT_TOKEN'],
        akamai_conf['AKAMAI_ACCESS_TOKEN'],
        akamai_conf['AKAMAI_CLIENT_SECRET'],
        akamai_conf['AKAMAI_API_URL']
    )

    logger.debug('{}'.format(debug_output))
    return akamai_conf


def get_database_creds(logger, cmd_args=None, database_config=None):
    """Returns database credentials

    This function returns database credentials either form environment variables,
    commandline arguments or configuration file.
    The precendence of overwritting arguments provided is as followed:
    Arguments provided by configuration file will be overridden by commandline arguments
    those are possible to override with os environment variables.

    Arguments:
        logger {logger} -- logging engine

    Keyword Arguments:
        cmd_args {argpase arguments} -- Arguments returned by argparse parser. (default: {None})
        database_config {dictionary} -- Contains dictionary with database credentials. (default: {None})

    Returns:
        dictionary -- dictionary with database configuration arguments.
    """

    database_conf = dict(
        DATABASE_HOST='',
        DATABASE_PORT='',
        DATABASE_DB='',
        DATABASE_USER='',
        DATABASE_PASSWORD=''
        )

    if database_config:
        database_conf['DATABASE_HOST'] = database_config['database']['host']
        database_conf['DATABASE_PORT'] = database_config['database']['port']
        database_conf['DATABASE_DB'] = database_config['database']['db']
        database_conf['DATABASE_USER'] = database_config['database']['user']
        database_conf['DATABASE_PASSWORD'] = database_config['database']['password']

    if 'DATABASE_HOST' in os.environ:
        database_conf['DATABASE_HOST'] = os.environ.get('DATABASE_HOST')
    elif cmd_args.database_host:
        database_conf['DATABASE_HOST'] = cmd_args.database_host
    if 'DATABASE_PORT' in os.environ:
        database_conf['DATABASE_PORT'] = os.environ.get('DATABASE_PORT')
    elif cmd_args.database_port:
        database_conf['DATABASE_PORT'] = cmd_args.database_port
    if 'DATABASE_DB' in os.environ:
        database_conf['DATABASE_DB'] = os.environ.get('DATABASE_DB')
    elif cmd_args.database:
        database_conf['DATABASE_DB'] = cmd_args.database
    if 'DATABASE_USER' in os.environ:
        database_conf['DATABASE_USER'] = os.environ.get('DATABASE_USER')
    elif cmd_args.database_user:
        database_conf['DATABASE_USER'] = cmd_args.database_user
    if 'DATABASE_PASSWORD' in os.environ:
        database_conf['DATABASE_PASSWORD'] = os.environ.get('DATABASE_PASSWORD')
    elif cmd_args.database_password:
        database_conf['DATABASE_PASSWORD'] = cmd_args.database_password

    debug_output = 'Database configuration:\n'
    debug_output += '\tDatabasehost: {}\n'
    debug_output += '\tDatabaseport: {}\n'
    debug_output += '\tDatabase: {}\n'
    debug_output += '\tDatabaseuser: {}\n'
    debug_output += '\tDatabase password: {}'
    logger.debug(debug_output.format(
            database_conf['DATABASE_HOST'],
            database_conf['DATABASE_PORT'],
            database_conf['DATABASE_DB'],
            database_conf['DATABASE_USER'],
            database_conf['DATABASE_PASSWORD']
            ))
    return database_conf


def get_retry_session(akamai_credentials, logger, retries=3, backoff_factor=0.03):
    """Akamai API authentication

    Authenticate against Akamai API and returns authenticated session object

    Arguments:
        akamai_credentials {dictionary} -- Dictionary with akamai credentials
        logger {logger} -- Logging engine

    Keyword Arguments:
    """

    try:
        akamai_session = requests.session()
        akamai_session.auth = EdgeGridAuth(
            akamai_credentials['AKAMAI_CLIENT_TOKEN'],
            akamai_credentials['AKAMAI_CLIENT_SECRET'],
            akamai_credentials['AKAMAI_ACCESS_TOKEN']
        )

        retry = Retry(
            total=retries,
            connect=retries,
            read=retries,
            redirect=retries,
            status=retries,
            backoff_factor=backoff_factor
        )
        adapter = HTTPAdapter(max_retries=retry)

        akamai_session.mount('http://', adapter)
        akamai_session.mount('https://', adapter)

        return akamai_session
    except:
        logger.error('Cannot authenticate against Akamai API')
        logger.debug('', sys_exc=True)
        sys.exit(127)


def get_product_statitics(reporting_group_id, product_id, requests_session, api_url, from_year, to_year, from_month, to_month, logger):
    # Get statistics from API and write them into DB
    query = '?fromYear={}&fromMonth={}&toYear={}&toMonth={}'
    query = query.format(from_year, from_month, to_year, to_month)
    logger.debug('URL Query parameters: {}'.format(query))
    url = '/billing-center-api/v2/reporting-groups/{}/products/{}/measures{}'
    url = url.format(reporting_group_id, product_id, query)

    response = requests_session.get(api_url + url)
    logger.debug('{}'.format(response.json()))
    return response


def assoc_repgrp_product(reporting_group_id, product_ids, sql_connection, logger):
    """ Makes the association between ReportingGroups and Products """

    # Association between Reporting Group and Product
    for product in product_ids:
        reporting_product = {'reportingGroupId': reporting_group_id,
                             'productId': product['marketingProductId']}

        sql_insert = 'INSERT INTO ztbl_reportingproduct(ProductsKey, ReportingGroupKey) '
        sql_insert += 'Values(%(productId)s, %(reportingGroupId)s) '
        sql_insert += 'ON DUPLICATE KEY UPDATE ProductsKey = %(productId)s, '
        sql_insert += 'ReportingGroupKey = %(reportingGroupId)s'

        with sql_connection.cursor() as cursor:
            cursor.execute(sql_insert, reporting_product)
            sql_connection.commit()


def assoc_repgrp_contract(reporting_group_id, contract_id, sql_connection, logger):
    """ Makes the association between ReportingGroups and Contracts """
    # Association between Reporting Group and Contract
    sql_insert = 'INSERT INTO ztbl_reportingcontract(ReportingGroupKey, ContractsKey) '
    sql_insert += 'Values(%(reportingGroupId)s, %(contractId)s) '
    sql_insert += 'ON DUPLICATE KEY UPDATE ReportingGroupKey = '
    sql_insert += '%(reportingGroupId)s, ContractsKey = %(contractId)s'

    sql_data = dict()
    sql_data['reportingGroupId'] = reporting_group_id
    sql_data['contractId'] = contract_id

    with sql_connection.cursor() as cursor:
        cursor.execute(sql_insert, sql_data)
        sql_connection.commit()


def insert_statistics_db(statistics, reporting_group_id, product_id, sql_connection, logger):
    """ Writes list of statistics into database """
    for statistic in statistics:
        if statistic:
            insert_data = dict()
            insert_data['value'] = statistic['value']
            insert_data['date'] = statistic['date']
            insert_data['final'] = statistic['final']
            insert_data['unit'] = statistic['statistic']['unit']
            insert_data['statistictype'] = statistic['statistic']['name']
            insert_data['productsid'] = product_id
            insert_data['reportinggroupid'] = reporting_group_id

            sql_insert = 'INSERT INTO tbl_reportinggroupstatistics('
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

    # Add argument parser
    cmd_args = add_argument_parser()

    # Initializing global Variables
    date = datetime.datetime.now()
    from_year = date.year
    to_year = date.year
    from_month = date.month-1
    to_month = date.month

    # Getting year and month if specified as an commandline argument
    if cmd_args.from_year:
        from_year = cmd_args.from_year
    if cmd_args.to_year:
        to_year = cmd_args.to_year
    if cmd_args.from_month:
        from_month = cmd_args.from_month
    if cmd_args.to_month:
        to_month = cmd_args.to_month

    # Getting logger and setting logging level
    if cmd_args.log_file_path:
        log_file_path = cmd_args.log_file_path
    else:
        log_file_path = None

    if 'LOG_LEVEL' in os.environ:
        logger = get_logger(log_level=os.environ.get('LOG_LEVEL').upper(), log_file_path=log_file_path)
    elif cmd_args.verbose:
        if cmd_args.verbose == 1:
            logger = get_logger(log_level=logging.DEBUG, log_file_path=log_file_path)
            logger.info('Setting Loglevel to DEBUG for akamaibilling')
        elif cmd_args.verbose >= 2:
            logger = get_logger(log_level=logging.DEBUG, akamai_log_level=logging.DEBUG, urllib3_log_level=logging.DEBUG, log_file_path=log_file_path)
            logger.info('Setting Loglevel to DEBUG for akamaibilling, akamai_edgegrid, urllib3')
    else:
        logger = get_logger(log_file_path=log_file_path)

    # Get configuration either provided via commandline argument directly from projects directory
    if cmd_args.configuration_file:
        configuration = get_configuration(config_file_path=cmd_args.configuration_file, logger=logger)
    else:
        configuration = get_configuration(logger=logger)

    # Getting credentials to connect to database and akamai api
    database_creds = get_database_creds(cmd_args=cmd_args, database_config=configuration, logger=logger)
    akamai_creds = get_akamai_credentials(cmd_args=cmd_args, akamai_api_config=configuration, logger=logger)
    api_url = akamai_creds['AKAMAI_API_URL']

    # Authenticate against Akamai API
    session = get_retry_session(akamai_creds, logger=logger)

    # Open SQL Connection to database
    try:
        sql_con = pymysql.connect(
            host=database_creds['DATABASE_HOST'],
            port=database_creds['DATABASE_PORT'],
            db=database_creds['DATABASE_DB'],
            user=database_creds['DATABASE_USER'],
            password=database_creds['DATABASE_PASSWORD']
        )
    except pymysql.DatabaseError as e:
        logger.error('DB errno({})'.format(e.args[0]))
        logger.debug('', exc_info=True)
        sys.exit(127)

    # Make API Calls to get contracts ids
    response = session.get(api_url + '/contract-api/v1/contracts/identifiers?depth=TOP')
    logger.debug('{}'.format(response.json()))

    # Insert Contracts to DB without duplicates
    if response.status_code == 200:
        try:
            for contract_id in response.json():
                sql_insert = 'INSERT INTO tbl_contracts (ContractId) VALUES("{0}") '
                sql_insert += 'ON DUPLICATE KEY UPDATE ContractId = "{0}"'
                sql_insert = sql_insert.format(contract_id)
                logger.debug('SQL Insert ContractId: {}'.format(sql_insert))

                with sql_con.cursor() as cursor:
                    cursor.execute(sql_insert)
                    sql_con.commit()
        except pymysql.DatabaseError as dberr:
            logger.error('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))
            logger.debug('', exc_info=True)
            sys.exit(127)

        # Generate list of products uri
        for contract_id in response.json():
            product_uri = '/contract-api/v1/contracts/{}/products/summaries'.format(contract_id)
            logger.debug('Product URI: {}'.format(product_uri))

            response = session.get(api_url + product_uri)
            if response.status_code == 200:
                products = response.json()['products']['marketing-products']
                logger.debug('{}'.format(products))
            else:
                logger.error('Products API request not successfull HTTP status: {}'.format(response.status_code))
                logger.debug('{}'.format(response.json()))
                sys.exit(127)

            # Call API with products_uri
            for product in products:
                # Insert products into db without duplicates
                logger.debug('{}'.format(product))
                try:
                    sql_insert = 'INSERT INTO tbl_products(ProductId, ProductName) '
                    sql_insert += 'VALUES ("{marketingProductId}", "{marketingProductName}") '
                    sql_insert += 'ON DUPLICATE KEY UPDATE ProductId = "{marketingProductId}"'
                    sql_insert = sql_insert.format_map(product)
                    logger.debug('SQL Insert Product: {}'.format(sql_insert))

                    with sql_con.cursor() as cursor:
                        cursor.execute(sql_insert, product)
                        sql_con.commit()
                except pymysql.DatabaseError as dberr:
                    logger.error('Errno({0}): {1}'.format(dberr.args[0], dberr.args[1]))
                    logger.debug('DEBUG: ', exc_info=True)
                    sys.exit(127)
    else:
        logger.error('Contracts API request not successfull HTTP status: {}'.format(response.status_code))
        logger.debug('{}'.format(response.json()))
        sys.exit(127)

    # Make API Call to get reporting group ids
    res_repgrp = session.get(api_url + '/contract-api/v1/reportingGroups/')

    if res_repgrp.status_code == 200:
        try:
            logger.debug('{}'.format(res_repgrp.json()))
            for repgrp in res_repgrp.json():
                # Insert Reporting Groups into DB
                sql_insert = 'INSERT INTO tbl_reportinggroups (ReportingGroupId, ReportingGroupName) VALUES ("{id}", "{name}") '
                sql_insert += 'ON DUPLICATE KEY UPDATE ReportingGroupId = "{id}",'
                sql_insert += 'ReportingGroupName = "{name}"'
                sql_insert = sql_insert.format_map(repgrp)
                logger.debug('{}'.format(sql_insert))

                with sql_con.cursor() as cursor:
                    # Insert reporting groups to DB without duplicates
                    cursor.execute(sql_insert, repgrp)
                    sql_con.commit()

                # Generating ReportingGroup URLs to get Products per ReportingGroup
                resp = session.get(api_url + '/contract-api/v1/reportingGroups/{}/products/summaries'.format(repgrp['id']))

                if resp.status_code == 200:
                    assoc_repgrp_contract(repgrp['id'], resp.json()['products']['contractId'], sql_con, logger)
                    assoc_repgrp_product(repgrp['id'], resp.json()['products']['marketing-products'], sql_con, logger)

                    for product in resp.json()['products']['marketing-products']:
                            response_stats = get_product_statitics(
                                repgrp['id'],
                                product['marketingProductId'],
                                session,
                                api_url,
                                from_year,
                                to_year,
                                from_month,
                                to_month,
                                logger
                            )

                            if response_stats.status_code == 200:
                                insert_statistics_db(response_stats.json(), repgrp['id'], product['marketingProductId'], sql_con, logger)

                elif resp.status_code == 300:
                    for contract_link in resp.json()['contracts']:
                        response = session.get(api_url + contract_link['href'])

                        assoc_repgrp_contract(repgrp['id'], response.json()['products']['contractId'], sql_con, logger)
                        assoc_repgrp_product(repgrp['id'], response.json()['products']['marketing-products'], sql_con, logger)
                        for product in response.json()['products']['marketing-products']:
                            response_stats = get_product_statitics(
                                repgrp['id'],
                                product['marketingProductId'],
                                session,
                                api_url,
                                from_year,
                                to_year,
                                from_month,
                                to_month,
                                logger
                            )

                            if response_stats.status_code == 200:
                                insert_statistics_db(response_stats.json(), repgrp['id'], product['marketingProductId'], sql_con, logger)

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
