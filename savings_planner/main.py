from crewai import Crew, Process
from dotenv import load_dotenv
import os
import sys
from agents.agents import Agents
from tasks.tasks import Tasks
from tools.tools import FinancialTools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    # Load environment variables
    load_dotenv()
    
    # Check for CSV file
    csv_file = "./data/expenses.csv"
    
    
    # Initialize components
    agents = Agents()
    tasks = Tasks(agents)
    tools = FinancialTools()
    
    try:
        # Load expense data from CSV
        #expenses = tools.load_from_csv(filepath=csv_file)
        expenses = tools.load_from_csv('./data/expenses.csv')
        logging.info("Successfully loaded expenses.csv file")
        
        # Create and run the crew
        crew = Crew(
            agents=agents.get_all_agents(),
            tasks=tasks.get_all_tasks(expenses),
            verbose=True,
            process=Process.sequential
        )
        
        # Execute the analysis
        result = crew.kickoff()
        
        # Print results
        logging.info("\n=== AI Savings Planner Results === %s", result)
                     

        # Calculate and display metrics
        data = {
            "expenses":[]
        }
        data["expenses"].extend(expenses)
        logging.info("\n==Calculating other mertrics %s", data)
        category_totals = tools.calculate_category_totals(data)
        daily_averages = tools.calculate_daily_averages(data)
        
        print("\n=== Expense Metrics ===")
        print("Category Totals:", category_totals)
        print("Daily Averages:", daily_averages)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: {e}")
        print("Your CSV file must contain these columns: date,category,amount,description")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()