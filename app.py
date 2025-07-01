import streamlit as st
import time
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Spectra - Supply Chain Agent Builder",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .template-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
        border: none;
    }
    
    .capability-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 0.5rem;
    }
    
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'welcome'
if 'agent_config' not in st.session_state:
    st.session_state.agent_config = {}
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None

# Templates data
templates = {
    'demand-forecasting': {
        'name': 'Demand Forecasting Agent',
        'description': 'Predicts future demand using historical sales data, market trends, and external factors.',
        'icon': '📈',
        'features': ['Time series analysis', 'Seasonal decomposition', 'External factor integration']
    },
    'inventory-optimization': {
        'name': 'Inventory Optimization Agent', 
        'description': 'Optimizes inventory levels across multiple locations to minimize costs while maintaining service levels.',
        'icon': '📦',
        'features': ['Multi-echelon optimization', 'Safety stock calculation', 'Reorder point optimization']
    },
    'supplier-risk': {
        'name': 'Supplier Risk Assessment Agent',
        'description': 'Monitors supplier performance and provides early warning for potential supply disruptions.',
        'icon': '⚠️', 
        'features': ['Financial health monitoring', 'Performance scoring', 'Risk alerts & recommendations']
    },
    'logistics-optimization': {
        'name': 'Logistics Optimization Agent',
        'description': 'Optimizes transportation routes, delivery schedules, and warehouse operations.',
        'icon': '🚚',
        'features': ['Route optimization', 'Load planning', 'Delivery scheduling']
    }
}

def show_welcome():
    st.markdown("""
    <div class="main-header">
        <h1>🌟 Welcome to Spectra</h1>
        <p style="font-size: 1.2rem; margin-bottom: 0;">Build powerful supply chain agents without code. Connect your data, choose capabilities, and deploy intelligent automation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🤖 Pre-built Templates")
        st.write("Start with industry-proven agent templates for common supply chain scenarios")
        
    with col2:
        st.markdown("### 🔧 Custom Builder")
        st.write("Create tailored agents from scratch with our intuitive interface")
        
    with col3:
        st.markdown("### 📊 Databricks Integration")
        st.write("Seamlessly connect to your Databricks data pipelines and lakehouse architecture")
        
    with col4:
        st.markdown("### ⚡ Real-time Insights")
        st.write("Get instant visibility into your supply chain operations with AI-powered analytics")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started", key="get_started", type="primary"):
            st.session_state.current_step = 'templates'
            st.rerun()

def show_templates():
    st.markdown("# Select an Agent Template")
    st.markdown("Choose from our pre-built templates or create a custom agent from scratch.")
    
    # Databricks connection status
    st.sidebar.markdown("""
    ### 🔗 Databricks Connected
    Your lakehouse is ready for agent deployment
    """)
    
    # Template selection
    cols = st.columns(2)
    
    for i, (template_id, template) in enumerate(templates.items()):
        col = cols[i % 2]
        with col:
            with st.container():
                st.markdown(f"""
                <div class="template-card">
                    <h3>{template['icon']} {template['name']}</h3>
                    <p>{template['description']}</p>
                    <ul>
                        {''.join([f'<li>{feature}</li>' for feature in template['features']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select {template['name']}", key=f"select_{template_id}"):
                    st.session_state.selected_template = template_id
                    st.session_state.agent_config = {
                        'name': template['name'],
                        'description': template['description'],
                        'category': template_id.replace('-', '_')
                    }
                    st.session_state.current_step = 'configure'
                    st.rerun()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🛠️ Build from Scratch", key="custom_build", type="secondary"):
            st.session_state.selected_template = 'custom'
            st.session_state.agent_config = {}
            st.session_state.current_step = 'configure'
            st.rerun()

def show_configure():
    st.markdown("# Configure Your Agent")
    
    # Progress indicator
    progress_value = 0.33
    st.progress(progress_value, text="Step 1 of 3: Basic Configuration")
    
    # Basic Info Form
    with st.form("agent_config_form"):
        st.markdown("### Basic Information")
        
        agent_name = st.text_input(
            "Agent Name", 
            value=st.session_state.agent_config.get('name', ''),
            placeholder="Enter agent name"
        )
        
        agent_description = st.text_area(
            "Description",
            value=st.session_state.agent_config.get('description', ''),
            placeholder="Describe what this agent will do"
        )
        
        categories = ['', 'forecasting', 'inventory', 'procurement', 'logistics', 'quality', 'risk']
        current_cat = st.session_state.agent_config.get('category', '')
        try:
            default_idx = categories.index(current_cat)
        except ValueError:
            default_idx = 0

        agent_category = st.selectbox(
            'Category',
            options=categories,
            format_func=lambda x: {
                '': 'Select category',
                'forecasting': 'Demand Forecasting',
                'inventory': 'Inventory Management',
                'procurement': 'Procurement',
                'logistics': 'Logistics & Transportation',
                'quality': 'Quality Management',
                'risk': 'Risk Management'
            }.get(x, x),
            index=default_idx
        )
        
        submitted = st.form_submit_button("Next: Data Sources", type="primary")
        
        if submitted:
            if agent_name and agent_description and agent_category:
                st.session_state.agent_config.update({
                    'name': agent_name,
                    'description': agent_description,
                    'category': agent_category
                })
                st.session_state.current_step = 'data_sources'
                st.rerun()
            else:
                st.error("Please fill in all required fields")

def show_data_sources():
    st.markdown("# Connect Data Sources")
    st.markdown("Select the data sources your agent will use. All sources connect through your Databricks lakehouse.")
    
    # Progress indicator
    progress_value = 0.66
    st.progress(progress_value, text="Step 2 of 3: Data Sources")
    
    # Data source selection
    st.markdown("### Available Data Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        databricks_tables = st.checkbox("🔷 Databricks Tables", help="Connect to existing tables")
        api_connectors = st.checkbox("🔌 API Connectors", help="REST APIs, databases")
        
    with col2:
        file_uploads = st.checkbox("📁 File Uploads", help="CSV, Excel, JSON files")
        streaming_data = st.checkbox("⚡ Real-time Streams", help="Kafka, event hubs")
    
    selected_sources = []
    if databricks_tables:
        selected_sources.append("Databricks Tables")
    if file_uploads:
        selected_sources.append("File Uploads")
    if api_connectors:
        selected_sources.append("API Connectors")
    if streaming_data:
        selected_sources.append("Real-time Streams")
    
    if selected_sources:
        st.success(f"Selected sources: {', '.join(selected_sources)}")
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous", key="prev_data"):
            st.session_state.current_step = 'configure' 
            st.rerun()
    
    with col2:
        if st.button("Next: Capabilities →", key="next_capabilities", type="primary"):
            if selected_sources:
                st.session_state.agent_config['data_sources'] = selected_sources
                st.session_state.current_step = 'capabilities'
                st.rerun()
            else:
                st.error("Please select at least one data source")

def show_capabilities():
    st.markdown("# Select Agent Capabilities")
    st.markdown("Choose the AI capabilities your agent will have. You can select multiple capabilities.")
    
    # Progress indicator  
    progress_value = 1.0
    st.progress(progress_value, text="Step 3 of 3: Capabilities")
    
    # Capabilities selection
    capabilities = {
        'forecasting': {
            'name': '📈 Predictive Analytics',
            'description': 'Time series forecasting, trend analysis, and demand prediction using advanced ML models.'
        },
        'optimization': {
            'name': '⚙️ Optimization', 
            'description': 'Mathematical optimization for inventory, routing, and resource allocation problems.'
        },
        'anomaly': {
            'name': '🔍 Anomaly Detection',
            'description': 'Identify unusual patterns, outliers, and potential issues in your supply chain data.'
        },
        'nlp': {
            'name': '💬 Natural Language Processing',
            'description': 'Process text data, extract insights from documents, and enable conversational interfaces.'
        },
        'alerts': {
            'name': '🚨 Smart Alerts',
            'description': 'Intelligent notification system that learns from your responses and priorities.'
        },
        'recommendations': {
            'name': '💡 Recommendations',
            'description': 'AI-powered suggestions for actions, optimizations, and strategic decisions.'
        }
    }
    
    selected_capabilities = []
    
    for cap_id, cap_info in capabilities.items():
        if st.checkbox(cap_info['name'], key=f"cap_{cap_id}"):
            selected_capabilities.append(cap_info['name'])
            st.markdown(f"<div class='capability-card'>{cap_info['description']}</div>", unsafe_allow_html=True)
    
    if selected_capabilities:
        st.success(f"Selected capabilities: {', '.join(selected_capabilities)}")
    
    # Navigation and Deploy
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Previous", key="prev_capabilities"):
            st.session_state.current_step = 'data_sources'
            st.rerun()
    
    with col2:
        if st.button("🚀 Deploy Agent", key="deploy", type="primary"):
            if selected_capabilities:
                st.session_state.agent_config['capabilities'] = selected_capabilities
                deploy_agent()
            else:
                st.error("Please select at least one capability")

def deploy_agent():
    st.markdown("# Deploying Your Agent")
    
    # Show agent summary
    config = st.session_state.agent_config
    
    st.markdown("### Agent Summary")
    st.json({
        "Name": config.get('name', 'N/A'),
        "Category": config.get('category', 'N/A'),
        "Data Sources": config.get('data_sources', []),
        "Capabilities": config.get('capabilities', [])
    })
    
    # Simulate deployment
    progress_bar = st.progress(0, text="Initializing deployment...")
    
    for i in range(100):
        time.sleep(0.02)  # Simulate deployment time
        progress_bar.progress(i + 1, 
            text=f"Deploying to Databricks... {i + 1}%")
    
    # Success message
    st.markdown("""
    <div class="success-box">
        <h3>✅ Agent Deployed Successfully!</h3>
        <p>Your agent is now running in your Databricks environment and ready to process data.</p>
        
        <h4>Next Steps:</h4>
        <ul>
            <li>Monitor agent performance in the dashboard</li>
            <li>Configure alerts and notifications</li>
            <li>Review initial results and optimize settings</li>
            <li>Scale deployment to additional data sources</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Return to Home", key="return_home"):
        # Reset session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.current_step = 'welcome'
        st.rerun()

# Main app routing
def main():
    # Sidebar navigation
    st.sidebar.markdown("## Navigation")
    if st.sidebar.button("🏠 Home"):
        st.session_state.current_step = 'welcome'
        st.rerun()
    if st.sidebar.button("📊 Dashboard"):
        st.info("Dashboard view would be implemented here")
    if st.sidebar.button("🤖 My Agents"):
        st.info("My Agents view would be implemented here")
    
    # Route to current step
    if st.session_state.current_step == 'welcome':
        show_welcome()
    elif st.session_state.current_step == 'templates':
        show_templates()
    elif st.session_state.current_step == 'configure':
        show_configure()
    elif st.session_state.current_step == 'data_sources':
        show_data_sources()
    elif st.session_state.current_step == 'capabilities':
        show_capabilities()

if __name__ == "__main__":
    main()
