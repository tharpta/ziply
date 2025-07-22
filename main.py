from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from typing import Annotated

import httpx

from sqlalchemy.orm import Session

from database import SessionLocal, init_db
from models import Ziplies

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


def get_client_ip(request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # In case of multiple IPs
    else:
        ip = request.client.host
    return ip


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    if "127.0.0" in ip or ip == "localhost":
        ip = "45.48.229.217"
    
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://ipinfo.io/{ip}/json")
        print(res)
        data = res.json()

    zipcode = data.get("postal")
    if zipcode == None:
        # Return a proper error response instead of raw integer
        return templates.TemplateResponse("index.html", {
            "request": request,
            "zipcode": "Unknown",
            "ziplies": []
        })
    
    ziplies = db.query(Ziplies).order_by(Ziplies.created_at.desc()).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "zipcode": zipcode,
        "ziplies": ziplies
    })

class FormData(BaseModel):
    name: str
    ziply: str
    poop: str
    model_config = {"extra": "forbid"}


@app.post("/submit-ziply")
def submitziply(name: Annotated[str, Form()], ziply: Annotated[str, Form()], request: Request, db: Session = Depends(get_db)):
    # Get client IP and zipcode
    ip = get_client_ip(request)
    # if "127.0.0" in ip or ip == "localhost":
    #commenting out to obfuscate testing IP and to make sure it works on railway.
    
    # Get zipcode from IP (you might want to cache this)
    import asyncio
    async def get_zipcode():
        async with httpx.AsyncClient() as client:
            res = await client.get(f"https://ipinfo.io/{ip}/json")
            data = res.json()
            return data.get("postal", "00000")
    
    zipcode = asyncio.run(get_zipcode())
    
    # Create new ziply with proper fields
    new_ziply = Ziplies(
        text=ziply,
        zipcode=zipcode,
        device_id=ip  # Using IP as device_id for now
    )
    db.add(new_ziply)
    db.commit()
    return RedirectResponse(url="/", status_code=303)