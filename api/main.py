from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import models
from api.utils.database import database, engine
from api.controllers.auth_controller import router
from api.controllers.transaction import router_tran

app = FastAPI()

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="Api{Lakem Api}",
    description="Lakem api",
    version=0.10,
    openapi_url="/openapi.json"
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get('/')
def root():
    return {
        "msg": "Welcome to lakem api"
    }


def create_tables():
    models.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    await database.connect()
    create_tables()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router, tags=["Authentication"])
app.include_router(router_tran, tags=["Transactions"])
