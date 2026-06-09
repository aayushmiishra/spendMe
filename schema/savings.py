from typing import List, Optional
from pydantic import BaseModel, Field

class EmergencyFund(BaseModel):
    recommended_amount: float=Field(..., description='size of recommended fund')
    current_amount: float=Field(..., description='current emergency fund')
    current_status: str=Field(..., description='Status assessment')

class SavingsRecommendation(BaseModel):
    category: str=Field(...,description='Savings category')
    amount: float=Field(..., description='Recommended monthly amount')
    rationale: Optional[str]=Field(None, description='Explanation for this recommendation')

class AutomationTechnique(BaseModel):
    name: str=Field(..., description='Name of automation technique')
    description: str = Field(..., description='Details of how to implement')

class SavingsStrategy(BaseModel):
    emergency_fund: EmergencyFund = Field(..., description='Emergency fund recommendation')
    recommendations: List[SavingsRecommendation] = Field(..., description='Savings allocation recommendations')
    automation_techniques: Optional[List[AutomationTechnique]] = Field(None, description='Automation techniques to help save')