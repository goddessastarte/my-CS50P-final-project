# RSI viewer
    #### Video Demo:  <URL HERE>
    #### Description: A simple Python desktop app to compare the Relative Strength of multiple cryptocurrencies using historical CSV data.

## What It Does

- Upload 2 or 3 CSV files of crypto price history
- Type the name for each coin (e.g., Bitcoin, Solana)
- Visualize how they performed over time, normalized to 100
- Great for spotting outperformers using Relative Strength

## How to Use It

1. Run `main.py`
2. Click the **Compare** button
3. Upload 2 or 3 CSV files
   - Required columns: `snapped_at`, `price`
   - Recommended: Download CSVs from CoinGecko (they match the expected format)
4. Type a custom name for each file
5. Click **Compare Now** to see the chart!

✅ All data is processed using `pandas`
✅ Charts are built using `matplotlib`
✅ Built with `tkinter` for GUI

## Example CSV Format

| snapped_at        | price   |
|-------------------|---------|
| 2023-01-01 UTC    | 100.50  |
| 2023-01-02 UTC    | 102.20  |

## How I Tested It

- Used `pytest` to test data-cleaning and normalization functions
- Built sample test cases for merging and chart input

## Requirements

- Python 3.10+
- `pandas` (for data processing)
- `matplotlib` (for charts)
- pytest (for testing)
- Tkinter (for GUI)

Install with:
```bash
pip install -r requirements.txt
```
## Inspiration

Built as my **CS50 final project**.
Inspired by the need to visualize relative crypto performance without using paid APIs.

---
