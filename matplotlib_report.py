"""Export a static Matplotlib monthly revenue chart from a sales CSV."""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from src.data import clean_sales_data
from src.analytics import monthly_revenue

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",default="data/sample_sales_data.csv")
    parser.add_argument("--output",default="outputs/monthly_revenue.png")
    args=parser.parse_args()
    raw=pd.read_csv(args.input)
    df,warnings=clean_sales_data(raw)
    for warning in warnings: print("Warning:",warning)
    trend=monthly_revenue(df)
    # Build a static chart suitable for reports and README screenshots.
    fig,ax=plt.subplots(figsize=(11,5))
    ax.plot(trend["month"],trend["revenue"],marker="o")
    ax.set(title="Monthly Net Revenue",xlabel="Month",ylabel="Revenue")
    ax.grid(True,alpha=.25)
    fig.autofmt_xdate()
    fig.tight_layout()
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(out,dpi=160,bbox_inches="tight")
    print(f"Saved chart: {out}")

if __name__=="__main__": main()
