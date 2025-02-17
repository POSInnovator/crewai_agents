from crewai import Task
from typing import List, Dict
import json
from agents.agents import Agents

class Tasks:
    def __init__(self, agents: Agents):
        self.agents = agents

    def create_expense_analysis_task(self, expenses: List[Dict]) -> Task:
        return Task(
            description=f"""Analyze the provided expenses data:
            1. Categorize all expenses into meaningful groups
            2. Identify recurring spending patterns
            3. Flag unnecessary or excessive spending
            4. Calculate spending distribution by category
            5. Identify potential areas for immediate cost reduction
            
            expenses: {json.dumps(expenses)}
            
            Provide a detailed analysis with specific numbers and percentages.
            """,
            expected_output="""Provide a structured JSON response with the following format:
            {
                "category_analysis": {
                    "category_name": {
                        "total_spent": float,
                        "percentage_of_total": float,
                        "transaction_count": int,
                        "average_transaction": float
                    }
                },
                "spending_patterns": {
                    "recurring_expenses": [
                        {
                            "category": string,
                            "frequency": string,
                            "typical_amount": float
                        }
                    ],
                    "unusual_transactions": [
                        {
                            "date": string,
                            "category": string,
                            "amount": float,
                            "reason_flagged": string
                        }
                    ]
                },
                "reduction_opportunities": [
                    {
                        "category": string,
                        "potential_savings": float,
                        "recommendation": string
                    }
                ]
            }""",
            agent=self.agents.create_expense_analyst()
        )

    def create_savings_suggestion_task(self, analysis_result: str, expenses: List[Dict]) -> Task:
        return Task(
            description=f"""Based on the expense analysis, provide comprehensive savings recommendations:
            1. Identify specific areas for potential savings
            2. Suggest realistic monthly and annual savings targets
            3. Provide actionable steps to achieve savings goals
            4. Recommend specific strategies for each expense category
            5. Prioritize quick wins vs long-term savings strategies
            
            Analysis results: {analysis_result}
            Expenses : {expenses}
            
            Focus on practical, implementable suggestions with estimated savings potential.
            """,
            expected_output="""Provide the output in the JSON format only:
            {
                "savings_targets": {
                    "monthly": float,
                    "annual": float,
                    "confidence_level": string
                },
                "category_recommendations": [
                    {
                        "category": string,
                        "current_spending": float,
                        "target_spending": float,
                        "savings_strategies": [
                            {
                                "description": string,
                                "estimated_savings": float,
                                "implementation_difficulty": string,
                                "timeframe": string
                            }
                        ]
                    }
                ],
                "quick_wins": [
                    {
                        "action": string,
                        "monthly_savings": float,
                        "implementation_steps": [string]
                    }
                ],
                "long_term_strategies": [
                    {
                        "strategy": string,
                        "annual_savings": float,
                        "timeline": string,
                        "milestones": [string]
                    }
                ]
            }""",
            agent=self.agents.create_savings_advisor()
        )

    def create_goal_tracking_task(self, analysis_result: str, savings_suggestions: str) -> Task:
        return Task(
            description=f"""Create a goal tracking framework based on the analysis and recommendations:
            1. Set SMART financial goals (Specific, Measurable, Achievable, Relevant, Time-bound)
            2. Create milestone checkpoints for each goal
            3. Define success metrics and KPIs
            4. Establish a monitoring and adjustment framework
            
            Analysis: {analysis_result}
            Savings Suggestions: {savings_suggestions}
            
            Provide a structured approach to tracking and achieving financial goals.
            """,
            expected_output="""Provide a JSON response with the following format only:
            {
                "financial_goals": [
                    {
                        "goal_id": string,
                        "description": string,
                        "target_amount": float,
                        "deadline": string,
                        "category": string,
                        "milestones": [
                            {
                                "description": string,
                                "target_date": string,
                                "target_amount": float,
                                "success_criteria": string
                            }
                        ]
                    }
                ],
                "tracking_metrics": {
                    "key_performance_indicators": [
                        {
                            "metric_name": string,
                            "current_value": float,
                            "target_value": float,
                            "measurement_frequency": string,
                            "data_source": string
                        }
                    ],
                    "review_schedule": {
                        "frequency": string,
                        "next_review_date": string,
                        "review_points": [string]
                    }
                },
                "adjustment_triggers": [
                    {
                        "trigger_condition": string,
                        "threshold": float,
                        "recommended_actions": [string]
                    }
                ]
            }""",
            agent=self.agents.create_goal_specialist()
        )

    def get_all_tasks(self, expenses: List[Dict]) -> List[Task]:
        """Return all tasks in the correct sequence."""
        return [
            self.create_expense_analysis_task(expenses),
            self.create_savings_suggestion_task("{{task1.expected_output}}", expenses),
            self.create_goal_tracking_task(expenses, "{{task2.expected_output}}")
        ]