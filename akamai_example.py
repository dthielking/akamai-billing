#!/usr/bin/env python3
import json
from pprint import pprint
import time
import requests
from akamai.edgegrid import EdgeGridAuth


def main():

    limit = 5

    with open('akamai_config.json', 'r') as file:
        config = json.load(file)

    api_url = config['akamai']['api_url']

    session = requests.Session()
    session.auth = EdgeGridAuth(client_secret=config['akamai']['client_secret'],
                                access_token=config['akamai']['access_token'],
                                client_token=config['akamai']['client_token'])
    print('Calling API: /contract-api/v1/reportingGroups/identifiers')
    start = time.time()
    reporting_group_ids = session.get(api_url +
                                      '/contract-api/v1/reportingGroups/identifiers').json()
    stop = time.time()
    print('API Call takes: {}s'.format(stop-start))

    ct_200 = 0
    ct_300 = 0
    ct_else = 0
    all_start = time.time()
    # Limit for to 5 rounds just for speed limits
    for rep_grp_id in reporting_group_ids[:limit]:
        url = '/contract-api/v1/reportingGroups/'
        url += str(rep_grp_id)
        url += '/products/summaries'
        print('Calling API: {}'.format(url))
        start = time.time()
        response = session.get(api_url + url)
        stop = time.time()
        print('API Call takes: {}s'.format(stop-start))

        if response.status_code == 200:
            ct_200 = ct_200 + 1
        if response.status_code == 300:
            ct_300 = ct_300 + 1
            for contract_link in response.json()['contracts']:
                print('Calling API: {}'.format(contract_link['href'].replace('v1.0', 'v1')))
                start = time.time()
                resp = session.get(api_url + contract_link['href'].replace('v1.0', 'v1'))
                stop = time.time()
                print('API Call takes: {}s'.format(stop-start))
        else:
            ct_else = ct_else + 1
    all_stop = time.time()
    print("Reporting Group API calls: {}".format(ct_200+ct_300+ct_else))
    print("Duration all calls: {}s".format(all_stop-all_start))
    print('HTTP 200: {}'.format(ct_200))
    print('HTTP 300: {}'.format(ct_300))
    print('HTTP 200+300: {}'.format(ct_200+ct_300))
    print('HTTP Else: {}'.format(ct_else))
if __name__ == "__main__":
    main()
