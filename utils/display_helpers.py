import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

def display_budget_analysis(analysis: Dict[str, Any]) -> None:
    if isinstance(analysis, str):
        try:
            analysis = json.loads(analysis)
        except json.JSONDecodeError:
            st.error("Failed to parse budget analysis results")
            return
    
    if not isinstance(analysis, dict):
        st.error("Invalid budget analysis format")
        return
    
    if "spending_categories" in analysis:
        st.subheader("Spending by Category")
        fig = px.pie(
            values=[cat["amount"] for cat in analysis["spending_categories"]],
            names=[cat["category"] for cat in analysis["spending_categories"]],
            title="Your Spending Breakdown"
        )
        st.plotly_chart(fig)
    
    if "total_expenses" in analysis:
        st.subheader("Income vs. Expenses")
        income = analysis.get("monthly_income", 0)
        expenses = analysis["total_expenses"]
        surplus_deficit = income - expenses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=["Income", "Expenses"], 
                            y=[income, expenses],
                            marker_color=["green", "red"]))
        fig.update_layout(title="Monthly Income vs. Expenses")
        st.plotly_chart(fig)
        
        st.metric("Monthly Surplus/Deficit", 
                  f"${surplus_deficit:.2f}", 
                  delta=f"{surplus_deficit:.2f}")
    
    if "recommendations" in analysis:
        st.subheader("Spending Reduction Recommendations")
        for rec in analysis["recommendations"]:
            st.markdown(f"**{rec['category']}**: {rec['recommendation']}")
            if "potential_savings" in rec:
                st.metric(f"Potential Monthly Savings", f"${rec['potential_savings']:.2f}")

def display_savings_strategy(strategy: Dict[str, Any]) -> None:
    if isinstance(strategy, str):
        try:
            strategy = json.loads(strategy)
        except json.JSONDecodeError:
            st.error("Failed to parse savings strategy results")
            return
    
    if not isinstance(strategy, dict):
        st.error("Invalid savings strategy format")
        return
    
    st.subheader("Savings Recommendations")
    
    if "emergency_fund" in strategy:
        ef = strategy["emergency_fund"]
        st.markdown(f"### Emergency Fund")
        st.markdown(f"**Recommended Size**: ${ef['recommended_amount']:.2f}")
        st.markdown(f"**Current Status**: {ef['current_status']}")
        
        if "current_amount" in ef and "recommended_amount" in ef:
            progress = ef["current_amount"] / ef["recommended_amount"] if ef["recommended_amount"] > 0 else 0
            st.progress(min(progress, 1.0))
            st.markdown(f"${ef['current_amount']:.2f} of ${ef['recommended_amount']:.2f}")
    
    if "recommendations" in strategy:
        st.markdown("### Recommended Savings Allocations")
        for rec in strategy["recommendations"]:
            st.markdown(f"**{rec['category']}**: ${rec['amount']:.2f}/month")
            st.markdown(f"_{rec['rationale']}_")
    
    if "automation_techniques" in strategy:
        st.markdown("### Automation Techniques")
        for technique in strategy["automation_techniques"]:
            st.markdown(f"**{technique['name']}**: {technique['description']}")

def display_debt_reduction(plan: Dict[str, Any]) -> None:
    if isinstance(plan, str):
        try:
            plan = json.loads(plan)
        except json.JSONDecodeError:
            st.error("Failed to parse debt reduction results")
            return
    
    if not isinstance(plan, dict):
        st.error("Invalid debt reduction format")
        return
    
    if "total_debt" in plan:
        st.metric("Total Debt", f"${plan['total_debt']:.2f}")
    
    if "debts" in plan:
        st.subheader("Your Debts")
        debt_df = pd.DataFrame(plan["debts"])
        st.dataframe(debt_df)
        
        fig = px.bar(debt_df, x="name", y="amount", color="interest_rate",
                    labels={"name": "Debt", "amount": "Amount ($)", "interest_rate": "Interest Rate (%)"},
                    title="Debt Breakdown")
        st.plotly_chart(fig)
    
    if "payoff_plans" in plan:
        st.subheader("Debt Payoff Plans")
        tabs = st.tabs(["Avalanche Method", "Snowball Method", "Comparison"])
        
        with tabs[0]:
            st.markdown("### Avalanche Method (Highest Interest First)")
            if "avalanche" in plan["payoff_plans"]:
                avalanche = plan["payoff_plans"]["avalanche"]
                st.markdown(f"**Total Interest Paid**: ${avalanche['total_interest']:.2f}")
                st.markdown(f"**Time to Debt Freedom**: {avalanche['months_to_payoff']} months")
                if "monthly_payment" in avalanche:
                    st.markdown(f"**Recommended Monthly Payment**: ${avalanche['monthly_payment']:.2f}")
        
        with tabs[1]:
            st.markdown("### Snowball Method (Smallest Balance First)")
            if "snowball" in plan["payoff_plans"]:
                snowball = plan["payoff_plans"]["snowball"]
                st.markdown(f"**Total Interest Paid**: ${snowball['total_interest']:.2f}")
                st.markdown(f"**Time to Debt Freedom**: {snowball['months_to_payoff']} months")
                if "monthly_payment" in snowball:
                    st.markdown(f"**Recommended Monthly Payment**: ${snowball['monthly_payment']:.2f}")
        
        with tabs[2]:
            st.markdown("### Method Comparison")
            if "avalanche" in plan["payoff_plans"] and "snowball" in plan["payoff_plans"]:
                avalanche = plan["payoff_plans"]["avalanche"]
                snowball = plan["payoff_plans"]["snowball"]
                comparison_data = {
                    "Method": ["Avalanche", "Snowball"],
                    "Total Interest": [avalanche["total_interest"], snowball["total_interest"]],
                    "Months to Payoff": [avalanche["months_to_payoff"], snowball["months_to_payoff"]]
                }
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df)
                fig = go.Figure(data=[
                    go.Bar(name="Total Interest", x=comparison_df["Method"], y=comparison_df["Total Interest"]),
                    go.Bar(name="Months to Payoff", x=comparison_df["Method"], y=comparison_df["Months to Payoff"])
                ])
                fig.update_layout(barmode='group', title="Debt Payoff Method Comparison")
                st.plotly_chart(fig)
    
    if "recommendations" in plan:
        st.subheader("Debt Reduction Recommendations")
        for rec in plan["recommendations"]:
            st.markdown(f"**{rec['title']}**: {rec['description']}")
            if "impact" in rec:
                st.markdown(f"_Impact: {rec['impact']}_")