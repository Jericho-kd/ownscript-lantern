from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)


templates = Jinja2Templates(directory="templates")


@router.get("/lantern")
def get_lantern_page(request: Request):
    return templates.TemplateResponse("lantern.html", {"request": request})
