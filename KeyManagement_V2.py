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
st.set_page_config(
    page_title="Key Management App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")

#from SessionState import get

#session_state = get(password='')

#if session_state.password != 'pwd123':
#    pwd_placeholder = st.empty()
#    pwd = pwd_placeholder.text_input("Password:", value="", type="password")
#    session_state.password = pwd
#    if session_state.password == 'pwd123':
#        pwd_placeholder.empty()
#        main()
#    else:
#        st.error("the password you entered is incorrect")
#else:
#    main()

# Create a connection object with googlesheets API
scope = ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('key-management-318608-1e9ed181d642.json', scope) #Change to your downloaded JSON file name
#credentials = service_account.Credentials.from_service_account_info(st.secrets['gcp_service_account'], scopes = scope)

conn = connect(credentials=credentials)
client = gc.authorize(credentials)
spreadsheets = ['Key Management']

#@st.cache(suppress_st_warning=True)
#Solely for displaying the data

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


#@st.cache(suppress_st_warning=True)
#For updating the database
def main(spreadsheets):
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

#Refresh database with new data
def refresh(spreadsheets):
    for spreadsheet in spreadsheets:
        #Open the Spreadsheet
        sh = client.open(spreadsheet)
        #Get all values in the first worksheet
        worksheet = sh.get_worksheet(0)
        key_list = list(range(1,71))
        location = ['Keypress' for i in range(1,71)]
        username = ['Admin' for i in range(1,71)]
        df_temp = pd.DataFrame(
                {'Key No.': key_list,
                'Name': username,
                'Location': location})
        worksheet.update([df_temp.columns.values.tolist()] + df_temp.values.tolist())
        data = worksheet.get_all_values()
        #Save the data inside the temporary pandas dataframe
        df_temp = pd.DataFrame(columns = [i for i in range(len(data[0]))])
        df_temp.columns = ['Key No.','Name','Location']
        for i in range(1,len(data)):
            df_temp.loc[len(df_temp)] = data[i]
    return df_temp
#---------------------------------#
# Title

#image = Image.open('photo_keys-on-wooden-background.jpg')

#st.image(image, width = 800)
st.title('AWOF Key Management App v1.2')
st.markdown('Please follow the sequence of instructions stated below and refer to the Overall Key Status below for an overview.')

with st.beta_expander("🧙 Click here for more instructions on how to use this app 🔮"):
    st.markdown('''
     <p>1. Select either 'Withdraw' or 'Return'.
     <p>2. If Withdraw is selected, please indicate your Name, Key Nos and Location which it is drawn to.
     <p>3. If Return is selected, please indicate your Name and Key Nos (Location is automatically set to Keypress).
     <p>4. If Hard Reset is selected, you do not need to key in your name and Key Nos as all keys are returned to Keypress.
     <p>5. Click on Submit to register the changes in the main database.
     <p>6. Check the Overall Key Status at the bottom of the web app for an overview.
     ''',unsafe_allow_html = True)
#Creating User Input UI for key selection
key_list = list(range(1,71))

#Deciding question to dictate form
decision = st.radio(
    "Would you like to withdraw or return the keys?",
    ('Withdraw', 'Return'))
if decision == 'Withdraw':
    #Set up placeholder widget
    withdraw_form = st.empty()
    with withdraw_form.form("Details"):
        username = st.text_input("Please key in your name")
        selected_key = st.multiselect('Please select the key(s)', key_list)
        selected_keylist = list(selected_key)
        loc_list = ['FMC','EGR Bay','Gun Bay','WO Office','MS Office','Ops Office','Project Room','OIC Office', 'OC Office']
        selected_loc = st.selectbox('Which location is/are the key(s) drawn to?',loc_list)
        reset_selection = ''
        if st.form_submit_button(label='Submit',help='Press to confirm details'):
            with st.spinner("Loading..."):
                time.sleep(1)
                st.success('Submitted!')
                df_temp = main(spreadsheets)
else:
    return_form = st.empty()
    with return_form.form("Details"):
        st.markdown('''***You do not need to fill up your Name or Keys if
        performing hard reset***''')
        username = st.text_input("Please key in your name")
        selected_key = st.multiselect('Please select the key(s)', key_list)
        selected_keylist = list(selected_key)
        selected_loc = 'Keypress'
        reset_selection = st.selectbox('Please indicate if you would like to perform a hard reset',['No','Yes'])
        if st.form_submit_button('Submit'):
            with st.spinner("Loading..."):
                time.sleep(1)
                st.success('Submitted!')
                if reset_selection == 'No':
                    df_temp = main(spreadsheets)
                else:
                    df_temp = refresh(spreadsheets)




#Printing/Updating of Key Status
#if decision == 'Return':
    #if username != '' and selected_loc != '' and selected_key != '':
#    if reset_selection == 'Yes':
#        df_temp = refresh(spreadsheets)
#        with st.spinner('Searching through endless piles of paperwork...'):
#            time.sleep(1)
#            st.success('Located! I hope...')
#        reset_selection = '' #Reset the variable
#    else:
#        if username != '' and selected_key != '' and selected_loc != '':
#            df_temp = main(spreadsheets)
#            with st.spinner('Searching through endless piles of paperwork...'):
#                time.sleep(1)
#                st.success('Located! I hope...')
#        else:
#            df_temp = display(spreadsheets)
#            with st.spinner('Searching through endless piles of paperwork...'):
#                time.sleep(1)
#                st.success('Located! I hope...')
#else :
#    if username != '' and selected_key != '' and selected_loc != '':
#        df_temp = main(spreadsheets)
#        with st.spinner('Searching through endless piles of paperwork...'):
#            time.sleep(1)
#            st.success('Located! I hope...')
#    else:
#        df_temp = display(spreadsheets)
#        with st.spinner('Searching through endless piles of paperwork...'):
#            time.sleep(1)
#            st.success('Located! I hope...')

#with st.beta_expander('Click here to show the Key Status Overview'):
with st.spinner('Painting the charts and drawing the tables...'):
    time.sleep(1)
    st.success('Success!')
    chart = st.empty()
    data_table = st.empty()
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
    chart.pyplot(fig)
    #Illustration of Overview
    data_table.table(df_temp)
