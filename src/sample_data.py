
"""Generate deterministic synthetic sales rows for demo and test use."""
import numpy as np
import pandas as pd

def make_sample_data(rows=1800, seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    prices = {"Laptop":850,"Monitor":240,"Keyboard":55,"Mouse":28,
              "Headphones":95,"Webcam":70,"Tablet":420,"Printer":180}
    cats = {"Laptop":"Computers","Monitor":"Displays","Keyboard":"Accessories",
            "Mouse":"Accessories","Headphones":"Audio","Webcam":"Accessories",
            "Tablet":"Computers","Printer":"Office"}
    products = list(prices)
    p = rng.choice(products, rows)
    unit_price = np.array([prices[x] for x in p]) * rng.uniform(.88, 1.12, rows)
    return pd.DataFrame({
        "order_id":[f"ORD-{i//2+1:05d}" for i in range(rows)],
        "order_date":rng.choice(dates, rows),
        "product":p, "category":[cats[x] for x in p],
        "region":rng.choice(["North","South","East","West","Central"], rows),
        "quantity":rng.integers(1,6,rows),
        "unit_price":np.round(unit_price,2),
        "discount":rng.choice([0,.05,.1,.15],rows,p=[.45,.25,.2,.1]),
        "unit_cost":np.round(unit_price*rng.uniform(.52,.78,rows),2),
        "customer_id":[f"CUST-{x:04d}" for x in rng.integers(1,501,rows)]
    })
