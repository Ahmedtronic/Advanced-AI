#!/bin/bash

# Data Agents Chat Application Startup Script
echo "🤖 Starting Data Agents Chat Application..."

# Check if virtual environment exists
if [ ! -d "data_agents_env" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   python3 -m venv data_agents_env"
    echo "   source data_agents_env/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source data_agents_env/bin/activate

# Check if all dependencies are installed
echo "📦 Checking dependencies..."
python -c "import streamlit, pandas, plotly, data_agents, utils" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Some dependencies are missing. Installing..."
    pip install -r requirements.txt
fi

# Start the Streamlit application
echo "🚀 Starting Streamlit application..."
echo "📱 Open your browser and go to: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

streamlit run app.py --server.port 8501 --server.address localhost