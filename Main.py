from fastapi import FastAPI
from routes.UserRoute import router as UserRoute
from routes.AuthRoute import router as AuthRoute
from routes.CarRoute import router as CarRoute
from routes.UserCarRoute import router as UserCarRoute
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(UserRoute, tags=["Users"], prefix="/api/user")
app.include_router(AuthRoute, tags=["Login"], prefix="/api/login")
app.include_router(CarRoute, tags=["Cars"], prefix="/api/car")
app.include_router(UserCarRoute, tags=["User_Car"], prefix="/api/user_car")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK!"
    }
