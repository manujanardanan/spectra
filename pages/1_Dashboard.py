import streamlit as st
import pandas as pd

st.title("📊 Dashboard")

st.markdown("### Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Active Agents", 5)
col2.metric("Today's Alerts", 12)
col3.metric("Estimated Savings", "$18,450")

st.markdown("---")
st.subheader("Recent Agent Runs")
df = pd.DataFrame({
    "Agent": ["Inventory Watcher", "Delay Notifier", "Risk Scanner"],
    "Status": ["Success", "Failed", "Running"],
    "Trigger": ["Auto", "Manual", "Auto"],
    "Timestamp": ["2025-06-29 14:00", "2025-06-29 13:00", "2025-06-29 12:45"]
})
st.dataframe(df, use_container_width=True)
