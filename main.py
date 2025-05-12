from fastapi import FastAPI, APIRouter
from app.api.endpoints import endpoints

app = FastAPI()
router = APIRouter()

router.include_router(endpoints.router)
app.include_router(router)
