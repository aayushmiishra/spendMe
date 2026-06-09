import streamlit as st
from utils.display_helpers import display_budget_analysis, display_savings_strategy, display_debt_reduction

def render_results(results: dict) -> None:
    tabs = st.tabs(["Budget Analysis", "Savings Strategy", "Debt Reduction"])
    
    with tabs[0]:
        st.subheader("Budget Analysis")
        if results.get("budget_analysis"):
            display_budget_analysis(results["budget_analysis"])
        else:
            st.write("No budget analysis available.")
    
    with tabs[1]:
        st.subheader("Savings Strategy")
        if results.get("savings_strategy"):
            display_savings_strategy(results["savings_strategy"])
        else:
            st.write("No savings strategy available.")
    
    with tabs[2]:
        st.subheader("Debt Reduction Plan")
        if results.get("debt_reduction"):
            display_debt_reduction(results["debt_reduction"])
        else:
            st.write("No debt reduction plan available.")