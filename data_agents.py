import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import os
import json

class BaseAgent:
    """Base class for all data agents"""
    
    def __init__(self, name, description, capabilities):
        self.name = name
        self.description = description
        self.capabilities = capabilities
    
    def process_query(self, query, data=None, history=None):
        """Process user query and return response"""
        raise NotImplementedError("Subclasses must implement process_query")
    
    def quick_analysis(self, data):
        """Perform quick analysis of data"""
        if data is None:
            return "No data available for analysis. Please upload a dataset first."
        
        analysis = f"""
## Quick Data Analysis

**Dataset Overview:**
- Rows: {len(data)}
- Columns: {len(data.columns)}
- Data Types: {dict(data.dtypes.value_counts())}

**Missing Values:**
{data.isnull().sum().to_dict() if data.isnull().sum().sum() > 0 else "No missing values found"}

**Numerical Summary:**
{data.describe().to_string() if len(data.select_dtypes(include=[np.number]).columns) > 0 else "No numerical columns found"}
        """
        return analysis

class DataAnalysisAgent(BaseAgent):
    """Agent specialized in data analysis and statistics"""
    
    def __init__(self):
        super().__init__(
            name="Data Analysis Agent",
            description="I specialize in statistical analysis, data exploration, and providing insights from your datasets.",
            capabilities=["Statistical Analysis", "Data Cleaning", "Correlation Analysis", "Trend Detection", "Data Profiling"]
        )
    
    def process_query(self, query, data=None, history=None):
        """Process data analysis queries"""
        if data is None:
            return "Please upload a dataset first so I can help with analysis."
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['correlation', 'corr', 'relationship']):
            return self._analyze_correlations(data)
        elif any(word in query_lower for word in ['missing', 'null', 'na']):
            return self._analyze_missing_values(data)
        elif any(word in query_lower for word in ['summary', 'describe', 'stats']):
            return self._statistical_summary(data)
        elif any(word in query_lower for word in ['outlier', 'anomal']):
            return self._detect_outliers(data)
        else:
            return self._general_analysis(query, data)
    
    def _analyze_correlations(self, data):
        """Analyze correlations in the dataset"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return "Need at least 2 numerical columns to analyze correlations."
        
        corr_matrix = data[numeric_cols].corr()
        
        # Create correlation heatmap
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", title="Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True)
        
        # Find strongest correlations
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))
        
        result = "## Correlation Analysis\n\n"
        if corr_pairs:
            result += "**Strong Correlations (|r| > 0.5):**\n"
            for col1, col2, corr in sorted(corr_pairs, key=lambda x: abs(x[2]), reverse=True):
                result += f"- {col1} ↔ {col2}: {corr:.3f}\n"
        else:
            result += "No strong correlations found (all |r| ≤ 0.5)"
        
        return result
    
    def _analyze_missing_values(self, data):
        """Analyze missing values in the dataset"""
        missing_counts = data.isnull().sum()
        missing_percent = (missing_counts / len(data)) * 100
        
        result = "## Missing Values Analysis\n\n"
        
        if missing_counts.sum() == 0:
            result += "✅ No missing values found in the dataset!"
        else:
            result += "**Missing Values by Column:**\n"
            for col in missing_counts[missing_counts > 0].index:
                result += f"- {col}: {missing_counts[col]} ({missing_percent[col]:.1f}%)\n"
            
            # Visualization
            missing_data = missing_counts[missing_counts > 0]
            if len(missing_data) > 0:
                fig = px.bar(x=missing_data.index, y=missing_data.values, 
                           title="Missing Values by Column")
                fig.update_xaxis(title="Columns")
                fig.update_yaxis(title="Missing Count")
                st.plotly_chart(fig, use_container_width=True)
        
        return result
    
    def _statistical_summary(self, data):
        """Provide statistical summary of the dataset"""
        result = "## Statistical Summary\n\n"
        
        # Numerical columns summary
        numeric_data = data.select_dtypes(include=[np.number])
        if len(numeric_data.columns) > 0:
            result += "**Numerical Columns:**\n"
            desc = numeric_data.describe()
            st.dataframe(desc, use_container_width=True)
            result += "Detailed statistics shown in the table above.\n\n"
        
        # Categorical columns summary
        categorical_data = data.select_dtypes(include=['object'])
        if len(categorical_data.columns) > 0:
            result += "**Categorical Columns:**\n"
            for col in categorical_data.columns:
                unique_count = data[col].nunique()
                result += f"- {col}: {unique_count} unique values\n"
        
        return result
    
    def _detect_outliers(self, data):
        """Detect outliers in numerical columns"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return "No numerical columns found for outlier detection."
        
        result = "## Outlier Detection (using IQR method)\n\n"
        
        for col in numeric_cols:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
            
            result += f"**{col}:**\n"
            result += f"- Outliers found: {len(outliers)}\n"
            result += f"- Range: [{lower_bound:.2f}, {upper_bound:.2f}]\n\n"
        
        return result
    
    def _general_analysis(self, query, data):
        """Handle general analysis queries"""
        return f"""
I understand you're asking: "{query}"

Based on your dataset with {len(data)} rows and {len(data.columns)} columns, here are some insights I can provide:

**Available Analysis Options:**
- Ask about correlations between variables
- Check for missing values or data quality issues
- Get statistical summaries and descriptive statistics
- Detect outliers in your numerical data
- Explore specific columns or relationships

What specific aspect would you like me to analyze?
        """

class VisualizationAgent(BaseAgent):
    """Agent specialized in data visualization"""
    
    def __init__(self):
        super().__init__(
            name="Visualization Agent",
            description="I create beautiful and insightful visualizations from your data to help you understand patterns and trends.",
            capabilities=["Charts Creation", "Interactive Plots", "Distribution Analysis", "Time Series Visualization", "Custom Dashboards"]
        )
    
    def process_query(self, query, data=None, history=None):
        """Process visualization queries"""
        if data is None:
            return "Please upload a dataset first so I can create visualizations."
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['histogram', 'distribution', 'hist']):
            return self._create_histogram(data, query)
        elif any(word in query_lower for word in ['scatter', 'relationship', 'vs']):
            return self._create_scatter_plot(data, query)
        elif any(word in query_lower for word in ['bar', 'count', 'frequency']):
            return self._create_bar_chart(data, query)
        elif any(word in query_lower for word in ['line', 'trend', 'time']):
            return self._create_line_chart(data, query)
        elif any(word in query_lower for word in ['box', 'boxplot', 'quartile']):
            return self._create_box_plot(data, query)
        else:
            return self.suggest_visualization(data)
    
    def suggest_visualization(self, data):
        """Suggest appropriate visualizations based on data"""
        suggestions = "## Visualization Suggestions\n\n"
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(include=['object']).columns
        
        if len(numeric_cols) >= 2:
            # Create correlation heatmap
            corr_matrix = data[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, title="Correlation Heatmap")
            st.plotly_chart(fig, use_container_width=True)
            suggestions += "📊 **Correlation Heatmap** created above\n\n"
        
        if len(numeric_cols) >= 1:
            # Create distribution plot for first numeric column
            col = numeric_cols[0]
            fig = px.histogram(data, x=col, title=f"Distribution of {col}")
            st.plotly_chart(fig, use_container_width=True)
            suggestions += f"📈 **Distribution Plot** for {col} created above\n\n"
        
        suggestions += "**You can ask me to create:**\n"
        suggestions += "- Histograms for distribution analysis\n"
        suggestions += "- Scatter plots to explore relationships\n"
        suggestions += "- Bar charts for categorical data\n"
        suggestions += "- Line charts for time series data\n"
        suggestions += "- Box plots for outlier detection\n"
        
        return suggestions
    
    def _create_histogram(self, data, query):
        """Create histogram visualization"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return "No numerical columns found for histogram creation."
        
        # Use first numeric column or try to extract column from query
        col = numeric_cols[0]
        for num_col in numeric_cols:
            if num_col.lower() in query.lower():
                col = num_col
                break
        
        fig = px.histogram(data, x=col, title=f"Distribution of {col}", 
                          marginal="box", hover_data=data.columns)
        st.plotly_chart(fig, use_container_width=True)
        
        return f"📊 Created histogram for '{col}' with summary statistics."
    
    def _create_scatter_plot(self, data, query):
        """Create scatter plot visualization"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return "Need at least 2 numerical columns for scatter plot."
        
        x_col, y_col = numeric_cols[0], numeric_cols[1]
        
        fig = px.scatter(data, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
        st.plotly_chart(fig, use_container_width=True)
        
        return f"📈 Created scatter plot: {x_col} vs {y_col}"
    
    def _create_bar_chart(self, data, query):
        """Create bar chart visualization"""
        categorical_cols = data.select_dtypes(include=['object']).columns
        if len(categorical_cols) == 0:
            return "No categorical columns found for bar chart creation."
        
        col = categorical_cols[0]
        value_counts = data[col].value_counts().head(10)
        
        fig = px.bar(x=value_counts.index, y=value_counts.values, 
                     title=f"Top Categories in {col}")
        fig.update_xaxis(title=col)
        fig.update_yaxis(title="Count")
        st.plotly_chart(fig, use_container_width=True)
        
        return f"📊 Created bar chart for '{col}' showing top categories."
    
    def _create_line_chart(self, data, query):
        """Create line chart visualization"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return "No numerical columns found for line chart creation."
        
        # Try to find date column
        date_cols = []
        for col in data.columns:
            if data[col].dtype == 'datetime64[ns]' or 'date' in col.lower() or 'time' in col.lower():
                date_cols.append(col)
        
        if date_cols:
            x_col = date_cols[0]
            y_col = numeric_cols[0]
            fig = px.line(data, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
        else:
            # Use index as x-axis
            y_col = numeric_cols[0]
            fig = px.line(data, y=y_col, title=f"{y_col} Trend")
        
        st.plotly_chart(fig, use_container_width=True)
        
        return f"📈 Created line chart for '{y_col}'"
    
    def _create_box_plot(self, data, query):
        """Create box plot visualization"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return "No numerical columns found for box plot creation."
        
        col = numeric_cols[0]
        fig = px.box(data, y=col, title=f"Box Plot of {col}")
        st.plotly_chart(fig, use_container_width=True)
        
        return f"📦 Created box plot for '{col}' showing quartiles and outliers."

class MLInsightsAgent(BaseAgent):
    """Agent specialized in machine learning insights"""
    
    def __init__(self):
        super().__init__(
            name="ML Insights Agent",
            description="I provide machine learning insights, model recommendations, and feature analysis for your datasets.",
            capabilities=["Model Recommendations", "Feature Importance", "Prediction Analysis", "ML Strategy", "Performance Metrics"]
        )
    
    def process_query(self, query, data=None, history=None):
        """Process ML-related queries"""
        if data is None:
            return "Please upload a dataset first so I can provide ML insights."
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['model', 'algorithm', 'recommend']):
            return self._recommend_models(data)
        elif any(word in query_lower for word in ['feature', 'importance', 'select']):
            return self._analyze_features(data)
        elif any(word in query_lower for word in ['predict', 'forecast', 'target']):
            return self._prediction_analysis(data, query)
        else:
            return self._general_ml_insights(data)
    
    def _recommend_models(self, data):
        """Recommend ML models based on data characteristics"""
        result = "## ML Model Recommendations\n\n"
        
        numeric_cols = len(data.select_dtypes(include=[np.number]).columns)
        categorical_cols = len(data.select_dtypes(include=['object']).columns)
        total_rows = len(data)
        
        result += f"**Dataset Characteristics:**\n"
        result += f"- Rows: {total_rows:,}\n"
        result += f"- Numerical features: {numeric_cols}\n"
        result += f"- Categorical features: {categorical_cols}\n\n"
        
        # Size-based recommendations
        if total_rows < 1000:
            result += "**Size Consideration:** Small dataset - consider simple models to avoid overfitting.\n\n"
        elif total_rows > 100000:
            result += "**Size Consideration:** Large dataset - can support complex models like deep learning.\n\n"
        
        # Feature-based recommendations
        result += "**Recommended Models:**\n"
        
        if numeric_cols > categorical_cols:
            result += "- **Random Forest**: Great for numerical data with feature importance\n"
            result += "- **Gradient Boosting**: Excellent for structured data\n"
            result += "- **Linear Models**: If relationships appear linear\n"
        
        if categorical_cols > 0:
            result += "- **Tree-based models**: Handle categorical features well\n"
            result += "- **Neural Networks**: With proper encoding for categories\n"
        
        if total_rows > 10000 and numeric_cols > 10:
            result += "- **Deep Learning**: For complex pattern recognition\n"
        
        return result
    
    def _analyze_features(self, data):
        """Analyze features for ML readiness"""
        result = "## Feature Analysis\n\n"
        
        # Data types analysis
        result += "**Data Types:**\n"
        type_counts = data.dtypes.value_counts()
        for dtype, count in type_counts.items():
            result += f"- {dtype}: {count} columns\n"
        
        result += "\n**Feature Quality Assessment:**\n"
        
        # Missing values
        missing_cols = data.columns[data.isnull().any()].tolist()
        if missing_cols:
            result += f"- Columns with missing values: {len(missing_cols)}\n"
            result += f"  {missing_cols}\n"
        else:
            result += "- ✅ No missing values detected\n"
        
        # High cardinality categorical features
        categorical_cols = data.select_dtypes(include=['object']).columns
        high_cardinality = []
        for col in categorical_cols:
            unique_ratio = data[col].nunique() / len(data)
            if unique_ratio > 0.5:
                high_cardinality.append(col)
        
        if high_cardinality:
            result += f"- High cardinality categorical features: {high_cardinality}\n"
            result += "  Consider encoding or dimensionality reduction\n"
        
        # Constant features
        constant_cols = []
        for col in data.columns:
            if data[col].nunique() == 1:
                constant_cols.append(col)
        
        if constant_cols:
            result += f"- Constant features (should be removed): {constant_cols}\n"
        
        return result
    
    def _prediction_analysis(self, data, query):
        """Analyze prediction scenarios"""
        result = "## Prediction Analysis\n\n"
        
        # Try to identify potential target variables
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(include=['object']).columns
        
        result += "**Potential Target Variables:**\n"
        
        # Look for common target variable names
        target_keywords = ['target', 'label', 'class', 'price', 'sales', 'revenue', 'score']
        potential_targets = []
        
        for col in data.columns:
            if any(keyword in col.lower() for keyword in target_keywords):
                potential_targets.append(col)
        
        if potential_targets:
            result += f"- Identified potential targets: {potential_targets}\n"
        else:
            result += "- No obvious target variables found\n"
            result += f"- Numerical columns suitable for regression: {list(numeric_cols)}\n"
            result += f"- Categorical columns suitable for classification: {list(categorical_cols)}\n"
        
        result += "\n**Prediction Strategy Recommendations:**\n"
        result += "1. **Define your target variable** - what do you want to predict?\n"
        result += "2. **Split your data** - 80% training, 20% testing\n"
        result += "3. **Feature engineering** - create meaningful features\n"
        result += "4. **Model selection** - start with simple models\n"
        result += "5. **Evaluation** - use appropriate metrics for your problem\n"
        
        return result
    
    def _general_ml_insights(self, data):
        """Provide general ML insights"""
        return f"""
## General ML Insights for Your Dataset

**Dataset Overview:**
- Shape: {data.shape[0]:,} rows × {data.shape[1]} columns
- Memory usage: ~{data.memory_usage(deep=True).sum() / 1024**2:.1f} MB

**ML Readiness Checklist:**
- ✅ Data loaded successfully
- {'✅' if data.isnull().sum().sum() == 0 else '⚠️'} Missing values: {data.isnull().sum().sum()}
- {'✅' if len(data.select_dtypes(include=[np.number]).columns) > 0 else '⚠️'} Numerical features available
- {'✅' if len(data) > 100 else '⚠️'} Sufficient data points

**Next Steps:**
1. Ask me about model recommendations
2. Request feature importance analysis
3. Discuss prediction strategies
4. Explore data visualizations

What specific ML task are you planning?
        """

class FileAnalysisAgent(BaseAgent):
    """Agent specialized in file analysis and data exploration"""
    
    def __init__(self):
        super().__init__(
            name="File Analysis Agent",
            description="I analyze file structures, data formats, and help with data import/export operations.",
            capabilities=["File Structure Analysis", "Data Format Detection", "Import/Export Help", "Data Validation", "Schema Analysis"]
        )
    
    def process_query(self, query, data=None, history=None):
        """Process file analysis queries"""
        if data is None:
            return self._file_import_help()
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['structure', 'schema', 'format']):
            return self._analyze_structure(data)
        elif any(word in query_lower for word in ['export', 'save', 'download']):
            return self._export_help(data)
        elif any(word in query_lower for word in ['validate', 'quality', 'clean']):
            return self._data_validation(data)
        else:
            return self._general_file_analysis(data)
    
    def _file_import_help(self):
        """Provide help for file import"""
        return """
## File Import Help

**Supported Formats:**
- 📄 **CSV** (.csv) - Comma-separated values
- 📊 **Excel** (.xlsx, .xls) - Microsoft Excel files
- 📋 **JSON** (.json) - JavaScript Object Notation

**Import Tips:**
1. Ensure your file has proper headers
2. Check for consistent data types in columns
3. Remove or handle special characters
4. Verify encoding (UTF-8 recommended)

**Sample Data Available:**
- Stock Prices - Financial time series data
- Sales Data - Business analytics dataset
- Customer Data - Customer segmentation data
- Iris Dataset - Classic ML dataset

Upload a file or select sample data to get started!
        """
    
    def _analyze_structure(self, data):
        """Analyze data structure and schema"""
        result = "## Data Structure Analysis\n\n"
        
        result += f"**Basic Information:**\n"
        result += f"- Dimensions: {data.shape[0]:,} rows × {data.shape[1]} columns\n"
        result += f"- Memory usage: {data.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n\n"
        
        result += "**Column Information:**\n"
        for i, (col, dtype) in enumerate(data.dtypes.items()):
            unique_vals = data[col].nunique()
            null_count = data[col].isnull().sum()
            result += f"{i+1}. **{col}** ({dtype})\n"
            result += f"   - Unique values: {unique_vals:,}\n"
            result += f"   - Missing values: {null_count:,}\n"
            
            # Sample values
            if dtype == 'object':
                sample_vals = data[col].dropna().unique()[:3]
                result += f"   - Sample values: {list(sample_vals)}\n"
            else:
                result += f"   - Range: {data[col].min():.2f} to {data[col].max():.2f}\n"
            result += "\n"
        
        return result
    
    def _export_help(self, data):
        """Provide export options"""
        result = "## Data Export Options\n\n"
        
        # CSV export
        csv_data = data.to_csv(index=False)
        st.download_button(
            label="📄 Download as CSV",
            data=csv_data,
            file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # JSON export
        json_data = data.to_json(orient='records', indent=2)
        st.download_button(
            label="📋 Download as JSON",
            data=json_data,
            file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        result += "**Export Options Available:**\n"
        result += "- CSV format for spreadsheet applications\n"
        result += "- JSON format for web applications\n"
        result += "- Excel format (coming soon)\n\n"
        
        result += "Click the download buttons above to export your data!"
        
        return result
    
    def _data_validation(self, data):
        """Validate data quality"""
        result = "## Data Quality Validation\n\n"
        
        issues = []
        
        # Check for missing values
        missing_count = data.isnull().sum().sum()
        if missing_count > 0:
            issues.append(f"Missing values: {missing_count:,}")
        
        # Check for duplicate rows
        duplicate_count = data.duplicated().sum()
        if duplicate_count > 0:
            issues.append(f"Duplicate rows: {duplicate_count:,}")
        
        # Check for constant columns
        constant_cols = [col for col in data.columns if data[col].nunique() == 1]
        if constant_cols:
            issues.append(f"Constant columns: {constant_cols}")
        
        # Check for high cardinality in small datasets
        if len(data) < 1000:
            high_card_cols = [col for col in data.select_dtypes(include=['object']).columns 
                             if data[col].nunique() > len(data) * 0.5]
            if high_card_cols:
                issues.append(f"High cardinality columns: {high_card_cols}")
        
        if issues:
            result += "**Issues Found:**\n"
            for issue in issues:
                result += f"- ⚠️ {issue}\n"
            result += "\n**Recommendations:**\n"
            result += "- Handle missing values (imputation or removal)\n"
            result += "- Remove or investigate duplicate rows\n"
            result += "- Consider removing constant features\n"
            result += "- Encode high cardinality categorical variables\n"
        else:
            result += "✅ **No major data quality issues detected!**\n"
            result += "Your dataset appears to be clean and ready for analysis.\n"
        
        return result
    
    def _general_file_analysis(self, data):
        """General file analysis overview"""
        return f"""
## File Analysis Overview

**Your dataset is loaded and ready!**

**Quick Stats:**
- 📊 Dimensions: {data.shape[0]:,} rows × {data.shape[1]} columns
- 💾 Size: ~{data.memory_usage(deep=True).sum() / 1024**2:.1f} MB
- 🔢 Numerical columns: {len(data.select_dtypes(include=[np.number]).columns)}
- 📝 Text columns: {len(data.select_dtypes(include=['object']).columns)}

**What I can help you with:**
- Analyze data structure and schema
- Validate data quality and cleanliness
- Export data in different formats
- Prepare data for analysis or modeling

**Try asking:**
- "Analyze the structure of my data"
- "Check data quality and validation"
- "Help me export this data"
- "What issues should I fix in this dataset?"
        """