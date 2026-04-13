import pandas as pd
from xgboost import XGBClassifier
import pickle

# 1. Giả lập dữ liệu: Click nhiều, giá rẻ, trẻ tuổi -> Thường sẽ mua (1)
data = {
    'click_rate': [0.1, 0.5, 0.8, 0.2, 0.9, 0.05],
    'price': [100, 200, 50, 300, 70, 400],
    'age': [20, 25, 22, 40, 19, 50],
    'buy': [0, 1, 1, 0, 1, 0] 
}
df = pd.DataFrame(data)

# 2. Huấn luyện Model XGBoost (Bộ não AI)
X = df[['click_rate', 'price', 'age']]
y = df['buy']
model = XGBClassifier()
model.fit(X, y)

# 3. Lưu mô hình lại thành file model.pkl
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Xong roi! Da tao duoc file model.pkl")