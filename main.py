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

# Custom OpenAPI schema generation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="Custom API",
        routes=app.routes,
    )
    # Remove HTTPValidationError and ValidationError references
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        openapi_schema["components"]["schemas"].pop("HTTPValidationError", None)
        openapi_schema["components"]["schemas"].pop("ValidationError", None)
    for path, methods in openapi_schema["paths"].items():
        for method, details in methods.items():
            if "responses" in details:
                for response_code, response_details in details["responses"].items():
                    if (
                        "content" in response_details
                        and "application/json" in response_details["content"]
                        and "schema" in response_details["content"]["application/json"]
                    ):
                        schema = response_details["content"]["application/json"]["schema"]
                        if (
                            isinstance(schema, dict)
                            and "$ref" in schema
                            and schema["$ref"].endswith("HTTPValidationError")
                        ):
                            del details["responses"][response_code]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Set the custom OpenAPI function
app.openapi = custom_openapi

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
