import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from packageKPS import *
from PIL import Image



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
    response3 = json.loads(requests.get("https://cmtprooptiki.gr/api/getfinancial.json").text)

    df=pd.json_normalize(response, max_level=2)
    df['year'] = df['year'].apply(format_year)

    df2=pd.json_normalize(response2, max_level=2)
    df2['year'] = df2['year'].apply(format_year)

    df3=pd.json_normalize(response3, max_level=2)
    df3['year'] = df3['year'].apply(format_year)

    # st.write(df)
    # st.write(df2)
    # st.write(df3)

    merged= pd.merge(pd.merge(df, df2, on=['koispe_id', 'year']), df3, on=['koispe_id', 'year'])
    # merged= pd.merge([df, df2, df3], on=['koispe_id', 'year'])

    # merged=pd.merge(dfs,on=['koispe_id','year'])

    st.write(merged)
    kdata=merged[merged['koispe_id']==int(id)]


    kdata.drop(columns=['id_x', 'id_y','id'],inplace=True)
    # st.write(kdata)
    ###Start Creating DiktesDataframe

    kpdf=get_data_from_json(kdata)
    st.title("Πίνακας Δεικτών")
    st.write(kpdf)
   #Radio button
    ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό")
    with ad_expander:
        selected_option1 = st.radio("Επιλέξτε επιλογή", ["Εργαζόμενοι", "Ώρες Απασχόλησης", "Ετήσιες Μονάδες Εργασίας", "Συνεταιριστές"])

    e_expander = st.sidebar.expander("Επιχειρηματικότητα")
    with e_expander:
        selected_option2 = st.radio("Επιλέξτε επιλογή", ["Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος", "% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος", "Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος"])

    selected_option3 = st.sidebar.button("Αναλυτικός Πίνακας Δεδομένων")

    ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό")


    #Buttons
    # with ad_expander:
    #     selected_option1 = st.button("Εργαζόμενοι")
    #     selected_option2 = st.button("Ώρες Απασχόλησης")
    #     selected_option3 = st.button("Ετήσιες Μονάδες Εργασίας")
    #     selected_option4 = st.button("Συνεταιριστές")

    # e_expander = st.sidebar.expander("Επιχειρηματικότητα")
    # with e_expander:
    #     selected_option5 = st.button("Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος")
    #     selected_option6 = st.button("% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος")
    #     selected_option7 = st.button("Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος")
    
    # selected_option8 = st.sidebar.button("Αναλυτικός Πίνακας Δεδομένων")


    # selected_item = st.sidebar.selectbox("", ["ad", "e", "pinkas"])


 
    if selected_option1=="Εργαζόμενοι":
        ad_button1(id,kpdf)
    elif selected_option1=="Ώρες Απασχόλησης":
        ad_button2(id,kpdf)
    elif selected_option1=="Ετήσιες Μονάδες Εργασίας":
        ad_button3(id,kpdf)
    elif selected_option1=="Συνεταιριστές":
        ad_button4(id)


    
    # if selected_option1:
    #     ad_button1(id,kpdf)
    # elif selected_option2:
    #     ad_button2(id,kpdf)
    # elif selected_option3:
    #     ad_button3(id,kpdf)
    # elif selected_option4:
    #     ad_button4(id)

    # #Buttons epixirimatikotita    
    # elif selected_option5:
    #     e_button5(id,kpdf)
    # elif selected_option6:
    #     e_button6(id,kpdf)
    # elif selected_option7:
    #     e_button7(id,kpdf)
    # elif selected_option8:
    #     display_pinkas_submenu(id)



def ad_button1(id,kpdf):
    st.subheader("button1 Submenu")

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    
    st.write("Content of button1")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('Col1 show D1')
            st.metric(label="Συνολο Μελών "+str(kpdf['D1'][kpdf['year']==str(year_filter)][0]), value=int(kpdf['D1'][kpdf['year']==str(year_filter)][0]), delta=-0.5,delta_color="inverse")

        with col2:
            st.write('Col2 Caption for first chart')

          
        with col3:
            st.write('Col3 Caption for first chart')

            st.write("Content of column3")

    with st.container():
        col1, col2,col3 = st.columns(3)

        with col1:
            st.write('Col1 Caption for second chart')
            
            # Select the relevant columns
            columns = ['D9', 'D10', 'D11']
            df_selected = kpdf[columns]

            # Calculate the percentage values for each column
            # df_percent = df_selected.div(df_selected.sum(axis=1), axis=0) * 100

            # Create the stacked bar plot using Plotly
            fig = go.Figure()

            for col in columns:
                fig.add_trace(go.Bar(
                    name=col,
                    x=kpdf['year'].apply(str),
                    y=df_selected[col],
                    text=kpdf[col],
                    textposition='inside'

                ))

            # Update the layout
            fig.update_layout(barmode='stack', title='100% Stacked Bar Plot', xaxis_title='Year',yaxis_title='Percentage')
            # Show the plot

            st.plotly_chart(fig)

            





        with col2:
            st.write('Col2 Caption for second chart col2')
            st.line_chart((1,0), height=100)
        with col3:
            st.write('Col3 Caption for second chart col3')
            st.line_chart((1,0), height=100)



def ad_button2(id,kpdf):
    st.subheader("button2 Submenu")
    st.write("Content of button2")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D12')
            st.metric(label="Συνολο"+str(kpdf['D12'][kpdf['year']=='2016'][0]), value=int(kpdf['D12'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")

        with col2:
            st.write('D13')
            st.metric(label="Συνολο"+str(kpdf['D13'][kpdf['year']=='2016'][0]), value=int(kpdf['D13'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")

  
        with col3:
            st.write('D14')
            st.write(kpdf['D14'])
            st.metric(label="Συνολο"+str(kpdf['D14'][kpdf['year']=='2016'][0]), value=int(kpdf['D14'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")
    with st.container():
        col1, col2,col3 = st.columns(3)

        with col1:
            st.write('D15')
            st.write(kpdf['D15'])
            st.metric(label="Συνολο"+str(kpdf['D15'][kpdf['year']=='2016'][0]), value=int(kpdf['D15'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")
        with col2:
            st.write('D16')
            st.write(kpdf['D16'])
        with col3:
            st.write('D17')
            st.write(kpdf['D17'])


          

   

def ad_button3(id,kpdf):
    st.subheader("button3 Submenu")
    st.write("Content of button3")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D18')
            st.write(kpdf['D18'])

        with col2:
            st.write('D19')
            st.write(kpdf['D19'])
        with col3:
            st.write('D20')
            st.write(kpdf['D20'])

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D21')
            st.write(kpdf['D21'])

        with col2:
            st.write('D22')
            st.write(kpdf['D22'])

        with col3:
            st.write('D23')
            st.write(kpdf['D23'])


          






def ad_button4(id):
    st.subheader("button4 Submenu")
    st.write("Content of button4")

def e_button5(id,kpdf):
    st.subheader("button5 Submenu")
    st.write("Content of button5")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D24')
            st.write(kpdf['D24'])
        with col2:
            st.write('D26')
            st.write(kpdf['D26'])
        with col3:
            st.write('D27')
            st.write(kpdf['D27'])
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D28')
            st.write(kpdf['D28'])




def e_button6(id,kpdf):
    st.subheader("button6 Submenu")
    st.write("Content of button6")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D29')
            st.write(kpdf['D29'])
        with col2:
            st.write('D30')
            st.write(kpdf['D30'])
        with col3:
            st.write('D31')
            st.write(kpdf['D31'])
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D32')
            st.write(kpdf['D32'])
        with col2:
            st.write('D36')
            st.write(kpdf['D36'])
        with col3:
            st.write('D38')
            st.write(kpdf['D38'])
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D39')
            st.write(kpdf['D39'])



def e_button7(id,kpdf):
    st.subheader("button7 Submenu")
    st.write("Content of button7")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D40')
            st.write(kpdf['D40'])


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
    
