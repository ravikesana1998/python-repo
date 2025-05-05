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
    # Remove Validation Errors
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        openapi_schema["components"]["schemas"].pop("HTTPValidationError", None)
        openapi_schema["components"]["schemas"].pop("ValidationError", None)

    # Remove invalid references to those errors in responses
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, details in methods.items():
            if "responses" in details:
                for code, response in list(details["responses"].items()):
                    if "content" in response:
                        content = response["content"]
                        if "application/json" in content:
                            schema = content["application/json"].get("schema", {})
                            if (
                                isinstance(schema, dict) and 
                                "$ref" in schema and 
                                schema["$ref"].endswith("HTTPValidationError")
                            ):
                                del details["responses"][code]
                            elif schema == {}:
                                # Replace empty schema with a simple valid schema
                                content["application/json"]["schema"] = {"type": "object"}

    app.openapi_schema = openapi_schema
    return app.openapi_schema



# Set the custom OpenAPI function
app.openapi = custom_openapi

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
