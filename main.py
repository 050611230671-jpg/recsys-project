import os
import pickle
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# MỞ KHÓA CORS: Cho phép App/Web bên ngoài kết nối với AI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Biến để giữ model
model = None
model_load_error = "Chưa thử nạp" 

def load_model():
    global model, model_load_error
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(current_dir, "model.pkl")
        
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        model_load_error = "Nạp AI thành công!"
    except Exception as e:
        model_load_error = str(e)
        model = None

load_model()

@app.get("/")
def home():
    return {"message": "He thong Goi y San pham da san sang!"}

@app.get("/predict")
def predict(click_rate: float, price: float, age: int):
    if model is None:
        return {"error": f"AI chưa được nạp. Lỗi thực sự là: {model_load_error}"}
    
    try:
        input_df = pd.DataFrame([[click_rate, price, age]], 
                                columns=['click_rate', 'price', 'age'])
        
        prediction = model.predict(input_df)
        result = "Nen goi y mua hang" if prediction[0] == 1 else "Khong nen goi y"
        
        return {
            "Ket qua": result,
            "Dau vao": {"ti_le_click": click_rate, "gia_ca": price, "tuoi": age}
        }
    except Exception as e:
        return {"error": f"Lỗi trong quá trình tính toán: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)