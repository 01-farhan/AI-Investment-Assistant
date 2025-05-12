import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import plotly.graph_objects as go
import openpyxl


# Intro animation using HTML + CSS
intro_animation = """
<style>
#intro-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #111;
    color: white;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeOut 3s ease-out forwards;
    animation-delay: 2s;
}
@keyframes fadeOut {
    to {opacity: 0; visibility: hidden;}
}
#intro-overlay h1 {
    font-size: 3em;
    animation: zoomIn 1.2s ease-out;
}
@keyframes zoomIn {
    0% { transform: scale(0.5); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}
</style>
<div id="intro-overlay">
    <h1>📊 Neuro</h1>
</div>
"""

st.markdown(intro_animation, unsafe_allow_html=True)

# Main title
st.title("📊 AI Investment Assistant")



# ---------- SIDEBAR DASHBOARD ----------
st.sidebar.title("📊 Investment Dashboard")

# 🌙 Theme toggle
theme_mode = st.sidebar.selectbox("🌓 Choose Theme", ["Light", "Dark"])

# Uploads
predicted_file = st.sidebar.file_uploader("📈 Predicted Data (.xlsx)", type=["xlsx"])
historical_file = st.sidebar.file_uploader("📉 Historical Data (.csv)", type=["csv"])

# Upload for time series financial ratios
time_series_file = st.sidebar.file_uploader("📂 Financial Ratios Time Series (.csv)", type=["csv"])

# Upload for Pie chart
ratios_file = st.sidebar.file_uploader("📂 Financial Ratios pie chart (.csv)", type=["csv"])

# Upload for Radar chart
radar_chart = st.sidebar.file_uploader("📂Financial Ratios Radar chart (.csv)", type=["csv"])


st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Make sure both files match in metrics and format.")
st.sidebar.markdown("---")
st.sidebar.markdown("🔎 _Built with AI + Financial Logic_")


# ---------- DYNAMIC STYLING ----------
if theme_mode == "Dark":
    bg_color = "#1e1e1e"
    text_color = "#ffffff"
else:
    bg_color = "#f9fafb"
    text_color = "#000000"

st.markdown(f"""
    <style>
        .main {{
            background-color: {bg_color};
            color: {text_color};
        }}
        h1, h2, h3, h4, h5, h6, p {{
            color: {text_color};
        }}
        .stButton>button {{
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
        }}
        .stButton>button:hover {{
            background-color: #145a86;
        }}
    </style>
""", unsafe_allow_html=True)

# ---------- APP TITLE ----------
st.markdown("<h1 style='text-align: center;'>💹 AI-Based Investment Recommendation</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>With LSTM Predictions and Financial Ratio Logic</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------- MAIN LOGIC ----------
if predicted_file and historical_file:
    with st.spinner("⏳ Analyzing your data..."):
        time.sleep(1)

        # Load data
        predicted_df = pd.read_excel(predicted_file)
        past_df = pd.read_csv(historical_file)

        # Clean predicted data
        predicted_clean = predicted_df.iloc[:, :2]
        predicted_clean.columns = ["Metric", "2025"]
        predicted_clean.set_index("Metric", inplace=True)
        predicted_clean = predicted_clean.squeeze()

        roe_2025 = predicted_clean["ROE(%)"] * 100
        eps_2025 = predicted_clean["EPS (Rs.)"]
        current_ratio_2025 = predicted_clean["Current Ratio"]

        # EPS Trend Logic
        eps_row = past_df[past_df["Year"] == "EPS (Rs.)"].iloc[:, 1:].astype(float)
        eps_trend = eps_row.values.flatten()
        eps_increasing = all(x < y for x, y in zip(eps_trend[-3:], eps_trend[-2:] + [eps_2025]))

        debt_to_equity_2025 = 2.0  # Placeholder

        # Recommendation Logic
        if roe_2025 > 15 and eps_increasing:
            recommendation = "Buy"
            color = "#00cc44"
            emoji = "🟢"
        elif debt_to_equity_2025 > 2.5 or current_ratio_2025 < 1:
            recommendation = "Sell"
            color = "#ff3300"
            emoji = "🔴"
        else:
            recommendation = "Hold"
            color = "#ffcc00"
            emoji = "🟡"

        # ---------- DISPLAY METRICS ----------
        st.subheader("📊 Key Financial Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ROE (2025)", f"{roe_2025:.2f} %")
            st.metric("Current Ratio", f"{current_ratio_2025}")
        with col2:
            st.metric("Debt-to-Equity", f"{debt_to_equity_2025}")
            st.metric("EPS Trend", "Increasing 📈" if eps_increasing else "Not Increasing ⚠️")



        # ---------- FINAL RECOMMENDATION ----------
        st.markdown("---")
        st.subheader("💡 Final Investment Recommendation")
        st.markdown(f"""
            <div style='background-color: {color}; padding: 20px; border-radius: 12px; text-align: center;'>
                <h2 style='color: white; font-size: 32px;'>{emoji} {recommendation}</h2>
            </div>
        """, unsafe_allow_html=True)

        # ---------- INTERACTIVE EPS CHART with AUTOPLAY ----------
        st.markdown("---")
        st.subheader("📈 EPS Trend Over Time (Animated)")

        # Years and EPS trend
        years = list(past_df.columns[1:])
        eps_history = eps_trend.tolist()
        years.append("2025")
        eps_history.append(eps_2025)

         # Create frames for animation
        frames = [
    go.Frame(
        data=[go.Scatter(x=years[:i+1], y=eps_history[:i+1], mode='lines+markers')],
        name=str(years[i])
    )
    for i in range(len(years))
]

        # Initial figure setup
        fig = go.Figure(
    data=[go.Scatter(x=[years[0]], y=[eps_history[0]], mode='lines+markers', line=dict(color='#007ACC'))],
    layout=go.Layout(
        xaxis=dict(title="Year"),
        yaxis=dict(title="EPS (Rs.)"),
        template="plotly_dark" if theme_mode == "Dark" else "plotly_white",
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="▶️ Play", method="animate", args=[None, {
                    "frame": {"duration": 600, "redraw": True},
                    "fromcurrent": True,
                    "mode": "immediate"
                }])
            ],
            x=0.05, y=1.15  # Optional: position of the button
        )],
        sliders=[dict(
            steps=[dict(method="animate", args=[[str(years[i])], {"mode": "immediate", "frame": {"duration": 600, "redraw": True}, "transition": {"duration": 0}}],
                        label=str(years[i])) for i in range(len(years))],
            transition={"duration": 0},
            x=0.1,
            y=0,
            currentvalue={"prefix": "Year: "}
        )]
    ),
    frames=frames
)

        # Automatically trigger animation on load
        fig.layout["updatemenus"][0]["buttons"][0]["args"][1]["autoplay"] = True

        st.plotly_chart(fig, use_container_width=True)


         # -----DASHBOARD SECTION-----
        st.markdown("---")
        st.subheader("📊 Interactive Financial Dashboard")

        # ---------- TIME SERIES ANALYSIS SECTION ----------

        if time_series_file:
         ratios_df = pd.read_csv(time_series_file)

                 
        if time_series_file:
            st.markdown("---")
            st.subheader("📉 Time Series Analysis: Financial Ratios (2015-2024)")

            # Year Selector
            selected_year = st.selectbox("📅 Select Year", sorted(ratios_df["Year"].unique()))

            # Filter by selected year
            filtered_ratios = ratios_df[ratios_df["Year"] == selected_year]

            # Display selected year's ratios
            st.write(f"### 📌 Financial Ratios for {selected_year}")
            st.dataframe(filtered_ratios.set_index("Year").T)

            # Time series line chart for all ratios
            st.write("### 📊 Ratio Trends Over Time")
            fig_ratios = go.Figure()
            for col in ratios_df.columns[1:]:
                fig_ratios.add_trace(go.Scatter(
                    x=ratios_df["Year"],
                    y=ratios_df[col],
                    mode='lines+markers',
                    name=col
                ))

            fig_ratios.update_layout(
                xaxis_title="Year",
                yaxis_title="Ratio Value",
                template="plotly_dark" if theme_mode == "Dark" else "plotly_white",
                legend_title="Ratios"
            )
            st.plotly_chart(fig_ratios, use_container_width=True)


            # ---------- PIE CHART: FINANCIAL RATIOS ----------
if ratios_file:
    raw_ratios_df = pd.read_csv(ratios_file, index_col=0)

    st.markdown("---")
    st.subheader("📊 Financial Ratios Breakdown")

    # Transpose so each row becomes a year
    ratios_df = raw_ratios_df.transpose().reset_index()
    ratios_df.rename(columns={"index": "Year"}, inplace=True)

    # Convert year column to string (for consistency)
    ratios_df["Year"] = ratios_df["Year"].astype(str)

    # Year selector
    selected_ratio_year = st.selectbox("📅 Select Year (2015-2024)", sorted(ratios_df["Year"].unique()))

    # Filter the row for the selected year
    selected_row = ratios_df[ratios_df["Year"] == selected_ratio_year]

    if not selected_row.empty:
        st.write(f"### 🔍 Financial Ratios for {selected_ratio_year}")

        # Drop 'Year' column for pie chart
        pie_data = selected_row.drop(columns=["Year"]).squeeze()
        labels = pie_data.index.tolist()
        values = pie_data.values.tolist()

        # Plot Pie Chart
        pie_fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        pie_fig.update_layout(
            template="plotly_dark" if theme_mode == "Dark" else "plotly_white",
            legend_title="Ratios",
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(pie_fig, use_container_width=True)

        with st.expander("Raw Ratio Data"):
            st.dataframe(selected_row.set_index("Year"))

             # ---------- RADAR CHART: FINANCIAL RATIOS BY YEAR ----------
if radar_chart:
    raw_ratios_df = pd.read_csv(radar_chart, index_col=0)

    st.markdown("---")
    st.subheader("Financial Ratios Radar chart")

    # Transpose so each row is a year
    ratios_df = raw_ratios_df.transpose().reset_index()
    ratios_df.rename(columns={"index": "Year"}, inplace=True)
    ratios_df["Year"] = ratios_df["Year"].astype(str)

    # Year selector
    selected_year = st.selectbox("📅 Select Year", sorted(ratios_df["Year"].unique()), key="radar_year")

    selected_row = ratios_df[ratios_df["Year"] == selected_year]
    if not selected_row.empty:
        ratios_for_radar = selected_row.drop(columns=["Year"]).squeeze().replace('%', '', regex=True).astype(float)

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=ratios_for_radar.values,
            theta=ratios_for_radar.index,
            fill='toself',
            name=f"Ratios in {selected_year}"
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(ratios_for_radar.values)*1.2])
            ),
            showlegend=False,
            template="plotly_dark" if theme_mode == "Dark" else "plotly_white",
            margin=dict(t=20, b=20)
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        with st.expander("📄 Raw Ratio Data"):
            st.dataframe(selected_row.set_index("Year"))

         # ---------- DOWNLOAD RESULT ----------
    st.markdown("#### ⬇️ Download Your Recommendation")

    result_df = pd.DataFrame({
            "ROE (2025)": [f"{roe_2025:.2f}%"],
            "EPS Trend": ["Increasing" if eps_increasing else "Not Increasing"],
            "Current Ratio": [current_ratio_2025],
            "Debt-to-Equity (2025)": [debt_to_equity_2025],
            "Final Recommendation": [recommendation]
        })

    
 

        # ---------- EXPANDERS ----------
    with st.expander("🔍 View Predicted Data"):
            st.dataframe(predicted_df)

    with st.expander("📜 View Historical EPS Data"):
            st.dataframe(past_df)

else:
    st.info("📂 Please upload both predicted and historical data from the sidebar to get started.")



