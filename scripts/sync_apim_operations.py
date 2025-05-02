#!/usr/bin/env python3
# sync_apim_operations.py - Synchronizes API operations in Azure API Management

import argparse
import json
import os
from azure.mgmt.apimanagement import ApiManagementClient
from azure.identity import DefaultAzureCredential


def sync_apim_operations(subscription_id, resource_group, service_name, spec_file, api_id):
    """Sync API operations in APIM based on Swagger specification"""

    if not os.path.exists(spec_file):
        raise FileNotFoundError(f"Spec file not found at: {spec_file}. Current working dir: {os.getcwd()}")

    credential = DefaultAzureCredential()
    client = ApiManagementClient(credential, subscription_id)

    with open(spec_file, 'r') as f:
        api_spec = json.load(f)

    try:
        api = client.api.get(resource_group, service_name, api_id)
        print(f"Found existing API: {api.display_name}")
    except:
        print("API not found, will create new API")
        api = None

    path = next(iter(api_spec.get('paths', {})))
    method = next(iter(api_spec['paths'][path]))
    operation = api_spec['paths'][path][method]

    print(f"Syncing API: {api_id} with path {path} and method {method}")

    poller = client.api.begin_create_or_update(
        resource_group_name=resource_group,
        service_name=service_name,
        api_id=api_id,
        parameters={
            "display_name": operation.get('summary', api_id),
            "service_url": "https://python-web-app-1-bgape3c8aqahgjcn.centralindia-01.azurewebsites.net",  # optionally make this dynamic
            "path": api_id,
            "protocols": ["https"],
        },
    )

    result = poller.result()
    print(f"Successfully synced API: {result.display_name}")


def main():
    parser = argparse.ArgumentParser(
        description='Sync API operations in Azure API Management'
    )
    parser.add_argument('--subscription-id', required=True, help='Azure subscription ID')
    parser.add_argument('--resource-group', required=True, help='Resource group name')
    parser.add_argument('--service-name', required=True, help='APIM service name')
    parser.add_argument('--spec-file', required=True, help='Path to OpenAPI/Swagger JSON file')
    parser.add_argument('--api-id', required=True, help='API identifier in APIM')
    
    args = parser.parse_args()
    
    sync_apim_operations(
        args.subscription_id,
        args.resource_group,
        args.service_name,
        args.spec_file,
        args.api_id
    )

if __name__ == '__main__':
    main()
