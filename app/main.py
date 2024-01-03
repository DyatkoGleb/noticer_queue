from fastapi import FastAPI, APIRouter, Request

app = FastAPI()
router = APIRouter()
@router.get("/addNotice")
def add_notice():
    pass

app.include_router(router)
