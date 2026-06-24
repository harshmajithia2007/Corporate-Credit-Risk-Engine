# Corporate-Credit-Risk-Engine
An automated Altman Z-Score risk engine built to evaluate corporate distress while eliminating look-ahead bias and fixing missing API data.

# Altman Z-Score Risk Backtester

As a finance student, I wanted to see how the classic Altman Z-Score holds up against modern corporate balance sheet distress. I built this Python script to backtest the model against real-world data while adjusting for real market conditions.

The math behind the Z-Score is straightforward, but when I started working with live financial APIs, I ran into two major data problems that textbook equations don't tell you about. This script focuses on solving those two issues:

### 1. The Hindsight Trap (Look-Ahead Bias)
Most basic models pull historical data and assume you had the company's balance sheet the exact day their fiscal year ended (e.g., Dec 31). In reality, no investor has that data instantly—companies take weeks to audit and file their reports. To fix this look-ahead bias, my script automatically adds a **30-day reporting lag** to the timeline. This ensures the model only triggers an alert when the data would have actually been public.

### 2. Broken Data in Distressed Firms
When a company is under severe financial pressure, public APIs frequently drop pre-calculated lines like `Working Capital`. To stop the script from crashing or returning errors, I wrote a quick backup rule: if the API drops the metric, the script manually pulls raw Current Assets and Current Liabilities and recalculates the Working Capital from scratch.

### Case Study: Testing Boeing ($BA)
I ran this engine live against Boeing’s financials over the last few years to track their capital runway:
* **The Trend:** The model caught a clear structural decay trend, tracking Boeing deep inside the "Distress Zone" (well below the standard 1.81 safety threshold) from 2022 all the way through 2025.
* **The Actionable Alert:** Because of the 30-day reporting lag rule, the model bypassed unrealistic hindsight and triggered a confirmed market alert in late January 2023—matching the exact window the audited numbers hit the public.

### How to Run This Project

You will need the `pandas` and `yfinance` libraries installed:

```bash
pip install yfinance pandas
python risk_engine.py
