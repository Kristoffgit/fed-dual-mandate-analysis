# fed-dual-mandate-analysis

A data analysis project from my M.S. Data Science coursework. It uses Python and the FRED API to test whether the Federal Reserve has managed to keep inflation near 2% and unemployment at or below about 4% at the same time.

## Data

Monthly data from the FRED API (Federal Reserve Bank of St. Louis), 2001–2026: CPI inflation (CPIAUCSL), the federal funds rate (FEDFUNDS), and the unemployment rate (UNRATE).

## Method

Pulled the data with requests, merged and calculated year-over-year inflation with pandas, and built three annotated charts with Matplotlib and Seaborn.

## Charts

### 1. Inflation vs. the federal funds rate

### 2. Unemployment vs. the federal funds rate

### 3. Unemployment vs. inflation, every month

## Findings

- Both goals were rarely met together. The main exception was 2018–2019.
- Recovery was slow. After the 2008 crisis, unemployment peaked near 10% in 2009 and took roughly eight years to return to about 4%.
- COVID-19 (2020) and the 2022 inflation surge hit faster than rate changes could respond.

Note: the 4% line labeled as a "target" in the charts is an approximate benchmark, not an official Fed target. The charts show patterns over time, not cause and effect.

The full written report is in this repo: Fed_Dual_Mandate_Report.docx

## How to run

1. Get a free API key at https://fred.stlouisfed.org/docs/api/api_key.html
2. Open fed_dual_mandate_analysis.py and paste the key into the API_KEY = "YOUR_FRED_API_KEY_HERE" line (it appears twice).
3. Install the packages: pip install pandas requests matplotlib seaborn
4. Run python fed_dual_mandate_analysis.py. The charts are saved as PNG files in the same folder.

## Tools

Python (pandas, requests, Matplotlib, Seaborn), FRED API
