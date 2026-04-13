def get_products_from_csv():
    df = pd.read_csv("products.csv")
    
    # Từ điển link ảnh theo loại hàng
    anh_theo_loai = {
        "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=500",
        "Fashion": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=500",
        "Sports": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500",
        "Beauty": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=500",
        "Home & Kitchen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500"
    }

    products = []
    for _, row in df.iterrows():
        # Lấy ảnh theo category, nếu không có thì lấy ảnh mặc định
        link_anh = anh_theo_loai.get(row['category'], "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500")
        
        products.append({
            "name": f"Sản phẩm {row['product_id']}",
            "category": row['category'],
            "price": f"{row['base_price']} USD",
            "img": link_anh,
            "rating": row['rating']
        })
    return products