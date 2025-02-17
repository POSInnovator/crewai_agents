# AI Savings Planner

An intelligent financial assistant that analyzes spending habits, identifies savings opportunities, and helps track financial goals using Agentic AI powered by CrewAI and LangChain.

## Features

- **Automated Expense Analysis**: Categorizes spending patterns and identifies areas for optimization
- **Smart Savings Recommendations**: Generates personalized savings strategies based on spending analysis
- **Goal Setting & Tracking**: Creates and monitors SMART financial goals
- **Interactive Insights**: Provides detailed financial metrics and projections

## Project Structure

```
savings_planner/
│── agents/                 # AI agent definitions
│   ├── expense_analyzer.py # Expense analysis specialist
│   ├── savings_advisor.py  # Savings recommendation expert
│   ├── goal_setting.py    # Financial goal tracking specialist
│── tasks/                  # Task definitions for agents
│   ├── analyze_expenses.py # Expense analysis tasks
│   ├── suggest_savings.py  # Savings recommendation tasks
│   ├── track_goals.py     # Goal tracking tasks
│── tools/                  # Utility functions and helpers
│   ├── expense_loader.py  # Data loading functionality
│   ├── savings_calculator.py # Financial calculations
│── main.py                # Application entry point
│── requirements.txt       # Python dependencies
│── pyproject.toml        # Project metadata and dependencies
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

4. Run the application:
   ```bash
   python main.py
   ```

## Usage

The AI Savings Planner will:
1. Analyze your expenses and identify spending patterns
2. Generate personalized savings recommendations
3. Create and track financial goals
4. Provide detailed metrics and projections

Sample expense data is included for testing. To use your own data, modify the `ExpenseLoader` class to load your expense data in the required format.

## Contributing

Feel free to submit issues and enhancement requests!