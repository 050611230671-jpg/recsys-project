from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    # Bản này không dùng giao diện HTML để tránh lỗi "Internal Server Error"
    # Nếu web hiện ra dòng chữ dưới đây là bạn đã thành công 100%
    return {
        "status": "Success",
        "message": "Chuc mung! Server cua ban da chay ruc ro tren Google Cloud",
        "author": "Recsys-app",
        "products": [
            {"id": 1, "name": "Giay Sneaker", "price": "1.200k"},
            {"id": 2, "name": "Ao Hoodie", "price": "450k"}
        ]
    }

# Luu y: Khong can them doan if __name__ == "__main__" o day nua