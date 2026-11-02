
"""Streamlit analytics dashboard: run with `streamlit run app.py`."""
import pandas as pd
import streamlit as st
import plotly.express as px
from src.data import clean_sales_data
from src.analytics import calculate_kpis, grouped_revenue, monthly_revenue
from src.sample_data import make_sample_data

st.set_page_config(page_title="Sales & Revenue Analytics", page_icon="📊", layout="wide")
st.title("📊 Sales & Revenue Analytics")
st.caption("Built by Tarun Katara | Python · Pandas · Plotly")

upload = st.sidebar.file_uploader("Upload sales CSV", type=["csv"])
try:
    raw = pd.read_csv(upload) if upload else make_sample_data()
    df, warnings = clean_sales_data(raw)
except Exception as exc:
    st.error(str(exc))
    st.stop()

for warning in warnings:
    st.sidebar.warning(warning)
st.sidebar.caption("Synthetic demo data" if upload is None else upload.name)

# Apply dashboard filters before computing all visible KPIs and charts.
date_min, date_max = df.order_date.min().date(), df.order_date.max().date()
date_range = st.sidebar.date_input("Order date range", (date_min, date_max))
regions = st.sidebar.multiselect("Region", sorted(df.region.unique()), default=sorted(df.region.unique()))
categories = st.sidebar.multiselect("Category", sorted(df.category.unique()), default=sorted(df.category.unique()))
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
else:
    start, end = date_min, date_max
view = df[df.order_date.dt.date.between(start,end) & df.region.isin(regions) & df.category.isin(categories)]
if view.empty:
    st.warning("No records match the selected filters.")
    st.stop()

k = calculate_kpis(view)
c = st.columns(5)
for col, label, value in zip(c, ["Net revenue","Orders","Units sold","Customers","Average order value"],
    [f"${k['revenue']:,.2f}",f"{k['orders']:,}",f"{k['units_sold']:,}",f"{k['customers']:,}",f"${k['average_order_value']:,.2f}"]):
    col.metric(label, value)
if k["profit"] is not None:
    a,b=st.columns(2)
    a.metric("Estimated gross profit",f"${k['profit']:,.2f}")
    b.metric("Profit margin",f"{k['profit_margin']:.1f}%")

left,right=st.columns(2)
with left:
    st.subheader("Monthly revenue")
    st.plotly_chart(px.line(monthly_revenue(view),x="month",y="revenue",markers=True),use_container_width=True)
with right:
    st.subheader("Category revenue")
    st.plotly_chart(px.bar(grouped_revenue(view,"category"),x="category",y="revenue",color="category"),use_container_width=True)
left,right=st.columns(2)
with left:
    st.subheader("Top products")
    st.plotly_chart(px.bar(grouped_revenue(view,"product",10),x="revenue",y="product",orientation="h"),use_container_width=True)
with right:
    st.subheader("Regional contribution")
    st.plotly_chart(px.pie(grouped_revenue(view,"region"),names="region",values="revenue",hole=.4),use_container_width=True)

st.subheader("Detailed category report")
st.dataframe(grouped_revenue(view,"category"),use_container_width=True,hide_index=True)
st.download_button("Download filtered CSV",view.to_csv(index=False),"sales_filtered.csv","text/csv")
st.download_button("Download KPI summary",pd.DataFrame([k]).to_csv(index=False),"sales_kpis.csv","text/csv")
