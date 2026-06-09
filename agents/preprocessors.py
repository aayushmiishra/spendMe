import pandas as pd
from typing import Dict, Any

def preprocess_transactions(session)->None:
    transaction=session.state.get('transaction', [])
    if not transaction:
        return
    
    df=pd.DataFrame(transaction)
    if 'Date' in df.columns:
        df['Date']=pd.to_datetime(df['Data']).dt.strftime('%Y-%m-%d')

    if 'category' in df.columns and 'Amount' in df.columns:
        category_spending=df.groupby('Category')['Amount'].sum().to_dict()
        session.state['category_spending']=category_spending
        session.state['total_spending']=df['Amount'].sum()

def preprocess_manual_expenses(session) -> None:
    manual_expenses=session.state.get('manual_expenses', {})
    if not manual_expenses or manual_expenses is None:
        return
    
    session.state.update({'total_manual_spending':sum(manual_expenses.value()), 'manual_category_spending':manual_expenses})

def create_default_results(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    monthly_income = financial_data.get("monthly_income", 0)
    expenses = financial_data.get("manual_expenses", {})
    
    if expenses is None:
        expenses = {}
    
    if not expenses and financial_data.get("transactions"):
        expenses = {}
        for transaction in financial_data["transactions"]:
            category = transaction.get("Category", "Uncategorized")
            amount = transaction.get("Amount", 0)
            expenses[category] = expenses.get(category, 0) + amount
    
    total_expenses = sum(expenses.values())
    
    return {
        "budget_analysis": {
            "total_expenses": total_expenses,
            "monthly_income": monthly_income,
            "spending_categories": [
                {"category": cat, "amount": amt, "percentage": (amt / total_expenses * 100) if total_expenses > 0 else 0}
                for cat, amt in expenses.items()
            ],
            "recommendations": [
                {"category": "General", "recommendation": "Consider reviewing your expenses carefully", "potential_savings": total_expenses * 0.1}
            ]
        },
        "savings_strategy": {
            "emergency_fund": {
                "recommended_amount": total_expenses * 6,
                "current_amount": 0,
                "current_status": "Not started"
            },
            "recommendations": [
                {"category": "Emergency Fund", "amount": total_expenses * 0.1, "rationale": "Build emergency fund first"},
                {"category": "Retirement", "amount": monthly_income * 0.15, "rationale": "Long-term savings"}
            ],
            "automation_techniques": [
                {"name": "Automatic Transfer", "description": "Set up automatic transfers on payday"}
            ]
        },
        "debt_reduction": {
            "total_debt": sum(debt.get("amount", 0) for debt in financial_data.get("debts", [])),
            "debts": financial_data.get("debts", []),
            "payoff_plans": {
                "avalanche": {
                    "total_interest": sum(debt.get("amount", 0) for debt in financial_data.get("debts", [])) * 0.2,
                    "months_to_payoff": 24,
                    "monthly_payment": sum(debt.get("amount", 0) for debt in financial_data.get("debts", [])) / 24 if sum(debt.get("amount", 0) for debt in financial_data.get("debts", [])) else 0
                },
                "snowball": {
                    "total_interest": sum(debt.get("amount", 0) for debt in financial_data.get("debts", [])) * 0.25,
                    "months_to_payoff": 24,
                    "monthly_payment": sum(debt.get("amount", 0) for debt in financial_data.get("debts", [])) / 24 if sum(debt.get("amount", 0) for debt in financial_data.get("debts", [])) else 0
                }
            },
            "recommendations": [
                {"title": "Increase Payments", "description": "Increase your monthly payments", "impact": "Reduces total interest paid"}
            ]
        }
    }