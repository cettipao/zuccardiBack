import secrets

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from routes.login import router as LoginRouter
from schemas.users import User
from database.sqlalchemy import SessionLocal, engine
from models.users import Base


# from routes.measures import router as MeasuresRouter

app = FastAPI(title="Zuccardi Clima Api", openapi_url="/v1/openapi.json")

Base.metadata.create_all(bind=engine)

security = HTTPBasic()


@app.get("/", tags=["Root"])
async def root(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "apizuccardi")
    correct_password = secrets.compare_digest(credentials.password, "passzuccardi")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return {
        "Service Status": "Up!!",
        "username": credentials.username,
        "password": credentials.password,
    }


app.include_router(LoginRouter, tags=["Login"], prefix="/v1")
# app.include_router(MeasuresRouter, tags=["Measures"], prefix="/v1")
