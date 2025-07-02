import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import json
from io import StringIO
import base64
from streamlit_option_menu import option_menu
from streamlit_chat import message
from data_agents import DataAnalysisAgent, VisualizationAgent, MLInsightsAgent, FileAnalysisAgent
from utils import load_sample_data, format_response, save_chat_history

# Page configuration
st.set_page_config(
    page_title="Data Agents Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        margin: 5px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

def main():
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Data Agents Chat Interface</h1>', unsafe_allow_html=True)
    
    # Sidebar for agent selection and configuration
    with st.sidebar:
        st.markdown("## 🔧 Configuration")
        
        # Agent selection
        agent_type = option_menu(
            "Choose Your Data Agent",
            ["Data Analysis", "Visualization", "ML Insights", "File Analysis"],
            icons=['bar-chart', 'graph-up', 'cpu', 'file-earmark-data'],
            menu_icon="robot",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )
        
        # File upload section
        st.markdown("## 📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload your dataset",
            type=['csv', 'xlsx', 'json'],
            help="Upload CSV, Excel, or JSON files for analysis"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_data = load_uploaded_file(uploaded_file)
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
            
            # Show data preview
            if st.session_state.uploaded_data is not None:
                st.markdown("### Data Preview")
                st.dataframe(st.session_state.uploaded_data.head(), use_container_width=True)
                
                st.markdown("### Data Info")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", len(st.session_state.uploaded_data))
                with col2:
                    st.metric("Columns", len(st.session_state.uploaded_data.columns))
                with col3:
                    st.metric("Missing Values", st.session_state.uploaded_data.isnull().sum().sum())
        
        # Sample data section
        st.markdown("## 📊 Sample Datasets")
        sample_dataset = st.selectbox(
            "Load sample dataset",
            ["None", "Stock Prices", "Sales Data", "Customer Data", "Iris Dataset"],
            help="Choose a sample dataset to get started quickly"
        )
        
        if sample_dataset != "None" and st.button("Load Sample Data"):
            st.session_state.uploaded_data = load_sample_data(sample_dataset)
            st.success(f"✅ Sample '{sample_dataset}' loaded!")
            st.rerun()
    
    # Main chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initialize the selected agent
    agent = get_agent(agent_type)
    st.session_state.current_agent = agent
    
    # Display agent info
    display_agent_info(agent)
    
    # Chat history display
    if st.session_state.messages:
        for i, (role, content) in enumerate(st.session_state.messages):
            if role == "user":
                message(content, is_user=True, key=f"user_{i}")
            else:
                message(content, key=f"assistant_{i}")
    
    # Chat input
    user_input = st.chat_input("Ask your data agent anything...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append(("user", user_input))
        
        # Generate agent response
        with st.spinner("Agent is thinking..."):
            response = agent.process_query(
                user_input, 
                st.session_state.uploaded_data,
                st.session_state.analysis_history
            )
        
        # Add agent response to history
        st.session_state.messages.append(("assistant", response))
        
        # Save to analysis history
        st.session_state.analysis_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,
            "query": user_input,
            "response": response
        })
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown("## 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📈 Analyze Data"):
            if st.session_state.uploaded_data is not None:
                quick_analysis = agent.quick_analysis(st.session_state.uploaded_data)
                st.session_state.messages.append(("assistant", quick_analysis))
                st.rerun()
            else:
                st.warning("Please upload data first!")
    
    with col2:
        if st.button("📊 Create Visualization"):
            if st.session_state.uploaded_data is not None:
                viz_suggestion = agent.suggest_visualization(st.session_state.uploaded_data)
                st.session_state.messages.append(("assistant", viz_suggestion))
                st.rerun()
            else:
                st.warning("Please upload data first!")
    
    with col3:
        if st.button("🧹 Clear Chat"):
            st.session_state.messages = []
            st.session_state.analysis_history = []
            st.rerun()
    
    with col4:
        if st.button("💾 Export Chat"):
            if st.session_state.messages:
                export_chat_history()
            else:
                st.warning("No chat history to export!")

def load_uploaded_file(uploaded_file):
    """Load uploaded file based on its type"""
    try:
        if uploaded_file.type == "text/csv":
            return pd.read_csv(uploaded_file)
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            return pd.read_excel(uploaded_file)
        elif uploaded_file.type == "application/json":
            return pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file format!")
            return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def get_agent(agent_type):
    """Get the appropriate agent based on selection"""
    agents = {
        "Data Analysis": DataAnalysisAgent(),
        "Visualization": VisualizationAgent(),
        "ML Insights": MLInsightsAgent(),
        "File Analysis": FileAnalysisAgent()
    }
    return agents[agent_type]

def display_agent_info(agent):
    """Display information about the current agent"""
    st.markdown(f"""
    <div class="agent-card">
        <h3>🤖 {agent.name}</h3>
        <p>{agent.description}</p>
        <p><strong>Capabilities:</strong> {', '.join(agent.capabilities)}</p>
    </div>
    """, unsafe_allow_html=True)

def export_chat_history():
    """Export chat history as JSON"""
    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "messages": st.session_state.messages,
        "analysis_history": st.session_state.analysis_history
    }
    
    json_string = json.dumps(chat_data, indent=2)
    b64 = base64.b64encode(json_string.encode()).decode()
    
    st.markdown(f"""
    <a href="data:application/json;base64,{b64}" download="chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json">
        <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
            📥 Download Chat History
        </button>
    </a>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()