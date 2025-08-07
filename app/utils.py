import pandas as pd
import os

DATA_DIR = "/tmp"
CSV_PATH = os.path.join(DATA_DIR, "books.csv")

os.makedirs(DATA_DIR, exist_ok=True)


def load_books():
    if not os.path.exists(CSV_PATH):
        return []
    return pd.read_csv(CSV_PATH).to_dict(orient="records")


def get_book_by_id(book_id: int):
    data = load_books()
    df = pd.DataFrame(data)    
    book = df[df["id"] == book_id]
    return book.to_dict(orient="records")[0] if not book.empty else None


def search_books(title: str = None, category: str = None):
    df = load_books()
    if title:
        df = df[df["title"].str.contains(title, case=False, na=False)]
    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]
    return df.to_dict(orient="records")


def get_list_categories():
    books = load_books()
    if not books:
        raise HTTPException(status_code=404, detail="Dados não encontrados.")
    categories = sorted(set(book["category"] for book in books))
    return {"categories": categories}


def get_stats_overview():
    data = load_books()
    if not data:
        raise HTTPException(status_code=404, detail="Dados não encontrados.")    
    book = pd.DataFrame(data)
    book["price_num"] = book["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)    
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    book["rating_num"] = book["rating"].map(rating_map)
    return {
        "total_books": len(book),
        "average_price": round(book["price_num"].mean(), 2),
        "rating_distribution": book["rating"].value_counts().to_dict()
    }


def get_stats_by_category():
    data = load_books()
    if not data:
        raise HTTPException(status_code=404, detail="Dados não encontrados.")    
    book = pd.DataFrame(data)    
    book["price_num"] = book["price"].str.replace("Â£", "").astype(float)
    grouped = book.groupby("category").agg(
        total_books=("id", "count"),
        avg_price=("price_num", "mean"),
        max_price=("price_num", "max"),
        min_price=("price_num", "min")
    ).round(2).reset_index()
    return grouped.to_dict(orient="records")


def get_top_rated_books():
    data = load_books()
    if not data:
        raise HTTPException(status_code=404, detail="Dados não encontrados.")  
    df = pd.DataFrame(data)
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    df["rating_num"] = df["rating"].map(rating_map)
    max_rating = df["rating"].max()
    top_books = df[df["rating"] == max_rating]
    return top_books.to_dict(orient="records")


def salvar_csv(books):
    df = pd.DataFrame(books)
    df.to_csv(CSV_PATH, index=False)
