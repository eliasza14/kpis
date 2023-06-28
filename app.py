import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

def format_year(year):
    return "{:d}".format(year)  # Removes the comma separator

def main():
    #st.write(home())
    st.sidebar.title("Menu")
    id=get_url_params()

    st.write("ID from Flask application: ",id)


    ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό")
    with ad_expander:
        selected_option1 = st.button("Εργαζόμενοι")
        selected_option2 = st.button("Ώρες Απασχόλησης")
        selected_option3 = st.button("Ετήσιες Μονάδες Εργασίας")

    e_expander = st.sidebar.expander("Επιχειρηματικότητα")
    with e_expander:
        selected_option4 = st.button("Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος")
        selected_option5 = st.button("% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος")
        selected_option6 = st.button("Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος")
    
    selected_option7 = st.sidebar.button("Αναλυτικός Πίνακας Δεδομένων")


    # selected_item = st.sidebar.selectbox("", ["ad", "e", "pinkas"])
    
    if selected_option1:
        ad_button1(id)
    elif selected_option2:
        ad_button2(id)
    elif selected_option3:
        ad_button3(id)
    elif selected_option4:
        ad_button4(id)
    elif selected_option5:
        ad_button5(id)
    elif selected_option6:
        ad_button6(id)
    elif selected_option7:
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
def ad_button1(id):
    st.subheader("button1 Submenu")
    st.write("Content of button1")
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

    st.write(df)
    koispe1df=df[df['id']==id]
    st.write(koispe1df)
    st.write(koispe1df['profile.meli_a']+koispe1df['profile.meli_b']+koispe1df['profile.meli_c'])
    
    st.metric(label="Gas price", value=4, delta=-0.5,delta_color="inverse")

    st.metric(label="Active developers", value=123, delta=123, delta_color="off")

def ad_button2(id):
    st.subheader("button2 Submenu")
    st.write("Content of button2")
def ad_button3(id):
    st.subheader("button3 Submenu")
    st.write("Content of button3")
def ad_button4(id):
    st.subheader("button4 Submenu")
    st.write("Content of button4")
def ad_button5(id):
    st.subheader("button5 Submenu")
    st.write("Content of button5")
def ad_button6(id):
    st.subheader("button6 Submenu")
    st.write("Content of button6")

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
    
