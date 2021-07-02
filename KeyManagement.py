import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import urllib
import csv
from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
from PIL import Image
import time
import plotly as pp
import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
from gspread_pandas import Spread,Client

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
st.secrets["gcp_service_account"],
scopes=[
"https://www.googleapis.com/auth/spreadsheets",
],
)
client = Client(scope = "https://www.googleapis.com/auth/spreadsheets", creds = credentials)
spreadsheetname = "Sheet1"
spread = Spread(spreadsheetname,client=client)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()
#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")

#---------------------------------#
# Title

image = Image.open('photo_keys-on-wooden-background.jpg')

st.image(image, width = 500)
st.title('Key Management App')

st.markdown("""
**AWOF 805 Key Status.**
""")

st.sidebar.header('User Input Features')

# Web scraping of data.gov.sg data
#
#@st.cache(persist=True,show_spinner = True)
#def load_data():

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")
