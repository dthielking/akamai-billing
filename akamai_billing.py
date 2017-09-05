#!/usr/bin/env python3
""" blub """
from pprint import pprint
import AkamaiCbc
import requests

def main():
    """ Main function """
    ab = AkamaiCbc.AkamaiBilling('./akamai_config.json')
    contract_uri = "/contract-api/v1/contracts/identifiers"
    rep_grps_uri = "/contract-api/v1/reportingGroups/identifiers"
    product_lst = list()

    # Make API Calls to get contracts ids
    contract_ids = ab.make_api_call(contract_uri)
    # Make API Call to get reporting groups ids
    rep_grp_ids = ab.make_api_call(rep_grps_uri)

    # Generate list of products uri
    for contract_id in contract_ids:
        products_uri = "/contract-api/v1/contracts/"
        products_uri += str(contract_id)
        products_uri += "/products/summaries"
        for product in ab.make_api_call(products_uri)['products']['marketing-products']:
            product_lst.append(product)

    # Insert Contracts to DB without duplicates
    sql_insert = "INSERT INTO tbl_contracts (ContractId) VALUES (%s)"
    sql_select_dup_ids = "SELECT ContractId FROM tbl_contracts"
    ab.sql_statement(sql_insert, contract_ids, sql_select_dup_ids)

    # Insert reporting groups to DB without duplicates
    sql_insert = "INSERT INTO tbl_reportinggroups (ReportingGroupId) VALUES (%s)"
    sql_select_dup_ids = "SELECT ReportingGroupId FROM tbl_reportinggroups"
    ab.sql_statement(sql_insert, rep_grp_ids, sql_select_dup_ids)

    # Insert products into db without duplicats
    sql_insert = "INSERT INTO tbl_products (ProductId, ProductName) "
    sql_insert += "VALUES (%(marketingProductId)s, %(marketingProductName)s)"
    sql_select_dup_ids = "SELECT ProductId FROM tbl_products"
    ab.sql_statement(
        sql_insert, product_lst, sql_select_dup_ids, search_id='marketingProductId')

    # Generating foreign key association between Contracts and ReportingGroups
    #Generating ReportingGroup URLs
    for rep_grp_id in rep_grp_ids:
        contract_reporting = dict()
        url_reporting_group_id = "/contract-api/v1/reportingGroups/"
        url_reporting_group_id += str(rep_grp_id)
        url_reporting_group_id += "/products/summaries"
        resp_api_call = ab.make_api_call(url_reporting_group_id)

        if isinstance(resp_api_call, dict):
            contract_reporting['contractId'] = resp_api_call['products']['contractId']
            contract_reporting['reportingGroupId'] = rep_grp_id

            sql_select = "SELECT PK_ContractKey FROM tbl_Contracts "
            sql_select += "WHERE ContractId = %s"
            sql_ret = ab.sql_statement(sql_select, contract_reporting['contractId'])
            pprint(sql_ret)
            # for row in sql_ret:
            #     result += row
            # if len(result) > 1:
            #     raise SystemExit
            # contract_id = sql_ret.fetchone()
            # print(contract_id)

            # sql_insert = 'INSERT IGNORE INTO '
            # sql_insert += 'ztbl_ReportingContract(FK_ContractsKey, FK_ReportingGroupKey)'
            # sql_insert += 'VALUES((SELECT PK_ContractKey FROM tbl_Contracts '
            # sql_insert += 'WHERE ContractId = %(contractId)s),'
            # sql_insert += '(SELECT PK_ReportingGroupKey FROM tbl_ReportingGroups '
            # sql_insert += 'WHERE ReportingGroupId = %(reportingGroupId)s))'
            # ab.sql_statement(sql_insert, contract_reporting)

if __name__ == "__main__":
    # Call main()
    main()
