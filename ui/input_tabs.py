import streamlit as st
import pandas as pd
from typing import Dict, Any, Tuple
from utils.csv_parser import validate_csv_format, parse_csv_transactions, display_csv_preview

def render_input_form() -> Tuple[Dict[str, Any], bool]:
    """
    Renders the input form for financial data.
    Returns a tuple: (financial_data, analyze_clicked)
    """
    financial_data = {
        "monthly_income": 0.0,
        "dependants": 0,
        "transactions": None,
        "manual_expenses": {},
        "debts": []
    }
    
    st.header("Enter Your Financial Information")
    st.caption("All data is processed locally and not stored anywhere.")
    
    # Income & Household
    with st.container():
        st.subheader("Income & Household")
        income_col, dependants_col = st.columns([2, 1])
        with income_col:
            monthly_income = st.number_input(
                "Monthly Income ($)",
                min_value=0.0,
                step=100.0,
                value=3000.0,
                key="income",
                help="Enter your total monthly income after taxes"
            )
        with dependants_col:
            dependants = st.number_input(
                "Number of Dependants",
                min_value=0,
                step=1,
                value=0,
                key="dependants",
                help="Include all dependants in your household"
            )
    
    st.divider()
    
    # Expenses
    with st.container():
        st.subheader("Expenses")
        expense_option = st.radio(
            "How would you like to enter your expenses?",
            ("Upload CSV Transactions", "Enter Manually"),
            key="expense_option",
            horizontal=True
        )
        
        transactions_df = None
        manual_expenses = {}
        use_manual_expenses = False
        
        if expense_option == "Upload CSV Transactions":
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                #### Upload your transaction data
                Your CSV file should have these columns:
                - Date (YYYY-MM-DD)
                - Category
                - ₹ Amount
                """)
                transaction_file = st.file_uploader(
                    "Choose your CSV file",
                    type=["csv"],
                    key="transaction_file",
                    help="Upload a CSV file containing your transactions"
                )
            
            if transaction_file is not None:
                is_valid, message = validate_csv_format(transaction_file)
                if is_valid:
                    try:
                        transaction_file.seek(0)
                        file_content = transaction_file.read()
                        parsed_data = parse_csv_transactions(file_content)
                        transactions_df = pd.DataFrame(parsed_data['transactions'])
                        display_csv_preview(transactions_df, st)
                        st.success("Transaction file uploaded and validated successfully!")
                    except Exception as e:
                        st.error(f"Error processing CSV file: {str(e)}")
                        transactions_df = None
                else:
                    st.error(message)
                    transactions_df = None
        else:
            use_manual_expenses = True
            st.markdown("#### Enter your monthly expenses by category")
            categories = [
                ("Housing", "Housing"),
                ("Utilities", "Utilities"),
                ("Food", "Food"),
                ("Transportation", "Transportation"),
                ("Healthcare", "Healthcare"),
                ("Entertainment", "Entertainment"),
                ("Personal", "Personal"),
                ("Savings", "Savings"),
                ("Other", "Other")
            ]
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
            for i, (emoji_cat, cat) in enumerate(categories):
                with cols[i % 3]:
                    manual_expenses[cat] = st.number_input(
                        emoji_cat,
                        min_value=0.0,
                        step=50.0,
                        value=0.0,
                        key=f"manual_{cat}",
                        help=f"Enter your monthly {cat.lower()} expenses"
                    )
            
            if manual_expenses and any(manual_expenses.values()):
                st.markdown("#### Summary of Entered Expenses")
                manual_df_disp = pd.DataFrame({
                    'Category': list(manual_expenses.keys()),
                    'Amount': list(manual_expenses.values())
                })
                manual_df_disp = manual_df_disp[manual_df_disp['Amount'] > 0]
                if not manual_df_disp.empty:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.dataframe(
                            manual_df_disp,
                            column_config={
                                "Category": "Category",
                                "Amount": st.column_config.NumberColumn("Amount", format="$%.2f")
                            },
                            hide_index=True
                        )
                    with col2:
                        st.metric("Total Monthly Expenses", f"${manual_df_disp['Amount'].sum():,.2f}")
    
    st.divider()
    
    # Debt Information
    with st.container():
        st.subheader("Debt Information")
        st.info("Enter your debts to get personalized payoff strategies using both avalanche and snowball methods.")
        num_debts = st.number_input(
            "How many debts do you have?",
            min_value=0,
            max_value=10,
            step=1,
            value=0,
            key="num_debts"
        )
        debts = []
        if num_debts > 0:
            cols = st.columns(min(num_debts, 3))
            for i in range(num_debts):
                col_idx = i % 3
                with cols[col_idx]:
                    st.markdown(f"##### Debt #{i+1}")
                    debt_name = st.text_input("Name", value=f"Debt {i+1}", key=f"debt_name_{i}")
                    debt_amount = st.number_input("Amount ($)", min_value=0.01, step=100.0, value=1000.0, key=f"debt_amount_{i}")
                    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1, value=5.0, key=f"debt_rate_{i}")
                    min_payment = st.number_input("Minimum Payment ($)", min_value=0.0, step=10.0, value=50.0, key=f"debt_min_payment_{i}")
                    debts.append({
                        "name": debt_name,
                        "amount": debt_amount,
                        "interest_rate": interest_rate,
                        "min_payment": min_payment
                    })
                    if col_idx == 2 or i == num_debts - 1:
                        st.markdown("---")
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button("Analyze My Finances", key="analyze_button", use_container_width=True)
    
    financial_data.update({
        "monthly_income": monthly_income,
        "dependants": dependants,
        "transactions": transactions_df.to_dict('records') if transactions_df is not None else None,
        "manual_expenses": manual_expenses if use_manual_expenses else None,
        "debts": debts
    })
    
    # For CSV upload path, ensure we know if manual was used
    financial_data["_use_manual_expenses"] = use_manual_expenses
    financial_data["_transactions_df"] = transactions_df
    
    return financial_data, analyze_clicked