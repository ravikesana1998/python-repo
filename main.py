from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import users
import uvicorn
from fastapi.openapi.utils import get_openapi

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include user routes
app.include_router(users.router, prefix="/users", tags=["Users"])

# Define a root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="Custom API",
        routes=app.routes,
    )

    # Remove schemas
    openapi_schema.get("components", {}).get("schemas", {}).pop("HTTPValidationError", None)
    openapi_schema.get("components", {}).get("schemas", {}).pop("ValidationError", None)

    # Recursively clean $ref and remove 422 responses
    def clean_paths(paths):
        for path in paths.values():
            for method in path.values():
                responses = method.get("responses", {})
                # Remove 422 response
                if "422" in responses:
                    del responses["422"]
                # Clean out $ref to HTTPValidationError if present
                for code, resp in list(responses.items()):
                    content = resp.get("content", {})
                    if (
                        "application/json" in content
                        and "$ref" in content["application/json"].get("schema", {})
                        and content["application/json"]["schema"]["$ref"].endswith("HTTPValidationError")
                    ):
                        del responses[code]

    clean_paths(openapi_schema.get("paths", {}))

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Set the custom OpenAPI function
app.openapi = custom_openapi

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
