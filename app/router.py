from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/addNotice")
async def add_notice():
    print('fleeeeex')
