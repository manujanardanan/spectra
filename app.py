
import streamlit as st
from pathlib import Path

# ---------- Page config ----------
st.set_page_config(page_title="Spectra Agent Builder", layout="wide")

# ---------- Helper ----------
def _safe_defaults(options_list, desired_defaults):
    """Return only defaults that are present in the options_list."""
    return [item for item in desired_defaults if item in options_list]

# ---------- Sidebar ----------
logo_path = Path("assets/spectra_logo.png")
if logo_path.is_file():
    st.sidebar.image(str(logo_path), width=160)
else:
    st.sidebar.markdown("## Spectra")

st.sidebar.markdown("### AI Agent Builder for Supply Chain")

# Multipage links (make sure your pages/ folder exists with these files)
try:
    st.sidebar.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/2_Agent_Templates.py", label="📂 Templates")
    st.sidebar.page_link("pages/3_Agent_Builder.py", label="🛠️ Builder")
    st.sidebar.page_link("pages/4_Run_Monitoring.py", label="📈 Monitoring")
except KeyError:
    st.sidebar.info("Pages not found. Ensure files are in the pages/ directory.")

st.sidebar.divider()
st.sidebar.write("Logged in as **supply_chain_user@example.com**")

# ---------- Main (placeholder) ----------
st.title("Welcome to Spectra 👋")

# Example data for multiselect demo
DATABRICKS_FEATURES = {
    "data_sources": [
        "Delta Tables",
        "Streaming Data",
        "External APIs",
        "ERP Inventory Data",
        "POS Transactions"
    ],
    "ml_models": [
        "Prophet Forecast",
        "XGBoost ETA",
        "BERT Risk Classifier"
    ]
}

template = {
    "data_sources": ["ERP Inventory Data", "Non‑Existing Source"],
    "ml_models": ["XGBoost ETA", "Non‑Existing Model"]
}

agent_type = "Inventory"  # not "Custom" ⇒ will attempt defaults

# ----- Multiselect with safe defaults -----
st.subheader("Configure your agent")

selected_sources = st.multiselect(
    "Select Data Sources",
    DATABRICKS_FEATURES["data_sources"],
    default=_safe_defaults(
        DATABRICKS_FEATURES["data_sources"],
        template.get("data_sources", [])[:3] if agent_type != "Custom" else []
    )
)

selected_models = st.multiselect(
    "Select ML Models",
    DATABRICKS_FEATURES["ml_models"],
    default=_safe_defaults(
        DATABRICKS_FEATURES["ml_models"],
        template.get("ml_models", [])[:2] if agent_type != "Custom" else []
    )
)

st.write("**Chosen data sources:**", selected_sources)
st.write("**Chosen ML models:**", selected_models)
