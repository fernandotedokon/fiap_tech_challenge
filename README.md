# 📚 Desafio Tech FIAP - Books Scraping & ML API

Este projeto realiza scraping de dados de livros, extrai informações do site [Books to Scrape](https://books.toscrape.com/), unificando sendo armazenado os dados no arquivo "books.csv" e processamento dos dados expõe uma API RESTful.


## 📦 Requisitos

- Python 3.8+
- pip

## 🚀 Tecnologias Utilizadas

- **FastAPI** — Framework web moderno, rápido para criar APIs RESTful com Python e gera documentação Swagger no padrão OpenAPI 3.0.
- **Uvicorn** — Servidor ASGI ultrarrápido usado para rodar aplicações FastAPI.
- **Requests** — Biblioteca para fazer requisições HTTP de forma simples.
- **BeautifulSoup4** — Ferramenta para fazer parsing (análise) de HTML/XML — usada em web scraping.
- **Pandas** — Biblioteca para análise e manipulação de dados estruturados (como planilhas, CSV, tabelas).



## 🗂️ Estrutura do Projeto

```
biblioteca/
├── app/
│   ├── scraper.py         # Scraper de livros e utilitários de unificação
│   ├── models.py          # Modelos ML serializados
│   └── utils.py           # Funções auxiliares auxiliam na consulta das informações
├── tmp/
│   └── books.csv          # CSVs exportados e unificados
├── main.py                # Inicializador do pipeline e da API
├── requirements.txt       # Dependências do projeto com as bibliotecas utilizada
└── README.md
```



## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone <https://github.com/fernandotedokon/fiap_tech_challenge.git>
cd fiap_tech_challenge
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o FlastAPI

```bash
uvicorn main:app --reload
```

### 5. Swagger - Verificar todas as rotas criadas funcionalidades disponiveis padrões e de estatísticas

- **Ambiente Local**
```bash
http://127.0.0.1:8000/docs
```
- **Ambiente Produção**
```bash
https://fiaptechchallenge-kejf3zeg2-fernandos-projects-a3731ebd.vercel.app/docs
```

### 6. Execute o Web Scraping executando a rota (opcional, se já houver CSV)

```bash
/api/v1/extrair/{pages}

Esse método extrai e salva livros de acordo com o número de páginas informado. Você pode solicitar entre 1 a 10 páginas ou exatamente 50 páginas para extrair todos os dados. Ele chama uma função que faz a extração, carrega os livros e retorna a quantidade de livros extraídos.
```
Essa funcionalidade irá baixar os dados dos livros e gerar o arquivo CSV em `tmp/books.csv`.


---


## 📡 Endpoints Core

| Método | Rota                                    | Descrição |
|--------|-----------------------------------------|-----------|
| GET    | /api/v1/extract/{pages}                 | Extrai e salva livros de acordo número de páginas informado |
| GET    | /api/v1/health                          | Verifica status da API |
| GET    | /api/v1/books                           | Lista todos os livros |
| GET    | /api/v1/books/{id}                      | Detalha um livro |
| GET    | /api/v1/books/search?title=&category=   | Busca por título/categoria |
| GET    | /api/v1/categories                      | Lista categorias únicas |


## 📡 Endpoints Insights

| Método | Rota                                    | Descrição |
|--------|-----------------------------------------|-----------|
| GET    | /api/v2/stats/overview                  | Estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings) |
| GET    | /api/v2/stats/categories                | Estatísticas detalhadas por categoria (quantidade de livros, preços por categoria) |
| GET    | /api/v2/books/top-rated                | Lista os livros com melhor avaliação (rating mais alto) |
| GET    | /api/v2/books/price-range                | Filtra livros dentro de uma faixa de preço específica |




## 🧠 scraper.py: Extração dos livros
- Realiza a extração de dados (web scraping) do site "https://books.toscrape.com/". Coleta informações sobre os livros disponíveis na página, como título, preço, disponibilidade, avaliação, categoria, URL da imagem e detalhes específicos de cada livro. Verifica uma ou mais páginas do site (dependendo do parâmetro pages), extrai os dados de cada livro listado, acessa a página de detalhes de cada um para obter informações adicionais, e então salva tudo em um arquivo CSV "books.csv". Faz a coleta e organização das informações de livros de forma automatizada.


## 📦 models.py Modelos da API
- Modelo com a definição dos campos, atributos do livro que serão extraidos do site [Books to Scrape](https://books.toscrape.com/).


## 🛠 utils.py: Funções auxiliares
- Os métodos do arquivo utils.py são funções auxiliares que ajudam a manipular e consultar uma base de dados de livros armazenada no arquivo CSV.

#### 1. load_books(): 
- Carrega todos os livros do arquivo CSV e retorna um DataFrame do pandas com esses dados.

#### 2. get_book_by_id(book_id): 
- Busca um livro específico pelo seu ID. Se encontrar, retorna um dicionário com as informações desse livro; se não, retorna None.

#### 3. search_books(title=None, category=None): 
- Permite procurar livros pelo título ou pela categoria. Você pode usar um ou ambos os filtros. Ele retorna uma lista de dicionários com os livros que correspondem aos critérios.

#### 4. get_categories(): 
- Lista todas as categorias de livros disponíveis, sem repetições, em ordem alfabética.

#### 5. get_stats_overview(): 
- Mostra o resumo do tamanho da coleção, quanto, em média, eles custam e como as avaliações estão distribuídas.

#### 6. get_stats_by_category(): 
- Fornece uma visão geral das categorias de livros, incluindo quantos livros há em cada uma e os preços médios, máximos e mínimos.

#### 7. get_top_rated_books(): 
- Verifica a avaliação mais alta entre os livros e seleciona aqueles que receberam essa nota máxima.





## 🚀 main.py: Rotas da API
- Os métodos do arquivo main.py são responsáveis por criar e gerenciar a API da sua biblioteca.

---
📁 Extrair Dados
#### /api/v1/extract/{pages}
- Esse método extrai e salva livros de acordo com o número de páginas informado. Você pode solicitar entre 1 a 10 páginas ou exatamente 50 páginas para extrair todos os dados. Ele chama uma função que faz a extração, carrega os livros e retorna a quantidade de livros extraídos.

---
✅ Health Check
#### /api/v1/health
- Essa rota verifica se a API está funcionando bem. Ela tenta carregar os livros e retorna um status "ok" junto com a quantidade de livros disponíveis. É como um teste de saúde do sistema.

---
📚 Listar Todos os Livros
#### /api/v1/books
- Aqui você consegue listar todos os livros disponíveis na sua biblioteca. Ela retorna uma lista com os detalhes de cada livro.

---
🔍 Buscar Livro por ID
#### /api/v1/books/{id}
- Essa rota busca um livro específico pelo seu ID. Se encontrar, retorna os detalhes do livro; se não, informa que o livro não foi encontrado.

---
🔎 Buscar por Título e/ou Categoria
#### /api/v1/books/search
- Essa busca permite procurar livros pelo título ou pela categoria. Você pode passar um ou ambos os parâmetros para filtrar os resultados.

---
📂 Listar Categorias
#### /api/v1/categories
- Essa rota retorna todas as categorias de livros disponíveis na sua biblioteca.

---
📊 Visão geral sobre uma coleção de livros
#### /api/v2/stats/overview
- É uma maneira bem prática de obter uma visão rápida e resumida sobre os livros que estão no sistema.

---
📊 Fornece estatísticas por categoria
#### /api/v2/stats/categories
- Muito útil para dashboards ou análises por área temática, retorna a quantidade de livros, preço médio, máximo e mínimo por categoria.

---
📊 Fornece todos os livros com avaliação máxima
#### /api/v2/books/top-rated
- Mostra os melhores livros da biblioteca.

---
📊 Buscar livros que estão dentro de uma faixa de preço específico
#### /api/v2/books/price-range
- Você pode informar um valor mínimo e um valor máximo, e ela vai retornar uma lista de livros cujo preço está entre esses dois valores.




---
## 🧭 Plano Arquitetural (Pipeline e Escalabilidade)

### 🔄 Pipeline da Solução

```
      ┌─────────────┐
      │ books.toscrape.com
      └──────┬──────┘
             │  (requests + BS4)
             ▼
      ┌────────────────┐
      │ Scraper Python │
      │ scraper.py     │
      └──────┬─────────┘
             ▼  (CSV: pandas)
      ┌────────────────────┐
      │  tmp/books.csv    │
      └──────┬─────────────┘
             ▼
      ┌────────────────────┐
      │   FastAPI backend  │
      │   main.py + models │
      └──────┬─────────────┘
             ▼
      ┌────────────────────┐
      │  REST Endpoints    │
      └──────┬─────────────┘
             ▼
     ┌────────────────────────┐
     │   Cientistas de Dados  │
     │   Frontends / ML / BI  │
     └────────────────────────┘
```


## 🧱 Arquitetura Pensada para Escalabilidade Futura

| Componente      | Escalável? | Estratégia                                                |
| --------------- | ---------- | --------------------------------------------------------- |
| Scraper         | ✅          | Tornar assíncrono, paralelizar scraping por páginas       |
| Armazenamento   | ⚠️ CSV     | Migrar para PostgreSQL, MongoDB, ou AWS S3                    |
| API FastAPI     | ✅          | Pode escalar horizontalmente com Gunicorn/Uvicorn         |
| Modelo de Dados | ✅          | Pydantic permite validação forte                          |
| Deploy          | ✅          | Docker, Kubernetes, serverless (AWS Lambda + API Gateway) |



## 🧠 Caso de Uso para Cientistas de Dados / ML

### 🎯 Cenário
Objetivo: Cientistas de dados querem explorar livros para entender preferências por categorias, preços, disponibilidade e aplicar técnicas de NLP.

💼 Aplicações:
🔍 Análise exploratória de dados (EDA)

📊 Dashboard com Streamlit, Dash ou Power BI

🤖 Treinamento de modelos de recomendação ou classificação de livros por categoria

🧠 Análise de sentimento via scraping de reviews (futuro)



## 🧠 Integração com Modelos de Machine Learning

### 🧩 Plano de Integração
| Etapa             | Detalhes                                                                       |
| ----------------- | ------------------------------------------------------------------------------ |
| Dados             | `books.csv` como entrada para pré-processamento                                |
| Pré-processamento | Limpeza, encoding de `rating`, one-hot de `category`, transformação de `price` |
| Treinamento       | Classificadores, clusterização de livros, sistemas de recomendação             |
| API ML            | Servir modelo via FastAPI ou usar ferramenta como BentoML ou TorchServe        |
| Integração        | Nova rota `/api/v1/predict` que recebe dados de entrada e retorna previsão     |


## 🔄 Exemplo de Rota Futuro:

```bash
@app.post("/api/v1/predict")
def predict(tmp: Book):
    # Preprocessar dados
    # Carregar modelo treinado
    # Retornar resultado
    return {"categoria_prevista": "Fiction"}
```


## 📈 Sugestão para Pipeline de ML

```bash
tmp/books.csv ──> Jupyter Notebook ──> Modelo treinado (.pkl/.joblib)
                                           │
FastAPI ── /predict ────────> Carrega modelo e retorna inferência
```