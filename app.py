
import streamlit as st
from pathlib import Path
import os

# ---------- Page config ----------
st.set_page_config(page_title="Spectra Agent Builder", layout="wide")

# ---------- Sidebar ----------
logo_path = Path("assets/spectra_logo.png")
if logo_path.is_file():
    st.sidebar.image(str(logo_path), width=160)
else:
    st.sidebar.markdown("## Spectra")

st.sidebar.markdown("### AI Agent Builder for Supply Chain")

# Navigation
PAGES = ["Dashboard", "Agent Builder"]
page = st.sidebar.radio("Navigate", PAGES)

# Session init
if "agent_config" not in st.session_state:
    st.session_state.agent_config = {}

# ---------- Functions ----------
def safe_defaults(options_list, desired):
    return [x for x in desired if x in options_list]

def llm_suggest_tables(erp_type, goal):
    # Dummy LLM stub
    suggestions = {
        ("SAP", "delayed"): ["EKPO", "EKET", "LIPS"],
        ("JDE", "inventory"): ["F4101", "F4111"]
    }
    for (t,g), tables in suggestions.items():
        if t == erp_type and g in goal.lower():
            return tables
    # fallback generic
    return ["<Table1>", "<Table2>", "<Table3>"]

# ---------- Dashboard placeholder ----------
if page == "Dashboard":
    st.title("Dashboard Placeholder")

# ---------- Agent Builder ----------
if page == "Agent Builder":
    st.title("Build Agent From Scratch")

    # Step 1 - goal
    goal = st.text_input("Agent Goal", value=st.session_state.agent_config.get("goal", ""))
    if goal:
        st.session_state.agent_config["goal"] = goal

    # Step 2 - connect data sources
    st.subheader("Connect Data Sources")

    data_source = st.selectbox(
        "Select Data Source",
        ["", "ERP", "CSV Upload", "API", "Database"],
        index=0 if "source" not in st.session_state.agent_config else
              ["", "ERP", "CSV Upload", "API", "Database"].index(st.session_state.agent_config["source"])
    )

    st.session_state.agent_config["source"] = data_source

    if data_source == "ERP":
        erp_type = st.selectbox(
            "Select ERP System",
            ["", "SAP", "JDE", "Oracle", "NetSuite"],
            index=0 if "erp_type" not in st.session_state.agent_config else
                  ["", "SAP", "JDE", "Oracle", "NetSuite"].index(st.session_state.agent_config["erp_type"])
        )
        st.session_state.agent_config["erp_type"] = erp_type

        if erp_type and goal:
            if st.button("Identify ERP Tables for this Goal"):
                with st.spinner("Consulting LLM to identify tables..."):
                    try:
                        import openai
                        openai.api_key = os.getenv("OPENAI_API_KEY")
                        prompt = f"""You are an {erp_type} ERP expert. A supply chain agent needs to fulfill this goal:
{goal}
List the most relevant {erp_type} tables to query, as a bullet list of table names only."""
                        response = openai.ChatCompletion.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=100
                        )
                        table_text = response["choices"][0]["message"]["content"]
                        tables = [t.strip() for t in table_text.replace('-', '').splitlines() if t.strip()]
                    except Exception:
                        # fallback dummy suggestion
                        tables = llm_suggest_tables(erp_type, goal)
                st.success("Suggested Tables:")
                st.write(", ".join(tables))
                st.session_state.agent_config["tables"] = tables

    if st.button("Save Agent Config"):
        st.write(st.session_state.agent_config)
        st.success("Configuration saved. Proceed to next steps...")
