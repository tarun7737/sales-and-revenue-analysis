
"""CSV schema normalization, validation, and metric-field preparation."""
import pandas as pd
import numpy as np

ALIASES = {
    "order_id": ["order id", "order_id", "invoice", "transaction id"],
    "order_date": ["order date", "order_date", "date", "transaction date"],
    "product": ["product", "product name", "item"],
    "category": ["category", "product category"],
    "region": ["region", "market", "territory"],
    "quantity": ["quantity", "qty", "units"],
    "unit_price": ["unit price", "unit_price", "price", "selling price"],
    "customer_id": ["customer id", "customer_id", "customer"],
    "discount": ["discount", "discount rate"],
    "unit_cost": ["unit cost", "unit_cost", "cost per unit"],
}
REQUIRED = ["order_id", "order_date", "product", "category", "region",
            "quantity", "unit_price", "customer_id"]

def normalize_columns(raw):
    """Map common spreadsheet headers to canonical internal field names."""
    df = raw.copy()
    lookup = {str(c).strip().lower().replace("_", " "): c for c in df.columns}
    rename = {}
    for canonical, aliases in ALIASES.items():
        for alias in aliases:
            if alias in lookup:
                rename[lookup[alias]] = canonical
                break
    return df.rename(columns=rename)

def clean_sales_data(raw):
    """Validate sales records and derive net revenue and optional gross profit."""
    if raw is None or raw.empty:
        raise ValueError("The CSV contains no data.")
    df = normalize_columns(raw)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    warnings = []
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for col in ["quantity", "unit_price", "discount", "unit_cost"]:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["order_id", "product", "category", "region", "customer_id"]:
        df[col] = df[col].astype("string").str.strip()
    old_count = len(df)
    df = df.drop_duplicates()
    if len(df) != old_count:
        warnings.append(f"Removed {old_count-len(df)} exact duplicate rows.")
    valid = df["order_date"].notna()
    valid &= df["quantity"].notna() & (df["quantity"] > 0)
    valid &= df["unit_price"].notna() & (df["unit_price"] >= 0)
    for col in ["order_id", "product", "category", "region", "customer_id"]:
        valid &= df[col].notna() & (df[col] != "")
    removed = int((~valid).sum())
    if removed:
        warnings.append(f"Excluded {removed} invalid rows.")
    df = df.loc[valid].copy()
    if df.empty:
        raise ValueError("No valid rows remain after validation.")
    if "discount" not in df:
        df["discount"] = 0.0
    df["discount"] = df["discount"].fillna(0.0)
    if ((df["discount"] < 0) | (df["discount"] > 1)).any():
        raise ValueError("Discount must be between 0 and 1 (e.g. 0.15).")
    if "unit_cost" not in df:
        df["unit_cost"] = np.nan
    elif (df["unit_cost"].dropna() < 0).any():
        raise ValueError("Unit cost cannot be negative.")
    df["gross_sales"] = df["quantity"] * df["unit_price"]
    df["revenue"] = df["gross_sales"] * (1 - df["discount"])
    df["profit"] = np.where(df["unit_cost"].notna(),
                            df["revenue"] - df["quantity"] * df["unit_cost"], np.nan)
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_year"] = df["order_date"].dt.year
    return df.sort_values("order_date"), warnings
