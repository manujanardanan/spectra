import streamlit as st
import json
import pandas as pd
from datetime import datetime
import uuid
import numpy as np

# Configure page
st.set_page_config(
    page_title="Supply Chain Agent Builder - Databricks Powered",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = []
if 'databricks_connected' not in st.session_state:
    st.session_state.databricks_connected = False
if 'data_sources' not in st.session_state:
    st.session_state.data_sources = []

# Databricks-specific configurations
DATABRICKS_FEATURES = {
    "data_sources": [
        "Delta Tables", "Streaming Data", "External APIs", "File Uploads", 
        "Database Connections", "IoT Sensors", "ERP Systems"
    ],
    "ml_models": [
        "Demand Forecasting (AutoML)", "Inventory Optimization", "Risk Prediction",
        "Supplier Scoring", "Route Optimization", "Quality Prediction"
    ],
    "compute_clusters": [
        "Single Node (Development)", "Multi-Node (Production)", 
        "Serverless (Auto-scaling)", "GPU Cluster (Deep Learning)"
    ],
    "deployment_options": [
        "Databricks Jobs", "MLflow Model Serving", "Delta Live Tables",
        "Databricks SQL Endpoints", "REST API Endpoints"
    ]
}


# Helper to safely pre-select only valid defaults in multiselect
def _safe_defaults(options_list, desired_defaults):
    return [item for item in desired_defaults if item in options_list]


# Enhanced agent templates with Databricks capabilities
AGENT_TEMPLATES = {
    "Intelligent Inventory Optimizer": {
        "description": "AI-powered inventory optimization using Databricks MLflow and Delta Lake",
        "databricks_features": ["Delta Lake", "MLflow", "AutoML", "Streaming"],
        "data_sources": ["ERP Inventory Data", "POS Transactions", "Weather Data", "Market Trends"],
        "ml_models": ["Demand Forecasting", "Safety Stock Calculation", "Reorder Point Optimization"],
        "inputs": ["Current Stock Levels", "Historical Demand", "Lead Times", "External Factors"],
        "outputs": ["Reorder Points", "Optimal Order Quantities", "Stock Alerts", "Cost Savings"],
        "triggers": ["Low Stock Alert", "Demand Spike Detection", "Scheduled Review"],
        "actions": ["Generate Purchase Orders", "Send Alerts", "Update Delta Tables"],
        "deployment": "Delta Live Tables + MLflow Serving"
    },
    "Real-time Supplier Performance Monitor": {
        "description": "Monitor supplier KPIs using Databricks streaming and real-time dashboards",
        "databricks_features": ["Structured Streaming", "Databricks SQL", "Unity Catalog"],
        "data_sources": ["Supplier APIs", "Delivery Tracking", "Quality Reports", "Financial Data"],
        "ml_models": ["Supplier Risk Scoring", "Performance Prediction", "Anomaly Detection"],
        "inputs": ["Delivery Times", "Quality Scores", "Cost Data", "Compliance Records"],
        "outputs": ["Performance Dashboards", "Risk Scores", "SLA Compliance", "Recommendations"],
        "triggers": ["Real-time Data Updates", "Threshold Breaches", "Contract Reviews"],
        "actions": ["Update Scorecards", "Send Alerts", "Generate Reports"],
        "deployment": "Databricks SQL + Streaming Jobs"
    },
    "Advanced Demand Forecaster": {
        "description": "Multi-horizon demand forecasting using Databricks AutoML and external data",
        "databricks_features": ["AutoML", "Feature Store", "Model Registry"],
        "data_sources": ["Sales History", "Market Data", "Weather", "Economic Indicators", "Social Media"],
        "ml_models": ["Prophet", "ARIMA", "Neural Networks", "Ensemble Models"],
        "inputs": ["Historical Sales", "Market Trends", "Seasonal Patterns", "External Factors"],
        "outputs": ["Short/Medium/Long-term Forecasts", "Confidence Intervals", "Feature Importance"],
        "triggers": ["New Data Available", "Model Retraining Schedule", "Accuracy Degradation"],
        "actions": ["Update Forecasts", "Retrain Models", "Alert Planners"],
        "deployment": "AutoML + Model Serving"
    },
    "Intelligent Logistics Optimizer": {
        "description": "AI-powered route optimization with real-time traffic and constraint handling",
        "databricks_features": ["Spark GraphX", "Geospatial Analytics", "Real-time Streaming"],
        "data_sources": ["GPS Data", "Traffic APIs", "Vehicle Telemetrics", "Delivery Constraints"],
        "ml_models": ["Route Optimization", "Delivery Time Prediction", "Cost Modeling"],
        "inputs": ["Delivery Locations", "Vehicle Capacity", "Traffic Data", "Time Windows"],
        "outputs": ["Optimal Routes", "ETAs", "Cost Analysis", "Driver Instructions"],
        "triggers": ["New Orders", "Traffic Updates", "Vehicle Breakdowns"],
        "actions": ["Update Routes", "Send Driver Notifications", "Track Performance"],
        "deployment": "Databricks Jobs + REST APIs"
    },
    "Comprehensive Risk Analyzer": {
        "description": "Enterprise risk management using Databricks Lakehouse and external data sources",
        "databricks_features": ["Delta Sharing", "Unity Catalog", "Databricks SQL"],
        "data_sources": ["Supplier Data", "News Feeds", "Financial Markets", "Weather", "Geopolitical"],
        "ml_models": ["Risk Scoring", "Event Impact Prediction", "Scenario Analysis"],
        "inputs": ["Supplier Networks", "Market Conditions", "News Sentiment", "Financial Metrics"],
        "outputs": ["Risk Heatmaps", "Impact Assessments", "Mitigation Plans", "Early Warnings"],
        "triggers": ["Risk Score Changes", "External Events", "Threshold Breaches"],
        "actions": ["Risk Alerts", "Escalation Workflows", "Dashboard Updates"],
        "deployment": "Delta Live Tables + Databricks SQL"
    }
}

# Main header with Databricks branding
st.title("🔗 Supply Chain Agent Builder")
st.markdown("*Powered by Databricks Data Intelligence Platform*")

# Connection status indicator
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("*Build intelligent agents for your supply chain operations - leveraging enterprise-grade AI/ML*")
with col2:
    if st.session_state.databricks_connected:
        st.success("🟢 Databricks Connected")
    else:
        st.warning("🟡 Demo Mode")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Agent Builder", "My Agents", "Data Sources", "Models & Deployment", "Analytics"])

# Databricks connection setup
with st.sidebar.expander("⚙️ Databricks Configuration"):
    workspace_url = st.text_input("Workspace URL", placeholder="https://your-workspace.databricks.com")
    access_token = st.text_input("Access Token", type="password", placeholder="Your access token")
    catalog_name = st.text_input("Unity Catalog", placeholder="supply_chain_catalog")
    
    if st.button("Connect to Databricks"):
        if workspace_url and access_token:
            st.session_state.databricks_connected = True
            st.success("Connected successfully!")
            st.rerun()
        else:
            st.error("Please provide workspace URL and token")

if page == "Agent Builder":
    st.header("🛠️ Build Your Databricks-Powered Agent")
    
    # Enhanced agent basic info
    col1, col2 = st.columns(2)
    
    with col1:
        agent_name = st.text_input("Agent Name", placeholder="e.g., AI Inventory Optimizer")
        agent_type = st.selectbox("Agent Template", ["Custom"] + list(AGENT_TEMPLATES.keys()))
    
    with col2:
        compute_type = st.selectbox("Compute Cluster", DATABRICKS_FEATURES["compute_clusters"])
        deployment_type = st.selectbox("Deployment Option", DATABRICKS_FEATURES["deployment_options"])
    
    agent_description = st.text_area("Description", placeholder="Describe your agent's AI capabilities...")
    
    # Show template info if selected
    if agent_type != "Custom" and agent_type in AGENT_TEMPLATES:
        template = AGENT_TEMPLATES[agent_type]
        
        with st.expander("📋 Template Details", expanded=True):
            st.info(f"**Description:** {template['description']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Databricks Features:**")
                for feature in template['databricks_features']:
                    st.write(f"• ✅ {feature}")
                
                st.write("**ML Models:**")
                for model in template['ml_models']:
                    st.write(f"• 🤖 {model}")
            
            with col_b:
                st.write("**Data Sources:**")
                for source in template['data_sources']:
                    st.write(f"• 📊 {source}")
                
                st.write(f"**Recommended Deployment:** {template['deployment']}")
    
    st.divider()
    
    # Enhanced configuration tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Data Pipeline", "🤖 AI/ML Models", "⚡ Triggers", "🎯 Actions", "🚀 Deployment"])
    
    with tab1:
        st.subheader("Data Pipeline Configuration")
        st.markdown("*Configure your data sources and Delta Lake tables*")
        
        # Data sources selection
        # Data sources selection
        selected_sources = st.multiselect(
            "Select Data Sources",
            DATABRICKS_FEATURES["data_sources"],
            default=_safe_defaults(
                DATABRICKS_FEATURES["data_sources"],
                template.get('data_sources', [])[:3] if agent_type != "Custom" else []
            )
        )
        )
        
        # Delta Lake configuration
        st.write("**Delta Lake Tables:**")
        col_a, col_b = st.columns(2)
        with col_a:
            source_table = st.text_input("Source Table", placeholder="supply_chain.raw_data")
            target_table = st.text_input("Target Table", placeholder="supply_chain.processed_data")
        with col_b:
            streaming_enabled = st.checkbox("Enable Streaming", value=True)
            schema_evolution = st.checkbox("Auto Schema Evolution", value=True)
    
    with tab2:
        st.subheader("AI/ML Model Configuration")
        st.markdown("*Configure your machine learning models and AutoML*")
        
        # Model selection
        selected_models = st.multiselect(
            "Select ML Models",
            DATABRICKS_FEATURES["ml_models"],
            default=_safe_defaults(
                DATABRICKS_FEATURES["ml_models"],
                template.get('ml_models', [])[:2] if agent_type != "Custom" else []
            )
        )
        )
        
        # Model configuration
        col_a, col_b = st.columns(2)
        with col_a:
            automl_enabled = st.checkbox("Use AutoML", value=True)
            model_registry = st.text_input("Model Registry Path", placeholder="supply_chain.models")
        with col_b:
            retraining_frequency = st.selectbox("Retraining Schedule", 
                                              ["Weekly", "Monthly", "Quarterly", "On-Demand"])
            performance_threshold = st.slider("Min Model Accuracy", 0.7, 0.99, 0.85)
    
    with tab3:
        st.subheader("Intelligent Triggers")
        st.markdown("*Configure when your agent should execute*")
        
        trigger_options = [
            "Delta Live Tables Change", "Streaming Data Threshold", "Model Performance Drop",
            "Scheduled Job", "API Webhook", "Manual Trigger"
        ]
        
        triggers = []
        for i in range(3):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                trigger_type = st.selectbox(f"Trigger {i+1}", trigger_options, key=f"trigger_type_{i}")
            with col_b:
                trigger_config = st.text_input(f"Configuration", 
                                             placeholder="e.g., threshold > 100 or schedule: 0 8 * * *",
                                             key=f"trigger_config_{i}")
            
            if trigger_config:
                triggers.append({"type": trigger_type, "config": trigger_config})
    
    with tab4:
        st.subheader("Intelligent Actions")
        st.markdown("*Define what your agent will do with AI insights*")
        
        action_options = [
            "Update Delta Table", "Send Databricks Alert", "Trigger Workflow", 
            "Call External API", "Generate Report", "Invoke Model Serving"
        ]
        
        actions = []
        for i in range(3):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                action_type = st.selectbox(f"Action {i+1}", action_options, key=f"action_type_{i}")
            with col_b:
                action_config = st.text_input(f"Configuration",
                                            placeholder="e.g., table: supply_chain.alerts",
                                            key=f"action_config_{i}")
            
            if action_config:
                actions.append({"type": action_type, "config": action_config})
    
    with tab5:
        st.subheader("Databricks Deployment")
        st.markdown("*Configure how your agent will be deployed and scaled*")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Compute Configuration:**")
            node_type = st.selectbox("Node Type", 
                                   ["i3.xlarge", "i3.2xlarge", "r5.xlarge", "c5.2xlarge"])
            min_workers = st.number_input("Min Workers", 1, 10, 1)
            max_workers = st.number_input("Max Workers", 1, 100, 5)
            
        with col_b:
            st.write("**Advanced Settings:**")
            unity_catalog = st.checkbox("Use Unity Catalog", value=True)
            photon_enabled = st.checkbox("Enable Photon", value=True)
            cost_optimization = st.checkbox("Auto-terminate", value=True)
    
    # Save agent with Databricks configuration
    if st.button("💾 Deploy Agent to Databricks", type="primary"):
        if agent_name and selected_sources:
            agent = {
                "id": str(uuid.uuid4()),
                "name": agent_name,
                "type": agent_type,
                "description": agent_description,
                "databricks_config": {
                    "compute_type": compute_type,
                    "deployment_type": deployment_type,
                    "node_type": node_type,
                    "min_workers": min_workers,
                    "max_workers": max_workers,
                    "photon_enabled": photon_enabled,
                    "unity_catalog": unity_catalog
                },
                "data_pipeline": {
                    "sources": selected_sources,
                    "source_table": source_table,
                    "target_table": target_table,
                    "streaming_enabled": streaming_enabled
                },
                "ml_config": {
                    "models": selected_models,
                    "automl_enabled": automl_enabled,
                    "retraining_frequency": retraining_frequency,
                    "performance_threshold": performance_threshold
                },
                "triggers": triggers,
                "actions": actions,
                "created_at": datetime.now().isoformat(),
                "status": "Deployed to Databricks"
            }
            
            st.session_state.agents.append(agent)
            st.success(f"✅ Agent '{agent_name}' deployed to Databricks successfully!")
            st.balloons()
            
            # Show deployment details
            with st.expander("🚀 Deployment Details"):
                st.code(f"""
# Databricks Job Configuration Generated:
{json.dumps(agent['databricks_config'], indent=2)}

# Next Steps:
1. Agent deployed to {deployment_type}
2. Compute cluster: {compute_type}
3. Auto-scaling: {min_workers}-{max_workers} workers
4. Photon acceleration: {'Enabled' if photon_enabled else 'Disabled'}
                """)
        else:
            st.error("❌ Please provide agent name and select at least one data source.")

elif page == "My Agents":
    st.header("📋 My Databricks Agents")
    
    if not st.session_state.agents:
        st.info("No agents deployed yet. Go to the Agent Builder to create your first Databricks-powered agent!")
    else:
        # Enhanced agents table with Databricks metrics
        agents_data = []
        for agent in st.session_state.agents:
            agents_data.append({
                "Name": agent["name"],
                "Type": agent["type"],
                "Status": agent["status"],
                "Compute": agent.get("databricks_config", {}).get("compute_type", "N/A"),
                "Models": len(agent.get("ml_config", {}).get("models", [])),
                "Data Sources": len(agent.get("data_pipeline", {}).get("sources", [])),
                "Created": agent["created_at"][:10]
            })
        
        df = pd.DataFrame(agents_data)
        st.dataframe(df, use_container_width=True)
        
        # Databricks performance metrics (simulated)
        st.subheader("🎯 Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("DBUs Consumed", "2,847", "↗️ 12%")
        with col2:
            st.metric("Model Accuracy", "94.2%", "↗️ 2.1%")
        with col3:
            st.metric("Data Processed", "847 GB", "↗️ 156 GB")
        with col4:
            st.metric("Cost Savings", "$45,200", "↗️ $8,400")
        
        # Visualizations using Streamlit native charts
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Agent performance chart
            dates = pd.date_range('2024-01-01', periods=30, freq='D')
            performance_data = pd.DataFrame({
                'Date': dates,
                'Accuracy': [0.85 + (i * 0.003) + (i % 7) * 0.01 for i in range(30)],
                'Latency': [2.5 - (i * 0.02) + (i % 5) * 0.1 for i in range(30)]
            })
            
            st.subheader("Model Performance Over Time")
            st.line_chart(performance_data.set_index('Date')['Accuracy'])
        
        with col_b:
            # Resource utilization
            resource_data = pd.DataFrame({
                'Resource': ['CPU', 'Memory', 'Storage', 'Network'],
                'Utilization': [75, 60, 45, 30]
            })
            
            st.subheader("Cluster Resource Utilization (%)")
            st.bar_chart(resource_data.set_index('Resource'))

elif page == "Data Sources":
    st.header("📊 Data Source Management")
    st.markdown("*Manage your Databricks data sources and Delta Lake tables*")
    
    # Mock data sources with Databricks context
    data_sources = [
        {"name": "ERP_Inventory", "type": "Delta Table", "status": "Active", "size": "2.4 TB"},
        {"name": "Supplier_API_Stream", "type": "Streaming", "status": "Running", "rate": "1.2K/sec"},
        {"name": "Market_Data_Feed", "type": "External API", "status": "Connected", "latency": "45ms"},
        {"name": "IoT_Sensors", "type": "Kafka Stream", "status": "Active", "events": "5K/min"}
    ]
    
    df_sources = pd.DataFrame(data_sources)
    st.dataframe(df_sources, use_container_width=True)
    
    # Data lineage visualization
    st.subheader("🔄 Data Lineage")
    st.info("Visual representation of your data flow through Delta Lake would appear here")
    
    # Add new data source
    with st.expander("➕ Add New Data Source"):
        col1, col2 = st.columns(2)
        with col1:
            source_name = st.text_input("Data Source Name")
            source_type = st.selectbox("Source Type", DATABRICKS_FEATURES["data_sources"])
        with col2:
            connection_string = st.text_input("Connection String")
            refresh_rate = st.selectbox("Refresh Rate", ["Real-time", "Hourly", "Daily"])
        
        if st.button("Add Data Source"):
            st.success("Data source configuration saved!")

elif page == "Models & Deployment":
    st.header("🤖 ML Models & Deployment")
    st.markdown("*Manage your MLflow models and deployment endpoints*")
    
    # Model registry view
    st.subheader("📚 Model Registry")
    
    models_data = [
        {"name": "demand_forecaster_v2", "stage": "Production", "accuracy": "94.2%", "version": "2.1"},
        {"name": "inventory_optimizer", "stage": "Staging", "accuracy": "91.8%", "version": "1.5"},
        {"name": "supplier_risk_scorer", "stage": "Development", "accuracy": "88.4%", "version": "0.9"}
    ]
    
    df_models = pd.DataFrame(models_data)
    st.dataframe(df_models, use_container_width=True)
    
    # Model serving endpoints
    st.subheader("🚀 Serving Endpoints")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Endpoints", "3", "↗️ 1")
        st.metric("Requests/Hour", "12.4K", "↗️ 2.1K")
    with col2:
        st.metric("Avg Latency", "45ms", "↘️ 5ms")
        st.metric("Success Rate", "99.7%", "↗️ 0.2%")

elif page == "Analytics":
    st.header("📈 Supply Chain Analytics")
    st.markdown("*Powered by Databricks SQL and real-time dashboards*")
    
    # Create sample analytics using Streamlit native charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Inventory levels over time
        st.subheader("Inventory Value Trend")
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        inventory_data = pd.DataFrame({
            'Date': dates,
            'Inventory_Value': [1000000 + i*5000 + (i%7)*20000 for i in range(30)],
            'Stock_Outs': [max(0, 5 - (i%10)) for i in range(30)]
        })
        
        st.line_chart(inventory_data.set_index('Date')['Inventory_Value'])
    
    with col2:
        # Supplier performance
        st.subheader("Supplier Performance Scores")
        supplier_data = pd.DataFrame({
            'Supplier': ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D'],
            'Performance_Score': [95, 87, 92, 78],
            'Risk_Level': ['Low', 'Medium', 'Low', 'High']
        })
        
        st.bar_chart(supplier_data.set_index('Supplier')['Performance_Score'])
    
    # Real-time KPIs
    st.subheader("⚡ Real-time KPIs")
    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        st.metric("Order Fill Rate", "97.8%", "↗️ 1.2%")
    with col_b:
        st.metric("Avg Lead Time", "4.2 days", "↘️ 0.3 days")
    with col_c:
        st.metric("Inventory Turnover", "8.4x", "↗️ 0.6x")
    with col_d:
        st.metric("Supply Chain Cost", "$2.4M", "↘️ $150K")

# Footer
st.divider()
st.markdown("---")
st.markdown("**Supply Chain Agent Builder** - Powered by Databricks Data Intelligence Platform")
st.markdown("*Enterprise-grade AI/ML • Real-time Analytics • Unified Data Governance*")

# Enhanced sidebar features
with st.sidebar:
    st.divider()
    st.subheader("🎯 Quick Actions")
    
    if st.button("📊 View Unity Catalog"):
        st.info("Unity Catalog browser would open here")
    
    if st.button("🔧 Cluster Manager"):
        st.info("Databricks cluster management interface")
    
    if st.button("📈 SQL Analytics"):
        st.info("Databricks SQL workspace")
    
    # Export configuration
    st.divider()
    st.subheader("💾 Configuration")
    
    if st.button("📥 Export to Databricks"):
        if st.session_state.agents:
            config = {
                "agents": st.session_state.agents,
                "databricks_config": {
                    "workspace_url": workspace_url,
                    "catalog": catalog_name
                }
            }
            st.download_button(
                label="Download Databricks Config",
                data=json.dumps(config, indent=2),
                file_name=f"databricks_agents_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
