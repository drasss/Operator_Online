import streamlit as st
import datetime
import time
#Before And tabs
st.set_page_config(layout="wide")
test, tab2, tab1 = st.tabs(["tests", "Résumé","TDL"])

#save

def saving():
    fichier=open("TDL.txt","w")
    for i in range(nb):
        content_write=str(i)+"".join([" | " + str(TABB[i][j]) for j in range(1,len(TABB[i]))])+"\n"
        fichier.write(str(content_write))
    fichier.close()

    
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

# tab1 TDL

#contenu tab
try : TDL==""
except :
    fichier=open("TDL.txt")
    TDL_text=fichier.read()
    fichier.close()


#transformation 

TDL_text=TDL_text.strip("\n").split("\n")
TDL=[TDL_text[i].split(" | ") for i in range(len(TDL_text))]
# numéro de ligne



if 'counter' not in st.session_state:
    st.session_state['counter']=len(TDL)
button_col1,button_col2=tab1.columns(2)



#boutons add row
tm=time.localtime()
if button_col1.button("add row"):
    TDL+=[['0', '', '', '', str(tm[0])+"-"+str(tm[1])+"-"+str(tm[2]), str(tm[3])+":"+str(tm[4])]]
    st.session_state['counter']+=1


#boutons delete row
def dlrow(i,**parameters):
    global TDL,nb
    print("-----------------",i,"/",nb)
    print(TABB[i])
    del TDL[i]
    del TABB[i]


    for j in range(i,len(TDL)):
        TDL[j][0]=j+i
    nb-=1
    st.session_state['counter']-=1
    print("-------------- PPPOOOOOOPPPPP--------------------------\n",TDL)
    print("-----")
    print(TABB)
    saving()
    


nb=st.session_state['counter']


TABB=[]
col_tab1=[]
for i in range(nb):
    col_tab1+=[tab1.columns([1,3,3,4,2,2],vertical_alignment="center")]
    # delete , name      ,   state    , description , 
    #button , text_input ,  selectbox , text_area , date_input , time_input

    TABB+=[[col_tab1[i][0].button("X",key=str(i)+"tab1button",on_click=dlrow,kwargs={"i":i}),
        col_tab1[i][1].text_input("name",key=str(i)+"tab1name",value=TDL[i][1]),
         col_tab1[i][2].selectbox("state",["","Fini","En cours","A commencer","Pas de mon ressort"],key=str(i)+"tab1state",index=["","Fini","En cours","A commencer","Pas de mon ressort"].index(TDL[i][2])),
         col_tab1[i][3].text_area("desc",key=str(i)+"tab1desc",value=str(TDL[i][3])).replace("\n"," "),
         col_tab1[i][4].date_input("Date",key=str(i)+"tab1date",value=datetime.datetime(int(TDL[i][4].split("-")[0]),int(TDL[i][4].split("-")[1]),int(TDL[i][4].split("-")[2]))),
        col_tab1[i][5].time_input("Time",key=str(i)+"tab1time",value=datetime.time(int(TDL[i][5].split(":")[0]),int(TDL[i][5].split(":")[1])))]]

##button=[TABB[i][0] for i in range(len(TABB))]
##print(button)
##if sum(button)>0:
##    dlrow(button.index(1))


saving()


# tab2
RES=[]
for i in range(nb):
    tab2.checkbox(TDL[i][1],key=str(i)+"resume")

