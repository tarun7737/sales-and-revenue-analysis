
import pandas as pd
from src.data import clean_sales_data
from src.analytics import calculate_kpis, grouped_revenue
from src.sample_data import make_sample_data

def test_demo_kpis_are_positive():
    df,_=clean_sales_data(make_sample_data(100))
    k=calculate_kpis(df)
    assert k["revenue"] > 0 and k["orders"] > 0

def test_discount_and_profit_math():
    raw=pd.DataFrame([{"order_id":"A","order_date":"2025-01-01","product":"P",
      "category":"C","region":"R","quantity":2,"unit_price":100,"discount":.1,
      "unit_cost":60,"customer_id":"X"}])
    df,_=clean_sales_data(raw)
    assert df.iloc[0].revenue == 180
    assert df.iloc[0].profit == 60

def test_grouped_revenue_sorted():
    df,_=clean_sales_data(make_sample_data(80))
    assert grouped_revenue(df,"category").revenue.is_monotonic_decreasing
