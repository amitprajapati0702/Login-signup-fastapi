from fastapi import FastAPI
from app.route import router
from app.Database import engine
from app.model import Base

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router)
