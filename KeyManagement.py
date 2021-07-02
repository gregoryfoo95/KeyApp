import streamlit as st
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
import gsheetsdb import connect
from google.oauth2 import service_account
# Create a connection object
 credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes =[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
 )
conn = connet(credentials = credentials)


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
