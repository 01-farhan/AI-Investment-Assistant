# Financial-Dashboard-app
A responsive and interactive financial dashboard built using React, Tailwind CSS, Recharts, and Framer Motion. It visualizes key financial metrics such as Revenue, Net Income, and EPS with sleek, animated line charts.
 Main Features:
1. 🎬 Intro Animation:
Custom CSS/HTML overlay displaying a quick animated "Financial Dashboard" intro.

2. 🌓 Theme Toggle:
Sidebar option to switch between Light and Dark themes, which updates the UI colors accordingly.

3. 📤 Upload Sections:
Predicted Data: .xlsx file with forecasted values (e.g., EPS, ROE, etc.).

Historical Data: .csv file with past financial metrics.

Financial Ratios Time Series: Yearly ratios used for trend analysis.

Pie Chart Data: Yearly breakdowns of financial ratios.

Radar Chart Data: (Uploaded but not used yet in the code).

4. 📈 Prediction-Based Recommendation Logic:
EPS Trend Analysis: Checks if EPS has been increasing for the past 3 years (and 2025).

ROE, Current Ratio & Debt-to-Equity: Thresholds used to generate a "Buy", "Sell", or "Hold" recommendation.

Visual display with color-coded recommendation and emojis.

5. 📉 EPS Trend Animation:
Interactive animated line chart using Plotly to show EPS growth up to 2025.

Autoplays when the section loads, with a year slider and play button.

6. 📊 Time Series Financial Ratio Analysis:
Visualizes how different ratios have changed from 2015–2024.

Select a year to see detailed values.

Line chart shows trends for all ratios over time.

7. 🥧 Financial Ratio Pie Chart:
Select a year and view the ratio composition as a pie chart.

Helps analyze the weight of different financial indicators.

🧠 Logic in a Nutshell:
If ROE > 15% and EPS is increasing → Buy

If Debt-to-Equity > 2.5 or Current Ratio < 1 → Sell

Else → Hold
