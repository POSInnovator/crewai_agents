import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
from main import EmailMarketingCrew  # Import CrewAI logic

# Streamlit UI Setup
st.set_page_config(page_title="Email Marketing Crew", layout="wide")
st.title("📩 Email Marketing Opt-in Crew")

# Description
st.markdown(
    """
    Welcome to the **Opt-in CrewAI App**!  
    This tool identifies customers who haven't opted in for marketing emails.  
    - **POSAgent**: Reads customer records from `customers.json`.  
    - **MarketingAgent**: Identifies customers who **never opted in**.  
    """
)

# Generate dynamic filename based on today's date
current_date = datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD
csv_file = f"data/{current_date}_filtered_customers.csv"

# Date range input (Passed to main.py but not used in filtering)
st.subheader("📅 Enter Customer Created Date Range")
date_range = st.text_input("Customer Created Date Range (e.g., 2024-01-01 to 2024-01-31)")

# Load full customer data (without filtering)
st.subheader("📋 Full Customer Data:")
try:
    with open("data/customers.json", "r") as file:
        customers_data = json.load(file)

    df = pd.DataFrame(customers_data)
    st.dataframe(df)  # Show the full dataset

except Exception as e:
    st.error(f"Error loading customer data: {e}")

# Placeholder for logs
log_output = st.empty()

# Run button
if st.button("🚀 Run CrewAI Process"):
    if not date_range:
        st.warning("⚠️ Please enter a valid date range.")
    else:
        log_output.text("🔄 Initializing CrewAI Process... Please wait.")
        time.sleep(1)

        # Run the CrewAI process with the entered date range
        crew = EmailMarketingCrew(date_range, "./data/customers.json")

        with st.spinner("🤖 Agents are working..."):
            time.sleep(1)
            log_output.text("🛠️ POSAgent is extracting customer data...")
            time.sleep(2)
            log_output.text("✅ POSAgent completed customer extraction!")

            log_output.text("🔍 MarketingAgent is analyzing data for opt-in status...")
            time.sleep(2)
            log_output.text("✅ MarketingAgent completed data analysis!")

            log_output.text("📂 Generating final CSV with opt-in required customers...")
            time.sleep(2)

        result = crew.run()

        # Display results
        st.success("✅ CrewAI Process Completed!")
        st.subheader("📝 CrewAI Output:")
        st.code(result, language="python")

        # Show process breakdown
        st.subheader("🔎 Detailed Process:")
        st.markdown(
            f"""
            - **Step 1**: `POSAgent` extracts full customer records from `customers.json` 📋  
            - **Step 2**: `MarketingAgent` analyzes customers who **never opted in** 🧐  
            - **Step 3**: Generates `{csv_file}` file in `data/` 📂  
            """
        )

        # Display the final filtered CSV file
        st.subheader("📂 Final Filtered Customer Data:")
        try:
            filtered_df = pd.read_csv("./data/filtered_customers.csv")
            st.dataframe(filtered_df)  # Display as a table
        except FileNotFoundError:
            st.error(f"⚠️ Filtered customer file `{csv_file}` not found.")
        except Exception as e:
            st.error(f"⚠️ Error loading filtered data: {e}")

        st.balloons()

# Footer
st.markdown("---")
st.caption("Powered by CrewAI, OpenAI & LangChain 🚀")
