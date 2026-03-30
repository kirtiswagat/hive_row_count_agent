import streamlit as st
import time
from tools.hive_tool import get_hive_row_count
from utils.logger import agent_logger

st.set_page_config(page_title="Hive Agent", page_icon="🐝")

st.title("🐝 Hive Row Count Agent")
st.info("Agentic tool to fetch record counts from Hive via Metastore or Live Query.")

table_query = st.text_input("Enter Table Name (e.g. db_name.table_name)")

if st.button("Run Agent", type="primary"):
    if table_query:
        with st.spinner("Agent is communicating with Hive..."):
            start = time.time()
            result = get_hive_row_count(table_query)
            end = time.time()
            
            if "Error" in result:
                st.error(result)
            else:
                st.success("Analysis Complete!")
                source, value = result.split(": ")
                st.metric(label=f"Row Count ({source})", value=value)
                st.caption(f"Execution time: {round(end - start, 2)} seconds")
                agent_logger.info(f"UI successfully displayed {value} for {table_query}")
    else:
        st.warning("Please enter a table name.")

st.divider()
with st.expander("View Recent Activity Log"):
    if os.path.exists("agent_activity.log"):
        with open("agent_activity.log", "r") as f:
            st.code(f.readlines()[-10:]) # Show last 10 lines