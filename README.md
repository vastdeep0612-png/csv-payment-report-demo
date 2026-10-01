# DEMO PROJECT

Self-initiated sample. This is not a client file.

## What problem it solves

A repeated order export needs a paid total. Refunded rows, amounts that are not numbers, empty amounts, currency symbols, and a repeated order id should not be added twice.

## Input format

CSV with a header:

```
order_id,status,amount
```

`status` is `paid` or another word such as `refunded`. `amount` is a plain decimal. `$`, `€`, and `£` are rejected.

## Output format

- `sample_output.csv` — one row per accepted payment, then `TOTAL`
- `sample_errors.csv` — invalid amounts and duplicate order ids, with a reason
- `sample_report.txt` — counts and the total

Rows whose status is not `paid` are counted as excluded. They are not in the error file.

## How to run

From this folder:

```
python process.py
python -m unittest tests.test_process
```

No third-party packages. Python 3.11 or newer is enough.

## Example result

Accepted payments are A-100 12.50, A-101 7.00, and A-104 3.25.

```
valid_payments_total: 22.75
```

A-102 is refunded. A-103 is not a number. The second A-100 is a duplicate. A-105 is empty. A-106 uses a currency symbol.

## Limitations

- One CSV file per run
- Does not read `.xlsx`
- Does not convert currency symbols
- Keeps the first valid `paid` row when an order id repeats
- Sample rows are synthetic
