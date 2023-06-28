import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from PIL import Image

def calculate_d4(row):
    d1 = row['D1']
    d3 = row['D3']
    return d1 / (d1 + d3)


def format_year(year):
    return "{:d}".format(year)  # Removes the comma separator

def main():
    #st.write(home())
    st.set_page_config(
        page_title="Koispe Dashboard",
        page_icon="✅",
        layout="wide",
    )    

    st.sidebar.title("Menu")
    id=get_url_params()

    st.write("ID from Flask application: ",id)
    # image = Image.open('https://dreamleague-soccerkits.com/wp-content/uploads/2021/07/Real-Madrid-Logo.png','rb')

    st.image("https://dreamleague-soccerkits.com/wp-content/uploads/2021/07/Real-Madrid-Logo.png", width=120)

    response = json.loads(requests.get("https://cmtprooptiki.gr/api/getkoisenew.json").text)
    response2 = json.loads(requests.get("https://cmtprooptiki.gr/api/getemploymentcmt.json").text)

    df=pd.json_normalize(response, max_level=2)
    df['year'] = df['year'].apply(format_year)

    df2=pd.json_normalize(response2, max_level=2)
    df2['year'] = df2['year'].apply(format_year)

    st.write(df)
    st.write(df2)


    merged=pd.merge(df,df2,on=['koispe_id','year'])
    st.write(merged)
    kdata=merged[merged['koispe_id']==int(id)]

    kdata.drop(columns=['id_x', 'id_y'],inplace=True)
    st.write(kdata)
    ###Start Creating DiktesDataframe

    kpdf=kdata[['koispe_id','year']]
    


    kpdf['D1'] = kdata['profile.meli_a']
    print(kpdf)



    ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό")
    with ad_expander:
        selected_option1 = st.button("Εργαζόμενοι")
        selected_option2 = st.button("Ώρες Απασχόλησης")
        selected_option3 = st.button("Ετήσιες Μονάδες Εργασίας")
        selected_option4 = st.button("Συνεταιριστές")

    e_expander = st.sidebar.expander("Επιχειρηματικότητα")
    with e_expander:
        selected_option5 = st.button("Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος")
        selected_option6 = st.button("% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος")
        selected_option7 = st.button("Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος")
    
    selected_option8 = st.sidebar.button("Αναλυτικός Πίνακας Δεδομένων")


    # selected_item = st.sidebar.selectbox("", ["ad", "e", "pinkas"])
    
    if selected_option1:
        ad_button1(id,kdata)
    elif selected_option2:
        ad_button2(id)
    elif selected_option3:
        ad_button3(id)
    elif selected_option4:
        ad_button4(id)

    #Buttons epixirimatikotita    
    elif selected_option5:
        e_button5(id)
    elif selected_option6:
        e_button6(id)
    elif selected_option7:
        e_button7(id)
    elif selected_option8:
        display_pinkas_submenu(id)






    # if selected_item == "ad":
    #     display_ad_submenu()
    # elif selected_item == "e":
    #     display_e_submenu()
    # elif selected_item == "pinkas":
    #     display_pinkas_submenu(id)

# def display_ad_submenu():
#     st.subheader("ad Submenu")
#     ad_options = ["2", "3"]
#     selected_option = st.selectbox("Select an option", ad_options)
    
#     if selected_option == "2":
#         st.write("Content for Option 2 in ad submenu")
#         # Add content for Option 2 in ad submenu here
#     elif selected_option == "3":
#         st.write("Content for Option 3 in ad submenu")
#         # Add content for Option 3 in ad submenu here

# def display_e_submenu():
#     st.subheader("e Submenu")
#     e_options = ["2", "5"]
#     selected_option = st.selectbox("Select an option", e_options)
    
#     if selected_option == "2":
#         st.write("Content for Option 2 in e submenu")
#         # Add content for Option 2 in e submenu here
#     elif selected_option == "5":
#         st.write("Content for Option 5 in e submenu")
#         # Add content for Option 5 in e submenu here
def ad_button1(id,kdata):
    st.subheader("button1 Submenu")
    response = json.loads(requests.get("https://cmtprooptiki.gr/api/getkoispe.json").text)



    # df=pd.json_normalize(response, max_level=1)
    # st.write(df)
    # data = json.loads(response.text)
    
    # Convert the JSON data to a list of dictionaries
    records = []
    for key, value in response.items():
        value['id'] = key
        records.append(value)
    
    # Create a dataframe from the list of dictionaries
    #df = pd.DataFrame(records)
    df=pd.json_normalize(records, max_level=2)
    # year_filter = st.selectbox("Select the Job", pd.unique(df["year"]))
    year_filter = st.selectbox("Έτος", ['2016','2017','2018','2019'])

    st.write("Content of button1")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('Col1 show kdata')
            st.write(kdata)
        with col2:
            st.write('Col2 Caption for first chart')

            st.line_chart((0,1), height=100)
                
            koispe1df=df[df['id']==id]
            st.write(koispe1df)
            totalmeloi=int(koispe1df['profile.meli_a'])+int(koispe1df['profile.meli_b'])+int(koispe1df['profile.meli_c'])
            
            st.metric(label="Συνολο Μελών "+str(koispe1df['profile.lastname'][0]), value=totalmeloi, delta=-0.5,delta_color="inverse")
        with col3:
            st.write('Col3 Caption for first chart')

            st.write("Content of column3")

    with st.container():
        col1, col2,col3 = st.columns(3)

        with col1:
            st.write('Col1 Caption for second chart')
        with col2:
            st.write('Col2 Caption for second chart col2')
            st.line_chart((1,0), height=100)
        with col3:
            st.write('Col3 Caption for second chart col3')
            st.line_chart((1,0), height=100)



def ad_button2(id):
    st.subheader("button2 Submenu")
    st.write("Content of button2")
def ad_button3(id):
    st.subheader("button3 Submenu")
    st.write("Content of button3")
def ad_button4(id):
    st.subheader("button4 Submenu")
    st.write("Content of button4")

def e_button5(id):
    st.subheader("button5 Submenu")
    st.write("Content of button5")
def e_button6(id):
    st.subheader("button6 Submenu")
    st.write("Content of button6")
def e_button7(id):
    st.subheader("button7 Submenu")
    st.write("Content of button7")

def display_pinkas_submenu(id):
    st.subheader("pinkas Submenu")
    st.write("Content for pinkas submenu")
    
    response = json.loads(requests.get("https://cmtprooptiki.gr/api/getemploymentcmt.json").text)
    df=pd.json_normalize(response, max_level=2)
    df['year'] = df['year'].apply(format_year)

    df1=df.groupby(['koispe_id','year'])['profile.eko.sum'].sum()
    dftest=pd.DataFrame(df1).reset_index()
    
    st.write(df)
    dffilter=dftest[dftest['koispe_id']==int(id)]
    # dffilter['year'] = dffilter['year'].apply(format_year)
    # dffilter
    # data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(dffilter, x=dffilter['year'].astype(str), y='profile.eko.sum',orientation='v')
    st.plotly_chart(fig)

    # Add content for pinkas submenu here




def get_url_params():
    query_params = st.experimental_get_query_params()
    id_received = query_params.get("id", [""])[0]
    
    return id_received
    # id_input = st.text_input("Enter ID", value=id_received)
    # if id_input:
    #     display_contents(id_input)

def display_contents(id_received):
    # Retrieve the contents of the specific ID (replace with your own logic)
    contents = {'id': id_received, 'name': 'John eseaas', 'email': 'john@example.com'}

    st.write(f'# Contents of ID: {id_received}')
    st.write(f'Name: {contents["name"]}')
    st.write(f'Email: {contents["email"]}')



if __name__ == "__main__":
    main()
    
