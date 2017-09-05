#!/usr/bin/env python3
""" This module works with Akamai API """
# Imports of this module
import datetime
import json
import grequests
import pymysql
from akamai.edgegrid import EdgeGridAuth

from pprint import pprint

class AkamaiBilling:
    """Main Class for Akamai Billing"""

    __api_session = None
    __sql_con = None
    __configuration = None
    __api_url = None
    marketing_product_ids = list()

    def __init__(self, path_to_config_file):
        self.path_to_config_file = path_to_config_file
        self.current_year = datetime.datetime.now().year
        self.current_month = datetime.datetime.now().month
        # Tries to open configuration file and load json
        self.__config()
        # Authenticate against Akamai API
        self.__akamai_auth()
        # Opens the sql db connections
        self.__sql_connection()
        # Get API URL and make them global Available
        self.__api_url = self.get_api_url()

    def __config(self):
        """Loads configuration file from given path and returns a python dictionary
        Keyword arguments:
        path_to_config_file -- Path to a JSON encoded Configuration file
        """
        try:
            config_file = open(self.path_to_config_file)
            self.__configuration = json.load(config_file)
        except IOError as io_error:
            print("I/O error({0}: {1}".format(io_error.errno, io_error.strerror))
        except json.JSONDecodeError as json_error:
            print("JSON error({0}): {1}".format(json_error.pos, json_error.msg))

    def __sql_connection(self):
        """ Opens connection to MySQL Database
        Keyword arguments:
        config -- Object that includes the Akamai API URL
        Return:
        Open connection to MySQL database
        """
        try:
            # Opening MySQL database connection
            self.__sql_con = pymysql.connect(
                host=self.__configuration['sql']['host'],
                port=self.__configuration['sql']['port'],
                db=self.__configuration['sql']['db'],
                user=self.__configuration['sql']['user'],
                password=self.__configuration['sql']['password'],
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.DatabaseError as db_error:
            print('DB error({0}): {1}'.format(db_error.args[0], db_error.args[1]))

    def __akamai_auth(self):
        """Authenticate against Akamai API
        Return:
        Session object that is authenticated against the Akamai API
        """
        api_client_token = self.__configuration['akamai']['client_token']
        api_client_secret = self.__configuration['akamai']['client_secret']
        api_access_token = self.__configuration['akamai']['access_token']

        # Opening Akamai http session
        self.__api_session = grequests.Session()
        self.__api_session.auth = EdgeGridAuth(
            api_client_token, api_client_secret, api_access_token)

    def get_api_url(self):
        """Returns the Akamai API URL
        Keyword arguments:
        config -- Object that includes the Akamai API URL
        Return:
        String with Akamai API URL
        """
        api_url = self.__configuration['akamai']['api_url']
        return api_url

    def make_api_call(self, api_path):
        """ Returns API Call as Python Object
        If status_code not 200 returns the response itself """
        response = self.__api_session.get(self.__api_url + api_path)
        if response.status_code == 200:
            return response.json()
        else:
            return response

    def sql_statement(self, sql_statement, sql_data=None,
                      sql_select_dup_ids_statement=None, search_id=None):
        """ Inserts SQL statement into db """
        # Insert SQL data into DB
        try:
            with self.__sql_con.cursor() as cursor:
                select_res = list()

                if sql_select_dup_ids_statement:
                    cursor.execute(sql_select_dup_ids_statement)
                    result = cursor.fetchall()
                    for row in result:
                        select_res += list(row.values())

                if sql_data:
                    if isinstance(sql_data, list):
                        for data in sql_data:
                            if search_id and isinstance(data, dict):
                                if data[search_id] not in select_res:
                                    cursor.execute(sql_statement, data)
                            else:
                                if data not in select_res:
                                    cursor.execute(sql_statement, data)
                    else:
                        cursor.execute(sql_statement, (sql_data))
                else:
                    cursor.execute(sql_statement)

                self.__sql_con.commit()
                return cursor
        except pymysql.DatabaseError as db_error:
            print("Errno({0}): {1}".format(db_error.args[0], db_error.args[1]))
        finally:
            cursor.close()

    def __close_db_conn(self):
        """ Closing Database connection """
        try:
            self.__sql_con.close()
        except pymysql.DatabaseError as db_error:
            print("Errno({0}): {1}".format(db_error.args[0], db_error.args[1]))

    def __del__(self):
        """ Destructor of this Object
        closing all oppened connection to db
        """
        self.__close_db_conn()
