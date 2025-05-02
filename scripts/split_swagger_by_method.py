#!/usr/bin/env python3
"""
Splits a Swagger/OpenAPI specification file into separate files by HTTP method
"""

import json
import os
from pathlib import Path

def split_swagger(input_file: str, output_dir: str = "split_swagger"):
    """Splits Swagger file by HTTP methods"""
    with open(input_file, 'r', encoding='utf-8') as f:
        swagger = json.load(f)
    
    Path(output_dir).mkdir(exist_ok=True)
    
    methods = ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']
    
    for path, path_item in swagger.get('paths', {}).items():
        for method in methods:
            if method in path_item:
                method_spec = {
                    "paths": {
                        path: {
                            method: path_item[method]
                        }
                    },
                    "info": swagger.get("info", {}),
                    "components": swagger.get("components", {})
                }
                
                filename = f"{path.replace('/', '_')}_{method}.json"
                with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
                    json.dump(method_spec, f, indent=2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input Swagger/OpenAPI JSON file")
    parser.add_argument("--output-dir", default="split_swagger", help="Output directory")
    args = parser.parse_args()
    
    split_swagger(args.input_file, args.output_dir)
