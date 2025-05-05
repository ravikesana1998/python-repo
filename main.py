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
    # Explicitly define schemas for HTTPValidationError and ValidationError
    openapi_schema["components"]["schemas"]["HTTPValidationError"] = {
        "type": "object",
        "properties": {
            "detail": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/ValidationError"},
            }
        },
    }
    openapi_schema["components"]["schemas"]["ValidationError"] = {
        "type": "object",
        "properties": {
            "loc": {"type": "array", "items": {"type": "string"}},
            "msg": {"type": "string"},
            "type": {"type": "string"},
        },
    }
    # Ensure the schema conforms to OpenAPI standards
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Set the custom OpenAPI function
app.openapi = custom_openapi

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
