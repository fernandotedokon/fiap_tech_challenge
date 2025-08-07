# app/utils.py

import pandas as pd
import os

DATA_DIR = "/tmp"
CSV_PATH = os.path.join(DATA_DIR, "books.csv")


def load_books():
    return pd.read_csv(CSV_PATH)


def get_book_by_id(book_id: int):
    df = load_books()
    book = df[df["id"] == book_id]
    return book.to_dict(orient="records")[0] if not book.empty else None


def search_books(title: str = None, category: str = None):
    df = load_books()
    if title:
        df = df[df["title"].str.contains(title, case=False, na=False)]
    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]
    return df.to_dict(orient="records")


def get_categories():
    df = load_books()
    return sorted(df["category"].dropna().unique().tolist())


def get_stats_overview():
    df = load_books()
    df["price_num"] = df["price"].str.replace("Â£", "").astype(float)
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    df["rating_num"] = df["rating"].map(rating_map)
    return {
        "total_books": len(df),
        "average_price": round(df["price_num"].mean(), 2),
        "rating_distribution": df["rating"].value_counts().to_dict()
    }


def get_stats_by_category():
    df = load_books()
    df["price_num"] = df["price"].str.replace("Â£", "").astype(float)
    grouped = df.groupby("category").agg(
        total_books=("id", "count"),
        avg_price=("price_num", "mean"),
        max_price=("price_num", "max"),
        min_price=("price_num", "min")
    ).round(2).reset_index()
    return grouped.to_dict(orient="records")


def get_top_rated_books():
    df = load_books()
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    df["rating_num"] = df["rating"].map(rating_map)
    max_rating = df["rating"].max()
    top_books = df[df["rating"] == max_rating]
    return top_books.to_dict(orient="records")



