import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from config import APP_NAME, USER_ID, logger
from schema.budget import BudgetAnalysis         
from schema.savings import SavingsStrategy       
from schema.debt import DebtReduction            
from agents.preprocessors import preprocess_transactions, preprocess_manual_expenses, create_default_results
from utils.json_helpers import parse_json_safely

class FinanceAdvisorSystem:
    def __init__(self):
        self.session_service=InMemorySessionService()
        self.budget_analysis_agent=LlmAgent(
            name='BudgetAnalysisAgent',
            model='gemini-2.5-flash',
            description='Analyzes financial data to categorize spending patterns and recomment budget improvements',
            instruction='''You are a Budget Analysis Agent specialised in reviewing financial transactions and expenses'''
        )

async def analyze_finances(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
    session_id = f"finance_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        initial_state = {
            "monthly_income": financial_data.get("monthly_income", 0),
            "dependants": financial_data.get("dependants", 0),
            "transactions": financial_data.get("transactions", []),
            "manual_expenses": financial_data.get("manual_expenses", {}),
            "debts": financial_data.get("debts", [])
        }
        
        session = self.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state=initial_state
        )
        
        if session.state.get("transactions"):
            preprocess_transactions(session)
        
        if session.state.get("manual_expenses"):
            preprocess_manual_expenses(session)
        
        default_results = create_default_results(financial_data)
        
        user_content = types.Content(
            role='user',
            parts=[types.Part(text=json.dumps(financial_data))]
        )
        
        async for event in self.runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=user_content
        ):
            if event.is_final_response() and event.author == self.coordinator_agent.name:
                break
        
        updated_session = self.session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )
        
        results = {}
        for key in ["budget_analysis", "savings_strategy", "debt_reduction"]:
            value = updated_session.state.get(key)
            results[key] = parse_json_safely(value, default_results[key]) if value else default_results[key]
        
        return results
        
    except Exception as e:
        logger.exception(f"Error during finance analysis: {str(e)}")
        raise
    finally:
        self.session_service.delete_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )