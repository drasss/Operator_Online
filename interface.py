import streamlit as st
import datetime
import time
import os
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
#Before And tabs
st.set_page_config(layout="wide")
#--------------------------- GSHEET

 
def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds
 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1FEdZ6HLUzO373k83tOCNLSqnoSd_3ZXR'+'JMc37TjQbHI'
 
creds=gsheet_api_check(SCOPES)
 
from googleapiclient.discovery import build
def pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=ranging).execute()
    values = result.get('values', [])
    if not values:
        pass
    else:
        data = values
        return data
 
 
#save
 
def saving():
    service = build("sheets", "v4", credentials=creds)
    values = [[""]*3]*10
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId="1FEdZ6HLUzO373"+"k83tOCNLSqnoSd_3ZXRJMc37TjQbHI",
            range="A1:C20",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute())
 
 
    values = [[str(st.session_state['TABB'][i][j]) for j in range(len(st.session_state['TABB'][i]))] for i in range(len(st.session_state['TABB']))]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId="1FEdZ6HLUzO373k83tOCNLS"+"qnoSd_3ZXRJMc37TjQbHI",
            range="A1:C20",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute())

 
    
 
 
    

 
# st TDL ----------------------------------------- A CHANGER
ranging = 'A1:C100'
data = pull_sheet_data(SCOPES,SPREADSHEET_ID,ranging)
df = pd.DataFrame(data)
st.write(df)
 
if 'counter' not in st.session_state:
    st.session_state['counter']=len(df) #------------------------

 
 
#------------------------------------------------------------------------------boutons add row
## ------------ DO NOT TOUCH
if 'TABB' not in st.session_state:
    st.session_state['TABB']=df.values.tolist() #------------------------


but=[]
## ------------ DO NOT TOUCH

def add_row():
    st.session_state['counter']+=1
    st.session_state['TABB'].append(["","","---"])

st.button("Ajouter une tâche",on_click=add_row)

def delrow(i):
    st.session_state['TABB'].pop(i)
    st.session_state['counter']-=1

## ------------ DO NOT TOUCH
TABB=[]
for i in range(len(st.session_state['TABB'])):
    cl=st.container(key="container"+str(i))
    ct=cl.columns([1,1,4,1])
    ct[0].button("X",key="del"+str(i),on_click=delrow,args=(i,))
    TABB+=[[ct[1].text_input("tâche",key="task"+str(i),value=str(st.session_state['TABB'][i][0])),
    ct[2].text_area("description",key="desc"+str(i),value=str(st.session_state['TABB'][i][1])),
    ct[3].selectbox("status",key="status"+str(i),options=["à faire","en cours","terminé","---"],index=["à faire","en cours","terminé","---"].index(str(st.session_state['TABB'][i][2])))]]
st.session_state['TABB']=TABB




saving()
## ------------ DO NOT TOUCH
st.write(st.session_state['TABB'])