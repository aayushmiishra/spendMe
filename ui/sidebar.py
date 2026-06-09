import streamlit as st

def render_sidebar() -> None:
    with st.sidebar:
        st.title("Setup & Templates")
        st.info("Please ensure you have your Gemini API key in the .env file:\n```\nGOOGLE_API_KEY=your_api_key_here\n```")
        st.caption("This application uses Google's ADK (Agent Development Kit) and Gemini AI to provide personalized financial advice.")
        
        st.divider()
        
        st.subheader("CSV Template")
        st.markdown("""
        Download the template CSV file with the required format:
        - Date (YYYY-MM-DD)
        - Category
        - Amount (numeric)
        """)
        
        sample_csv = """Date,Category,Amount
2024-01-01,Housing,1200.00
2024-01-02,Food,150.50
2024-01-03,Transportation,45.00"""
        
        st.download_button(
            label="Download CSV Template",
            data=sample_csv,
            file_name="expense_template.csv",
            mime="text/csv"
        )