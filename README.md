# Challenge 1 — Messy Transactions

## Overview

This project cleans and validates transaction data from `input.csv` and generates two output files: `cleaned.csv` and `report.json`.

The program uses Python and Pandas to normalize transaction fields, identify data quality issues, detect duplicates, and generate a summary report.

## Requirements

- Python 3.8 or later
- Pandas

Install Pandas using:

```bash
pip install pandas
```

## How to Run

1. Place `clean_transactions.py` and `input.csv` in the same folder.
2. Update the input file path in the Python script if necessary.
3. Open a terminal in that folder.
4. Run the program:

```bash
python clean_transactions.py
```

The program generates:

- `cleaned.csv` — normalized transaction data with validation results and issue explanations.
- `report.json` — summary statistics, duplicate counts, and total revenue.

## Data Cleaning and Validation

### Customer Names

- Remove leading and trailing whitespace.
- Replace repeated whitespace between words with a single space.
- Standardize capitalization.
- Preserve the original customer name.

### Transaction IDs

- Remove leading and trailing whitespace from transaction IDs.
- Preserve original IDs.
- Flag all rows containing a repeated non-empty transaction ID.

### Dates

- Convert supported date formats to `YYYY-MM-DD`.
- Supported formats include `YYYY-MM-DD`, `YYYY/MM/DD`, `DD/MM/YYYY`, and `DD-MM-YYYY`.
- Dates that cannot be parsed or are identified as ambiguous are marked as untrusted.
- The original date is preserved.

### Amounts

- Convert valid numeric amounts to numbers.
- Remove commas used as thousands separators.
- Mark missing and non-numeric amounts as invalid.
- Treat negative amounts as invalid.
- Accept zero as a valid amount.
- Preserve the original amount.

### Statuses

Normalize statuses to the following accepted values:

- `paid`
- `pending`
- `cancelled`
- `refund`

Missing or unrecognized statuses are flagged as issues.

### Row Validity

Each row receives an `is_valid` flag and an `issues` field.

- `True` means no validation issues were detected.
- `False` means one or more validation issues were detected.
- Multiple issues are recorded together in the `issues` field.
- Repeated transaction IDs are treated as validation issues.
- Likely duplicates are flagged for review and do not automatically invalidate a row.

### Duplicate Detection

Two types of duplicates are identified:

1. **Repeated transaction IDs:** All rows sharing the same non-empty cleaned transaction ID are flagged.
2. **Likely duplicate transactions:** Rows with matching cleaned customer names, dates, and amounts are flagged when the matching fields are present.

Likely duplicates are retained in the output and are not automatically treated as confirmed duplicate transactions.

## Revenue Calculation

Total revenue is calculated from valid transactions with the normalized status `paid`, excluding rows flagged as likely duplicates.

This is an implementation assumption for the challenge. In a real business, revenue rules may differ, particularly when handling refunds and duplicate transactions.

## Report Reconciliation

The report includes:

- Total input rows
- Valid rows
- Invalid rows
- Repeated transaction ID row count
- Likely duplicate row count
- Total revenue

The following condition must hold:

`input_rows = valid_rows + invalid_rows`

The number of data rows in `cleaned.csv` must also equal `input_rows`.

Duplicate counts may overlap because a transaction can have both duplicate flags.

## Edge Case Tested

**Invalid date:** The value `not a date` cannot be interpreted using the supported date formats.

Expected behavior:

- `cleaned_transaction_date` is empty.
- `date_issue` contains `Invalid or unsupported date`.
- The row is marked invalid.
- The original date is preserved.

## Output Files

After successful execution, the folder contains:

```text
clean_transactions.py
input.csv
cleaned.csv
report.json
README.md
```
