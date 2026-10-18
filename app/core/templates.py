# core/templates.py
from pathlib import Path
import os
from starlette.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent.parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")

