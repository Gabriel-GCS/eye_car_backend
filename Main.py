from fastapi import FastAPI
from routes.UserRoute import router as UserRoute
from routes.AuthRoute import router as AuthRoute
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(UserRoute, tags=["Users"], prefix="/api/user")
app.include_router(AuthRoute, tags=["Login"], prefix="/api/login")

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
