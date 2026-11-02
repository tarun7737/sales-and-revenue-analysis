
"""Reusable business intelligence calculations."""
import pandas as pd

def calculate_kpis(df):
    """Calculate headline sales metrics; profit is absent if costs were not supplied."""
    revenue = float(df["revenue"].sum())
    orders = int(df["order_id"].nunique())
    profit_available = df["profit"].notna().any()
    profit = float(df["profit"].sum()) if profit_available else None
    return {
        "revenue": revenue, "orders": orders,
        "units_sold": int(df["quantity"].sum()),
        "customers": int(df["customer_id"].nunique()),
        "average_order_value": revenue / orders if orders else 0.0,
        "profit": profit,
        "profit_margin": profit / revenue * 100 if profit_available and revenue else None
    }

def grouped_revenue(df, dimension, limit=None):
    """Aggregate revenue, unique orders and units by a dataset dimension."""
    out = (df.groupby(dimension, dropna=False)
           .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"),
                units=("quantity", "sum"))
           .reset_index().sort_values("revenue", ascending=False))
    return out.head(limit) if limit else out

def monthly_revenue(df):
    """Aggregate net revenue by month."""
    out = df.groupby("order_month", as_index=False)["revenue"].sum()
    out["month"] = pd.to_datetime(out["order_month"])
    return out.sort_values("month")

def make_report(df, warnings=None):
    """Return JSON-safe dashboard data for API consumers."""
    trend = monthly_revenue(df).copy()
    trend["month"] = trend["month"].astype(str)
    return {
        "rows_analyzed": int(len(df)), "warnings": warnings or [],
        "kpis": calculate_kpis(df),
        "monthly_revenue": trend[["month", "revenue"]].to_dict("records"),
        "category_revenue": grouped_revenue(df, "category").to_dict("records"),
        "region_revenue": grouped_revenue(df, "region").to_dict("records"),
        "top_products": grouped_revenue(df, "product", 10).to_dict("records")
    }
