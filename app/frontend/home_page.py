from pathlib import Path

from fastapi import Request,Response,Form,HTTPException
from fastapi.responses import JSONResponse,HTMLResponse

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

from app.core.templates import templates

router = APIRouter(
    prefix="/auth",
    tags=["Frontend"]
)

@router.get("/")
async def dashboard_page(request: Request) -> Response:
    return templates.TemplateResponse(request, "login.html")


@router.post("/login")
async def authentication(username: str = Form(...),password: str = Form(...)):
    if username != "admin" or password != "1234":
        # Devuelves únicamente el HTML que deseas inyectar en el target
        return HTMLResponse("Usuario o contraseña incorrectos")

    response = HTMLResponse("")
    response.headers["HX-Redirect"] = "/dashboard"
    return response
