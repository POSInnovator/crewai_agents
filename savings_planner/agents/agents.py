from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List
from tools.tools import FinancialTools

class Agents:
        
    def __init__(self):
        """
        Initializes the agent with two OpenAI GPT models.
        Attributes:
            OpenAIGPT35 (ChatOpenAI): An instance of the ChatOpenAI class using the GPT-3.5-turbo model with a temperature of 0.7.
            OpenAIGPT4 (ChatOpenAI): An instance of the ChatOpenAI class using the GPT-4 model with a temperature of 0.7.
        """

        self.OpenAIGPT35 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model="gpt-4", temperature=0.7)


    def create_expense_analyst(self) -> Agent:
        return Agent(
            role='Expense Analyst',
            goal='Analyze and categorize expenses, identifying patterns and potential savings',
            backstory="""You are an expert financial analyst specializing in personal expense analysis.
            Your expertise lies in identifying spending patterns and finding opportunities for savings.
            You have years of experience in categorizing expenses and detecting unusual spending patterns.""",
            tools=[
                FinancialTools.calculate_category_totals,
                FinancialTools.calculate_daily_averages
            ],
            llm=self.OpenAIGPT35,
            verbose=True
        )

    def create_savings_advisor(self) -> Agent:
        return Agent(
            role='Savings Advisor',
            goal='Generate actionable savings recommendations based on expense analysis',
            backstory="""You are a professional financial advisor with years of experience in helping
            people optimize their savings. You excel at creating personalized saving strategies and
            providing practical advice that leads to measurable results.""",
            tools=[
                FinancialTools.project_annual_savings
            ],
            llm=self.OpenAIGPT35,
            verbose=True
        )

    def create_goal_specialist(self) -> Agent:
        return Agent(
            role='Financial Goal Specialist',
            goal='Set and track realistic financial goals based on spending patterns and savings potential',
            backstory="""You are a goal-setting expert who specializes in creating achievable financial
            targets. You understand how to balance ambition with reality, ensuring that financial goals
            are both challenging and attainable.""",
            tools=[
                FinancialTools.project_annual_savings
            ],
            llm=self.OpenAIGPT35,
            verbose=True
        )

    def get_all_agents(self) -> List[Agent]:
        """Return all agents in the correct order for the workflow."""
        return [
            self.create_expense_analyst(),
            self.create_savings_advisor(),
            self.create_goal_specialist()
        ]