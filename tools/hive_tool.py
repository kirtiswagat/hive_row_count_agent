import os
import re
from pyhive import hive
from dotenv import load_dotenv
from utils.logger import agent_logger

load_dotenv()

def get_hive_row_count(table_name: str):
    # 1. Validation
    if not re.match(r"^[a-zA-Z0-9._]+$", table_name):
        agent_logger.error(f"Malicious or invalid table name: {table_name}")
        return "Error: Invalid table name format."

    agent_logger.info(f"Starting row count request for: {table_name}")
    conn = None
    try:
        conn = hive.Connection(
            host=os.getenv("HIVE_HOST"),
            port=int(os.getenv("HIVE_PORT", 10000)),
            username=os.getenv("HIVE_USERNAME"),
            password=os.getenv("HIVE_PASSWORD"),
            database=os.getenv("HIVE_DATABASE", "default"),
            auth=os.getenv("HIVE_AUTH_MECHANISM", "PLAIN")
        )
        cursor = conn.cursor()

        # 2. Strategy A: Check Metastore
        agent_logger.info(f"Querying Hive Metastore for {table_name}")
        cursor.execute(f"DESCRIBE FORMATTED {table_name}")
        results = cursor.fetchall()
        
        for row in results:
            if row[0] and 'numRows' in str(row[0]):
                count_val = str(row[1]).strip()
                if count_val and count_val != "-1":
                    agent_logger.info(f"Metadata match found: {count_val}")
                    return f"Metadata: {int(count_val):,}"

        # 3. Strategy B: Live Fallback
        agent_logger.warning(f"Metadata missing for {table_name}. Running live SELECT COUNT.")
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        return f"Live Query: {count:,}"

    except Exception as e:
        agent_logger.error(f"Database error: {str(e)}")
        return f"Hive Error: {str(e)}"
    finally:
        if conn:
            conn.close()