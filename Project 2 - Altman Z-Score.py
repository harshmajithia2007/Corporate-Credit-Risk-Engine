import yfinance as yf
import pandas as pd
import datetime

ticker = "BA"
company = yf.Ticker(ticker)

income = company.financials.transpose()
balance = company.balance_sheet.transpose()

income.index = pd.to_datetime(income.index).date
balance.index = pd.to_datetime(balance.index).date

prices = company.history(period="5y")
prices.index = pd.to_datetime(prices.index).tz_localize(None).date
matched_prices = prices['Close'].reindex(balance.index, method='ffill')

current_assets = balance.get('Total Current Assets', balance.get('Current Assets'))
current_liabilities = balance.get('Total Current Liabilities', balance.get('Current Liabilities'))

if current_assets is None or current_liabilities is None:
    print("Error: Could not find current assets or liabilities in the API data.")
    exit()

working_capital = current_assets - current_liabilities

assets = balance.get('Total Assets')
liabilities = balance.get('Total Liabilities Net Minority Interest')
retained_earnings = balance.get('Retained Earnings')
ebit = income.get('EBIT')
revenue = income.get('Total Revenue')
shares = balance.get('Ordinary Shares Number')

x1 = working_capital / assets
x2 = retained_earnings / assets
x3 = ebit / assets
x4 = (shares * matched_prices) / liabilities
x5 = revenue / assets

model_output = pd.DataFrame(index=balance.index)
model_output['z_score'] = (1.2 * x1) + (1.4 * x2) + (3.3 * x3) + (0.6 * x4) + (0.999 * x5)
model_output = model_output.sort_index(ascending=True).dropna()

alert_date = None
danger_line = 1.81

print(f"=== BACKTESTING RISK TIMELINE FOR: {ticker} ===")
for date, row in model_output.iterrows():
    score = round(row['z_score'], 3)
    public_date = date + datetime.timedelta(days=30)
    
    if score > 2.99:
        zone = "Safe Zone"
    elif score >= 1.81:
        zone = "Grey Zone"
    else:
        zone = "DISTRESS ZONE"
        
    print(f"Fiscal Period: {date} | Public Release: {public_date} | Z-Score: {score} | [{zone}]")
    
    if score < danger_line and alert_date is None:
        alert_date = public_date

print("=" * 50)

if alert_date:
    print(f"🚨 AUDIT ALERT: Engine flagged actionable market distress on Public Release Date: {alert_date}.")
else:
    print("✅ PASS: The company remained out of the critical distress zone during this period.")