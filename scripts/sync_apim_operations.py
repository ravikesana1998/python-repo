#!/usr/bin/env python3
"""
Syncs API operations with Azure API Management (APIM)
"""

import json
from azure.mgmt.apimanagement import ApiManagementClient
from azure.identity import DefaultAzureCredential

class APIMSync:
    def __init__(self, subscription_id, resource_group, service_name):
        self.credential = DefaultAzureCredential()
        self.client = ApiManagementClient(
            credential=self.credential,
            subscription_id=subscript_id
        )
        self.resource_group = resource_group
        self.service_name = service_name
    
    def sync_operation(self, api_id, operation_spec):
        """Syncs a single operation with APIM"""
        try:
            # Check if operation exists
            existing = self.client.api_operation.get(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                api_id=api_id,
                operation_id=operation_spec['operationId']
            )
            
            # Update existing operation
            self.client.api_operation.update(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                api_id=api_id,
                operation_id=operation_spec['operationId'],
                parameters=operation_spec
            )
        except:
            # Create new operation
            self.client.api_operation.create_or_update(
                resource_group_name=self.resource_group,
                service_name=self.service_name,
                api_id=api_id,
                operation_id=operation_spec['operationId'],
                parameters=operation_spec
            )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("api_id", help="APIM API ID")
    parser.add_argument("spec_file", help="Operation specification JSON file")
    parser.add_argument("--subscription-id", required=True)
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--service-name", required=True)
    args = parser.parse_args()
    
    with open(args.spec_file, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    sync = APIMSync(args.subscription_id, args.resource_group, args.service_name)
    
    # Assuming the file contains a single operation
    for path, path_item in spec.get('paths', {}).items():
        for method, operation in path_item.items():
            sync.sync_operation(args.api_id, operation)
