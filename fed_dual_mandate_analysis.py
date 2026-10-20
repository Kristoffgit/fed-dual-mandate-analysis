#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 18:41:32 2026

@author: kristoffoliphant
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns

API_KEY = "YOUR_FRED_API_KEY_HERE"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
START_DATE = "2000-01-01"
END_DATE = "2026-09-01"

def fetch_fred_series(series_id):
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": START_DATE,
        "observation_end": END_DATE,
        }
    response = requests.get(BASE_URL, params=params)
    data = response.json().get("observations", [])
    
    df = pd.DataFrame(data)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.rename(columns={"value": series_id})

cpi = fetch_fred_series("CPIAUCSL")
fedfunds = fetch_fred_series("FEDFUNDS")

df_v1 = cpi.merge(fedfunds, on="date")
df_v1["INFLATION_YOY"] = df_v1["CPIAUCSL"].pct_change(periods=12) * 100
df_v1 = df_v1[df_v1["date"] >= "2001-01-01"].reset_index(drop=True)

sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.sans-serif": "Arial", "font.family": "sans-serif"})

fig, ax = plt.subplots(figsize=(12, 5.2))

recessions = [
    ("2001-03-01", "2001-11-01"),
    ("2007-12-01", "2009-06-01"),
    ("2020-02-01", "2020-04-01"),
]
for start, end in recessions:
    ax.axvspan(
        pd.to_datetime(start), pd.to_datetime(end), color="gray", alpha=0.18
        )
sns.lineplot(
    data=df_v1,
    x="date",
    y="INFLATION_YOY",
    ax=ax,
    color="#d95f02",
    linewidth=2.3,
    label="Inflation Rate (CPI YoY %)",
    )
sns.lineplot(
    data=df_v1,
    x="date",
    y="FEDFUNDS",
    ax=ax,
    color="#7570b3",
    linewidth=2.0,
    linestyle="--",
    label="Federal Funds Rate (%)",
    )
ax.axhline(
    2.0,
    color="#e41a1c",
    linestyle=":",
    linewidth=1.6,
    label="Fed 2.0% Inflation Target",
    )
ax.annotate(
    "2009 Deflation (-2.0%)\nFed cuts rate to 0.0%",
    xy=(pd.to_datetime("2009-07-01"), -2.0),
    xytext=(pd.to_datetime("2003-06-01"), -1.8),
    arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2),
    fontsize=9.5,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#888888"),
    )
ax.annotate(
    "2022 Inflation Surge (9.0%)\nAggressive Rate Hikes (>5.0%)",
    xy=(pd.to_datetime("2022-06-01"), 9.0),
    xytext=(pd.to_datetime("2014-06-01"), 8.5),
    arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2),
    fontsize=9.5,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#888888"),
    )
ax.set_title(
    "Price Stability Mandate: CPI Inflation vs. Federal Funds Rate (2001-2026)",
    fontsize=13,
    fontweight="bold",
    pad=12,
    )
ax.set_ylabel("Rate (%)", fontsize=11, fontweight="bold")
ax.set_xlabel("Year", fontsize=11, fontweight="bold")
ax.set_ylim(-3.5, 11)

ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.legend(
    loc="upper left", frameon=True, facecolor="white", framealpha=0.92, fontsize=10
    )
plt.tight_layout()
plt.savefig("visual1_inflation_funds.png", dpi=300)
plt.show()
print("Saved: visual1_inflation_funds.png")

#Visual 2

API_KEY = "YOUR_FRED_API_KEY_HERE"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
START_DATE = "2000-01-01"
END_DATE = "2026-09-01"

def fetch_fred_series(series_id):
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": START_DATE,
        "observation_end": END_DATE,
        }
    response = requests.get(BASE_URL, params=params)
    data = response.json().get("observations", [])
    
    df = pd.DataFrame(data)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.rename(columns={"value": series_id})

fedfunds = fetch_fred_series("FEDFUNDS")
unrate = fetch_fred_series("UNRATE")

df_v2 = fedfunds.merge(unrate, on="date")
df_v2 = df_v2[df_v2["date"] >= "2001-01-01"].reset_index(drop=True)

sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.sans-serif": "Arial", "font.family": "sans-serif"})

fig, ax = plt.subplots(figsize=(12, 5.2))

recessions = [
    ("2001-03-01", "2001-11-01"),
    ("2007-12-01", "2009-06-01"),
    ("2020-02-01", "2020-04-01"),
    ]
for start, end in recessions:
    ax.axvspan(
        pd.to_datetime(start), pd.to_datetime(end), color="gray", alpha=0.18
        )
sns.lineplot(
    data=df_v2,
    x="date",
    y="FEDFUNDS",
    ax=ax,
    color="#7570b3",
    linewidth=2.0,
    linestyle="--",
    label="Federal Funds Rate (%)",
    )
sns.lineplot(
    data=df_v2,
    x="date",
    y="UNRATE",
    ax=ax,
    color="#1b9e77",
    linewidth=2.3,
    label="Civilian Unemployment Rate (%)",
    )

ax.axhline(
    4.0,
    color="#666666",
    linestyle=":",
    linewidth=1.6,
    label="Approx. Full Employment Target (~4.0%)",
    )

ax.annotate(
    "Great Recession Policy Lag:\nUnemployment peaks at 10.0%\nTakes ~8 years"
    " to reach 4.0%",
    xy=(pd.to_datetime("2009-10-01"), 10.0),
    xytext=(pd.to_datetime("2011-02-01"), 11.5),
    arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2),
    fontsize=9.5,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#888888"),
    )
ax.annotate(
    "COVID Shock (14.8%)\nSudden labor market surge",
    xy=(pd.to_datetime("2020-04-01"), 14.8),
    xytext=(pd.to_datetime("2021-03-01"), 13.0),
    arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2),
    fontsize=9.5,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#888888"),
    )
ax.set_title(
    "Maximum Employment Mandate: Labor Market Response & Policy Lag"
    " (2001-2026)",
    fontsize=13,
    fontweight="bold",
    pad=12,
    )
ax.set_ylabel("Rate (%)", fontsize=11, fontweight="bold")
ax.set_xlabel("Year", fontsize=11, fontweight="bold")
ax.set_ylim(0, 16.5)

ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.legend(
    loc="upper left",
    frameon=True,
    facecolor="white",
    framealpha=0.92,
    fontsize=10,
    )

plt.tight_layout()
plt.savefig("visual2_unemployment_funds.png", dpi=300)
plt.show()
print("Saved: visual2_unemployment_funds.png")

#Visual 3

df_master = cpi.merge(fedfunds, on="date").merge(unrate, on="date")
df_master["INFLATION_YOY"] = df_master["CPIAUCSL"].pct_change(periods=12) * 100
df_v3 = df_master[df_master["date"] >= "2001-01-01"].dropna().reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 6.5))

target_zone = plt.Rectangle(
    (2.5, 1.5), 1.5, 1.0, 
    color="#2ca02c", alpha=0.22, 
    label="Statutory Target Zone (Unemp <= 4%, Infl ~2%)"
    )
ax.add_patch(target_zone)

ax.scatter(
    df_v3["UNRATE"],
    df_v3["INFLATION_YOY"],
    color="#4a5568",
    alpha=0.45,
    edgecolors="none",
    s=42,
    label="Monthly Observation (2001–2026)"
    )

ax.axhline(2.0, color="#d95f02", linestyle=":", linewidth=1.5, label="2.0% Inflation Target")
ax.axvline(4.0, color="#1b9e77", linestyle=":", linewidth=1.5, label="4.0% Full Employment Target")

row_2009 = df_v3[df_v3["date"] == "2009-07-01"].iloc[0]
ax.annotate(
    "July 2009:\nDeflation (-2.0%) with High Unemp (9.5%)",
    xy=(row_2009["UNRATE"], row_2009["INFLATION_YOY"]),
    xytext=(row_2009["UNRATE"] - 3.8, row_2009["INFLATION_YOY"] - 0.9),
    arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2),
    fontsize=9.0,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#888888")
)

row_2020 = df_v3[df_v3["date"] == "2020-04-01"].iloc[0]
ax.annotate(
    "April 2020 COVID Spike:\nUnemployment surges to 14.8%",
    xy=(row_2020["UNRATE"], row_2020["INFLATION_YOY"]),
    xytext=(row_2020["UNRATE"] - 4.5, row_2020["INFLATION_YOY"] + 1.2),
    arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2),
    fontsize=9.0,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#888888")
)

row_2022 = df_v3[df_v3["date"] == "2022-06-01"].iloc[0]
ax.annotate(
    "June 2022 Peak:\nInflation hits 9.0% (Unemp 3.6%)",
    xy=(row_2022["UNRATE"], row_2022["INFLATION_YOY"]),
    xytext=(row_2022["UNRATE"] + 1.0, row_2022["INFLATION_YOY"] - 0.2),
    arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2),
    fontsize=9.0,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#888888")
)

ax.set_title(
    "The Dual Mandate Trade-Off: Empirical Phillips Curve & Policy Target Zone (2001–2026)",
    fontsize=12.5,
    fontweight="bold",
    pad=12
)
ax.set_xlabel("Civilian Unemployment Rate (%)", fontsize=11, fontweight="bold")
ax.set_ylabel("Inflation Rate (CPI YoY %)", fontsize=11, fontweight="bold")
ax.set_xlim(2.0, 16.0)
ax.set_ylim(-3.5, 10.5)

ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.92, fontsize=9.5)

plt.tight_layout()
plt.savefig("visual3_tradeoff_scatter.png", dpi=300)
plt.show()
print("Saved: visual3_tradeoff_scatter.png")