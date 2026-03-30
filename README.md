🐝 Hive Row Count Agent
A high-performance Streamlit-based AI agent designed to retrieve row counts from Apache Hive. This tool uses a "Smart-Fetch" strategy: it prioritizes the Hive Metastore (metadata) for instant results and falls back to a live SELECT COUNT(*) only if statistics are unavailable or stale.

🌟 Key Features
Metadata-First approach: Retrieves counts in milliseconds for analyzed tables.

Robust Logging: Full traceability via utils/logger.py to track queries and errors.

Enterprise-Ready: Secure credential management using .env and SQL injection protection.

Interactive UI: Built with Streamlit for a seamless, user-friendly experience.

📂 Project Structure
Plaintext
hive-rowcount-agent/
├── .env                 # Secret credentials (Not committed to Git)
├── .gitignore           # Ensures security by ignoring .env and logs
├── requirements.txt     # Python dependencies
├── app.py               # Streamlit Frontend UI
├── agent_activity.log   # Auto-generated log file (managed by logger)
├── tools/
│   ├── __init__.py
│   └── hive_tool.py     # Core logic: Hive connection & counting
└── utils/
    ├── __init__.py
    └── logger.py        # Logging utility (File + Console)
🛠️ Installation & Setup
1. Clone & Navigate
First, clone the repository to your local machine or server:

Bash
git clone <your-repository-link>
cd hive-rowcount-agent
2. Environment Setup
It is highly recommended to use a virtual environment to manage dependencies:

Bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
3. Configuration
The application reads secrets from a .env file. Create this file in the root directory:

Bash
touch .env  # Or create via Notepad/VS Code
Add the following configuration to .env:

Code snippet
HIVE_HOST=your.hive.server.com
HIVE_PORT=10000
HIVE_USERNAME=your_username
HIVE_PASSWORD=your_password
HIVE_DATABASE=default
HIVE_AUTH_MECHANISM=PLAIN
🚀 Usage
Launch the agent via Streamlit:

Bash
streamlit run app.py
Enter Table Name: Provide the Hive table in the input box (e.g., sales_db.transactions).

Run Agent: Click "Run Agent." The tool will first attempt to pull numRows from the Metastore.

View Results: The count is displayed with a metric card showing the source (Metadata vs. Live Query).

Audit: You can view the last 10 lines of the execution log directly within the app expander.

⚙️ Technical Details
Smart-Fetch Logic
Validate: Checks table name against regex ^[a-zA-Z0-9._]+$ to prevent SQL injection.

Metadata Check: Executes DESCRIBE FORMATTED <table_name> to find the numRows property.

Fallback: If numRows is -1, missing, or 0, it executes a live SELECT COUNT(*).

Logging Utility
The project uses a centralized logger (utils/logger.py) that captures:

INFO: Successful connections and metadata hits.

WARNING: Fallbacks to live counts (indicates statistics need refreshing).

ERROR: Connection failures or invalid table formats.
