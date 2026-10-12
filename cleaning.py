import pandas as pd
from datetime import datetime


df = pd.read_csv(r'input.csv')


df['cleaned_customer_name'] = (
    df['customer_name']
    .str.split()
    .str.join(' ')
    .str.title()
)


col = df.pop('cleaned_customer_name')
pos = df.columns.get_loc('customer_name') + 1
df.insert(pos, 'cleaned_customer_name', col)



df['cleaned_transaction_id'] = df['transaction_id'].str.strip()

col = df.pop('cleaned_transaction_id')
pos = df.columns.get_loc('transaction_id') + 1
df.insert(pos, 'cleaned_transaction_id', col)


df['duplicate_transaction_id'] = (
    df['cleaned_transaction_id'].notna()
    & df['cleaned_transaction_id'].ne('')
    & df['cleaned_transaction_id'].duplicated(keep=False)
)



def clean_date(value):
    if pd.isna(value) or str(value).strip() == "":
        return None, "Missing date"

    value = str(value).strip()

    
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d"), None
        except ValueError:
            pass

    
    for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
        try:
            parsed = datetime.strptime(value, fmt)
            parts = value.replace("/", "-").split("-")

            if int(parts[0]) <= 12 and int(parts[1]) <= 12:
                return None, "Ambiguous date"

            return parsed.strftime("%Y-%m-%d"), None
        except ValueError:
            pass

    return None, "Invalid or unsupported date"


df[["cleaned_transaction_date", "date_issue"]] = (
    df["transaction_date"]
    .apply(lambda value: pd.Series(clean_date(value)))
)

col = df.pop('cleaned_transaction_date')
pos = df.columns.get_loc('transaction_date') + 1
df.insert(pos, 'cleaned_transaction_date', col)


def clean_amount(value):
    if pd.isna(value) or str(value).strip() == "":
        return None, "Missing amount"

    value = str(value).strip().replace(",", "")

    try:
        amount = float(value)
    except ValueError:
        return None, "Invalid amount"

    if amount < 0:
        return None, "Negative amount"

    return amount, None


df[["cleaned_amount", "amount_issue"]] = (
    df["amount"]
    .apply(lambda value: pd.Series(clean_amount(value)))
)

col = df.pop('cleaned_amount')
pos = df.columns.get_loc('amount') + 1
df.insert(pos, 'cleaned_amount', col)


def clean_status(value):
    if pd.isna(value) or str(value).strip() == "":
        return None, "Missing status"

    value = str(value).strip().lower()
    valid_statuses = {"paid", "pending", "cancelled", "refund"}

    if value not in valid_statuses:
        return None, "Unknown status"

    return value, None


df[["cleaned_status", "status_issue"]] = (
    df["status"]
    .apply(lambda value: pd.Series(clean_status(value)))
)

col = df.pop('cleaned_status')
pos = df.columns.get_loc('status') + 1
df.insert(pos, 'cleaned_status', col)



df["name_issue"] = None
df.loc[
    df["customer_name"].isna()
    | df["customer_name"].astype("string").str.strip().eq("").fillna(False),
    "name_issue"
] = "Missing customer name"

df["transaction_id_issue"] = None
df.loc[
    df["cleaned_transaction_id"].isna()
    | df["cleaned_transaction_id"].eq("").fillna(False),
    "transaction_id_issue"
] = "Missing transaction ID"



duplicate_columns = [
    "cleaned_customer_name",
    "cleaned_transaction_date",
    "cleaned_amount"
]

has_required_values = (
    df[duplicate_columns].notna().all(axis=1)
    & df["cleaned_customer_name"].astype("string").str.strip().ne("").fillna(False)
)

df["likely_duplicate"] = False

df.loc[has_required_values, "likely_duplicate"] = (
    df.loc[has_required_values]
    .duplicated(subset=duplicate_columns, keep=False)
)



issue_columns = [
    "name_issue",
    "transaction_id_issue",
    "date_issue",
    "amount_issue",
    "status_issue"
]

df["issues"] = df[issue_columns].apply(
    lambda row: "; ".join(
        str(issue)
        for issue in row
        if pd.notna(issue) and str(issue).strip() != ""
    ),
    axis=1
)


df.loc[df["duplicate_transaction_id"], "issues"] = (
    df.loc[df["duplicate_transaction_id"], "issues"]
    .apply(lambda x: "; ".join(filter(None, [x, "Repeated transaction ID"])))
)


df["is_valid"] = df["issues"].eq("")



df.to_csv("cleaned.csv", index=False, na_rep="")