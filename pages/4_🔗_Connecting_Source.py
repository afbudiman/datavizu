import streamlit as st 
from pandas import DataFrame
from gspread_pandas import Spread,Client
from google.oauth2 import service_account
import pandas as pd

st.set_page_config(page_title="Connecting Demo", page_icon=":link:")

scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes=scope)
client = Client(scope=scope, creds=credentials)
spreadsheetname = "streamlit"
spread = Spread(spreadsheetname, client=client)

sh = client.open(spreadsheetname)
# worksheet_list = sh.worksheets()

worksheet = sh.worksheet('Sheet1')

st.header('Connecting Streamlit Application to Data Source')

st.markdown(
    '''The sample spreadsheet can be found [here](https://docs.google.com/spreadsheets/d/1pNlChcOvhuFRCG_iAETraJRf0s1M4uMpaX6J1uNRqpg)
''')

df = DataFrame(worksheet.get_all_records())
table = st.table(df)

st.sidebar.header('Update Data')

with st.sidebar.form(key='my_form', clear_on_submit=True):
    name = st.text_input(label='Name')
    pet = st.text_input(label='Pet')
    add = st.form_submit_button(label='add')

    if add:
        row = []
        row.append([name, pet])
        new_df = pd.DataFrame(row, columns=['name','pet'])
        table.add_rows(new_df)
        df1 = pd.concat([df, new_df])
        spread.df_to_sheet(df1, sheet='Sheet1', index = False)