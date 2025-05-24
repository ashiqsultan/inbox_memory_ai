from fastapi import APIRouter


router = APIRouter()


@router.get("/hello")
async def hello_world():
    print("Hello World started")
    print("Hello World ended")
    return {"message": "Hello World"}