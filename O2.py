import yaml
import requests
import os
import sys
import json
import ast
import argparse

def create_org_query(org_id,path,query,queryname):
    # Build query structure
    payload = {
        "search_body":{
                        "query": query,
                      },
        "scope": 'org',
        "label": queryname
    }
    headers = {
        "x-sevco-target-org": org_id,
        "authorization": token,
        "content-type": "application/json"
    }   
    
    resp = requests.post(api_endpoint + path,headers=headers,json=payload)
    resp.raise_for_status()
    results = resp.json()
    return(results)

def create_query_report(org_id,path,favorite_id,label):
    # Build query structure
    payload = {
                "favorite_id": favorite_id,
                "label": label,
                "search_type": "device-inventory",
                "query_type": "org-search-favorite"
    }
    headers = {
        "x-sevco-target-org": org_id,
        "authorization": token,
        "content-type": "application/json"
    }   
    
    resp = requests.post(api_endpoint + path,headers=headers,json=payload)
    resp.raise_for_status()

device_query_path = "/v1/search/favorites/device-inventory" 
user_query_path = "/v1/search/favorites/user-inventory"
query_report_path = "/v2/trends"

parser = argparse.ArgumentParser()
parser.add_argument("-i", required=True, dest="yamlfile", action="store",
                    help="YAML file containing customer configuration")

args = parser.parse_args()

# Load the variables from the YAML file
with open(args.yamlfile) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    sources = yaml.load(file, Loader=yaml.FullLoader)
    queries = sources['queries']
    target_orgs = sources['target_orgs']

api_endpoint = "https://api.sev.co"

# Check for API key to hit target ORG
if not os.environ.get("JWT"):
    raise Exception("Need API key in JWT environment variable.")
if os.environ.get("API"):
    api_endpoint = os.environ['API']

# Populate API creds
token = os.environ['JWT']

# Loop through the Orgs and create org-wide queries plus query reports
for org in target_orgs:
    for query in sources['queries']:
        org_query_info = create_org_query(org['id'],device_query_path,json.loads(query['query']),query['name'])
        create_query_report(org['id'],query_report_path,org_query_info['favorite_id'],org_query_info['label'])
        print(org['name'],query_report_path,org_query_info['label'])

