#swagger_by_method.py

import json
import os
import argparse

def split_swagger(input_file, output_dir):
    with open(input_file, 'r') as f:
        swagger = json.load(f)

    methods = ['get', 'post', 'patch', 'delete']
    output_files = {method: {'paths': {}} for method in methods}

    for path, path_item in swagger.get('paths', {}).items():
        for method, operation in path_item.items():
            method_lower = method.lower()
            if method_lower in methods:
                output_files[method_lower]['paths'][path] = {method: operation}

    os.makedirs(output_dir, exist_ok=True)

    for method in methods:
        if output_files[method]['paths']:
            output_spec = {
                'openapi': swagger.get('openapi', '3.0.0'),
                'info': swagger.get('info', {}),
                'paths': output_files[method]['paths']
            }
            
            output_path = os.path.join(output_dir, f'swagger-{method}.json')
            with open(output_path, 'w') as f:
                json.dump(output_spec, f, indent=2)
            print(f"Created {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("swagger_file", help="Path to Swagger JSON file")
    parser.add_argument("--output-dir", default="split_swagger", help="Output directory")
    args = parser.parse_args()
    
    split_swagger(args.swagger_file, args.output_dir)
