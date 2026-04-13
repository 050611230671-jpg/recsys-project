from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    products = [
        {"name": "Giày Sneaker Nike", "price": "1.250.000đ", "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"},
        {"name": "Áo Hoodie Local Brand", "price": "450.000đ", "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500"}
    ]
    return templates.TemplateResponse("index.html", {"request": request, "products": products})