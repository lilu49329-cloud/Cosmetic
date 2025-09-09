from fastapi import FastAPI
from typing import List

app = FastAPI()

# Giả lập dữ liệu sản phẩm (id)
PRODUCTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

@app.get("/recommendations/{product_id}", response_model=List[int])
def recommend(product_id: int):
    # Gợi ý 4 sản phẩm khác (giả lập)
    return [pid for pid in PRODUCTS if pid != product_id][:4]
