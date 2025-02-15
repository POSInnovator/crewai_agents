from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.file_handler import FileHandlerTool


class MarketingAgent():

    """
    A class used to represent a Marketing Agent that utilizes OpenAI's GPT models to process and analyze customer data.
    Attributes
    ----------
    OpenAIGPT35 : ChatOpenAI
        An instance of the ChatOpenAI class using the GPT-3.5-turbo model with a temperature of 0.7.
    OpenAIGPT4 : ChatOpenAI
        An instance of the ChatOpenAI class using the GPT-4 model with a temperature of 0.7.
    Methods
    -------
    pos_agent():
        Creates an Agent responsible for processing customer data from JSON to CSV.
    marketing_agent():
        Creates an Agent responsible for analyzing CSV data to find customers who have never opted in for marketing.
    """
    

    def __init__(self):
        """
        Initializes the agent with two OpenAI GPT models.
        Attributes:
            OpenAIGPT35 (ChatOpenAI): An instance of the ChatOpenAI class using the GPT-3.5-turbo model with a temperature of 0.7.
            OpenAIGPT4 (ChatOpenAI): An instance of the ChatOpenAI class using the GPT-4 model with a temperature of 0.7.
        """

        self.OpenAIGPT35 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model="gpt-4", temperature=0.7)


    
    def pos_agent(self):
        """POSAgent: Reads JSON and converts it to CSV"""
        return Agent(
            role="POS Customer Data Processor",
            goal="Use the customers.json file and extracts customers data based on the filter critera and save them into CSV",
            backstory="You are responsible for processing customer data efficiently.",
            tools=[FileHandlerTool.load_json, FileHandlerTool.save_csv],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

   
    def marketing_agent(self):
        """ # MarketingAgent: Identifies customers not opted in and lists them"""
        return Agent(
            role="Marketing Data Analyst",
            goal="Analyze CSV file and find customers who has opt-in as N and save it.",
            backstory="Your job is to extract customers needing marketing emails into a CSV file.",
            tools=[FileHandlerTool.filter_customer],
            verbose=True,
            llm=self.OpenAIGPT35,
        )
