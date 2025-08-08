from fastapi import FastAPI, HTTPException, Query
from app.scraper import extract_books
from app.models import Book
from app.utils import load_books, get_list_categories, salvar_csv, get_book_by_id, search_books, get_stats_overview, get_stats_by_category, get_top_rated_books
import pandas as pd
import os

app = FastAPI(title="Books Scraping - Desafio Tech API", version="1.0 powered by Group 44, 6MLET")

@app.get("/api/v1/extract/{pages}")
def extract_and_save(pages: int):
    try:
        if (pages >= 0 and pages <= 10) or pages == 50:
            books = extract_books(pages=pages)
        else:
            raise HTTPException(status_code=400, detail="Número de páginas deve ser entre 1 e 10 ou 50 para extrair todas as paginas")
        salvar_csv(books)
        return {"message": f"{len(books)} livros salvos com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/health")
def health_check():
    try:
        df = load_books()
        return {"status": "ok", "books_count": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao carregar dados")


@app.get("/api/v1/books")
def list_books():
    books = load_books()
    if not books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado.")
    return {"books": books}


@app.get("/api/v1/categories")
def list_categories():
    return get_list_categories()


# Endpoints de Insights
@app.get("/api/v2/stats/overview")
def stats_overview():
    return get_stats_overview()


@app.get("/api/v2/stats/categories")
def stats_by_category():
    return get_stats_by_category()


@app.get("/api/v2/books/top-rated")
def top_rated_books():
    return get_top_rated_books()


@app.get("/api/v2/books/price-range")
def books_by_price_range(min: float, max: float):
    data = load_books()
    if not data:
        raise HTTPException(status_code=404, detail="Dados não encontrados.")
    df = pd.DataFrame(data)    
    df["price_num"] = df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
    filtered = df[(df["price_num"] >= min) & (df["price_num"] <= max)]
    return filtered.to_dict(orient="records")


@app.get("/api/v1/books/search")
def search_books(title=None, category=None):
    data = load_books()
    df = pd.DataFrame(data)
    if title:
        df = df[df["title"].str.contains(title, case=False, na=False)]
    if category:
        df = df[df["category"].str.lower() == category.lower()]
    return df.to_dict(orient="records")


# Endpoints Core
@app.get("/api/v1/books/{book_id}")
def get_book(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book

