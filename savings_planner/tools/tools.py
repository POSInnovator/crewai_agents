from typing import List, Dict
import csv
from datetime import datetime
from collections import defaultdict
from langchain.tools import tool
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class FinancialTools:

    @tool("load_csv_data")
    def load_from_csv(filepath: str) -> List[Dict]:
        """Load and validate expense data from a CSV file.
        
        Args:
            filepath (str): Path to the CSV file containing expense data
            
        Returns:
            List[Dict]: List of validated expense records
            
        The CSV file must have the following columns:
        - date: Date in YYYY-MM-DD format
        - category: Expense category
        - amount: Numeric amount
        - description: Transaction description
        """
        expenses = []
        try:
            with open(filepath, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Validate and convert amount to float
                    try:
                        amount = float(row['amount'])
                    except ValueError:
                        print(f"Warning: Invalid amount '{row['amount']}' in row {reader.line_num}")
                        continue

                    # Validate date format
                    try:
                        datetime.strptime(row['date'], '%Y-%m-%d')
                    except ValueError:
                        print(f"Warning: Invalid date format '{row['date']}' in row {reader.line_num}")
                        continue

                    expense = {
                        'date': row['date'],
                        'category': row['category'],
                        'amount': amount,
                        'description': row['description']
                    }
                    expenses.append(expense)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        except KeyError as e:
            raise KeyError(f"Missing required column: {e}")

        expenses = sorted(expenses, key=lambda x: x['date'])
        return expenses

    @tool("calculate_category_totals")
    def calculate_category_totals(expenses: List[Dict]) -> Dict[str, float]:
        """Calculate the total spending for each expense category.
        
        Args:
            expenses (List[Dict]): List of expense records
            
        Returns:
            Dict[str, float]: Dictionary mapping categories to their total amounts
        """
        totals = defaultdict(float)
        for expense in expenses:
            totals[expense["category"]] += expense["amount"]
        
        return dict(totals)

    @tool("calculate_daily_averages")
    def calculate_daily_averages(expenses: List[Dict]) -> Dict[str, float]:
        """Calculate the average daily spending for each category.
        
        Args:
            expenses (List[Dict]): List of expense records
            
        Returns:
            Dict[str, float]: Dictionary mapping categories to their daily average spending
        """
        category_totals = defaultdict(float)
        category_counts = defaultdict(int)
        
        for expense in expenses:
            category = expense["category"]
            category_totals[category] += expense["amount"]
            category_counts[category] += 1
        
        averages = {
            category: total / count
            for category, total in category_totals.items()
            for count in [category_counts[category]]
        }
        
        return averages

    @tool("project_annual_savings")
    def project_annual_savings(reduction_targets: Dict[str, float], 
                               expenses: List[Dict]) -> float:
        """Project potential annual savings based on reduction targets for each category.
        
        Args:
            reduction_targets (Dict[str, float]): Percentage reduction targets per category
            expenses (List[Dict]): List of expense records
            
        Returns:
            float: Projected annual savings amount
        """
       
        #logging.info("Received reduction_targets: %s", type(reduction_targets))
        #logging.info("Received expenses: %s", type(expenses))
        logging.info("Received expenses: %s", expenses)
        
        data = {
            "expenses":[]
        }
        data["expenses"].extend(expenses)
        category_totals = FinancialTools.calculate_category_totals(data)
        
        # Calculate potential savings
        total_savings = 0
        for category, target in reduction_targets.items():
            if category in category_totals:
                savings = category_totals[category] * (target / 100)
                total_savings += savings
        
        # Extrapolate to annual savings
        days_in_data = len(set(expense["date"] for expense in data['expenses']))
        annual_savings = (total_savings / days_in_data) * 365

        logging.info("annual_savings==>: %s", annual_savings)
        return round(annual_savings, 2)
