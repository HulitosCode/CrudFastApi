from fastapi import FastAPI
from App.auth_routes import auth_router
from App.order_routes import order_router


app = FastAPI()


app.include_router(auth_router)
app.include_router(order_router)