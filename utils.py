import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os

def load_sample_data(dataset_name):
    """Load sample datasets for demonstration"""
    
    if dataset_name == "Stock Prices":
        # Generate sample stock price data
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)
        
        price = 100
        prices = []
        volumes = []
        
        for _ in dates:
            price += np.random.normal(0, 2)
            price = max(price, 50)  # Prevent negative prices
            prices.append(price)
            volumes.append(np.random.randint(100000, 1000000))
        
        data = pd.DataFrame({
            'Date': dates,
            'Open': [p + np.random.normal(0, 1) for p in prices],
            'High': [p + abs(np.random.normal(2, 1)) for p in prices],
            'Low': [p - abs(np.random.normal(2, 1)) for p in prices],
            'Close': prices,
            'Volume': volumes
        })
        
        # Calculate additional indicators
        data['MA_7'] = data['Close'].rolling(window=7).mean()
        data['MA_30'] = data['Close'].rolling(window=30).mean()
        data['Daily_Return'] = data['Close'].pct_change()
        
        return data
    
    elif dataset_name == "Sales Data":
        # Generate sample sales data
        np.random.seed(42)
        n_records = 1000
        
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
        regions = ['North', 'South', 'East', 'West', 'Central']
        salespersons = [f'Sales_Person_{i}' for i in range(1, 21)]
        
        data = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=n_records, freq='D'),
            'Category': np.random.choice(categories, n_records),
            'Region': np.random.choice(regions, n_records),
            'Salesperson': np.random.choice(salespersons, n_records),
            'Units_Sold': np.random.randint(1, 100, n_records),
            'Unit_Price': np.random.uniform(10, 500, n_records),
            'Customer_Age': np.random.randint(18, 80, n_records),
            'Customer_Gender': np.random.choice(['Male', 'Female'], n_records)
        })
        
        data['Total_Sales'] = data['Units_Sold'] * data['Unit_Price']
        data['Month'] = data['Date'].dt.month
        data['Quarter'] = data['Date'].dt.quarter
        
        return data
    
    elif dataset_name == "Customer Data":
        # Generate sample customer data
        np.random.seed(42)
        n_customers = 1500
        
        data = pd.DataFrame({
            'Customer_ID': range(1, n_customers + 1),
            'Age': np.random.randint(18, 80, n_customers),
            'Gender': np.random.choice(['Male', 'Female'], n_customers),
            'Income': np.random.normal(50000, 20000, n_customers),
            'Education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_customers),
            'Marital_Status': np.random.choice(['Single', 'Married', 'Divorced'], n_customers),
            'Children': np.random.randint(0, 5, n_customers),
            'Years_Customer': np.random.randint(1, 15, n_customers),
            'Monthly_Spend': np.random.uniform(50, 2000, n_customers),
            'Support_Tickets': np.random.poisson(2, n_customers),
            'Satisfaction_Score': np.random.randint(1, 11, n_customers)
        })
        
        # Ensure income is positive
        data['Income'] = np.abs(data['Income'])
        
        # Calculate customer value
        data['Customer_Value'] = data['Monthly_Spend'] * data['Years_Customer']
        data['Churn_Risk'] = np.where(
            (data['Satisfaction_Score'] < 5) | (data['Support_Tickets'] > 5), 
            'High', 
            np.where(data['Satisfaction_Score'] < 7, 'Medium', 'Low')
        )
        
        return data
    
    elif dataset_name == "Iris Dataset":
        # Classic Iris dataset
        np.random.seed(42)
        
        # Generate iris-like data
        n_per_species = 50
        species = ['Setosa', 'Versicolor', 'Virginica']
        
        data_list = []
        
        # Setosa (smaller flowers)
        setosa = pd.DataFrame({
            'Species': ['Setosa'] * n_per_species,
            'Sepal_Length': np.random.normal(5.0, 0.35, n_per_species),
            'Sepal_Width': np.random.normal(3.4, 0.38, n_per_species),
            'Petal_Length': np.random.normal(1.5, 0.17, n_per_species),
            'Petal_Width': np.random.normal(0.25, 0.11, n_per_species)
        })
        
        # Versicolor (medium flowers)
        versicolor = pd.DataFrame({
            'Species': ['Versicolor'] * n_per_species,
            'Sepal_Length': np.random.normal(5.9, 0.52, n_per_species),
            'Sepal_Width': np.random.normal(2.8, 0.31, n_per_species),
            'Petal_Length': np.random.normal(4.3, 0.47, n_per_species),
            'Petal_Width': np.random.normal(1.3, 0.20, n_per_species)
        })
        
        # Virginica (larger flowers)
        virginica = pd.DataFrame({
            'Species': ['Virginica'] * n_per_species,
            'Sepal_Length': np.random.normal(6.6, 0.64, n_per_species),
            'Sepal_Width': np.random.normal(3.0, 0.32, n_per_species),
            'Petal_Length': np.random.normal(5.6, 0.55, n_per_species),
            'Petal_Width': np.random.normal(2.0, 0.27, n_per_species)
        })
        
        data = pd.concat([setosa, versicolor, virginica], ignore_index=True)
        
        # Add some additional features
        data['Sepal_Area'] = data['Sepal_Length'] * data['Sepal_Width']
        data['Petal_Area'] = data['Petal_Length'] * data['Petal_Width']
        data['Total_Length'] = data['Sepal_Length'] + data['Petal_Length']
        data['Length_Ratio'] = data['Petal_Length'] / data['Sepal_Length']
        
        return data
    
    else:
        return None

def format_response(response_text):
    """Format agent responses for better display"""
    # Add proper markdown formatting
    if not response_text.startswith('#'):
        response_text = f"## Response\n\n{response_text}"
    
    return response_text

def save_chat_history(messages, analysis_history, filename=None):
    """Save chat history to file"""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"chat_history_{timestamp}.json"
    
    chat_data = {
        'timestamp': datetime.now().isoformat(),
        'messages': messages,
        'analysis_history': analysis_history,
        'session_info': {
            'total_messages': len(messages),
            'agents_used': list(set([entry.get('agent_type') for entry in analysis_history])),
            'duration': None  # Could calculate based on timestamps
        }
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(chat_data, f, indent=2)
        return filename
    except Exception as e:
        return f"Error saving chat history: {str(e)}"

def load_chat_history(filename):
    """Load chat history from file"""
    try:
        with open(filename, 'r') as f:
            chat_data = json.load(f)
        return chat_data
    except Exception as e:
        return f"Error loading chat history: {str(e)}"

def get_data_summary(data):
    """Get a quick summary of the dataset"""
    if data is None:
        return "No data available"
    
    summary = {
        'shape': data.shape,
        'columns': list(data.columns),
        'dtypes': dict(data.dtypes),
        'missing_values': dict(data.isnull().sum()),
        'memory_usage_mb': data.memory_usage(deep=True).sum() / 1024**2,
        'numerical_columns': list(data.select_dtypes(include=[np.number]).columns),
        'categorical_columns': list(data.select_dtypes(include=['object']).columns)
    }
    
    return summary

def detect_data_type(data, column):
    """Detect the likely data type and purpose of a column"""
    col_data = data[column]
    
    # Basic type detection
    if col_data.dtype in ['int64', 'float64']:
        if col_data.min() >= 0 and col_data.max() <= 1 and col_data.nunique() == 2:
            return "binary"
        elif col_data.nunique() < 10 and col_data.dtype == 'int64':
            return "categorical_numeric"
        else:
            return "continuous_numeric"
    
    elif col_data.dtype == 'object':
        # Check if it could be datetime
        sample_vals = col_data.dropna().head(10)
        try:
            pd.to_datetime(sample_vals)
            return "datetime_string"
        except:
            pass
        
        # Check cardinality
        unique_ratio = col_data.nunique() / len(col_data)
        if unique_ratio > 0.8:
            return "high_cardinality_categorical"
        elif unique_ratio < 0.05:
            return "low_cardinality_categorical"
        else:
            return "medium_cardinality_categorical"
    
    elif col_data.dtype == 'datetime64[ns]':
        return "datetime"
    
    elif col_data.dtype == 'bool':
        return "boolean"
    
    else:
        return "unknown"

def suggest_preprocessing_steps(data):
    """Suggest preprocessing steps based on data characteristics"""
    suggestions = []
    
    # Check for missing values
    missing_cols = data.columns[data.isnull().any()].tolist()
    if missing_cols:
        suggestions.append(f"Handle missing values in columns: {missing_cols}")
    
    # Check for categorical encoding needs
    categorical_cols = data.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        suggestions.append(f"Consider encoding categorical variables: {list(categorical_cols)}")
    
    # Check for scaling needs
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        ranges = data[numeric_cols].max() - data[numeric_cols].min()
        if ranges.max() / ranges.min() > 100:  # Large scale differences
            suggestions.append("Consider feature scaling due to different value ranges")
    
    # Check for duplicates
    if data.duplicated().any():
        suggestions.append("Remove duplicate rows")
    
    # Check for constant features
    constant_cols = [col for col in data.columns if data[col].nunique() == 1]
    if constant_cols:
        suggestions.append(f"Remove constant features: {constant_cols}")
    
    return suggestions

def create_data_profile(data):
    """Create a comprehensive data profile"""
    profile = {
        'basic_info': {
            'shape': data.shape,
            'memory_usage_mb': round(data.memory_usage(deep=True).sum() / 1024**2, 2),
            'duplicates': data.duplicated().sum()
        },
        'column_info': {},
        'data_quality': {
            'missing_values_total': data.isnull().sum().sum(),
            'missing_value_columns': data.columns[data.isnull().any()].tolist(),
            'complete_rows': len(data) - data.isnull().any(axis=1).sum()
        },
        'preprocessing_suggestions': suggest_preprocessing_steps(data)
    }
    
    # Analyze each column
    for col in data.columns:
        col_info = {
            'dtype': str(data[col].dtype),
            'unique_values': data[col].nunique(),
            'missing_count': data[col].isnull().sum(),
            'missing_percentage': round((data[col].isnull().sum() / len(data)) * 100, 2),
            'data_type_suggestion': detect_data_type(data, col)
        }
        
        if data[col].dtype in ['int64', 'float64']:
            col_info.update({
                'min': data[col].min(),
                'max': data[col].max(),
                'mean': round(data[col].mean(), 2),
                'std': round(data[col].std(), 2)
            })
        elif data[col].dtype == 'object':
            value_counts = data[col].value_counts().head(5)
            col_info['top_values'] = dict(value_counts)
        
        profile['column_info'][col] = col_info
    
    return profile