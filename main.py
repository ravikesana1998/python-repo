from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import users
import uvicorn
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include user routes
app.include_router(users.router, prefix="/users", tags=["Users"])

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Response model for validation
class SimpleResponse(BaseModel):
    message: str

# Custom OpenAPI schema generation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Generate base schema
    openapi_schema = get_openapi(
        title="User Management API",
        version="1.0.0",
        description="API for managing users",
        routes=app.routes,
    )

    # Clean up components
    if "components" in openapi_schema:
        # Remove all schemas to simplify
        openapi_schema["components"].pop("schemas", None)
        
        # Ensure securitySchemes exists if needed
        if not openapi_schema["components"]:
            openapi_schema.pop("components")

    # Clean paths and responses
    for path_item in openapi_schema.get("paths", {}).values():
        for operation in path_item.values():
            # Ensure all responses have content
            for response in operation.get("responses", {}).values():
                if "content" not in response:
                    response["content"] = {
                        "application/json": {
                            "schema": SimpleResponse.schema()
                        }
                    }
                else:
                    for content_type, content in response["content"].items():
                        if "schema" not in content:
                            content["schema"] = {"type": "object"}

    # Force OpenAPI 3.0.1
    openapi_schema["openapi"] = "3.0.1"
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
