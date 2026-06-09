import streamlit as st
import asyncio
from config import GEMINI_API_KEY
from ui import render_sidebar, render_input_form, render_results
from agents import FinanceAdvisorSystem

def main():
    st.set_page_config(
        page_title="SpendME",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    render_sidebar()
    
    if not GEMINI_API_KEY:
        st.error("GOOGLE_API_KEY issue")
        return
    
    st.title("SpendME")
    # st.caption("Powered by Google's Agent Development Kit (ADK) and Gemini AI")
    # st.info("This tool analyzes your financial data and provides tailored recommendations for budgeting, savings, and debt management using multiple specialized AI agents.")
    st.divider()
    
    input_tab, about_tab = st.tabs(["Financial Information", "About"])
    
    with input_tab:
        financial_data, analyze_clicked = render_input_form()
        
        if analyze_clicked:
            # Validation
            expense_option = st.session_state.get("expense_option")
            if expense_option == "Upload CSV Transactions" and financial_data["_transactions_df"] is None:
                st.error("Please upload a valid transaction CSV file or choose manual entry.")
                return
            if financial_data.get("_use_manual_expenses") and (not financial_data.get("manual_expenses") or not any(financial_data["manual_expenses"].values())):
                st.warning("No manual expenses entered. Analysis might be limited.")
            
            st.header("Financial Analysis Results")
            with st.spinner("AI agents are analyzing your financial data..."):
                # Remove internal keys before sending to agent
                clean_data = {k: v for k, v in financial_data.items() if not k.startswith("_")}
                advisor = FinanceAdvisorSystem()
                try:
                    analyze_method = (
                        getattr(advisor, "analyze_finances", None)
                        or getattr(advisor, "analyze", None)
                        or getattr(advisor, "run", None)
                    )
                    if analyze_method is None:
                        raise AttributeError("FinanceAdvisorSystem has no analysis method.")
                    analysis_result = analyze_method(clean_data)
                    results = asyncio.run(analysis_result) if asyncio.iscoroutine(analysis_result) else analysis_result
                    render_results(results)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
    
    with about_tab:
        st.markdown("""
        ### About AI Financial Coach
        
        This application uses Google's Agent Development Kit (ADK) to provide comprehensive financial analysis and advice through multiple specialized AI agents:
        
        1. **Budget Analysis Agent**
           - Analyzes spending patterns
           - Identifies areas for cost reduction
           - Provides actionable recommendations
        
        2. **Savings Strategy Agent**
           - Creates personalized savings plans
           - Calculates emergency fund requirements
           - Suggests automation techniques
        
        3. **Debt Reduction Agent**
           - Develops optimal debt payoff strategies
           - Compares different repayment methods
           - Provides actionable debt reduction tips
        
        ### Privacy & Security
        
        - All data is processed locally
        - No financial information is stored or transmitted
        - Secure API communication with Google's services
        """)

if __name__ == "__main__":
    main()