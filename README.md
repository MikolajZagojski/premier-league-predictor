# Football Analytics — Premier League Pipeline + ML

A portfolio project: an end-to-end data pipeline for Premier League matches,
combining a data lake and a data warehouse, with ML models predicting match
outcomes and exact scorelines.

## What it does

1. Ingests Premier League fixture data from an external API.
2. Lands raw data in a data lake (MinIO), then cleans and models it into a
   data warehouse (PostgreSQL) using dbt.
3. Builds ML features from the warehouse and trains models to predict:
   - the probability of a home win / draw / away win
   - the most likely exact scoreline
4. Serves predictions through an API and a simple dashboard.

## Tech stack

- **Python** — ingestion, feature engineering, ML
- **MinIO** — data lake (raw + cleaned data)
- **PostgreSQL** — data warehouse
- **dbt** — data transformations and testing
- **scikit-learn / XGBoost / statsmodels** — ML models
- **FastAPI** — serving layer
- **Streamlit** — dashboard

## Architecture

```
API-Football
     │
     ▼
Ingestion (Python)   ← run on a schedule (cron / Airflow later)
     │
     ▼
┌──────────────────────────────────────────┐
│  MinIO — Data Lake                       │
│                                          │
│  Bronze (raw JSON)                       │
│     │                                    │
│     ▼                                    │
│  dbt + DuckDB  →  Silver (Parquet)       │
└──────────────────────────────────────────┘
     │  loader (Python)
     ▼
┌──────────────────────────────────────────┐
│  PostgreSQL — Data Warehouse             │
│                                          │
│  raw  →  dbt  →  marts (star schema)     │
│                      │                   │
│                      ▼                   │
│                 gold (ML features)       │
└──────────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────┐
│  ML                                      │
│                                          │
│  Logistic Regression / XGBoost           │
│  Poisson (home / away goals)             │  ┄┄▶ MLflow (later)
└──────────────────────────────────────────┘
     │  batch scoring
     ▼
serving (predictions — same Postgres)
     │
     ▼
FastAPI  →  Streamlit
```

## Project structure

```
football-analytics/
├── ingestion/     # pulls data from the API into the data lake
├── dbt/           # data transformations (Silver / warehouse)
├── features/      # ML feature engineering
├── ml/            # model training and prediction
├── api/           # FastAPI serving layer
├── app/           # dashboard frontend
├── tests/         # tests
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```
