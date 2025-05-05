import argparse
import json
import os
from azure.mgmt.apimanagement import ApiManagementClient
from azure.identity import DefaultAzureCredential

def validate_spec(spec_path):
    """Validate OpenAPI spec before import"""
    with open(spec_path, 'r') as f:
        spec = json.load(f)
    
    # Ensure required fields exist
    if "openapi" not in spec:
        spec["openapi"] = "3.0.1"
    if "info" not in spec:
        spec["info"] = {"title": "API", "version": "1.0.0"}
    
    # Clean paths
    for path in spec.get("paths", {}).values():
        for operation in path.values():
            # Ensure all responses have content
            for response in operation.get("responses", {}).values():
                if "content" not in response:
                    response["content"] = {
                        "application/json": {"schema": {"type": "object"}}
    
    return spec

def sync_apim_operations(subscription_id, resource_group, service_name, spec_file, api_id):
    """Sync API operations in APIM with validation"""
    if not os.path.exists(spec_file):
        raise FileNotFoundError(f"Spec file not found: {spec_file}")
    
    # Validate and clean spec
    validated_spec = validate_spec(spec_file)
    temp_spec = f"{spec_file}.validated.json"
    with open(temp_spec, 'w') as f:
        json.dump(validated_spec, f)
    
    credential = DefaultAzureCredential()
    client = ApiManagementClient(credential, subscription_id)

    try:
        poller = client.api.begin_create_or_update(
            resource_group_name=resource_group,
            service_name=service_name,
            api_id=api_id,
            parameters={
                "display_name": api_id,
                "service_url": "https://python-web-app-1-bgape3c8aqahgjcn.centralindia-01.azurewebsites.net",
                "path": api_id,
                "protocols": ["https"],
                "format": "openapi+json",
                "value": json.dumps(validated_spec)
            },
        )
        result = poller.result()
        print(f"Successfully synced API: {result.display_name}")
    except Exception as e:
        print(f"Error syncing API: {str(e)}")
        raise
    finally:
        if os.path.exists(temp_spec):
            os.remove(temp_spec)

def main():
    parser = argparse.ArgumentParser(description='Sync API operations in Azure API Management')
    parser.add_argument('--subscription-id', required=True)
    parser.add_argument('--resource-group', required=True)
    parser.add_argument('--service-name', required=True)
    parser.add_argument('--spec-file', required=True)
    parser.add_argument('--api-id', required=True)
    
    args = parser.parse_args()
    sync_apim_operations(**vars(args))

if __name__ == '__main__':
    main()
