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
from oauth2client.service_account import ServiceAccountCredentials
from gsheetsdb import connect
from gspread_pandas import Spread,Client
import gspread as gc
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


# Create a connection object.
scope = ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']
#credentials = ServiceAccountCredentials.from_json_keyfile_name('key-management-318608-1e9ed181d642.json', scopes = scope) #Change to your downloaded JSON file name
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes = scope)

conn = connect(credentials=credentials)
client = gc.authorize(credentials)
spreadsheets = ['Key Management']
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def main(spreadsheets):
	df = pd.DataFrame()
	for spreadsheet in spreadsheets:
		#Open the Spreadsheet
		sh = client.open(spreadsheet)

		#Get all values in the first worksheet
		worksheet = sh.get_worksheet(0)
		data = worksheet.get_all_values()

		#Save the data inside the temporary pandas dataframe
		df_temp = pd.DataFrame(columns = [i for i in range(len(data[0]))])
		for i in range(1,len(data)):
			df_temp.loc[len(df_temp)] = data[i]

    #return df_temp

df_temp = main(spreadsheets)
st.dataframe(df_temp)
#def run_query(query):
#    rows = conn.execute(query, headers=3)
#    return rows

#sheet_url = st.secrets["private_gsheets_url"]
#rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
#for row in rows:
#    st.write(f"{row.number} has a :{row.name}:")
