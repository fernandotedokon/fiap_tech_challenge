
# 📐 Arquitetura da API Biblioteca

## Pipeline

books.toscrape.com → Scraper (requests + bs4) → data/books.csv → FastAPI → REST Endpoints → Consumidores (Data Science, ML, BI)

## Escalabilidade

- Scraper pode ser paralelizado
- Substituir CSV por banco (PostgreSQL, MongoDB, S3)
- API pode rodar com Gunicorn em containers (Docker/Kubernetes)
- Deploy em nuvem: AWS, GCP, Azure

## Integração com ML

- Fonte de dados rica para sistemas de recomendação
- Modelo pode ser servido como nova rota `/predict`
- Ideal para classificação de categorias, análise de preços e NLP
