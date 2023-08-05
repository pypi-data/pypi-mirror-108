from fastapi import APIRouter, Response, status

leetcode_router = APIRouter()


@leetcode_router.get("/healthcheck")
async def root():
    return Response(status_code=status.HTTP_200_OK)
