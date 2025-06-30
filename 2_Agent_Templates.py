import streamlit as st

st.title("📂 Agent Templates")

categories = ["Inventory", "Logistics", "Procurement", "Risk"]
selected = st.selectbox("Filter by Category", ["All"] + categories)

st.markdown("### Available Templates")
cols = st.columns(3)

templates = [
    ("Inventory Reorder Agent", "Alerts when stock < threshold."),
    ("Delayed Shipment Notifier", "Flags delayed deliveries."),
    ("Supplier Risk Evaluator", "Checks news for supplier risks.")
]

for i, (title, desc) in enumerate(templates):
    with cols[i % 3]:
        st.subheader(title)
        st.caption(desc)
        st.button("Use Template", key=title)
