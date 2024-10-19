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
test, tab2, tab1 = st.tabs(["tests", "Résumé","TDL"])
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
SPREADSHEET_ID = '1FEdZ6HLUzO373k83tOCNLSqnoSd_3ZXRJMc37TjQbHI'
 
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
    values = [[""]*6]*10
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId="1FEdZ6HLUzO373k83tOCNLSqnoSd_3ZXRJMc37TjQbHI",
            range="A1:F20",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute())
 
 
    values = [[str(TABB[i][j]) for j in range(len(TABB[i]))] for i in range(len(TABB))]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId="1FEdZ6HLUzO373k83tOCNLSqnoSd_3ZXRJMc37TjQbHI",
            range="A1:F20",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute())
 
 
    
 
 
    
#test
def dele():
    xx=st.empty()
dele=test.button("Click me")
test.feedback("thumbs")
test.checkbox("I agree")
test.toggle("Enable")
k=test.radio("Pick one", ["cats", "dogs"])
test.selectbox("Pick one", ["cats", "dogs"])
xx=test.multiselect("Buy", ["milk", "apples", "potatoes"])
test.slider("Pick a number", 0, 100)
test.select_slider("Pick a size", ["S", "M", "L"])
test.text_input("Firtest name")
test.number_input("Pick a number", 0, 10)
test.text_area("Text to translate")
test.date_input("Your birthday")
test.time_input("Meeting time")
test.file_uploader("Upload a CSV")
test.camera_input("Take a picture")
test.color_picker("Pick a color")
x=test.text("rr")
 
# tab1 TDL ----------------------------------------- A CHANGER
ranging = 'A1:F100'
data = pull_sheet_data(SCOPES,SPREADSHEET_ID,ranging)
df = pd.DataFrame(data)
 
 
if 'counter' not in st.session_state:
    st.session_state['counter']=len(df) #------------------------
button_col1,button_col2=tab1.columns(2)
 
 
#------------------------------------------------------------------------------boutons add row
tm=time.localtime()
 
def add_ro():
    service = build("sheets", "v4", credentials=creds)
 
    values = [[False,"","--","",str(tm[0])+"-"+str(tm[1])+"-"+str(tm[2]),str(tm[3])+":"+str(tm[4])]]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId="1FEdZ6HLUzO373k83tOCNLSqnoSd_3ZXRJMc37TjQbHI",
            range="A1:A1",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )
 
    st.session_state['counter']+=1
 
button_col1.button("add row",on_click=add_ro)
 
#boutons delete row
def dlrow(i,**parameters):
    global nb,df
    start_time=time.time()
    df=df.drop([i])
    del TABB[i]
 
    nb-=1
    st.session_state['counter']-=1
    end_time=time.time()
 
nb=st.session_state['counter']
 
 
TABB=[]
col_tab1=[]
for i in range(nb):
    col_tab1+=[tab1.columns([1,3,3,4,2,2],vertical_alignment="center")]
    # delete , name      ,   state    , description , 
    #button , text_input ,  selectbox , text_area , date_input , time_input
 
    TABB+=[[col_tab1[i][0].button("X",key=str(i)+"tab1button",on_click=dlrow,kwargs={"i":i}),
        col_tab1[i][1].text_input("name",key=str(i)+"tab1name",value=df[1][i]),
         col_tab1[i][2].selectbox("state",["--","Fini","En cours","A commencer","Pas de mon ressort"],key=str(i)+"tab1state",index=["--","Fini","En cours","A commencer","Pas de mon ressort"].index(df[2][i])),
         col_tab1[i][3].text_area("desc",key=str(i)+"tab1desc",value=str(df[3][i])).replace("\n"," "),
         col_tab1[i][4].date_input("Date",key=str(i)+"tab1date",value=datetime.datetime(int(df[4][i].split("-")[0]),int(df[4][i].split("-")[1]),int(df[4][i].split("-")[2]))),
        col_tab1[i][5].time_input("Time",key=str(i)+"tab1time",value=datetime.time(int(df[5][i].split(":")[0]),int(df[5][i].split(":")[1])))]]
 
 
saving()
 
 
# tab2
RES=[]
for i in range(nb):
    tab2.checkbox(df[1][i],key=str(i)+"resume")
