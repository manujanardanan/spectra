import streamlit as st

st.title("🛠️ Build a New Agent")

step = st.radio("Step", ["1. Define Goal", "2. Connect Data", "3. Configure Logic", "4. Output Actions"])

if step == "1. Define Goal":
    st.text_input("Agent Goal", placeholder="e.g., Alert for delayed shipments > 2 days")

elif step == "2. Connect Data":
    st.selectbox("Choose Data Source", ["ERP System", "CSV Upload", "API"])
    st.file_uploader("Upload sample CSV (optional)")

elif step == "3. Configure Logic":
    st.text_area("Agent Logic (Prompt to LLM)", height=200, placeholder="e.g., If delivery_date > ETA + 2 then flag...")

elif step == "4. Output Actions":
    st.multiselect("Choose Output Channels", ["Email", "Slack", "Webhook"])
    st.button("Preview & Save Agent")
