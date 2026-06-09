import csv
import pandas as pd
from io import StringIO
from typing import List, Dict, Any, Tuple

def parse_csv_transactions(file_content: bytes) -> Dict[str, Any]:
    """Parse CSV file content into a list of transactions"""
    try:
        df = pd.read_csv(StringIO(file_content.decode('utf-8')))
        
        required_columns = ['Date', 'Category', 'Amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        df['Amount'] = df['Amount'].replace('[\$,]', '', regex=True).astype(float)
        
        category_totals = df.groupby('Category')['Amount'].sum().reset_index()
        
        return {
            'transactions': df.to_dict('records'),
            'category_totals': category_totals.to_dict('records')
        }
    except Exception as e:
        raise ValueError(f"Error parsing CSV file: {str(e)}")

def validate_csv_format(file) -> Tuple[bool, str]:
    """Validate CSV file format and content"""
    try:
        content = file.read().decode('utf-8')
        dialect = csv.Sniffer().sniff(content)
        has_header = csv.Sniffer().has_header(content)
        file.seek(0)
        
        if not has_header:
            return False, "CSV file must have headers"
            
        df = pd.read_csv(StringIO(content))
        required_columns = ['Date', 'Category', 'Amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
            
        try:
            pd.to_datetime(df['Date'])
        except:
            return False, "Invalid date format in Date column"
            
        try:
            df['Amount'].replace('[\$,]', '', regex=True).astype(float)
        except:
            return False, "Invalid amount format in Amount column"
            
        return True, "CSV format is valid"
    except Exception as e:
        return False, f"Invalid CSV format: {str(e)}"

def display_csv_preview(df: pd.DataFrame, st) -> None:
    """Display a preview of the CSV data with basic statistics (streamlit required)"""
    st.subheader("CSV Data Preview")
    
    total_transactions = len(df)
    total_amount = df['Amount'].sum()
    
    df_dates = pd.to_datetime(df['Date'])
    date_range = f"{df_dates.min().strftime('%Y-%m-%d')} to {df_dates.max().strftime('%Y-%m-%d')}"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Transactions", total_transactions)
    with col2:
        st.metric("Total Amount", f"${total_amount:,.2f}")
    with col3:
        st.metric("Date Range", date_range)
    
    st.subheader("Spending by Category")
    category_totals = df.groupby('Category')['Amount'].agg(['sum', 'count']).reset_index()
    category_totals.columns = ['Category', 'Total Amount', 'Transaction Count']
    st.dataframe(category_totals)
    
    st.subheader("Sample Transactions")
    st.dataframe(df.head())