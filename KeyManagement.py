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

st.image(image, width = 800)
st.title('AWOF Key Management App v1.0')
st.markdown('Please follow the sequence of instructions stated below and refer to the Overall Key Status below for an overview.')

txt = st.text_area('Instructions', '''
     1) Select either Withdraw or return. \n
     2) If Withdraw is selected, please indicate your Name, Key Nos and Location which it is drawn to. \n
     3) If Return is selected, please indicate your Name and Key Nos (Location is automatically set to Keypress). \n
     4) Click on Submit to register the changes in the main database. \n
     5) Check the Overall Key Status at the bottom of the web app for an overview.
     ''')
#Creating User Input UI for key selection
key_list = list(range(1,68))

decision = st.radio(
    "Would you like to withdraw or return the keys?",
    ('Withdraw', 'Return'))
with st.form("Details"):
    if decision == 'Withdraw':
        username = st.text_input("Please key in your name")
        selected_key = st.multiselect('Please select the key(s)', key_list)
        selected_keylist = list(selected_key)
        loc_list = ['FMC','EGR Bay','Gun Bay','WO Office','MS Office','Ops Office','Project Room',' OIC Office', 'OC Office']
        selected_loc = st.selectbox('Which location is/are the key(s) drawn to?',loc_list)
    else:
        username = st.text_input("Please key in your name")
        selected_key = st.multiselect('Please select the key(s)', key_list)
        selected_keylist = list(selected_key)
        selected_loc = ['Keypress']
    st.form_submit_button(label='Submit',help='Press to confirm details')



# Create a connection object.
scope = ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']
#credentials = ServiceAccountCredentials.from_json_keyfile_name('key-management-318608-1e9ed181d642.json', scope) #Change to your downloaded JSON file name
credentials = service_account.Credentials.from_service_account_info(st.secrets['gcp_service_account'], scopes = scope)

conn = connect(credentials=credentials)
client = gc.authorize(credentials)
spreadsheets = ['Key Management']

#@st.cache(suppress_st_warning=True)
def display(spreadsheets):
    for spreadsheet in spreadsheets:
        sh=client.open(spreadsheet)
        worksheet = sh.get_worksheet(0)
        data = worksheet.get_all_values()
        df_temp = pd.DataFrame(columns = [i for i in range(len(data[0]))])
        df_temp.columns = ['Key No.','Name','Location']
        for i in range(1,len(data)):
            df_temp.loc[len(df_temp)] = data[i]

    return df_temp
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(suppress_st_warning=True)
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
                worksheet.update_cell(keynum+1,3,selected_loc)

        data = worksheet.get_all_values()
        #Save the data inside the temporary pandas dataframe
        df_temp = pd.DataFrame(columns = [i for i in range(len(data[0]))])
        df_temp.columns = ['Key No.','Name','Location']
        for i in range(1,len(data)):
            df_temp.loc[len(df_temp)] = data[i]

    return df_temp
    #return df_temp

#Printing/Updating of Key Status
if username != '':
    df_temp = main(spreadsheets)
else :
    df_temp = display(spreadsheets)

#Plotting of Illustration of Key locations
fig,ax = plt.subplots(figsize = (5,8))
plt.rcParams["font.family"] = "comic sans"
fig.patch.set_facecolor('xkcd:turquoise')
ax.set_facecolor('azure')
ax.scatter(df_temp['Location'], df_temp['Key No.'], c = 'black', edgecolors = 'none', s = 20)
ax.set_title('Illustration of Keys in various Locations')
ax.set_xlabel('Location')
ax.set_ylabel('Key No.')
ax.tick_params(axis = 'x', labelsize = 7)
ax.tick_params(axis = 'y',labelsize = 5)
#For secondary axes
ax2 = ax.twinx()
ax2.scatter(df_temp['Location'], df_temp['Key No.'], c = 'black', edgecolors = 'none', s = 20)
ax2.tick_params(axis = 'y',labelsize = 5)
plt.grid(color = 'lightgray', linestyle = '-.', linewidth = 0.5)
st.pyplot(fig)

#Illustration of Overview
st.table(df_temp)

