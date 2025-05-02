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

if not paths:
    print("⚠️ No paths found in the Swagger file!")
    exit(1)

# DEBUG: Print all paths and methods
print("=== DEBUG: All Paths and Methods ===")
for path, methods in paths.items():
    print(f"Path: {path}")
    for method in methods:
        print(f"  - Method: {method}")
print("===================================")

os.makedirs(args.output_dir, exist_ok=True)

files_created = 0

for path, methods in paths.items():
    normalized_path = path.strip('/')
    for method, operation in methods.items():
        method_lower = method.lower()

        # DEBUG: Print current processing
        print(f"Processing: {normalized_path} ({method_lower})")

        # Custom filename mapping
        if normalized_path == "users" and method_lower == "get":
            file_name = "users_get.json"
        elif normalized_path == "users" and method_lower == "post":
            file_name = "users_post.json"
        else:
            operation_id = operation.get("operationId", f"{normalized_path.replace('/', '_')}_{method_lower}")
            file_name = f"{operation_id}.json"

        new_spec = {
            **swagger,
            "paths": {
                path: {
                    method: methods[method]  # Keep original method case
                }
            }
        }

        out_path = os.path.join(args.output_dir, file_name)
        with open(out_path, "w") as out_file:
            json.dump(new_spec, out_file, indent=2)

        print(f"✅ Created: {file_name}")
        files_created += 1

if files_created == 0:
    print("⚠️ No files were created! Check if your paths match expected patterns.")
    exit(1)
