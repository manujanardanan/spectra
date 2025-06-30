import streamlit as st
import pandas as pd

st.title("📈 Agent Run Monitoring")

st.markdown("### Recent Executions")

df = pd.DataFrame({
    "Agent": ["Inventory Watcher", "Delay Notifier"],
    "Status": ["Success", "Failed"],
    "Trigger": ["Auto", "Manual"],
    "Latency (ms)": [320, 890],
    "Timestamp": ["2025-06-29 14:00", "2025-06-29 13:00"]
})
st.dataframe(df, use_container_width=True)

selected = st.selectbox("Select an Agent to View Logs", df["Agent"])
if selected:
    st.markdown(f"#### Logs for {selected}")
    st.code(f"[INFO] Agent started\n[INFO] Checking thresholds...\n[INFO] {selected} completed.", language="bash")
