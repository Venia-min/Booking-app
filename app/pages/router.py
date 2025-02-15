from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_available_hotels_by_loc

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(
    request: Request,
    hotels=Depends(get_available_hotels_by_loc),
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels},
    )
