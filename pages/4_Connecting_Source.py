import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import time

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=10)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

st.dataframe(rows)
# st.experimental_rerun()

# table = st.empty()
# while True:
#      # update every 5 mins
#      table.dataframe(rows)
#      time.sleep(100)  

# # Print results.
# area_1 = st.empty()
# for row in rows:
#     area_1.write(f"{row.name} has a :{row.pet}:")
#     time.sleep(1)