import streamlit as st

st.set_page_config(page_title="Spectra Agent Builder", layout="wide")

# Sidebar logo
from pathlib import Path
import streamlit as st

logo_path = Path("assets/spectra_logo.png")

# Safely skip logo if not present
if logo_path.is_file():
    st.sidebar.image(str(logo_path), width=160)
else:
    st.sidebar.markdown("## Spectra")  # fallback text logo or leave blank
st.sidebar.title("Spectra")
st.sidebar.markdown("### AI Agent Builder for Supply Chain")

st.sidebar.markdown("---")
st.sidebar.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
st.sidebar.page_link("pages/2_Agent_Templates.py", label="📂 Agent Templates")
st.sidebar.page_link("pages/3_Agent_Builder.py", label="🛠️ Build Agent")
st.sidebar.page_link("pages/4_Run_Monitoring.py", label="📈 Monitoring")
st.sidebar.markdown("---")
st.sidebar.markdown("👤 Logged in as: `supply_chain_user@example.com`")
