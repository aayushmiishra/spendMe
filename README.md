# spendME - AI Financial Coach

**spendME** is an AI‑powered financial advisor built with Google’s Agent Development Kit (ADK) and Gemini AI.  
It analyses your income, expenses, and debts, then provides personalised recommendations for budgeting, savings, and debt reduction using three specialised agents.

---

## Features

- **Multi‑Agent Analysis**  
  - *Budget Analysis Agent* – categorises spending, finds savings opportunities  
  - *Savings Strategy Agent* – builds emergency fund plans & saving automations  
  - *Debt Reduction Agent* – compares avalanche vs snowball payoff methods

- **Flexible Input**  
  - Upload CSV files (Date, Category, Amount)  
  - Manually enter expenses by category

- **Rich Visualisations**  
  - Pie charts for spending breakdown  
  - Income vs expenses bar charts  
  - Debt comparison graphs  
  - Payoff method comparison

- **Privacy First**  
  - All data stays on your machine – no external storage  
  - Secure communication with Google’s Gemini API

---

## Project Structure

```
spendME/
├── .env                         # API key 
├── app.py                       # Streamlit entry point
├── config.py                    # App constants & logging
├── agents/
│   ├── __init__.py
│   ├── finance_advisor.py       # FinanceAdvisorSystem (agents + runner)
│   └── preprocessors.py         # Data preprocessing helpers
├── schema/                      # Pydantic models (renamed to avoid circular imports)
│   ├── __init__.py
│   ├── budget.py
│   ├── savings.py
│   └── debt.py
├── utils/
│   ├── __init__.py
│   ├── csv_parser.py            # CSV validation & parsing
│   ├── display_helpers.py       # Plotly + Streamlit output functions
│   └── json_helpers.py          # Safe JSON parsing
└── ui/
    ├── __init__.py
    ├── sidebar.py               # API key notice & CSV template download
    ├── input_tabs.py            # User input forms (income, expenses, debts)
    └── results_tabs.py          # Display analysis results
```

<!-- ## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/aayushmiishra/spendME.git
cd spendME

2. Create a virtual enviroment

python -m venv .venv
.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Set up your Gemini API key

GOOGLE_API_KEY=your_actual_gemini_api_key_here

5. Run the app

streamlit run app.py -->