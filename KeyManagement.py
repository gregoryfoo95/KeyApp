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
import gspread as gs

credentials = {
  "type": "service_account",
  "project_id": "key-management-318608",
  "private_key_id": "ce2e843792641cd84e3bc48939146c58c856de43",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC2lfrRP2qC2sC5\nx4B37wq5bo9ZfHbEbMM5+g5+wUJH7RvhK3EuHQ+Rme3PjdID0BDV6Jwy6p2AmiEa\n9e+kcA2M9jQ05IelxRw30ruCO9L1dfS8L4SfgrzrAdY5rBDKfTc4X5nXXGrhVJ+y\nReDXuB3fWVq6SjivwAfOH0IdOmrcrRSM4U+R6FI5787F/UgOLI1559z/ozUPogAN\nORB3m0ijC55NHc3bWU/ttIpEnTkMlEu9Tg1S7ODWW6G0EAGrqodzIJOfgSrtkCff\n4UyNcgxuKNP6j5pcbx5nY41us/KfBJlnO0KU68Kvg9G+Dflwf0YRE7vLpu92HOvT\nS6dx/ptJAgMBAAECggEABjws6oRd4MYTmsSDUJUrKpXp80Zaz+5e5FXztMRovQgN\n0ayoGskHRROamWHgcBzk1kkxPFPiuQeKZd9MJbNl4xBtS/kZ4MFQa1+Y46OjWpqC\nlwKQZtoSFXxkkmeb0y5fel9ZY49WXweCxJW6TeONsZjdjksGkIngOlu66ECccZiw\nlBrDOFWyT8jnHQBa+RuALhPwMIQUCZslVULeONg6i1VyJsJs06XQfTIvPxG/Actj\nzUB3V4MeItTjm+ww2UjkBToQXdS5ZlyD5PtLdFW2JgJgE9k66nORE+epfgSvL5Gl\nChPO++VoKWquVBgSyllxfisDj+0jKxfqezl1Lit2AQKBgQD6XRWnMm/Kk1BruGJS\nyxeGG9nCAJ+ChiQDIXzk0swkDYNsZ1mYT0tC8fO3maa+n4EGSxLbtmpnCfrBaPpS\nf05FOYMrpDZVTzUilVvYrV/UGftaXfGhNZhKEi6qHgF2V70uYm1+JSrWIn9zmSse\n9EEud2fRhd9WIwQ0RoKgKHScIQKBgQC6skXmtANSol2gJbACIoqzdHYq9WAPOjNM\nt40aD5iJERJvL5hU4Yss5XwjvWFOyE+22HabiXf+CVgh2+wwCLOAcEhZH4r6yOrk\nLRobYadTlca+rSsKWKg2ib2JNtNKmup3LPin35SI8HAmdoNaUpQhQNk+Wr8833DY\nImlamq5aKQKBgDcn5qtM+z/fsGnq1w5yW55Z6GFLDdkNgEWITSGEJyESMQ/ivORH\nI8d90jlyij+YmC4wv9jTmSFWG34ciHlAPpgVkYY9yRKGPqh9yxwzJdduWeeQprjj\nO8eltc4Yii3uKmlbmc+elI9UTkvDRLKvEOURvTd1jLxHPpfdqM1r3DTBAoGAOcZb\nfWZttM/MO3gOPMrls10yCF9A59Vx9KbEwrDa2mfvFXtcH8Bgandl8EV17IRurr3U\nDpP/Dx1jKa8+Kys2KWQV74akYrF0h0Ix1xFkT6iFBZLfQ+dlvuLnRaQyxN6l+lVv\nabv14l7Nxglc4sG1V4kS8YnxrmvTJv+XLNO7aukCgYALZm74ly06HEqGk+0HiL4Y\n1CWk+bxreib5SAeBhL6ZMug2hOFdj1Hlk0LJGejUMAybQTgkhH7YkUEg6/epF9uY\nQZkUk+KAjjpdlYoJIjGuuJMeMbNe9HgffxF15381rlQekzQ8eY16/9SmY84Juvtr\nqpVJD/HzsoTYwIMDX1jLig==\n-----END PRIVATE KEY-----\n",
  "client_email": "service-acc@key-management-318608.iam.gserviceaccount.com",
  "client_id": "115066392756484337303",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-acc%40key-management-318608.iam.gserviceaccount.com"
}

gc = gs.service_account_from_dict(credentials)
sh = gc.open("Key Management")
print(sh.sheet1.get('A1'))

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
