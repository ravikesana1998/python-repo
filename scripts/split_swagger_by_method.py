import json
import os
import argparse

def sanitize_spec(spec):
    """Ensure spec is valid OpenAPI 3.0.1"""
    # Remove problematic components
    if 'components' in spec:
        spec.pop("components")
    
    # Clean paths
    if 'paths' in spec:
        for path_item in spec['paths'].values():
            for operation in path_item.values():
                if 'responses' in operation:
                    for response in operation['responses'].values():
                        if 'content' not in response:
                            response['content'] = {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
    return spec

def split_swagger(input_file, output_dir):
    """Split Swagger file by HTTP methods"""
    with open(input_file, 'r') as f:
        swagger = json.load(f)

    methods = ['get', 'post', 'patch', 'delete']
    os.makedirs(output_dir, exist_ok=True)

    for method in methods:
        paths = {}
        for path, path_item in swagger.get("paths", {}).items():
            if method in path_item:
                paths[path] = {method: path_item[method]}
        
        if paths:
            output_spec = {
                "openapi": "3.0.1",
                "info": swagger.get("info", {
                    "title": f"{method.upper()} Operations",
                    "version": "1.0.0"
                }),
                "paths": paths
            }
            
            output_spec = sanitize_spec(output_spec)
            
            output_path = os.path.join(output_dir, f'swagger-{method}.json')
            with open(output_path, 'w') as f:
                json.dump(output_spec, f, indent=2)
            print(f"Created {method} spec at {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Split Swagger/OpenAPI file by HTTP methods'
    )
    parser.add_argument(
        "swagger_file",
        help="Path to Swagger JSON file"
    )
    parser.add_argument(
        "--output-dir",
        default="split_swagger",
        help="Output directory for split files"
    )
    args = parser.parse_args()
    split_swagger(args.swagger_file, args.output_dir)
