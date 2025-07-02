# 🤖 Data Agents Chat Interface

A powerful Streamlit application that lets you chat with specialized AI agents for data analysis, visualization, and machine learning insights.

![Data Agents Demo](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## ✨ Features

### 🤖 Four Specialized Agents

1. **📊 Data Analysis Agent**
   - Statistical analysis and data exploration
   - Correlation analysis and trend detection
   - Missing value analysis and outlier detection
   - Data profiling and quality assessment

2. **📈 Visualization Agent**
   - Interactive charts and plots
   - Distribution analysis with histograms
   - Relationship exploration with scatter plots
   - Time series and trend visualizations

3. **🧠 ML Insights Agent**
   - Machine learning model recommendations
   - Feature importance analysis
   - Prediction strategy development
   - ML readiness assessment

4. **📁 File Analysis Agent**
   - Data structure and schema analysis
   - File format detection and validation
   - Import/export assistance
   - Data quality validation

### 💫 Key Capabilities

- **Chat Interface**: Natural language interaction with data agents
- **File Upload**: Support for CSV, Excel, and JSON files
- **Sample Datasets**: Pre-loaded datasets for quick exploration
- **Interactive Visualizations**: Powered by Plotly for dynamic charts
- **Data Export**: Download processed data and chat history
- **Real-time Analysis**: Instant insights and recommendations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Open in Browser

Navigate to `http://localhost:8501` in your web browser.

## 📁 Project Structure

```
data-agents-chat/
├── app.py                 # Main Streamlit application
├── data_agents.py         # Agent classes and logic
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## 🛠️ Usage Guide

### Getting Started

1. **Choose an Agent**: Select from the four specialized agents in the sidebar
2. **Upload Data**: Upload your dataset or choose from sample data
3. **Start Chatting**: Ask questions about your data in natural language

### Example Queries

**Data Analysis Agent:**
- "Show me correlations in my data"
- "Check for missing values"
- "Analyze outliers in the dataset"
- "Give me a statistical summary"

**Visualization Agent:**
- "Create a histogram of sales data"
- "Show relationship between age and income"
- "Make a bar chart of categories"
- "Plot time series trends"

**ML Insights Agent:**
- "What models do you recommend for this data?"
- "Analyze features for machine learning"
- "Help me with prediction strategy"
- "Assess ML readiness of my dataset"

**File Analysis Agent:**
- "Analyze my data structure"
- "Check data quality issues"
- "Help me export this data"
- "Validate my dataset"

### Sample Datasets

The application includes several sample datasets:

- **Stock Prices**: Financial time series data with OHLC prices
- **Sales Data**: Business analytics with regional and category breakdowns
- **Customer Data**: Customer segmentation with demographics and behavior
- **Iris Dataset**: Classic machine learning dataset for classification

## 🎨 Features in Detail

### Interactive Chat Interface

- **Real-time Responses**: Agents respond instantly to your queries
- **Context Awareness**: Agents remember your conversation history
- **Rich Formatting**: Responses include tables, charts, and formatted text

### Data Upload and Processing

- **Multiple Formats**: CSV, Excel (.xlsx, .xls), and JSON support
- **Automatic Detection**: File type and structure auto-detection
- **Data Preview**: Instant preview of uploaded data
- **Quality Metrics**: Missing values, data types, and size information

### Visualization Engine

- **Interactive Charts**: Plotly-powered dynamic visualizations
- **Smart Suggestions**: Automatic chart type recommendations
- **Customizable**: Modify charts based on your preferences
- **Export Ready**: High-quality charts for presentations

### Export Capabilities

- **Chat History**: Download conversation logs as JSON
- **Data Export**: Export processed data in multiple formats
- **Visualization Export**: Save charts and plots
- **Analysis Reports**: Comprehensive analysis summaries

## 🔧 Advanced Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Optional API keys for enhanced features
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# App configuration
DEBUG=False
STREAMLIT_SERVER_PORT=8501
```

### Custom Agents

Extend the application by creating custom agents:

```python
class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Custom Agent",
            description="Your custom agent description",
            capabilities=["Custom Feature 1", "Custom Feature 2"]
        )
    
    def process_query(self, query, data=None, history=None):
        # Your custom logic here
        return "Custom response"
```

## 🧪 Example Workflows

### 1. Data Exploration Workflow

```
1. Upload your dataset
2. Use Data Analysis Agent to get overview
3. Switch to Visualization Agent for charts
4. Check ML readiness with ML Insights Agent
5. Export findings with File Analysis Agent
```

### 2. Business Intelligence Workflow

```
1. Load sales or customer data
2. Analyze trends and patterns
3. Create executive dashboards
4. Generate insights and recommendations
5. Export reports for stakeholders
```

### 3. Machine Learning Preparation

```
1. Upload training dataset
2. Assess data quality and structure
3. Get model recommendations
4. Analyze feature importance
5. Prepare data for ML pipeline
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/data-agents-chat.git
cd data-agents-chat

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py --server.runOnSave true
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

Having issues? Here are some quick solutions:

### Common Issues

**Q: Application won't start**
- Check Python version (3.8+ required)
- Verify all dependencies are installed
- Run `pip install -r requirements.txt` again

**Q: Charts not displaying**
- Ensure Plotly is installed correctly
- Check browser compatibility
- Try refreshing the page

**Q: File upload fails**
- Verify file format (CSV, Excel, JSON only)
- Check file size (max 200MB)
- Ensure proper encoding (UTF-8 recommended)

**Q: Agent responses seem slow**
- Large datasets may take time to process
- Consider using sample data for testing
- Check system memory availability

### Getting Help

- 📧 **Email**: [your-email@example.com](mailto:your-email@example.com)
- 💬 **Issues**: Open an issue on GitHub
- 📖 **Documentation**: Check the wiki for detailed guides

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **Plotly** for interactive visualizations
- **Pandas** for data manipulation capabilities
- **NumPy** for numerical computing support

## 🔮 Future Enhancements

- [ ] Real-time data streaming support
- [ ] Advanced ML model integration
- [ ] Multi-user collaboration features
- [ ] Custom dashboard builder
- [ ] API endpoints for programmatic access
- [ ] Cloud deployment options
- [ ] Enhanced natural language processing

---

**Made with ❤️ for the data science community**

Happy analyzing! 🚀