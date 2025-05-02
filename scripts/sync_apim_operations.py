"# sync_apim_operations.py" hi


- script: |
    curl -sSL $(swaggerUrl) -o $(fullSwagger)
  displayName: 'Download Full Swagger'

- script: |
    python3 scripts/split_swagger_by_method.py $(fullSwagger) --output-dir $(outputDir)
  displayName: 'Split Swagger by Method'

# ✅ Debug: List split_swagger folder contents
- script: |
    echo "Checking output folder contents:"
    ls -R $(outputDir)
  displayName: 'Debug: List split_swagger output'

# ✅ Debug: Show content of users_get.json
- script: |
    echo "Content of users_get.json:"
    cat $(outputDir)/users_get.json || echo "File not found!"
  displayName: 'Debug: Show users_get.json content'

- script: |
    python3 scripts/sync_apim_operations.py \
      --subscription-id $(subscriptionId) \
      --resource-group $(resourceGroup) \
      --service-name $(apimName) \
      --spec-file $(outputDir)/users_get.json \
      --api-id $(apiGet)
  displayName: 'Sync GET operations in APIM'

- task: AzureCLI@2
  displayName: 'Import GET API'
  inputs:
    azureSubscription: 'Azure Resource Connection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      ls -l $(outputDir)
      if [ -f "$(outputDir)/users_get.json" ]; then
        echo "users_get.json found, proceeding with import..."
      else
        echo "ERROR: users_get.json not found!"
        exit 1
      fi

      az apim api import \
        --resource-group $(resourceGroup) \
        --service-name $(apimName) \
        --path users/get_user \
        --api-id $(apiGet) \
        --specification-format OpenApi \
        --specification-path $(outputDir)/users_get.json \
        --service-url "$(appBaseUrl)"
