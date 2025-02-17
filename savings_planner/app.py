import streamlit as st
import pandas as pd
import logging
from crewai import Crew, Process
from dotenv import load_dotenv
from agents.agents import Agents
from tasks.tasks import Tasks
from tools.tools import FinancialTools
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    

def main():
    load_dotenv()
    csv_file = "./data/expenses.csv"
    agents = Agents()
    tasks = Tasks(agents)
    tools = FinancialTools()
    
    try:
        # Load expense data from CSV
        expenses = tools.load_from_csv(csv_file)
        logging.info("Successfully loaded expenses.csv file")

        st.title("AI-Powered Savings Planner")
        st.subheader("📊 Expenses Data")
        df_expenses = pd.DataFrame(expenses)
        st.dataframe(df_expenses)

        if st.button("Run AI Analysis"):  # Wait for user to trigger agent execution
            st.info("🤖 Agents are being activated...")
            
             # Create and run the crew
            crew = Crew(
                agents=agents.get_all_agents(),
                tasks=tasks.get_all_tasks(expenses),
                verbose=True,
                process=Process.sequential
            )
            
            # Execute the analysis
            result = crew.kickoff()
            print(dir(result))
            logging.info("=== result ===  %s", result)
            logging.info("=== dir(result) ===  %s", dir(result))

            # Extract financial goals
                    
            logging.info("CrewAI Analysis Completed")
            st.success("✅ AI Analysis Completed!")
                   
            data = {
                "expenses": []
            }
            data["expenses"].extend(expenses)
            category_totals = tools.calculate_category_totals(data)
            daily_averages = tools.calculate_daily_averages(data)
                
            st.subheader("🤖 CrewAI Analysis Results")
            
            logging.info("=== AI Savings Planner Results ===  %s", result)
            st.json(result)
            
            st.subheader("💰 Category Totals")
            st.table(category_totals)
            
            st.subheader("📅 Daily Averages")
            st.table(daily_averages)
            
    except FileNotFoundError as e:
        st.error(f"Error: {e}")
    except KeyError as e:
        st.error(f"Error: {e}. Your CSV file must contain columns: date, category, amount, description.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
