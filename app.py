import streamlit as st
import json
import pandas as pd
from datetime import datetime
import uuid

# Configure page
st.set_page_config(
    page_title="Supply Chain Agent Builder",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = []
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = None

# Agent templates for supply chain use cases
AGENT_TEMPLATES = {
    "Inventory Optimizer": {
        "description": "Optimizes inventory levels based on demand forecasting and stock data",
        "inputs": ["Current Stock Levels", "Historical Demand", "Lead Times", "Safety Stock Requirements"],
        "outputs": ["Reorder Points", "Optimal Order Quantities", "Stock Alerts"],
        "triggers": ["Low Stock Alert", "Demand Spike Detection", "Scheduled Review"],
        "actions": ["Generate Purchase Orders", "Send Alerts", "Update Inventory Records"]
    },
    "Supplier Performance Monitor": {
        "description": "Monitors and evaluates supplier performance metrics",
        "inputs": ["Delivery Times", "Quality Scores", "Cost Data", "Compliance Records"],
        "outputs": ["Performance Rankings", "Risk Assessments", "Improvement Recommendations"],
        "triggers": ["Performance Threshold Breach", "Quality Issue", "Contract Review"],
        "actions": ["Send Performance Reports", "Flag High-Risk Suppliers", "Schedule Reviews"]
    },
    "Demand Forecaster": {
        "description": "Predicts future demand using historical data and market trends",
        "inputs": ["Historical Sales", "Market Trends", "Seasonal Patterns", "External Factors"],
        "outputs": ["Demand Forecasts", "Confidence Intervals", "Trend Analysis"],
        "triggers": ["New Data Available", "Market Change", "Scheduled Forecast"],
        "actions": ["Update Forecasts", "Alert Planners", "Adjust Production Plans"]
    },
    "Logistics Optimizer": {
        "description": "Optimizes transportation and distribution routes",
        "inputs": ["Delivery Locations", "Vehicle Capacity", "Traffic Data", "Cost Constraints"],
        "outputs": ["Optimal Routes", "Cost Savings", "Delivery Schedules"],
        "triggers": ["New Orders", "Route Disruption", "Daily Planning"],
        "actions": ["Generate Route Plans", "Update Schedules", "Send Driver Instructions"]
    },
    "Risk Analyzer": {
        "description": "Identifies and assesses supply chain risks",
        "inputs": ["Supplier Data", "Market Conditions", "Geopolitical Events", "Financial Metrics"],
        "outputs": ["Risk Scores", "Mitigation Strategies", "Early Warnings"],
        "triggers": ["Risk Threshold Exceeded", "External Event", "Periodic Review"],
        "actions": ["Send Risk Alerts", "Recommend Actions", "Update Risk Register"]
    }
}

# Main header
st.title("🔗 Supply Chain Agent Builder")
st.markdown("*Build intelligent agents for your supply chain operations - no coding required*")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Agent Builder", "My Agents", "Templates", "Deploy"])

if page == "Agent Builder":
    st.header("🛠️ Build Your Agent")
    
    # Agent basic info
    col1, col2 = st.columns(2)
    
    with col1:
        agent_name = st.text_input("Agent Name", placeholder="e.g., My Inventory Manager")
        agent_type = st.selectbox("Agent Type", ["Custom"] + list(AGENT_TEMPLATES.keys()))
    
    with col2:
        agent_description = st.text_area("Description", placeholder="Describe what your agent does...")
        priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Critical"])
    
    # Use template if selected
    if agent_type != "Custom" and agent_type in AGENT_TEMPLATES:
        template = AGENT_TEMPLATES[agent_type]
        st.info(f"Using template: {template['description']}")
        
        # Pre-fill with template data
        default_inputs = template['inputs']
        default_outputs = template['outputs']
        default_triggers = template['triggers']
        default_actions = template['actions']
    else:
        default_inputs = []
        default_outputs = []
        default_triggers = []
        default_actions = []
    
    st.divider()
    
    # Agent configuration tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Inputs", "📤 Outputs", "⚡ Triggers", "🎯 Actions"])
    
    with tab1:
        st.subheader("Data Inputs")
        st.markdown("Define what data your agent needs to work with:")
        
        inputs = []
        for i in range(max(3, len(default_inputs))):
            default_val = default_inputs[i] if i < len(default_inputs) else ""
            input_name = st.text_input(f"Input {i+1}", value=default_val, key=f"input_{i}")
            if input_name:
                inputs.append(input_name)
        
        # Add more inputs button
        if st.button("+ Add More Inputs"):
            st.rerun()
    
    with tab2:
        st.subheader("Expected Outputs")
        st.markdown("Define what your agent will produce:")
        
        outputs = []
        for i in range(max(3, len(default_outputs))):
            default_val = default_outputs[i] if i < len(default_outputs) else ""
            output_name = st.text_input(f"Output {i+1}", value=default_val, key=f"output_{i}")
            if output_name:
                outputs.append(output_name)
    
    with tab3:
        st.subheader("Automation Triggers")
        st.markdown("Define when your agent should run:")
        
        triggers = []
        trigger_types = ["Time-based", "Event-based", "Threshold-based", "Manual"]
        
        for i in range(max(2, len(default_triggers))):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                trigger_type = st.selectbox(f"Trigger {i+1} Type", trigger_types, key=f"trigger_type_{i}")
            with col_b:
                default_val = default_triggers[i] if i < len(default_triggers) else ""
                trigger_desc = st.text_input(f"Trigger {i+1} Description", value=default_val, key=f"trigger_{i}")
            
            if trigger_desc:
                triggers.append({"type": trigger_type, "description": trigger_desc})
    
    with tab4:
        st.subheader("Actions & Responses")
        st.markdown("Define what actions your agent will take:")
        
        actions = []
        action_types = ["Send Alert", "Generate Report", "Update Database", "Create Order", "Send Email"]
        
        for i in range(max(2, len(default_actions))):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                action_type = st.selectbox(f"Action {i+1} Type", action_types, key=f"action_type_{i}")
            with col_b:
                default_val = default_actions[i] if i < len(default_actions) else ""
                action_desc = st.text_input(f"Action {i+1} Description", value=default_val, key=f"action_{i}")
            
            if action_desc:
                actions.append({"type": action_type, "description": action_desc})
    
    st.divider()
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            frequency = st.selectbox("Run Frequency", ["Real-time", "Hourly", "Daily", "Weekly", "Monthly"])
            timeout = st.number_input("Timeout (minutes)", min_value=1, max_value=60, value=5)
        
        with col2:
            retry_attempts = st.number_input("Retry Attempts", min_value=0, max_value=5, value=3)
            notification_email = st.text_input("Notification Email", placeholder="your.email@company.com")
    
    # Save agent
    if st.button("💾 Save Agent", type="primary"):
        if agent_name and inputs and outputs:
            agent = {
                "id": str(uuid.uuid4()),
                "name": agent_name,
                "type": agent_type,
                "description": agent_description,
                "priority": priority,
                "inputs": inputs,
                "outputs": outputs,
                "triggers": triggers,
                "actions": actions,
                "settings": {
                    "frequency": frequency,
                    "timeout": timeout,
                    "retry_attempts": retry_attempts,
                    "notification_email": notification_email
                },
                "created_at": datetime.now().isoformat(),
                "status": "Draft"
            }
            
            st.session_state.agents.append(agent)
            st.success(f"✅ Agent '{agent_name}' saved successfully!")
            st.balloons()
        else:
            st.error("❌ Please fill in at least the agent name, inputs, and outputs.")

elif page == "My Agents":
    st.header("📋 My Agents")
    
    if not st.session_state.agents:
        st.info("No agents created yet. Go to the Agent Builder to create your first agent!")
    else:
        # Display agents in a table
        agents_data = []
        for agent in st.session_state.agents:
            agents_data.append({
                "Name": agent["name"],
                "Type": agent["type"],
                "Priority": agent["priority"],
                "Status": agent["status"],
                "Created": agent["created_at"][:10],
                "Inputs": len(agent["inputs"]),
                "Outputs": len(agent["outputs"])
            })
        
        df = pd.DataFrame(agents_data)
        st.dataframe(df, use_container_width=True)
        
        # Agent details
        st.subheader("Agent Details")
        selected_agent = st.selectbox("Select an agent to view details:", 
                                    [agent["name"] for agent in st.session_state.agents])
        
        if selected_agent:
            agent = next(a for a in st.session_state.agents if a["name"] == selected_agent)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Description:** {agent['description']}")
                st.write(f"**Priority:** {agent['priority']}")
                st.write(f"**Status:** {agent['status']}")
                
                st.write("**Inputs:**")
                for inp in agent['inputs']:
                    st.write(f"• {inp}")
            
            with col2:
                st.write(f"**Frequency:** {agent['settings']['frequency']}")
                st.write(f"**Timeout:** {agent['settings']['timeout']} minutes")
                
                st.write("**Outputs:**")
                for out in agent['outputs']:
                    st.write(f"• {out}")
            
            # Actions
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("✏️ Edit Agent"):
                    st.info("Edit functionality would open the agent in builder mode")
            with col_b:
                if st.button("🚀 Deploy Agent"):
                    agent['status'] = "Deployed"
                    st.success("Agent deployed successfully!")
                    st.rerun()
            with col_c:
                if st.button("🗑️ Delete Agent"):
                    st.session_state.agents = [a for a in st.session_state.agents if a["name"] != selected_agent]
                    st.success("Agent deleted successfully!")
                    st.rerun()

elif page == "Templates":
    st.header("📋 Agent Templates")
    st.markdown("Choose from pre-built templates for common supply chain use cases:")
    
    for template_name, template_info in AGENT_TEMPLATES.items():
        with st.expander(f"🔧 {template_name}"):
            st.write(f"**Description:** {template_info['description']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Typical Inputs:**")
                for inp in template_info['inputs']:
                    st.write(f"• {inp}")
                
                st.write("**Expected Outputs:**")
                for out in template_info['outputs']:
                    st.write(f"• {out}")
            
            with col2:
                st.write("**Common Triggers:**")
                for trigger in template_info['triggers']:
                    st.write(f"• {trigger}")
                
                st.write("**Typical Actions:**")
                for action in template_info['actions']:
                    st.write(f"• {action}")
            
            if st.button(f"Use {template_name} Template", key=f"use_{template_name}"):
                st.info(f"Go to Agent Builder and select '{template_name}' from the Agent Type dropdown!")

elif page == "Deploy":
    st.header("🚀 Deployment Center")
    
    deployed_agents = [agent for agent in st.session_state.agents if agent.get("status") == "Deployed"]
    
    if not deployed_agents:
        st.info("No deployed agents yet. Deploy agents from the 'My Agents' page.")
    else:
        st.success(f"You have {len(deployed_agents)} deployed agent(s)")
        
        # Deployment status
        for agent in deployed_agents:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{agent['name']}** ({agent['type']})")
                    st.write(f"Priority: {agent['priority']} | Frequency: {agent['settings']['frequency']}")
                
                with col2:
                    st.metric("Status", "🟢 Active")
                
                with col3:
                    if st.button("⏸️ Pause", key=f"pause_{agent['id']}"):
                        st.info("Agent paused")
                
                st.divider()
        
        # Deployment metrics (simulated)
        st.subheader("📊 Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Executions", "1,247", "↗️ 12%")
        with col2:
            st.metric("Success Rate", "98.5%", "↗️ 0.3%")
        with col3:
            st.metric("Avg Response Time", "2.3s", "↘️ 0.5s")
        with col4:
            st.metric("Cost Savings", "$12,450", "↗️ $2,100")

# Footer
st.divider()
st.markdown("---")
st.markdown("**Supply Chain Agent Builder** - Empowering supply chain professionals with no-code AI automation")

# Export/Import functionality
with st.sidebar:
    st.divider()
    st.subheader("Data Management")
    
    if st.button("📥 Export Agents"):
        if st.session_state.agents:
            agents_json = json.dumps(st.session_state.agents, indent=2)
            st.download_button(
                label="Download JSON",
                data=agents_json,
                file_name=f"supply_chain_agents_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        else:
            st.warning("No agents to export")
    
    uploaded_file = st.file_uploader("📤 Import Agents", type="json")
    if uploaded_file:
        try:
            imported_agents = json.load(uploaded_file)
            st.session_state.agents.extend(imported_agents)
            st.success(f"Imported {len(imported_agents)} agents!")
            st.rerun()
        except Exception as e:
            st.error(f"Error importing agents: {e}")
