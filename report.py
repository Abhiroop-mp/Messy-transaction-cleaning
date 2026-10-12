import pandas as pd
import json
df = pd.read_csv(r'cleaned.csv')
revenue_rows = (
    df["is_valid"]
    & df["cleaned_status"].eq("paid")
    & ~df["likely_duplicate"]
)

total_revenue = round(
    df.loc[revenue_rows, "cleaned_amount"].sum(),
    2
)

report = {
    "input_rows": int(len(df)),
    "valid_rows": int(df["is_valid"].sum()),
    "invalid_rows": int((~df["is_valid"]).sum()),
    "duplicate_counts": {
        "repeated_transaction_id": int(
            df["duplicate_transaction_id"].sum()
        ),
        "likely_duplicate": int(df["likely_duplicate"].sum())
    },
    "total_revenue": total_revenue
}

with open("report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)