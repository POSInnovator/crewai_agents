from crewai import Crew
from agents import MarketingAgent
from tasks import MarketingTask
from dotenv import load_dotenv

load_dotenv()

class EmailMarketingCrew():

    def __init__(self, date_range, customers_file):
        self.date_range = date_range
        self.customers_file = customers_file

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = MarketingAgent()
        tasks = MarketingTask()

        # Define your custom agents and tasks here
        pos_agent = agents.pos_agent()
        marketing_agent = agents.marketing_agent()

        # Custom tasks include agent name and variables as input
        extract_customers_task = tasks.extract_customers_task(
            pos_agent,
            self.date_range,
            self.customers_file
        )

        identify_opt_out_customers = tasks.identify_opt_out_customers(
            marketing_agent,
        )

        # Define your custom crew here
        crew = Crew(
            agents=[
                    pos_agent, 
                    marketing_agent
                ],
            tasks=[
                    extract_customers_task, 
                    identify_opt_out_customers,
                ],
            verbose=True,
        )

        result = crew.kickoff()
        return result

# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to Optin Crew")
    print("-------------------------------")
    customers = "./data/customers.json"
    date_range = input("What is customer created date range? ")
    trip_crew = EmailMarketingCrew(date_range, customers)
    result = trip_crew.run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)


