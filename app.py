import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit.components.v1 import html

from packageKPS import *
from packageCharts import *

from PIL import Image



def main():
 

    
    #st.write(home())
    st.set_page_config(
        page_title="Koispe Dashboard",
        page_icon="✅",
        layout="wide",
    )    

       # Define the CSS style
    css_style = """
    <style>
    
    *{
    font-family:Copperplate;
    }
    .css-1xarl3l.e1vioofd1{
    display:none;
    }

    .css-wnm74r{
    text-align:center;
    font-size: 2rem;
    display: flex;
    flex-direction: row;
    -webkit-box-align: center;
    align-items: center;
    font-weight: 400;
    }
    
    .e1ugi8lo1.css-jhkj9c.ex0cdmw0{
        vertical-align: middle;
        overflow: hidden;
        color: inherit;
        fill: currentcolor;
        display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        font-size: 1.25rem;
        width: 40px;
        height: 40px;
        margin: 0px 0.125rem 0px 0px;
    }
    [data-testid="stSidebar"] {
        background-color: #f2f6fc; /* Replace with your desired color */
    }

    
    </style>"""

    with open( "style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    #st.markdown(css_style, unsafe_allow_html=True)

            # Load the JavaScript function code
    with open("animated_counter.js", "r") as file:
            js_code = file.read()


    st.sidebar.title("KPI's Dashboard")
    id=get_url_params()
    st.write("URL ID FROM VIDAVO:",id)
    st.write("ID from Flask application: ",id)
    # image = Image.open('https://dreamleague-soccerkits.com/wp-content/uploads/2021/07/Real-Madrid-Logo.png','rb')
    # with st.container():
    #     col1,col2,col3=st.columns(3)
    #     with col1:
    #         pass
    #     with col2:
    #         st.image("https://cmtprooptiki.gr/api/profile_images/"+str(id)+".png", width=300)
    #     with col3:
    #         pass
    # https://app.koispesupport.gr/koispe/api/getkoispe?id=1128

    #VIDAVO API CALL SPEICIFIC KOISPE WITH ID
    response = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getkoispe?id="+str(id)).text)
    response2 = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getemployment?id="+str(id)).text)
    response3 = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getfinancial?id="+str(id)).text)




    #VIDAVO API CALL GENERAL
    # response = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getkoispe").text)
    # response2 = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getemployment").text)
    # response3 = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getfinancial").text)

    #MYAPP ON MY API
    # response = json.loads(requests.get("https://cmtprooptiki.gr/api/getkoisenew.json").text)
    # response2 = json.loads(requests.get("https://cmtprooptiki.gr/api/getemploymentcmt.json").text)
    # response3 = json.loads(requests.get("https://cmtprooptiki.gr/api/getfinancial.json").text)

    df=pd.json_normalize(response, max_level=2)

    st.write(df)

    df['year'] = df['year'].map(lambda x: str(x) if pd.notnull(x) else None)
    df['year'] = df['year'].str.split('.').str[0]

    st.write("GET KOIPSE")
    st.write(df)

    #this command is need on our api
    # df['year'] = df['year'].apply(format_year)
    st.write(df)

    df2=pd.json_normalize(response2, max_level=2)
    df2['year'] = df2['year'].map(lambda x: str(x) if pd.notnull(x) else None)
    df2['year'] = df2['year'].str.split('.').str[0]
    
    st.write("GET employement")

    st.write(df2)

    #this command is need on our api

    # df2['year'] = df2['year'].apply(format_year)

    df3=pd.json_normalize(response3, max_level=2)
    df3['year'] = df3['year'].map(lambda x: str(x) if pd.notnull(x) else None)
    df3['year'] = df3['year'].str.split('.').str[0]
    st.write("GET financial")

    st.write(df3)
    
    #this command is need on our api

    # df3['year'] = df3['year'].apply(format_year)

    # st.write(df)
    # st.write(df2)
    # st.write(df3)

    merged=pd.merge(df,df2, left_on=['id', 'year'],right_on=['koispe_id','year'],how='inner')
    merged=pd.merge(merged,df3, left_on=['id', 'year'],right_on=['koispe_id','year'],how='inner')

    # merged= pd.merge(pd.merge(df, df2, on=['koispe_id', 'year']), df3, on=['koispe_id', 'year'])



    st.write(merged)
    merged.rename(columns={'id': 'koispe_id'}, inplace=True)

    ##NOT NEED WHEN ID ON URL EXIST
    # kdata=merged[merged['koispe_id']==int(id)]

    kdata=merged.copy()

    #Our code
    # kdata.drop(columns=['id_x', 'id_y','id'],inplace=True)

    kdata.drop(columns=['uid_x', 'uid_y','uid'],inplace=True)
    st.write(kdata)
    # st.write(kdata)
    ###Start Creating DiktesDataframe
    matching_columns = kdata.columns[kdata.columns.str.startswith("report.kad.81.")]
    print(matching_columns)
    kdata[matching_columns] = kdata[matching_columns].fillna(0)

    matching_columns2 = kdata.columns[kdata.columns.str.startswith("report.kad.56.")]
    kdata[matching_columns2] = kdata[matching_columns2].fillna(0)

    matching_columns3 = kdata.columns[kdata.columns.str.startswith("report.kad.")]
    kdata[matching_columns3] = kdata[matching_columns3].fillna(0)


    # kdata['report.kad.81.21.00.00']=kdata['report.kad.81.21.00.00'].fillna(0)
    # kdata['report.kad.81.30.00.00']= kdata['report.kad.81.30.00.00'].fillna(0)
    # kdata['report.kad.81.29.19.02']=kdata['report.kad.81.29.19.02'].fillna(0)
    # kdata['report.kad.81.29.19.03']=kdata['report.kad.81.29.19.03'].fillna(0)

    # kdata['report.kad.56.10.12.01']=kdata['report.kad.56.10.12.01'].fillna(0)
    # kdata['report.kad.56.10.11.02']= kdata['report.kad.56.10.11.02'].fillna(0)
    # kdata['report.kad.56.10.11.09']= kdata['report.kad.56.10.11.09'].fillna(0)


    st.write(kdata)

    kpdf=get_data_from_json(kdata)
    # kpdf=kpdf.fillna(0)
 

    st.title("Πίνακας Δεικτών")
    st.write(kpdf)
   #Radio button
    ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό / Επιχειρηματικότητα",expanded=True)
    with ad_expander:
        selected_option1 = st.radio("Επιλέξτε:", ["Συνεταιριστές","Εργαζόμενοι", "Ώρες Απασχόλησης", "Ετήσιες Μονάδες Εργασίας","Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος", "% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος", "Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος"])
    


    #RADIO OPTION ANTHROPINO DYNAMIKO
    if selected_option1=="Συνεταιριστές":
        ad_button1(id,kpdf,js_code)
    elif selected_option1=="Εργαζόμενοι":
        ad_button2(id,kpdf,js_code)
    elif selected_option1=="Ώρες Απασχόλησης":
        ad_button3(id,kpdf,js_code)
    elif selected_option1=="Ετήσιες Μονάδες Εργασίας":
        ad_button4(id,kpdf,js_code)

    #RADIO OPTION EPIXEIRIMATIKOTITA
    if selected_option1=="Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος":
        e_button5(id,kpdf,js_code)
    elif selected_option1=="% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος":
        e_button6(id,kpdf,js_code)
    elif selected_option1=="Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος":
        e_button7(id,kpdf,js_code)
   


def ad_button1(id,kpdf,js_code):
    st.subheader("Συνεταιριστές")

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    
    with st.container():


        # Display the HTML and JavaScript code
       
        #st.write('Col1 show D1')
        val=kpdf['D1'][kpdf['year']==str(year_filter)].iloc[0]
        # text="Συνεταιριστες Κατηγορια Α: "+str(val)+" 👪" 
        #st.write(kpdf['D1'][kpdf['year']==str(year_filter)])
        st.markdown("<h3 style='text-align: center; color: grey;'>Συνεταιριστές Κατηγορίας Α</h3>", unsafe_allow_html=True)
        #antonis tab
        # html(
        #         f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
        #         <div style="  width:300px; border-radius:10px; background: linear-gradient(45deg, rgba(220,255,89,1) 0%, rgba(255,104,104,1) 100%);">
        #             <div style="font-size:30px; "><p style=" margin:5px; background:white; width:fit-content; border:1px solid transparent; border-radius:50%;">💀</p></div>
        #             <div style="text-align:center;">Συνεταιριστές Κατηγορίας Α</div>
        #             <div style="display: flex; flex-wrap: nowrap; align-items: flex-end;">
        #                 <div id="counter" style="text-align: left; color:white;    font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;   "></div>
        #                 <div>Συνεταιριστές</div>
        #             </div>
        #         </div>
        #         <script type="text/javascript">
        #         {js_code}
        #         animateCounter("counter", 0, """+str(val)+""", 1000);  // Increase from 0 to 100 in 1 second
        #         </script></body>
        #         """
        #     )
        html(
        f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
        <div style="  width:300px; border-radius:10px; background: linear-gradient(45deg, rgba(220,255,89,1) 0%, rgba(255,104,104,1) 100%);">
            <div style="font-size:30px; "><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" fill="none">
<circle cx="16" cy="16" r="16" fill="white"/>
<path d="M11.323 12.8515C11.83 13.1657 12.3282 13.4938 12.817 13.8355C13.849 14.5495 14.951 15.0865 16.219 15.2155L6.00203 26.1575C6.00205 26.0309 6.02006 13.6214 6.03403 13.4955C6.10103 12.8975 6.41003 12.5545 7.00003 12.4185M11.323 12.8515C10.703 12.4715 10.009 12.3465 9.29303 12.3075C8.52303 12.2645 7.75703 12.2445 7.00003 12.4185M11.323 12.8515L11.0597 13.2765C11.06 13.2768 11.0604 13.277 11.0608 13.2773M11.323 12.8515L11.0617 13.2778C11.0614 13.2776 11.0611 13.2775 11.0608 13.2773M7.00003 12.4185L7.11234 12.9058M7.00003 12.4185L7.11234 12.9058M7.11234 12.9058C7.7942 12.7491 8.49779 12.7639 9.26515 12.8068L9.26584 12.8068C9.94573 12.8438 10.5434 12.9604 11.0608 13.2773M7.11234 12.9058L11.0608 13.2773M11.0608 13.2773C11.5596 13.5864 12.0497 13.9092 12.5306 14.2453L12.5325 14.2467C13.6035 14.9877 14.786 15.5723 16.1684 15.713L11.0608 13.2773ZM12.8172 26.0295L12.8172 26.0294C12.7972 25.1903 12.8129 24.342 12.8283 23.5063C12.8355 23.1161 12.8426 22.7285 12.8461 22.346L13.346 22.3505L12.8461 22.346L12.8911 17.358L12.8911 17.3576L12.8911 17.3498C12.8924 17.2168 12.8947 16.9632 13.0533 16.7547C13.2147 16.5425 13.4617 16.4759 13.5893 16.4415L13.5936 16.4404C14.3261 16.2357 15.0971 16.2103 15.8415 16.3661L15.8432 16.3665C17.273 16.6711 18.3413 17.7859 18.4973 19.263C18.5618 19.8692 18.5693 20.4812 18.5765 21.0632L12.8172 26.0295ZM12.8172 26.0295C12.8372 26.8668 12.202 27.4715 11.557 27.4715C11.1915 27.4715 10.829 27.474 10.4686 27.4765M12.8172 26.0295L10.4686 27.4765M12.85 7.68849V7.68842C12.8518 7.27148 12.7714 6.85827 12.6135 6.47238C12.4555 6.0865 12.2231 5.7355 11.9296 5.43943C11.636 5.14336 11.287 4.90802 10.9024 4.74684C10.5179 4.58565 10.1054 4.50179 9.68842 4.50003C9.27147 4.49827 8.85826 4.57865 8.47238 4.73659C8.0865 4.89452 7.7355 5.12691 7.43943 5.4205C7.14336 5.71408 6.90802 6.0631 6.74683 6.44764C6.58566 6.83215 6.50179 7.24465 6.50003 7.66157L12.85 7.68849ZM12.85 7.68849C12.8466 8.53041 12.5089 9.33566 11.9109 9.92876C11.3131 10.5218 10.5041 10.853 9.66207 10.8495C8.82001 10.8461 8.0138 10.5083 7.4208 9.91044C6.82782 9.31259 6.49661 8.50368 6.50003 7.66164L12.85 7.68849ZM10.4686 27.4765C9.51853 27.483 8.58261 27.4894 7.643 27.45L10.4686 27.4765ZM6.53297 13.5339C6.55942 13.3201 6.62228 13.1965 6.69294 13.1178C6.76591 13.0366 6.88831 12.9574 7.11222 12.9058L6.53297 13.5339ZM18.6227 25.1247C18.6104 23.8114 18.598 22.4968 18.578 21.1825L16.1684 15.713C17.2181 15.8212 18.2459 15.7309 19.2521 15.5276L19.2521 15.5276C19.4987 15.4778 19.7381 15.4261 19.9738 15.3752C20.4692 15.2682 20.9479 15.1649 21.4412 15.0898L21.4416 15.0898C22.3372 14.9529 23.2508 14.9915 24.1316 15.2036C24.3283 15.2549 24.5167 15.3339 24.691 15.4384L24.691 15.4385L24.6994 15.4433C24.8293 15.5178 24.912 15.6438 24.9328 15.8896L24.9328 15.8896L24.9334 15.8963C24.9356 15.9187 24.936 15.9468 24.936 16.0031C24.9351 17.0146 24.9345 18.0261 24.9339 19.0374C24.9324 21.3969 24.9309 23.7559 24.926 26.1152C24.9249 26.5454 24.7729 26.8848 24.539 27.1163C24.3046 27.3482 23.9606 27.4987 23.5271 27.4995C22.3571 27.5005 21.1873 27.4985 20.0176 27.4925H20.0173C19.2065 27.4888 18.6395 26.9222 18.632 26.1059L18.632 26.1057C18.6288 25.7788 18.6258 25.4518 18.6227 25.1247ZM21.6827 6.38053L21.7625 6.3809C22.5748 6.40505 23.3481 6.7397 23.9221 7.31767C24.5149 7.91447 24.8468 8.72196 24.845 9.56309C24.842 10.4042 24.5056 11.2098 23.9096 11.8033C23.3136 12.3969 22.5065 12.73 21.6653 12.7295C21.2471 12.7293 20.833 12.6464 20.4469 12.4855C20.0609 12.3247 19.7104 12.0891 19.4158 11.7922C19.1212 11.4954 18.8881 11.1433 18.7301 10.756C18.5721 10.3688 18.4922 9.95416 18.495 9.53594L18.495 9.53539C18.4998 8.69445 18.8383 7.88982 19.436 7.29826C20.0337 6.70671 20.8418 6.37662 21.6827 6.38053Z" fill="white" stroke="black"/>
</svg>
            <p style=" margin:5px; background:white; width:fit-content; border:1px solid transparent; border-radius:50%;">💀</p></div>
            <div style="text-align:center;">Συνεταιριστές Κατηγορίας Α</div>
            <div style="display: flex; flex-wrap: nowrap; align-items: flex-end;">
                <div id="counter" style="text-align: left; color:white;    font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;   "></div>
                <div>Συνεταιριστές</div>
            </div>
        </div>
        <script type="text/javascript">
        {js_code}
        animateCounter("counter", 0, """+str(val)+""", 1000);  // Increase from 0 to 100 in 1 second
        </script></body>
        """
    )






def ad_button2(id,kpdf,js_code):
    st.subheader("Εργαζόμενοι")
    #colors = px.colors.qualitative.Plotly
    colors = ["rgb(65,105,225)", "rgb(135,206,235)", "rgb(255,0,0)"]
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            
            text=str(kpdf['D3'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('Δ3-Εργαζόμενοι Γενικού Πληθυσμού: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι Γεν. Πληθυσμού</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;     font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
            #st.write(kpdf['D3'][kpdf['year']==str(year_filter)])

        with col2:
            
            text=kpdf['D5'][kpdf['year']==str(year_filter)].iloc[0]
            # st.write('Δ5-Εργαζόμενοι ΛΥΨΥ: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΛΥΨΥ</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
            #st.write(kpdf['D5'][kpdf['year']==str(year_filter)])


          
        with col3:
            #st.write('D7-Εργαζόμενοι ΕΚΟ')
            text=kpdf['D7'][kpdf['year']==str(year_filter)].iloc[0]
            # st.write('D7-Εργαζόμενοι ΕΚΟ: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΕΚΟ</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
            #st.write(kpdf['D7'][kpdf['year']==str(year_filter)])

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            # Filter the dataframe based on the selected year
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι Γεν. Πληθ. (% επί του Συνόλου)</h3>", unsafe_allow_html=True)
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]
            # Select the value from the filtered dataframe
            d9_value = filtered_kpdf["D9"].iloc[0]
            fig=gaugeChart(d9_value,'royalblue')
            st.plotly_chart(fig,use_container_width=True)
            

        with col2:
            # Filter the dataframe based on the selected year
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΛΥΨΥ (% επί του Συνόλου)</h3>", unsafe_allow_html=True)
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]
            # Select the value from the filtered dataframe
            d10_value = filtered_kpdf["D10"].iloc[0]
            fig=gaugeChart(d10_value,'skyblue')

            st.plotly_chart(fig,use_container_width=True)
        with col3:
            # Filter the dataframe based on the selected year
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΕΚΟ (% επί του Συνόλου)</h3>", unsafe_allow_html=True)
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]
            # Select the value from the filtered dataframe
            d11_value = filtered_kpdf["D11"].iloc[0]
            fig=gaugeChart(d11_value,'red')
            st.plotly_chart(fig,use_container_width=True)

        with st.container():
            col1, col2,col3 = st.columns(3)
            with col1:
                pass
            with col2:
                # Select the relevant columns
                st.markdown("<h3 style='text-align: center; color: grey;'>Διαχρονική Κατανομή Εργαζομένων ΚοιΣΠΕ</h3>", unsafe_allow_html=True)

                # Select the relevant columns
                columns = ['D9', 'D10', 'D11']
                # kpdf_selected = kpdf[columns]
                # Create the stacked bar plot using Plotly
                legend_labels = ['Γενικού Πληθυσμού', 'ΛΥΨΥ', 'ΕΚΟ']


                fig=stackedChart(columns,kpdf,legend_labels,'Έτος','% επι του Συνόλου',colors)

                # Show the plot
                st.plotly_chart(fig, use_container_width=True)
            with col3:
                pass



def ad_button3(id,kpdf,js_code):
    st.subheader("Ωρες απασχόλησης εργαζομένων")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
   
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #st.write('Δ14-Ωρες απασχολησης εργαζομένων ΛΥΨΥ(Μεσος Όρος)')
            text=kpdf['D14'][kpdf['year']==str(year_filter)].iloc[0]
            text=str(text.round())
            #st.write(kpdf['D14'][kpdf['year']==str(year_filter)])
            # st.write('Δ14-'+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Ωρες απασχολησης εργαζομένων ΛΥΨΥ(Μεσος Όρος)</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
            # st.metric(label="Συνολο Μελών "+str(kpdf['D1'][kpdf['year']==str(year_filter)][0]), value=int(kpdf['D1'][kpdf['year']==str(year_filter)][0]), delta=-0.5,delta_color="inverse")

        with col2:
            #st.write('Δ15-Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος)')
            #st.write(kpdf['D15'][kpdf['year']==str(year_filter)])
            text=kpdf['D15'][kpdf['year']==str(year_filter)].iloc[0]
            text=str(text.round())
            # st.write('Δ15-Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος): '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος)</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
        
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #st.write('Δ12-Ωρες απασχολησης εργαζομένων ΛΥΨΥ')
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μεταβολή Ωρών Απασχόλησης ΛΥΨΥ</h3>", unsafe_allow_html=True)
            categories=kpdf['year'].tolist()
            values =kpdf['D12'].tolist()
            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            #st.write('Δ13-Ωρες απασχολησης εργαζομένων ΕΚΟ')
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μεταβολή Ωρών Απασχόλησης ΕΚΟ</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D13'].tolist()

            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)
        


def ad_button4(id,kpdf,js_code):
    st.subheader("Ετήσιες Μονάδες Εργασίας")
    colors = px.colors.qualitative.Plotly

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #st.write('D18')
            #st.write(kpdf['D18'][kpdf['year']==str(year_filter)])
            text=str(kpdf['D18'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('D18 Ετησιες μοναδες εργασιας: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
        with col2:
            #st.write('D19')
            #st.write(kpdf['D19'][kpdf['year']==str(year_filter)])
            text=str(kpdf['D19'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('D19 Ετησιες μοναδες εργασιας: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας(Μέσος Όρος)</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )

    with st.container():
        col1, col2 =st.columns(2)
        
        #     # val=50
        with col1:
            # Create the layout with two y-axes
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας ΛΥΨΥ % επί του Συνόλου</h3>", unsafe_allow_html=True)
            val = float(kpdf['D22'][kpdf['year'] == str(year_filter)].iloc[0])
            fig=donut_pct_Chart(val,'rgb(135 206 235)', 'rgb(240,240,240)',['(%) Μ.Ε. ΛΥΨΥ επι του συνόλου', ' '])
            st.plotly_chart(fig, use_container_width=True)


        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας ΕΚΟ % επί του Συνόλου</h3>", unsafe_allow_html=True)
            val2=float(kpdf['D23'][kpdf['year']==str(year_filter)].iloc[0])
            fig=donut_pct_Chart(val2,'rgb(113,209,145)','rgb(240,240,240)',['(%) Μ.Ε. ΕΚΟ επι του συνόλου', ' '])
            st.plotly_chart(fig,use_container_width=True)

    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Μονάδων Εργασίας ΛΥΨΥ</h3>", unsafe_allow_html=True)
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D18_lipsi'].astype(int).tolist()

            fig=pctChangeChart(values,categories,'Αρ.Μονάδων Εργασίας ΛΥΨΥ','Ποσοστιαία μεταβολή','% Μεταβολή','Μ.Ε. ΛΥΨΥ')
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Μονάδων Εργασίας ΕΚΟ</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D18_eko'].astype(int).tolist()
            fig=pctChangeChart(values,categories,'Αρ.Μονάδων Εργασίας ΕΚΟ','Ποσοστιαία μεταβολή','% Μεταβολή','Μ.Ε. ΕΚΟ')
            st.plotly_chart(fig,use_container_width=True)


    with st.container():
         col1, col2,col3 = st.columns(3)
         with col1:
             pass
         with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Διαχρονική Κατανομή Μονάδων Εργασίας ΚοιΣΠΕ</h3>", unsafe_allow_html=True)

            # Select the relevant columns
            columns = ['D22', 'D23', 'D22_23_g']
            legend_labels = ['Μ.Ε. ΛΥΨΥ', 'Μ.Ε. ΕΚΟ', 'Μ.Ε. Γεν.Πληθ.']
            kpdf_selected = kpdf[columns]
            fig=stackedChart(columns,kpdf,legend_labels,'Έτος','% επι του Συνόλου',colors)
            st.plotly_chart(fig, use_container_width=True)
         with col3:
            pass
             



        




def e_button5(id,kpdf,js_code):
    st.subheader("Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος")
    colors = px.colors.qualitative.Plotly


    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    val2=float(kpdf['D24'][kpdf['year']==str(year_filter)].iloc[0])
        #st.write(first_alias_value)
        #st.markdown(text)
    st.markdown("<h3 style='text-align: center; color: grey;'>Κυκλοι Εργασιών</h3>", unsafe_allow_html=True)
    # text="**"+str(val2)+"** **&#8364;**"
    html(
        f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
        <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
        <script type="text/javascript">
        {js_code}
        animateCounter3("counter", 0, """+str(val2)+""", 1000);  // Increase from 0 to 100 in 1 second
        </script></body>
        """
    )

    st.markdown("<h3 style='text-align: center; color: grey;'>Yπηρεσίες</h3>", unsafe_allow_html=True)

    with st.container():
        col1, col2,col3 = st.columns(3)

        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>🏠 Κτηρίων & Εξ. Χώρων</h3>", unsafe_allow_html=True)

            val26=float(kpdf['D26'][kpdf['year']==str(year_filter)].iloc[0])
            # text26="**🏠** **"+str(val26)+"** &#8364; "

            html(
                    f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                    <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                    <script type="text/javascript">
                    {js_code}
                    animateCounter3("counter", 0, """+str(val26)+""", 1000);  // Increase from 0 to 100 in 1 second
                    </script></body>
                    """
                )


        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>🍴 Εστίασης</h3>", unsafe_allow_html=True)

            val27=float(kpdf['D27'][kpdf['year']==str(year_filter)].iloc[0])
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter3("counter", 0, """+str(val27)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
        with col3:
            st.markdown("<h3 style='text-align: center; color: grey;'>💬 Λοιπές Δραστηρίοτητες</h3>", unsafe_allow_html=True)

            val28=float(kpdf['D28'][kpdf['year']==str(year_filter)].iloc[0])
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter3("counter", 0, """+str(val28)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            pass
        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Ποσοστό επί του Συνόλου ανά Κατηγορία Κύκλου Εργασιών</h3>", unsafe_allow_html=True)

            labels = ['Κτηρια & Εξ.Χώροι ','Εστίαση','Λοιπές Δραστηριότητες']
            values=[val26,val27,val28]
            fig=pieChart(labels,values,colors)
            st.plotly_chart(fig,use_container_width=True)
        with col3:
            pass

    with st.container():
        col1,col2,col3 = st.columns(3)
        with col1:
            pass
        with col2:
             # Select the relevant columns
            st.markdown("<h3 style='text-align: center; color: grey;'>Διαχρονική Κατανομή Κύκλου Εργασιών ανά Κατηγορία</h3>", unsafe_allow_html=True)





            columns = ['D26', 'D27', 'D28']
            legend_labels = ['Κτηρια & Εξ.Χώροι ','Εστίαση','Λοιπές Δραστηριότητες']

            kpdf_selected = kpdf[columns]
            # Create the stacked bar plot using Plotly
            fig=stackedChart2(columns,kpdf,legend_labels,'Έτος','Συχνότητα',colors)
            st.plotly_chart(fig,use_container_width=True)
        with col3:
            pass
   




def e_button6(id,kpdf,js_code):
    st.subheader("% Mεταβολή κύκλου εργασιών ανά δραστηριότητα ανά έτος")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    val1=float(kpdf['D24'][kpdf['year']==str(year_filter)].iloc[0])
    val2=float(kpdf['D29'][kpdf['year']==str(year_filter)].iloc[0])
    val3=float(kpdf['D26'][kpdf['year']==str(year_filter)].iloc[0])
    val4=float(kpdf['D30'][kpdf['year']==str(year_filter)].iloc[0])
    val5=float(kpdf['D27'][kpdf['year']==str(year_filter)].iloc[0])
    val6=float(kpdf['D31'][kpdf['year']==str(year_filter)].iloc[0])
    val7=float(kpdf['D28'][kpdf['year']==str(year_filter)].iloc[0])
    val8=float(kpdf['D32'][kpdf['year']==str(year_filter)].iloc[0])
    with st.container():
        col1, col2,col3,col4 = st.columns(4)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μεταβολή Κύκλου Εργασιών</h3>", unsafe_allow_html=True)
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val1)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
                        )
            st.metric(label="% Μεταβολή Κύκλου Εργασιών",label_visibility="hidden", value=val1, delta=f'{val2}%')



        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μετ.Kύκλ.Εργ. Κτήρια/Εξωτερικοί Χώροι</h3>", unsafe_allow_html=True)
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val3)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
                        )
            st.metric(label="% Μετ.Kύκλ.Εργ. Κτήρια/Εξωτ. Χώροι ", label_visibility="hidden", value=val3, delta=f'{val4}%')
        with col3:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μετ.Κύκλ.Εργ. Υπηρ. Εστίασης</h3>", unsafe_allow_html=True)
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val5)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
                        )
            st.metric(label="% Μετ.Κύκλ.Εργ. Υπηρ. Εστίασης",label_visibility="hidden", value=val5, delta=f'{val6}%')
        with col4:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μετ.Κύκλ.Εργ. Λοιπ. Εργασίες</h3>", unsafe_allow_html=True)
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val7)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
                        )

            st.metric(label="% Μετ.Kυκλ.Εργ. Λοιπές εργασίες",label_visibility="hidden", value=val7, delta=f'{val8}%')

        

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Κύκλου Εργασιών</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D24'].astype(int).tolist()

            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μετ.Kύκλ.Εργ. Κτήρια/Εξωτ. Χώροι</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D26'].astype(int).tolist()

            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μετ.Κύκλ.Εργ. Υπηρ. Εστίασης</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D27'].astype(int).tolist()
            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μετ.Κύκλ.Εργ. Λοιπ. Δραστ.</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D28'].astype(int).tolist()
            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)





def e_button7(id,kpdf,js_code):
    st.subheader("Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος")

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    val1=float(kpdf['D36_overal'][kpdf['year']==str(year_filter)].iloc[0])
    val2=float(kpdf['D36'][kpdf['year']==str(year_filter)].iloc[0])
    val3=float(kpdf['D38'][kpdf['year']==str(year_filter)].iloc[0])
    val4=float(kpdf['D40'][kpdf['year']==str(year_filter)].iloc[0])
    val5=float(kpdf['D40_metaboli'][kpdf['year']==str(year_filter)].iloc[0])

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Καθαρών αποτελεσμάτων</h3>", unsafe_allow_html=True)
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val1)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
                        )
            st.metric(label="% Ετήσια Μεταβολή Καθαρών αποτελεσμάτων",label_visibility="hidden", value=val1, delta=f'{val2}%')
        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Αριθμοδείκτη καθαρών αποτελεσμάτων</h3>", unsafe_allow_html=True)
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val3)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
                        )
            st.metric(label="Αριθμοδείκτη καθαρών αποτελεσμάτων", label_visibility="hidden",value=val3)
        with col3:
            st.markdown("<h3 style='text-align: center; color: grey;'>Έσοδα ανά εργαζόμενο / % Ετήσια Μεταβολή</h3>", unsafe_allow_html=True)
            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center;     font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val4)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """    )

            st.metric(label="Έσοδα ανά εργαζόμενο / % Ετήσια Μεταβολή", label_visibility="hidden", value=val4, delta=f'{val5}%')
    
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Καθαρών Αποτελεσμάτων</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D36_overal'].astype(int).tolist()
            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)
        with col2:

            st.markdown("<h3 style='text-align: center; color: grey;'>Συμμετοχή (%) Επιδοτήσεων στα έσοδα / Ετος</h3>", unsafe_allow_html=True)

             
            val39=float(kpdf['D39'][kpdf['year']==str(year_filter)].iloc[0])
            fig=donut_pct_Chart(val39,'rgb(135 206 235)', 'rgb(240,240,240)',['% Συμμετοχή Επιδοτήσεων', ' '])
            st.plotly_chart(fig, use_container_width=True)
        

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1,col2,col3 = st.columns(3)  
        with col1:
            pass
        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Αριθμοδείκτης Καθαρών Αποτελεσμάτων / Έτος</h3>", unsafe_allow_html=True)

            fig = px.area(kpdf,x='year', y='D38', markers=True)
            st.plotly_chart(fig,use_container_width=True)
        with col3:
            pass



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
    
