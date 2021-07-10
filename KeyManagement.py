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
username = st.text_input("Please key in your name")
st.sidebar.header('Choose Key Numbers which you wish to draw.')


# Create a connection object.
scope = ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('key-management-318608-1e9ed181d642.json', scope) #Change to your downloaded JSON file name
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"],
#    scopes = scope)

#conn = connect(credentials=credentials)
client = gc.authorize(credentials)
spreadsheets = ['Key Management']

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache()
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
        df_temp.columns = ['S/N', 'Name', 'Location']
        for i in range(1,len(data)):
            df_temp.loc[len(df_temp)] = data[i]

    return df_temp
    #return df_temp

#Printing of Key Status
df_temp = main(spreadsheets)
st.table(df_temp)

#Creating User Input UI for key selection
key_list = sorted(df_temp['S/N'].unique())
selected_key = st.sidebar.multiselect('S/N', key_list)
loc_list = ['Keypress','FMC','EGR Bay','Gun Bay','WO Office','MS Office','Ops Office','Project Room',' OIC Office', 'OC Office']
selected_loc = st.sidebar.multiselect('Location',loc_list)

# Creating another connection to google sheet
sheet = client.open(spreadsheets[0])
sheet.update_cell(1,1,"hello")
