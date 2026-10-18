from fastapi import APIRouter
from fastapi import Request,Response,Form,HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi import status, Depends

from app.core.templates import templates


router = APIRouter(
    prefix="/dashboard",
    tags=["Frontend"]
)

async def get_current_user(request: Request):
    # Lees la cookie que guardaste cuando el usuario hizo Login
    session_id = request.cookies.get("session_id")
    
    # Si la cookie no existe en el navegador del usuario, lanzas un error
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No has iniciado sesión"
        )

@router.get("/")
async def dashboard_page(request: Request) -> Response:
    return templates.TemplateResponse(request, "dashboard.html")

