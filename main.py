from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    products = [
        {"name": "Giày Sneaker", "price": "1.200k", "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"},
        {"name": "Áo Hoodie", "price": "450k", "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400"}
    ]
    return templates.TemplateResponse("index.html", {"request": request, "products": products})