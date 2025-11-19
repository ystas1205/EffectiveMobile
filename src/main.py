import uvicorn
from fastapi import FastAPI

from src.load_permissions.initial_data import lifespan

app = FastAPI(ltitle="API AUTH USERS",
              lifespan=lifespan,
              docs_url="/api/v1/docs",
              openapi_url="/api/v1/openapi.json"
              )


from src.api_get_mock.endpoints import router_mock_objects
from src.api_user_management.endpoints import router_admin_permissions
from src.api_user_services.endpoints import router_user

app.include_router(router_user,prefix="/api/v1/auth")
app.include_router(router_admin_permissions,prefix="/api/v1/admin")
app.include_router(router_mock_objects,prefix="/api/v1/mock")
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
