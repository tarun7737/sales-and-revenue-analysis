
# Sales & Revenue Analytics — Complete Project

**Author:** Tarun Katara  
**Project:** Resume-ready Python analytics platform with Streamlit dashboard, FastAPI backend and React web frontend.

## What is included

- CSV ingestion, schema normalization, validation and cleaning.
- Revenue, order, customer, units and average-order-value KPIs.
- Profit and margin only when unit-cost data is supplied.
- Monthly, category, product and regional analysis.
- Streamlit dashboard (`app.py`).
- FastAPI REST API (`api.py`) for future web/mobile clients.
- React + Vite frontend (`frontend/`).
- Deterministic synthetic sample dataset generator.
- Pytest unit tests.
- Matplotlib report example in `src/matplotlib_report.py` (if included in a later extension).

## Important metric definitions

- Gross sales = quantity × unit price.
- Net revenue = gross sales × (1 − discount).
- Estimated gross profit = net revenue − quantity × unit cost.
- AOV = net revenue / distinct order IDs.
- Discount is a decimal rate from 0 to 1, e.g. `0.15` means 15%.
- Cost data is optional. Profit is not fabricated when unit cost is absent.
- Currency is not converted automatically; source data must use one consistent currency.

## Required CSV fields

`order_id`, `order_date`, `product`, `category`, `region`, `quantity`, `unit_price`, `customer_id`

Optional: `discount`, `unit_cost`.

Common header variants are normalized. Quantity must be positive; unit price and unit cost cannot be negative.

## Build and run: Streamlit dashboard

Python 3.10+ recommended.

```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`.

The dashboard uses synthetic demo data by default. Upload a CSV from the sidebar to analyze your own data.

## Build and run: FastAPI backend

Open a second terminal in the project root and activate the same virtual environment.

```bash
uvicorn api:app --reload
```

- Health: `http://127.0.0.1:8000/health`
- Demo analytics: `http://127.0.0.1:8000/analytics/demo`
- API documentation: `http://127.0.0.1:8000/docs`

The API accepts a CSV at `POST /analytics/upload`, multipart field name `file`.

## Build and run: React frontend

Install Node.js LTS first. Open a third terminal:

```bash
cd frontend
npm install
```

Optional: copy `.env.example` to `.env` and set `VITE_API_URL` if the API is not at the default local URL.

```bash
npm run dev
```

Open `http://localhost:5173`. The FastAPI backend must be running.

Build the static frontend:

```bash
npm run build
npm run preview
```

The production build is written to `frontend/dist/`.

## Tests

From the project root:

```bash
pytest -q
```

## Project structure

```text
Sales-Revenue-Analytics-Complete/
├── app.py
├── api.py
├── requirements.txt
├── README.md
├── .env.example
├── data/
├── outputs/
├── src/
│   ├── data.py
│   ├── analytics.py
│   └── sample_data.py
├── tests/
│   └── test_analytics.py
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        └── style.css
```

## Recommended build roadmap

1. Run the Streamlit dashboard and verify the supplied synthetic data.
2. Upload a clean, representative CSV and validate totals against a trusted spreadsheet.
3. Run the FastAPI backend and inspect `/docs`.
4. Run the React frontend and confirm it reads demo data and accepts CSV uploads.
5. Add PostgreSQL persistence with SQLAlchemy and Alembic migrations.
6. Add secure user registration/login, role-based access, and per-user dataset ownership.
7. Add persistent dataset storage, audit logging, and report history.
8. Add PDF/Excel exports, comparison periods, customer cohorts and forecasting.
9. Add authentication and authorization tests, integration tests, and upload limits.
10. Deploy API, frontend and database with HTTPS, secrets management, backups and monitoring.

## Security and production notes

This package is a local-development starter. It does not yet implement production authentication, user-specific data isolation, database persistence, or cloud deployment. Do not expose sensitive business/customer data to a public deployment until those controls are implemented. Configure CORS to the exact production frontend origin. Add file-size limits, rate limiting, authentication, authorization, TLS, logging and backups.

## Resume description

**Sales & Revenue Analytics Platform | Python, Pandas, NumPy, Matplotlib, Plotly, Streamlit, FastAPI, React**
- Built a sales analytics application with CSV validation, reusable KPI calculations and interactive dashboards.
- Developed Streamlit and React interfaces backed by a FastAPI analytics API.
- Analyzed revenue, orders, customers, products, categories and regional performance.
- Added automated tests and documented metric definitions, setup and deployment roadmap.

## Author

**Tarun Katara**  
Data Analytics | Python | Business Intelligence | Data Visualization
