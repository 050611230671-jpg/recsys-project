import pandas as pd
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Cấu hình ảnh
ANH_THEO_LOAI = {
    "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=500",
    "Clothing": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=500",
    "Sports": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500",
    "Beauty": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=500",
    "Home & Kitchen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500"
}

def get_data():
    # Sử dụng file đã làm sạch của bạn
    file_name = "cleaned_product_data.csv"
    if not os.path.exists(file_name):
        return pd.DataFrame()
    return pd.read_csv(file_name)

# THUẬT TOÁN CHÍNH: TÍNH TOÁN ĐỘ TƯƠNG ĐỒNG
def get_content_based_recommendations(product_id, top_n=4):
    df = get_data()
    if df.empty: return []

    # 1. Vector hóa danh mục sản phẩm (TF-IDF)
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['name_category'])

    # 2. Tính Ma trận tương đồng (Cosine Similarity Matrix)
    # Đây chính là Phần V.1 trong tài liệu của bạn
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 3. Tìm vị trí của sản phẩm đang xem
    try:
        idx = df.index[df['product_id'] == product_id][0]
    except:
        return []

    # 4. Lấy điểm số tương đồng của sản phẩm này với tất cả sản phẩm khác
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # 5. Sắp xếp giảm dần theo điểm số
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # 6. Lấy Top N (bỏ qua chính nó ở vị trí số 0)
    sim_scores = sim_scores[1:top_n+1]
    
    product_indices = [i[0] for i in sim_scores]
    results = df.iloc[product_indices]

    recs = []
    for _, row in results.iterrows():
        recs.append({
            "id": row['product_id'],
            "name": f"Sản phẩm {row['product_id']}",
            "price": f"{round(row['base_price'], 2)} USD",
            "img": ANH_THEO_LOAI.get(row['name_category'], "https://via.placeholder.com/500")
        })
    return recs

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    df = get_data()
    sample_df = df.sample(min(len(df), 8))
    products = []
    for _, row in sample_df.iterrows():
        products.append({
            "id": row['product_id'],
            "name": f"Sản phẩm {row['product_id']}",
            "price": f"{round(row['base_price'], 2)} USD",
            "img": ANH_THEO_LOAI.get(row['name_category'], "")
        })
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    df = get_data()
    # Lấy thông tin sản phẩm mục tiêu
    target_row = df[df['product_id'] == product_id].iloc[0]
    
    current_product = {
        "id": target_row['product_id'],
        "name": f"Siêu phẩm {target_row['product_id']}",
        "category": target_row['name_category'],
        "price": f"{round(target_row['base_price'], 2)} USD",
        "rating": target_row['rating'],
        "img": ANH_THEO_LOAI.get(target_row['name_category'], "")
    }

    # GỌI THUẬT TOÁN GỢI Ý
    recs = get_content_based_recommendations(product_id)

    return templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": current_product,
        "recommendations": recs
    })