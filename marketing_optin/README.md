# 📩 Email Marketing Opt-in Crew

This project leverages **CrewAI, OpenAI, and LangChain** to identify customers who haven't opted in for marketing emails. It processes customer records, applies filtering criteria, and generates a **filtered CSV file** with customers who have never opted in for marketing emails.

## 📂 Project Structure
Email-Marketing-Crew │── 📂 data │ ├── customers.json # Raw customer data (input) │ ├── YYYYMMDD_filtered_customers.csv # Processed customer data (output) │── 📂 tools │ ├── file_handler.py # File handling utilities │── main.py # CrewAI implementation │── app.py # Streamlit UI │── README.md # Documentation │── requirements.txt # Dependencies


## 🔧 Installation

1️⃣ **Clone the repository:**
```sh
git clone https://github.com/POSInnovator/crewai_agents.git
cd email-marketing-crew

How It Works
Agents & Workflow
    POSAgent → Extracts customer records from customers.json.
    MarketingAgent → Identifies customers who never opted in.
    CrewAI Process → Saves the filtered data as a CSV file (YYYYMMDD_filtered_customers.csv).
    Streamlit UI → Displays the final CSV in a table format.

Launch the Streamlit UI
 streamlit run app.py

Sample customers.json file
[
  {
    "customer_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "opt_in": false
  },
  {
    "customer_id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "opt_in": true
  }
]


