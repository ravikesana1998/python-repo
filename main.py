from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import users
import uvicorn

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )

app.include_router(users.router, prefix="/users", tags=["Users"])

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
    openapi_schema["components"]["schemas"].pop("HTTPValidationError", None)
    openapi_schema["components"]["schemas"].pop("ValidationError", None)
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# helloworld

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)

