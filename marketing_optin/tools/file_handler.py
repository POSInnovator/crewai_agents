import json
import pandas as pd
from datetime import datetime
from langchain.tools import tool
from glob import glob
import os

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
    def filter_customer(filter_column="opt_in", filter_value=False):
        """
        Reads the latest available '*_filtered_customers.csv' file and applies a filter condition.
        After reading, the file is renamed to '*.csv.read'.
        The filtered data is saved as a new 'filtered_customers.csv'.
        """
        try:
            # Step 1: Find the latest file matching *_filtered_customers.csv
            file_list = glob("data/*_filtered_customers.csv")
            if not file_list:
                return "No matching files found."

            # Sort files by modification time (most recent first)
            latest_file = max(file_list, key=os.path.getmtime)

            # Step 2: Read the latest CSV file
            df = pd.read_csv(latest_file)

            # Ensure the filter column exists
            if filter_column not in df.columns:
                raise KeyError(f"Column '{filter_column}' not found in CSV file.")

            # Apply filtering
            filtered_df = df[df[filter_column] == filter_value]

            # Step 3: Save the filtered data with the same pattern
            filtered_filepath = "data/filtered_customers.csv"
            filtered_df.to_csv(filtered_filepath, index=False)

            return filtered_filepath
        except Exception as e:
            return f"Error processing file: {str(e)}"

