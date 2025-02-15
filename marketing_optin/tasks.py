from crewai import Task
from textwrap import dedent



class MarketingTask():


    def extract_customers_task(self, agent, date_range, customers):
        """
        Extract customer records from JSON based on the given date range and save them as a CSV file.
        Args:
            agent (str): The agent responsible for the task.
            date_range (str): The date range for extracting customer records.
        Returns:
            Task: A Task object with the description and expected output.
        """
  
        return Task(
                    description="""Load the {} file from the data folder and apply filter on the created date 
                    which should be within date range {} provided.""".format(customers,date_range) ,
                    agent=agent,
                    expected_output="""A CSV file containing all the fileds in the original file but should only have filtered records matching the
                    criteria.""",
           
                )

    def identify_opt_out_customers(self, agent):
        """
        Identifies customers who never opted in for marketing and stores the information in a CSV file.

        Args:
            agent: The agent responsible for performing the task.

        Returns:
            Task: A Task object with a description of the task and the expected output.
        """
  
        return Task(
                    description="Using the CSV file from the extract_customers_task task find records which have opt_in as N and store in the CSV.",
                    agent=agent,
                    expected_output="A CSV file listing customers needing marketing emails.",
        )
