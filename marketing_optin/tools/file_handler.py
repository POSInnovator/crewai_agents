import json
import pandas as pd
from datetime import datetime
from langchain.tools import tool

class FileHandlerTool():

    @tool("Load the JSON file from the path")
    def load_json(filepath):
        """
        Loads the JSON file provided in the data folder.
        """
        with open(filepath, 'r') as file:
            return json.load(file)

    @tool("Save the data in the CSV file")
    def save_csv(customers, filename_prefix="filtered_customers"):
        """
        Extracts data from JSON and saves it into a CSV file.
        The filename follows the pattern: YYYYMMDD_HHMMSS_filename_prefix.csv.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
        filepath = f"data/{timestamp}_{filename_prefix}.csv"
        
        # Ensure customers is a valid DataFrame
        if isinstance(customers, list) and all(isinstance(c, dict) for c in customers):
            df = pd.DataFrame(customers)
        elif isinstance(customers, pd.DataFrame):
            df = customers
        else:
            raise ValueError("Invalid format: 'customers' should be a list of dictionaries or a DataFrame.")

        df.to_csv(filepath, index=False)
        return filepath

    @tool("Filter customer data based on conditions")
    def filter_customer(csv_filepath="data/customer.csv", filter_column="opt_in", filter_value=False):
        """
        Reads 'customer_data.csv' and applies a filter condition.
        The filtered data is saved as 'filtered_customers.csv'.
        """
        try:
            df = pd.read_csv(csv_filepath)

            # Ensure the filter column exists
            if filter_column not in df.columns:
                raise KeyError(f"Column '{filter_column}' not found in CSV file.")

            # Apply filtering
            filtered_df = df[df[filter_column] == filter_value]

            # Save filtered data
            filtered_filepath = "data/filtered_customers.csv"
            filtered_df.to_csv(filtered_filepath, index=False)

            return filtered_filepath
        except Exception as e:
            return f"Error processing file: {str(e)}"
