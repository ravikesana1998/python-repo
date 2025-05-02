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
        method_lower = method.lower()

        # Custom filename mapping
        if path == "/users" and method_lower == "get":
            file_name = "users_get.json"
        elif path == "/users" and method_lower == "post":
            file_name = "users_post.json"
        else:
            # Fallback to operationId-based filename
            operation_id = operation.get("operationId", f"{path.strip('/').replace('/', '_')}_{method_lower}")
            file_name = f"{operation_id}.json"

        # Create individual swagger with only the relevant method
        new_spec = {
            **swagger,
            "paths": {
                path: {
                    method_lower: methods[method]
                }
            }
        }

        out_path = os.path.join(args.output_dir, file_name)
        with open(out_path, "w") as out_file:
            json.dump(new_spec, out_file, indent=2)

        print(f"Created: {file_name}")
