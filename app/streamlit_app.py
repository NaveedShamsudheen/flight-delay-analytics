import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")
st.title("✈️ Flight Delay Analytics (2019–2023)")

# Load monthly dataset
df = pd.read_csv("data/processed.csv")

# Sidebar filters
years = sorted(df["year_month"].str[:4].unique().tolist())
year_filter = st.sidebar.multiselect("Select Year(s)", years, default=years)

# Filter dataframe
filtered = df[df["year_month"].str[:4].isin(year_filter)]

# KPIs (based on filtered data)
latest = filtered.iloc[-1]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Flights (latest)", f"{latest['total_flights']:,}")
c2.metric("Avg DEP Delay (min)", round(latest["avg_dep_delay"], 1))
c3.metric("Avg ARR Delay (min)", round(latest["avg_arr_delay"], 1))
c4.metric("On-time Rate (%)", f"{round(latest['ontime_rate']*100, 1)}")

# Charts
st.subheader("Trends Over Time")

fig1 = px.line(
    filtered, x="year_month", y="total_flights", title="Total Flights per Month"
)
fig2 = px.line(
    filtered, x="year_month", y="avg_arr_delay", title="Average Arrival Delay per Month"
)
fig3 = px.line(
    filtered, x="year_month", y="cancel_rate", title="Cancellation Rate per Month"
)

st.plotly_chart(fig1, use_container_width=True)
left, right = st.columns(2)
left.plotly_chart(fig2, use_container_width=True)
right.plotly_chart(fig3, use_container_width=True)

# Highlight COVID automatically
if "2020" in year_filter:
    st.markdown(
        "🦠 **COVID Impact**: Flight activity collapsed in early 2020, then gradually recovered from 2021 onward."
    )
