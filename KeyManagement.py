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

st.sidebar.header('Select the Keys and Location it is drawn to.')

#Creating User Input UI for key selection
#key_list = sorted(df_temp['S/N'].unique())

with st.form("Details"):
    username = st.text_input("Please key in your name")
    st.form_submit_button(label='Submit',help='Press to confirm details')

if username == None:
    print("Missing username.")
else:
    key_list = list(range(1,68))
    selected_key = st.sidebar.multiselect('S/N', key_list)
    selected_keylist = list(selected_key)
    loc_list = ['Keypress','FMC','EGR Bay','Gun Bay','WO Office','MS Office','Ops Office','Project Room',' OIC Office', 'OC Office']
    selected_loc = st.sidebar.multiselect('Location',loc_list)



# Create a connection object.
scope = ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']
#credentials = ServiceAccountCredentials.from_json_keyfile_name('key-management-318608-1e9ed181d642.json', scope) #Change to your downloaded JSON file name
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes = scope)

conn = connect(credentials=credentials)
client = gc.authorize(credentials)
spreadsheets = ['Key Management']

@st.cache()
def display(spreadsheets):
    for spreadsheet in spreadsheets:
        sh=client.open(spreadsheet)
        worksheet = sh.get_worksheet(0)
        data = worksheet.get_all_values()
        df_temp = pd.DataFrame(columns = [i for i in range(len(data[0]))])
        df_temp.columns = ['S/N','Name','Location']
        for i in range(1,len(data)):
            df_temp.loc[len(df_temp)] = data[i]

    return df_temp
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
        #Updating Google Sheet
        for keynum in selected_keylist:
            worksheet.update_cell(keynum+1,2,username)
            if not selected_loc:
                break
            else :
                worksheet.update_cell(keynum+1,3,selected_loc[0])

        data = worksheet.get_all_values()
        #Save the data inside the temporary pandas dataframe
        df_temp = pd.DataFrame(columns = [i for i in range(len(data[0]))])
        df_temp.columns = ['S/N','Name','Location']
        for i in range(1,len(data)):
            df_temp.loc[len(df_temp)] = data[i]

    return df_temp
    #return df_temp

#Printing/Updating of Key Status
if username != '':
    df_temp = main(spreadsheets)
else :
    df_temp = display(spreadsheets)
st.table(df_temp)
