# scripts/split_swagger_by_method.py
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("swagger_file", help="Path to Swagger JSON file")
parser.add_argument("--output-dir", default="split_swagger", help="Directory to write split files")
args = parser.parse_args()

with open(args.swagger_file, "r") as f:
    swagger = json.load(f)

paths = swagger.get("paths", {})
os.makedirs(args.output_dir, exist_ok=True)

for path, methods in paths.items():
    for method, operation in methods.items():
        method_upper = method.upper()
        operation_id = operation.get("operationId", f"{path.strip('/').replace('/', '_')}_{method}")
        file_name = f"{operation_id}.json"

        new_spec = {
            **swagger,
            "paths": {
                path: {
                    method: methods[method]
                }
            }
        }

        with open(os.path.join(args.output_dir, file_name), "w") as out_file:
            json.dump(new_spec, out_file, indent=2)

        print(f"Created: {file_name}")
