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
    # css_style = """
    # <style>
    
    # *{
    # font-family:Copperplate;
    # }
    # .css-1xarl3l.e1vioofd1{
    # display:none;
    # }

    # .css-wnm74r{
    # text-align:center;
    # font-size: 2rem;
    # display: flex;
    # flex-direction: row;
    # -webkit-box-align: center;
    # align-items: center;
    # font-weight: 400;
    # }
    
    # .e1ugi8lo1.css-jhkj9c.ex0cdmw0{
    #     vertical-align: middle;
    #     overflow: hidden;
    #     color: inherit;
    #     fill: currentcolor;
    #     display: inline-flex;
    #     -webkit-box-align: center;
    #     align-items: center;
    #     font-size: 1.25rem;
    #     width: 40px;
    #     height: 40px;
    #     margin: 0px 0.125rem 0px 0px;
    # }
    # [data-testid="stSidebar"] {
    #     background-color: #f2f6fc; /* Replace with your desired color */
    # }
    # </style>"""
    
 




    with open( "style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


    #st.markdown(css_style, unsafe_allow_html=True)

            # Load the JavaScript function code
    with open("animated_counter.js", "r") as file:
            js_code = file.read()

    with open("style2.css", "r") as file:
            css_code = file.read()


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
        selected_option1 = st.radio("Επιλέξτε:", ["Συνεταιριστές","Εργαζόμενοι", "Ώρες Απασχόλησης", "Ετήσιες Μονάδες Εργασίας","Κύκλοι εργασιών", "Διαχρονική (%) μεταβολή Κύκλων Εργασιών", "Κατανομή πλήθους με βάση το καθαρό εισόδημα"])
    


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
    if selected_option1=="Κύκλοι εργασιών":
        e_button5(id,kpdf,js_code,css_code)
    elif selected_option1=="Διαχρονική (%) μεταβολή Κύκλων Εργασιών":
        e_button6(id,kpdf,js_code)
    elif selected_option1=="Κατανομή πλήθους με βάση το καθαρό εισόδημα":
        e_button7(id,kpdf,js_code,css_code)
   


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
        
       


        # html(
        #     f"""
            
        #         <div class="Component3" style="width: 329px; height: 201px; padding-bottom: 24px; padding-left: 24px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); border-radius: 15px; justify-content: space-between; align-items: flex-end; gap: 24px; display: inline-flex">
        #     <div class="Rectangle19" style="width: 329px; height: 210px; left: 0px; top: 0px; position: absolute; border-radius: 15px"></div>
        #     <div style="width: 56px; height: 56px; left: 285px; top: 27px; position: absolute">
        #         <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">

        #     <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
        #     <path id="Vector" d="M42.0002 27.3717C41.9987 26.1341 41.6395 24.9233 40.9659 23.8849C40.2924 22.8466 39.3331 22.025 38.2036 21.519V21.2022C38.2024 19.998 37.8029 18.8279 37.0674 17.8743C36.3319 16.9208 35.3016 16.2372 34.1371 15.9303C32.9726 15.6233 31.7393 15.7101 30.6293 16.1772C29.5193 16.6443 28.5949 17.4654 28.0002 18.5126C27.4055 17.4654 26.4811 16.6443 25.3711 16.1772C24.2611 15.7101 23.0278 15.6233 21.8633 15.9303C20.6988 16.2372 19.6685 16.9208 18.933 17.8743C18.1975 18.8279 17.798 19.998 17.7968 21.2022V21.519C16.6664 22.0233 15.7063 22.8442 15.0325 23.8826C14.3588 24.9209 14.0002 26.1322 14.0002 27.37C14.0002 28.6077 14.3588 29.819 15.0325 30.8573C15.7063 31.8957 16.6664 32.7166 17.7968 33.2209V33.5413C17.798 34.7455 18.1975 35.9156 18.933 36.8692C19.6685 37.8227 20.6988 38.5062 21.8633 38.8132C23.0278 39.1202 24.2611 39.0334 25.3711 38.5663C26.4811 38.0992 27.4055 37.2781 28.0002 36.2309C28.5949 37.2781 29.5193 38.0992 30.6293 38.5663C31.7393 39.0334 32.9726 39.1202 34.1371 38.8132C35.3016 38.5062 36.3319 37.8227 37.0674 36.8692C37.8029 35.9156 38.2024 34.7455 38.2036 33.5413V33.2209C39.3331 32.7159 40.2925 31.895 40.9661 30.8572C41.6397 29.8194 41.9989 28.609 42.0002 27.3717ZM23.2544 37.5752C22.206 37.5757 21.1986 37.168 20.4456 36.4385C19.6926 35.709 19.2532 34.7149 19.2205 33.667C19.6116 33.7412 20.0089 33.7785 20.407 33.7785H21.3561C21.5449 33.7785 21.726 33.7035 21.8595 33.57C21.993 33.4365 22.068 33.2555 22.068 33.0667C22.068 32.8779 21.993 32.6968 21.8595 32.5633C21.726 32.4298 21.5449 32.3548 21.3561 32.3548H20.407C19.2308 32.3558 18.0921 31.9406 17.1926 31.1829C16.293 30.4251 15.6905 29.3735 15.4916 28.2143C15.2927 27.055 15.5103 25.8628 16.1059 24.8485C16.7015 23.8342 17.6367 23.0634 18.7459 22.6722C18.8848 22.6231 19.005 22.5322 19.09 22.4119C19.175 22.2917 19.2206 22.148 19.2205 22.0007V21.2022C19.2205 20.1324 19.6455 19.1063 20.402 18.3498C21.1585 17.5933 22.1846 17.1683 23.2544 17.1683C24.3243 17.1683 25.3503 17.5933 26.1068 18.3498C26.8633 19.1063 27.2883 20.1324 27.2883 21.2022V29.8692C26.7777 29.3066 26.1551 28.8571 25.4603 28.5496C24.7656 28.242 24.0142 28.0833 23.2544 28.0836C23.0656 28.0836 22.8846 28.1586 22.7511 28.2921C22.6176 28.4256 22.5426 28.6067 22.5426 28.7955C22.5426 28.9843 22.6176 29.1653 22.7511 29.2988C22.8846 29.4323 23.0656 29.5073 23.2544 29.5073C24.3243 29.5073 25.3503 29.9323 26.1068 30.6889C26.8633 31.4454 27.2883 32.4714 27.2883 33.5413C27.2883 34.6111 26.8633 35.6372 26.1068 36.3937C25.3503 37.1502 24.3243 37.5752 23.2544 37.5752ZM35.5934 32.3548H34.6443C34.4555 32.3548 34.2744 32.4298 34.1409 32.5633C34.0074 32.6968 33.9324 32.8779 33.9324 33.0667C33.9324 33.2555 34.0074 33.4365 34.1409 33.57C34.2744 33.7035 34.4555 33.7785 34.6443 33.7785H35.5934C35.9915 33.7785 36.3888 33.7412 36.7799 33.667C36.7552 34.459 36.4978 35.2262 36.0398 35.8728C35.5818 36.5195 34.9435 37.0169 34.2045 37.303C33.4656 37.5891 32.6588 37.6513 31.8847 37.4817C31.1107 37.3122 30.4037 36.9184 29.8521 36.3495C29.3005 35.7807 28.9286 35.062 28.7828 34.2831C28.6371 33.5042 28.724 32.6997 29.0327 31.9699C29.3413 31.2401 29.8581 30.6174 30.5185 30.1794C31.1789 29.7415 31.9536 29.5077 32.746 29.5073C32.9348 29.5073 33.1158 29.4323 33.2493 29.2988C33.3828 29.1653 33.4578 28.9843 33.4578 28.7955C33.4578 28.6067 33.3828 28.4256 33.2493 28.2921C33.1158 28.1586 32.9348 28.0836 32.746 28.0836C31.9862 28.0833 31.2348 28.242 30.5401 28.5496C29.8453 28.8571 29.2227 29.3066 28.7121 29.8692V21.2022C28.7121 20.1324 29.1371 19.1063 29.8936 18.3498C30.6501 17.5933 31.6761 17.1683 32.746 17.1683C33.8158 17.1683 34.8419 17.5933 35.5984 18.3498C36.3549 19.1063 36.7799 20.1324 36.7799 21.2022V22.0007C36.7798 22.148 36.8254 22.2917 36.9104 22.4119C36.9954 22.5322 37.1156 22.6231 37.2545 22.6722C38.3637 23.0634 39.2989 23.8342 39.8945 24.8485C40.4901 25.8628 40.7077 27.055 40.5088 28.2143C40.3099 29.3735 39.7074 30.4251 38.8078 31.1829C37.9083 31.9406 36.7696 32.3558 35.5934 32.3548ZM37.2545 25.948C37.2545 26.1368 37.1795 26.3179 37.046 26.4514C36.9125 26.5849 36.7314 26.6599 36.5426 26.6599H36.068C34.9982 26.6599 33.9721 26.2349 33.2156 25.4784C32.4591 24.7219 32.0341 23.6958 32.0341 22.626V22.1514C32.0341 21.9626 32.1091 21.7815 32.2426 21.648C32.3761 21.5145 32.5572 21.4395 32.746 21.4395C32.9348 21.4395 33.1158 21.5145 33.2493 21.648C33.3828 21.7815 33.4578 21.9626 33.4578 22.1514V22.626C33.4578 23.3182 33.7328 23.9821 34.2224 24.4716C34.7119 24.9611 35.3758 25.2361 36.068 25.2361H36.5426C36.7314 25.2361 36.9125 25.3111 37.046 25.4446C37.1795 25.5781 37.2545 25.7592 37.2545 25.948ZM19.9324 26.6599H19.4578C19.269 26.6599 19.0879 26.5849 18.9544 26.4514C18.8209 26.3179 18.7459 26.1368 18.7459 25.948C18.7459 25.7592 18.8209 25.5781 18.9544 25.4446C19.0879 25.3111 19.269 25.2361 19.4578 25.2361H19.9324C20.6246 25.2361 21.2886 24.9611 21.7781 24.4716C22.2676 23.9821 22.5426 23.3182 22.5426 22.626V22.1514C22.5426 21.9626 22.6176 21.7815 22.7511 21.648C22.8846 21.5145 23.0656 21.4395 23.2544 21.4395C23.4432 21.4395 23.6243 21.5145 23.7578 21.648C23.8913 21.7815 23.9663 21.9626 23.9663 22.1514V22.626C23.9663 23.6958 23.5413 24.7219 22.7848 25.4784C22.0283 26.2349 21.0022 26.6599 19.9324 26.6599Z" fill="#8E8D8D"/>

        #     </svg>

                
            
            
        #     </div>
        #     <div class="Frame15" style="left: 29px; top: 115px; position: absolute; justify-content: flex-start; align-items: flex-end; gap: 24px; display: inline-flex">
        #         <div id="counter" style="color: #111416; font-size: 150px; font-family:  'Source Sans Pro',sans-serif; font-weight: 700; line-height: 47.93px; word-wrap: break-word"></div>
        #         <div class="Frame9" style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 0px; display: inline-flex">
        #         <div style="color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Σύνολο Εργαζομένων</div>
        #         <div style="color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Γεν. Πληθυσμού</div>
        #         </div>
        #     </div>
        #     </div>
        #       <script type="text/javascript">
        #         {js_code}
        #         animateCounter("counter", 0, """+str(val)+""", 1000);  // Increase from 0 to 100 in 1 second
        #         </script>
        #     """,height = 250
        # )
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
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g id="&#206;&#147;&#206;&#181;&#206;&#189;&#206;&#185;&#206;&#186;&#207;&#140;&#207;&#130; &#207;&#128;&#206;&#187;&#206;&#183;&#206;&#184;&#207;&#133;&#207;&#131;&#206;&#188;&#207;&#140;&#207;&#130;">
                                <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
                                <g id="Group">
                                <path id="Vector" fill-rule="evenodd" clip-rule="evenodd" d="M19.9398 24.2348C20.8399 24.2348 21.7032 23.8772 22.3397 23.2407C22.9762 22.6042 23.3337 21.741 23.3337 20.8408C23.3337 19.9407 22.9762 19.0775 22.3397 18.441C21.7032 17.8045 20.8399 17.4469 19.9398 17.4469C19.0397 17.4469 18.1764 17.8045 17.5399 18.441C16.9034 19.0775 16.5458 19.9407 16.5458 20.8408C16.5458 21.741 16.9034 22.6042 17.5399 23.2407C18.1764 23.8772 19.0397 24.2348 19.9398 24.2348ZM19.9398 25.9318C20.6083 25.9318 21.2703 25.8001 21.888 25.5442C22.5057 25.2884 23.0669 24.9134 23.5396 24.4407C24.0123 23.9679 24.3873 23.4067 24.6432 22.7891C24.899 22.1714 25.0307 21.5094 25.0307 20.8408C25.0307 20.1723 24.899 19.5103 24.6432 18.8926C24.3873 18.275 24.0123 17.7138 23.5396 17.241C23.0669 16.7683 22.5057 16.3933 21.888 16.1375C21.2703 15.8816 20.6083 15.7499 19.9398 15.7499C18.5896 15.7499 17.2947 16.2863 16.34 17.241C15.3852 18.1958 14.8489 19.4907 14.8489 20.8408C14.8489 22.191 15.3852 23.4859 16.34 24.4407C17.2947 25.3954 18.5896 25.9318 19.9398 25.9318Z" fill="url(#paint0_linear_31_789)"/>
                                <path id="Vector_2" fill-rule="evenodd" clip-rule="evenodd" d="M17.9949 24.0583C18.0739 24.1371 18.1366 24.2307 18.1794 24.3338C18.2222 24.4369 18.2442 24.5474 18.2442 24.659C18.2442 24.7706 18.2222 24.8811 18.1794 24.9842C18.1366 25.0873 18.0739 25.1809 17.9949 25.2597L17.4213 25.8316C16.3175 26.9358 15.6974 28.433 15.6972 29.9943V33.1439C15.6972 33.3689 15.6078 33.5847 15.4487 33.7438C15.2896 33.903 15.0738 33.9924 14.8487 33.9924C14.6237 33.9924 14.4079 33.903 14.2488 33.7438C14.0896 33.5847 14.0002 33.3689 14.0002 33.1439V29.9943C14.0005 27.983 14.7995 26.0542 16.2216 24.6319L16.7935 24.0583C16.8723 23.9793 16.9659 23.9166 17.069 23.8738C17.1721 23.831 17.2826 23.809 17.3942 23.809C17.5058 23.809 17.6163 23.831 17.7194 23.8738C17.8225 23.9166 17.9161 23.9793 17.9949 24.0583ZM38.0056 23.5492C37.9266 23.628 37.8639 23.7216 37.8211 23.8247C37.7783 23.9278 37.7563 24.0383 37.7563 24.1499C37.7563 24.2615 37.7783 24.372 37.8211 24.4751C37.8639 24.5782 37.9266 24.6718 38.0056 24.7507L38.5792 25.3225C39.1258 25.8692 39.5594 26.5182 39.8552 27.2324C40.151 27.9466 40.3033 28.7121 40.3033 29.4852V33.1439C40.3033 33.3689 40.3927 33.5847 40.5518 33.7438C40.7109 33.903 40.9267 33.9924 41.1518 33.9924C41.3768 33.9924 41.5926 33.903 41.7517 33.7438C41.9109 33.5847 42.0002 33.3689 42.0002 33.1439V29.4852C42 27.4739 41.201 25.5451 39.7789 24.1228L39.207 23.5492C39.1282 23.4702 39.0346 23.4075 38.9315 23.3647C38.8284 23.3219 38.7179 23.2999 38.6063 23.2999C38.4947 23.2999 38.3842 23.3219 38.2811 23.3647C38.178 23.4075 38.0844 23.4702 38.0056 23.5492Z" fill="url(#paint1_linear_31_789)"/>
                                <path id="Vector_3" fill-rule="evenodd" clip-rule="evenodd" d="M35.2122 24.2348C34.3121 24.2348 33.4488 23.8772 32.8124 23.2407C32.1759 22.6042 31.8183 21.741 31.8183 20.8408C31.8183 19.9407 32.1759 19.0775 32.8124 18.441C33.4488 17.8045 34.3121 17.4469 35.2122 17.4469C36.1124 17.4469 36.9756 17.8045 37.6121 18.441C38.2486 19.0775 38.6062 19.9407 38.6062 20.8408C38.6062 21.741 38.2486 22.6042 37.6121 23.2407C36.9756 23.8772 36.1124 24.2348 35.2122 24.2348ZM35.2122 25.9318C34.5437 25.9318 33.8817 25.8001 33.264 25.5442C32.6464 25.2884 32.0852 24.9134 31.6124 24.4407C31.1397 23.9679 30.7647 23.4067 30.5088 22.7891C30.253 22.1714 30.1213 21.5094 30.1213 20.8408C30.1213 20.1723 30.253 19.5103 30.5088 18.8926C30.7647 18.275 31.1397 17.7138 31.6124 17.241C32.0852 16.7683 32.6464 16.3933 33.264 16.1375C33.8817 15.8816 34.5437 15.7499 35.2122 15.7499C36.5624 15.7499 37.8573 16.2863 38.8121 17.241C39.7668 18.1958 40.3031 19.4907 40.3031 20.8408C40.3031 22.191 39.7668 23.4859 38.8121 24.4407C37.8573 25.3954 36.5624 25.9318 35.2122 25.9318ZM27.5759 31.4469C26.4507 31.4469 25.3716 31.8939 24.576 32.6895C23.7804 33.4851 23.3334 34.5642 23.3334 35.6893V37.8954C23.3334 38.1204 23.2441 38.3362 23.0849 38.4954C22.9258 38.6545 22.71 38.7439 22.485 38.7439C22.2599 38.7439 22.0441 38.6545 21.885 38.4954C21.7259 38.3362 21.6365 38.1204 21.6365 37.8954V35.6893C21.6365 34.1141 22.2622 32.6034 23.3761 31.4895C24.4899 30.3757 26.0006 29.7499 27.5759 29.7499C29.1511 29.7499 30.6618 30.3757 31.7757 31.4895C32.8895 32.6034 33.5153 34.1141 33.5153 35.6893V37.8954C33.5153 38.1204 33.4259 38.3362 33.2667 38.4954C33.1076 38.6545 32.8918 38.7439 32.6668 38.7439C32.4417 38.7439 32.2259 38.6545 32.0668 38.4954C31.9077 38.3362 31.8183 38.1204 31.8183 37.8954V35.6893C31.8183 35.1322 31.7086 34.5805 31.4954 34.0658C31.2822 33.5511 30.9697 33.0834 30.5757 32.6895C30.1818 32.2955 29.7141 31.983 29.1994 31.7698C28.6847 31.5566 28.133 31.4469 27.5759 31.4469Z" fill="url(#paint2_linear_31_789)"/>
                                <path id="Vector_4" fill-rule="evenodd" clip-rule="evenodd" d="M27.5758 28.9014C28.4759 28.9014 29.3392 28.5438 29.9756 27.9074C30.6121 27.2709 30.9697 26.4076 30.9697 25.5075C30.9697 24.6073 30.6121 23.7441 29.9756 23.1076C29.3392 22.4711 28.4759 22.1135 27.5758 22.1135C26.6756 22.1135 25.8124 22.4711 25.1759 23.1076C24.5394 23.7441 24.1818 24.6073 24.1818 25.5075C24.1818 26.4076 24.5394 27.2709 25.1759 27.9074C25.8124 28.5438 26.6756 28.9014 27.5758 28.9014ZM27.5758 30.5984C28.926 30.5984 30.2209 30.062 31.1756 29.1073C32.1303 28.1526 32.6667 26.8577 32.6667 25.5075C32.6667 24.1573 32.1303 22.8624 31.1756 21.9077C30.2209 20.9529 28.926 20.4166 27.5758 20.4166C26.2256 20.4166 24.9307 20.9529 23.976 21.9077C23.0212 22.8624 22.4849 24.1573 22.4849 25.5075C22.4849 26.8577 23.0212 28.1526 23.976 29.1073C24.9307 30.062 26.2256 30.5984 27.5758 30.5984Z" fill="url(#paint3_linear_31_789)"/>
                                </g>
                                </g>
                                <defs>
                                <linearGradient id="paint0_linear_31_789" x1="16.1032" y1="16.407" x2="27.9294" y2="29.368" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                <linearGradient id="paint1_linear_31_789" x1="17.4496" y1="23.9899" x2="25.1997" y2="46.2324" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                <linearGradient id="paint2_linear_31_789" x1="23.936" y1="17.2337" x2="50.5736" y2="40.9334" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                <linearGradient id="paint3_linear_31_789" x1="23.7392" y1="21.0736" x2="35.5654" y2="34.0346" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                </defs>
                            </svg>
                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
                            <div>
                                <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Σύνολο Εργαζομένων</div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Γεν. Πληθυσμού</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(val)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
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
            # st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι Γεν. Πληθυσμού</h3>", unsafe_allow_html=True)
            # html(
            #     f"""
            #         <div class="Component3" style="width: 290px; height: 183px; padding-bottom: 24px; padding-left: 24px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); border-radius: 15px; justify-content: space-between; align-items: flex-end; gap: 24px; display: inline-flex">
            #     <div class="Rectangle19" style="width: 329px; height: 210px; left: 0px; top: 0px; position: absolute; border-radius: 15px"></div>
            #     <div style="width: 56px; height: 56px; left: 256px; top: 19px; position: absolute">
            #         <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">

            #     <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
            #     <path id="Vector" d="M42.0002 27.3717C41.9987 26.1341 41.6395 24.9233 40.9659 23.8849C40.2924 22.8466 39.3331 22.025 38.2036 21.519V21.2022C38.2024 19.998 37.8029 18.8279 37.0674 17.8743C36.3319 16.9208 35.3016 16.2372 34.1371 15.9303C32.9726 15.6233 31.7393 15.7101 30.6293 16.1772C29.5193 16.6443 28.5949 17.4654 28.0002 18.5126C27.4055 17.4654 26.4811 16.6443 25.3711 16.1772C24.2611 15.7101 23.0278 15.6233 21.8633 15.9303C20.6988 16.2372 19.6685 16.9208 18.933 17.8743C18.1975 18.8279 17.798 19.998 17.7968 21.2022V21.519C16.6664 22.0233 15.7063 22.8442 15.0325 23.8826C14.3588 24.9209 14.0002 26.1322 14.0002 27.37C14.0002 28.6077 14.3588 29.819 15.0325 30.8573C15.7063 31.8957 16.6664 32.7166 17.7968 33.2209V33.5413C17.798 34.7455 18.1975 35.9156 18.933 36.8692C19.6685 37.8227 20.6988 38.5062 21.8633 38.8132C23.0278 39.1202 24.2611 39.0334 25.3711 38.5663C26.4811 38.0992 27.4055 37.2781 28.0002 36.2309C28.5949 37.2781 29.5193 38.0992 30.6293 38.5663C31.7393 39.0334 32.9726 39.1202 34.1371 38.8132C35.3016 38.5062 36.3319 37.8227 37.0674 36.8692C37.8029 35.9156 38.2024 34.7455 38.2036 33.5413V33.2209C39.3331 32.7159 40.2925 31.895 40.9661 30.8572C41.6397 29.8194 41.9989 28.609 42.0002 27.3717ZM23.2544 37.5752C22.206 37.5757 21.1986 37.168 20.4456 36.4385C19.6926 35.709 19.2532 34.7149 19.2205 33.667C19.6116 33.7412 20.0089 33.7785 20.407 33.7785H21.3561C21.5449 33.7785 21.726 33.7035 21.8595 33.57C21.993 33.4365 22.068 33.2555 22.068 33.0667C22.068 32.8779 21.993 32.6968 21.8595 32.5633C21.726 32.4298 21.5449 32.3548 21.3561 32.3548H20.407C19.2308 32.3558 18.0921 31.9406 17.1926 31.1829C16.293 30.4251 15.6905 29.3735 15.4916 28.2143C15.2927 27.055 15.5103 25.8628 16.1059 24.8485C16.7015 23.8342 17.6367 23.0634 18.7459 22.6722C18.8848 22.6231 19.005 22.5322 19.09 22.4119C19.175 22.2917 19.2206 22.148 19.2205 22.0007V21.2022C19.2205 20.1324 19.6455 19.1063 20.402 18.3498C21.1585 17.5933 22.1846 17.1683 23.2544 17.1683C24.3243 17.1683 25.3503 17.5933 26.1068 18.3498C26.8633 19.1063 27.2883 20.1324 27.2883 21.2022V29.8692C26.7777 29.3066 26.1551 28.8571 25.4603 28.5496C24.7656 28.242 24.0142 28.0833 23.2544 28.0836C23.0656 28.0836 22.8846 28.1586 22.7511 28.2921C22.6176 28.4256 22.5426 28.6067 22.5426 28.7955C22.5426 28.9843 22.6176 29.1653 22.7511 29.2988C22.8846 29.4323 23.0656 29.5073 23.2544 29.5073C24.3243 29.5073 25.3503 29.9323 26.1068 30.6889C26.8633 31.4454 27.2883 32.4714 27.2883 33.5413C27.2883 34.6111 26.8633 35.6372 26.1068 36.3937C25.3503 37.1502 24.3243 37.5752 23.2544 37.5752ZM35.5934 32.3548H34.6443C34.4555 32.3548 34.2744 32.4298 34.1409 32.5633C34.0074 32.6968 33.9324 32.8779 33.9324 33.0667C33.9324 33.2555 34.0074 33.4365 34.1409 33.57C34.2744 33.7035 34.4555 33.7785 34.6443 33.7785H35.5934C35.9915 33.7785 36.3888 33.7412 36.7799 33.667C36.7552 34.459 36.4978 35.2262 36.0398 35.8728C35.5818 36.5195 34.9435 37.0169 34.2045 37.303C33.4656 37.5891 32.6588 37.6513 31.8847 37.4817C31.1107 37.3122 30.4037 36.9184 29.8521 36.3495C29.3005 35.7807 28.9286 35.062 28.7828 34.2831C28.6371 33.5042 28.724 32.6997 29.0327 31.9699C29.3413 31.2401 29.8581 30.6174 30.5185 30.1794C31.1789 29.7415 31.9536 29.5077 32.746 29.5073C32.9348 29.5073 33.1158 29.4323 33.2493 29.2988C33.3828 29.1653 33.4578 28.9843 33.4578 28.7955C33.4578 28.6067 33.3828 28.4256 33.2493 28.2921C33.1158 28.1586 32.9348 28.0836 32.746 28.0836C31.9862 28.0833 31.2348 28.242 30.5401 28.5496C29.8453 28.8571 29.2227 29.3066 28.7121 29.8692V21.2022C28.7121 20.1324 29.1371 19.1063 29.8936 18.3498C30.6501 17.5933 31.6761 17.1683 32.746 17.1683C33.8158 17.1683 34.8419 17.5933 35.5984 18.3498C36.3549 19.1063 36.7799 20.1324 36.7799 21.2022V22.0007C36.7798 22.148 36.8254 22.2917 36.9104 22.4119C36.9954 22.5322 37.1156 22.6231 37.2545 22.6722C38.3637 23.0634 39.2989 23.8342 39.8945 24.8485C40.4901 25.8628 40.7077 27.055 40.5088 28.2143C40.3099 29.3735 39.7074 30.4251 38.8078 31.1829C37.9083 31.9406 36.7696 32.3558 35.5934 32.3548ZM37.2545 25.948C37.2545 26.1368 37.1795 26.3179 37.046 26.4514C36.9125 26.5849 36.7314 26.6599 36.5426 26.6599H36.068C34.9982 26.6599 33.9721 26.2349 33.2156 25.4784C32.4591 24.7219 32.0341 23.6958 32.0341 22.626V22.1514C32.0341 21.9626 32.1091 21.7815 32.2426 21.648C32.3761 21.5145 32.5572 21.4395 32.746 21.4395C32.9348 21.4395 33.1158 21.5145 33.2493 21.648C33.3828 21.7815 33.4578 21.9626 33.4578 22.1514V22.626C33.4578 23.3182 33.7328 23.9821 34.2224 24.4716C34.7119 24.9611 35.3758 25.2361 36.068 25.2361H36.5426C36.7314 25.2361 36.9125 25.3111 37.046 25.4446C37.1795 25.5781 37.2545 25.7592 37.2545 25.948ZM19.9324 26.6599H19.4578C19.269 26.6599 19.0879 26.5849 18.9544 26.4514C18.8209 26.3179 18.7459 26.1368 18.7459 25.948C18.7459 25.7592 18.8209 25.5781 18.9544 25.4446C19.0879 25.3111 19.269 25.2361 19.4578 25.2361H19.9324C20.6246 25.2361 21.2886 24.9611 21.7781 24.4716C22.2676 23.9821 22.5426 23.3182 22.5426 22.626V22.1514C22.5426 21.9626 22.6176 21.7815 22.7511 21.648C22.8846 21.5145 23.0656 21.4395 23.2544 21.4395C23.4432 21.4395 23.6243 21.5145 23.7578 21.648C23.8913 21.7815 23.9663 21.9626 23.9663 22.1514V22.626C23.9663 23.6958 23.5413 24.7219 22.7848 25.4784C22.0283 26.2349 21.0022 26.6599 19.9324 26.6599Z" fill="#8E8D8D"/>

            #     </svg>

                    
                
                
            #     </div>
            #     <div class="Frame15" style="left: 29px; top: 115px; position: absolute; justify-content: flex-start; align-items: flex-end; gap: 24px; display: inline-flex">
            #         <div id="counter" style="color: #111416; font-size: 150px; font-family:  'Source Sans Pro',sans-serif; font-weight: 700; line-height: 47.93px; word-wrap: break-word"></div>
            #         <div class="Frame9" style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 0px; display: inline-flex">
            #         <div style="color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
            #         <div style="color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Γεν. Πληθυσμού</div>
            #         </div>
            #     </div>
            #     </div>
            #     <script type="text/javascript">
            #         {js_code}
            #         animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #         </script>
            #     """,height = 250
            # )
            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;     font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            # )
            #st.write(kpdf['D3'][kpdf['year']==str(year_filter)])
            html(
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g id="&#206;&#147;&#206;&#181;&#206;&#189;&#206;&#185;&#206;&#186;&#207;&#140;&#207;&#130; &#207;&#128;&#206;&#187;&#206;&#183;&#206;&#184;&#207;&#133;&#207;&#131;&#206;&#188;&#207;&#140;&#207;&#130;">
                                <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
                                <g id="Group">
                                <path id="Vector" fill-rule="evenodd" clip-rule="evenodd" d="M19.9398 24.2348C20.8399 24.2348 21.7032 23.8772 22.3397 23.2407C22.9762 22.6042 23.3337 21.741 23.3337 20.8408C23.3337 19.9407 22.9762 19.0775 22.3397 18.441C21.7032 17.8045 20.8399 17.4469 19.9398 17.4469C19.0397 17.4469 18.1764 17.8045 17.5399 18.441C16.9034 19.0775 16.5458 19.9407 16.5458 20.8408C16.5458 21.741 16.9034 22.6042 17.5399 23.2407C18.1764 23.8772 19.0397 24.2348 19.9398 24.2348ZM19.9398 25.9318C20.6083 25.9318 21.2703 25.8001 21.888 25.5442C22.5057 25.2884 23.0669 24.9134 23.5396 24.4407C24.0123 23.9679 24.3873 23.4067 24.6432 22.7891C24.899 22.1714 25.0307 21.5094 25.0307 20.8408C25.0307 20.1723 24.899 19.5103 24.6432 18.8926C24.3873 18.275 24.0123 17.7138 23.5396 17.241C23.0669 16.7683 22.5057 16.3933 21.888 16.1375C21.2703 15.8816 20.6083 15.7499 19.9398 15.7499C18.5896 15.7499 17.2947 16.2863 16.34 17.241C15.3852 18.1958 14.8489 19.4907 14.8489 20.8408C14.8489 22.191 15.3852 23.4859 16.34 24.4407C17.2947 25.3954 18.5896 25.9318 19.9398 25.9318Z" fill="url(#paint0_linear_31_789)"/>
                                <path id="Vector_2" fill-rule="evenodd" clip-rule="evenodd" d="M17.9949 24.0583C18.0739 24.1371 18.1366 24.2307 18.1794 24.3338C18.2222 24.4369 18.2442 24.5474 18.2442 24.659C18.2442 24.7706 18.2222 24.8811 18.1794 24.9842C18.1366 25.0873 18.0739 25.1809 17.9949 25.2597L17.4213 25.8316C16.3175 26.9358 15.6974 28.433 15.6972 29.9943V33.1439C15.6972 33.3689 15.6078 33.5847 15.4487 33.7438C15.2896 33.903 15.0738 33.9924 14.8487 33.9924C14.6237 33.9924 14.4079 33.903 14.2488 33.7438C14.0896 33.5847 14.0002 33.3689 14.0002 33.1439V29.9943C14.0005 27.983 14.7995 26.0542 16.2216 24.6319L16.7935 24.0583C16.8723 23.9793 16.9659 23.9166 17.069 23.8738C17.1721 23.831 17.2826 23.809 17.3942 23.809C17.5058 23.809 17.6163 23.831 17.7194 23.8738C17.8225 23.9166 17.9161 23.9793 17.9949 24.0583ZM38.0056 23.5492C37.9266 23.628 37.8639 23.7216 37.8211 23.8247C37.7783 23.9278 37.7563 24.0383 37.7563 24.1499C37.7563 24.2615 37.7783 24.372 37.8211 24.4751C37.8639 24.5782 37.9266 24.6718 38.0056 24.7507L38.5792 25.3225C39.1258 25.8692 39.5594 26.5182 39.8552 27.2324C40.151 27.9466 40.3033 28.7121 40.3033 29.4852V33.1439C40.3033 33.3689 40.3927 33.5847 40.5518 33.7438C40.7109 33.903 40.9267 33.9924 41.1518 33.9924C41.3768 33.9924 41.5926 33.903 41.7517 33.7438C41.9109 33.5847 42.0002 33.3689 42.0002 33.1439V29.4852C42 27.4739 41.201 25.5451 39.7789 24.1228L39.207 23.5492C39.1282 23.4702 39.0346 23.4075 38.9315 23.3647C38.8284 23.3219 38.7179 23.2999 38.6063 23.2999C38.4947 23.2999 38.3842 23.3219 38.2811 23.3647C38.178 23.4075 38.0844 23.4702 38.0056 23.5492Z" fill="url(#paint1_linear_31_789)"/>
                                <path id="Vector_3" fill-rule="evenodd" clip-rule="evenodd" d="M35.2122 24.2348C34.3121 24.2348 33.4488 23.8772 32.8124 23.2407C32.1759 22.6042 31.8183 21.741 31.8183 20.8408C31.8183 19.9407 32.1759 19.0775 32.8124 18.441C33.4488 17.8045 34.3121 17.4469 35.2122 17.4469C36.1124 17.4469 36.9756 17.8045 37.6121 18.441C38.2486 19.0775 38.6062 19.9407 38.6062 20.8408C38.6062 21.741 38.2486 22.6042 37.6121 23.2407C36.9756 23.8772 36.1124 24.2348 35.2122 24.2348ZM35.2122 25.9318C34.5437 25.9318 33.8817 25.8001 33.264 25.5442C32.6464 25.2884 32.0852 24.9134 31.6124 24.4407C31.1397 23.9679 30.7647 23.4067 30.5088 22.7891C30.253 22.1714 30.1213 21.5094 30.1213 20.8408C30.1213 20.1723 30.253 19.5103 30.5088 18.8926C30.7647 18.275 31.1397 17.7138 31.6124 17.241C32.0852 16.7683 32.6464 16.3933 33.264 16.1375C33.8817 15.8816 34.5437 15.7499 35.2122 15.7499C36.5624 15.7499 37.8573 16.2863 38.8121 17.241C39.7668 18.1958 40.3031 19.4907 40.3031 20.8408C40.3031 22.191 39.7668 23.4859 38.8121 24.4407C37.8573 25.3954 36.5624 25.9318 35.2122 25.9318ZM27.5759 31.4469C26.4507 31.4469 25.3716 31.8939 24.576 32.6895C23.7804 33.4851 23.3334 34.5642 23.3334 35.6893V37.8954C23.3334 38.1204 23.2441 38.3362 23.0849 38.4954C22.9258 38.6545 22.71 38.7439 22.485 38.7439C22.2599 38.7439 22.0441 38.6545 21.885 38.4954C21.7259 38.3362 21.6365 38.1204 21.6365 37.8954V35.6893C21.6365 34.1141 22.2622 32.6034 23.3761 31.4895C24.4899 30.3757 26.0006 29.7499 27.5759 29.7499C29.1511 29.7499 30.6618 30.3757 31.7757 31.4895C32.8895 32.6034 33.5153 34.1141 33.5153 35.6893V37.8954C33.5153 38.1204 33.4259 38.3362 33.2667 38.4954C33.1076 38.6545 32.8918 38.7439 32.6668 38.7439C32.4417 38.7439 32.2259 38.6545 32.0668 38.4954C31.9077 38.3362 31.8183 38.1204 31.8183 37.8954V35.6893C31.8183 35.1322 31.7086 34.5805 31.4954 34.0658C31.2822 33.5511 30.9697 33.0834 30.5757 32.6895C30.1818 32.2955 29.7141 31.983 29.1994 31.7698C28.6847 31.5566 28.133 31.4469 27.5759 31.4469Z" fill="url(#paint2_linear_31_789)"/>
                                <path id="Vector_4" fill-rule="evenodd" clip-rule="evenodd" d="M27.5758 28.9014C28.4759 28.9014 29.3392 28.5438 29.9756 27.9074C30.6121 27.2709 30.9697 26.4076 30.9697 25.5075C30.9697 24.6073 30.6121 23.7441 29.9756 23.1076C29.3392 22.4711 28.4759 22.1135 27.5758 22.1135C26.6756 22.1135 25.8124 22.4711 25.1759 23.1076C24.5394 23.7441 24.1818 24.6073 24.1818 25.5075C24.1818 26.4076 24.5394 27.2709 25.1759 27.9074C25.8124 28.5438 26.6756 28.9014 27.5758 28.9014ZM27.5758 30.5984C28.926 30.5984 30.2209 30.062 31.1756 29.1073C32.1303 28.1526 32.6667 26.8577 32.6667 25.5075C32.6667 24.1573 32.1303 22.8624 31.1756 21.9077C30.2209 20.9529 28.926 20.4166 27.5758 20.4166C26.2256 20.4166 24.9307 20.9529 23.976 21.9077C23.0212 22.8624 22.4849 24.1573 22.4849 25.5075C22.4849 26.8577 23.0212 28.1526 23.976 29.1073C24.9307 30.062 26.2256 30.5984 27.5758 30.5984Z" fill="url(#paint3_linear_31_789)"/>
                                </g>
                                </g>
                                <defs>
                                <linearGradient id="paint0_linear_31_789" x1="16.1032" y1="16.407" x2="27.9294" y2="29.368" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                <linearGradient id="paint1_linear_31_789" x1="17.4496" y1="23.9899" x2="25.1997" y2="46.2324" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                <linearGradient id="paint2_linear_31_789" x1="23.936" y1="17.2337" x2="50.5736" y2="40.9334" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                <linearGradient id="paint3_linear_31_789" x1="23.7392" y1="21.0736" x2="35.5654" y2="34.0346" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                </defs>
                            </svg>
                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
                            <div>
                                <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Γεν. Πληθυσμού</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
        )
        with col2:
            
            text=kpdf['D5'][kpdf['year']==str(year_filter)].iloc[0]
            # st.write('Δ5-Εργαζόμενοι ΛΥΨΥ: '+text)
            # st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΛΥΨΥ</h3>", unsafe_allow_html=True)
            # html(
            #     f"""
            #         <div class="Component3" style="width: 290px; height: 183px; padding-bottom: 24px; padding-left: 24px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); border-radius: 15px; justify-content: space-between; align-items: flex-end; gap: 24px; display: inline-flex">
            #     <div class="Rectangle19" style="width: 329px; height: 210px; left: 0px; top: 0px; position: absolute; border-radius: 15px"></div>
            #     <div style="width: 56px; height: 56px; left: 256px; top: 19px; position: absolute">
            #         <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">

            #     <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
            #     <path id="Vector" d="M42.0002 27.3717C41.9987 26.1341 41.6395 24.9233 40.9659 23.8849C40.2924 22.8466 39.3331 22.025 38.2036 21.519V21.2022C38.2024 19.998 37.8029 18.8279 37.0674 17.8743C36.3319 16.9208 35.3016 16.2372 34.1371 15.9303C32.9726 15.6233 31.7393 15.7101 30.6293 16.1772C29.5193 16.6443 28.5949 17.4654 28.0002 18.5126C27.4055 17.4654 26.4811 16.6443 25.3711 16.1772C24.2611 15.7101 23.0278 15.6233 21.8633 15.9303C20.6988 16.2372 19.6685 16.9208 18.933 17.8743C18.1975 18.8279 17.798 19.998 17.7968 21.2022V21.519C16.6664 22.0233 15.7063 22.8442 15.0325 23.8826C14.3588 24.9209 14.0002 26.1322 14.0002 27.37C14.0002 28.6077 14.3588 29.819 15.0325 30.8573C15.7063 31.8957 16.6664 32.7166 17.7968 33.2209V33.5413C17.798 34.7455 18.1975 35.9156 18.933 36.8692C19.6685 37.8227 20.6988 38.5062 21.8633 38.8132C23.0278 39.1202 24.2611 39.0334 25.3711 38.5663C26.4811 38.0992 27.4055 37.2781 28.0002 36.2309C28.5949 37.2781 29.5193 38.0992 30.6293 38.5663C31.7393 39.0334 32.9726 39.1202 34.1371 38.8132C35.3016 38.5062 36.3319 37.8227 37.0674 36.8692C37.8029 35.9156 38.2024 34.7455 38.2036 33.5413V33.2209C39.3331 32.7159 40.2925 31.895 40.9661 30.8572C41.6397 29.8194 41.9989 28.609 42.0002 27.3717ZM23.2544 37.5752C22.206 37.5757 21.1986 37.168 20.4456 36.4385C19.6926 35.709 19.2532 34.7149 19.2205 33.667C19.6116 33.7412 20.0089 33.7785 20.407 33.7785H21.3561C21.5449 33.7785 21.726 33.7035 21.8595 33.57C21.993 33.4365 22.068 33.2555 22.068 33.0667C22.068 32.8779 21.993 32.6968 21.8595 32.5633C21.726 32.4298 21.5449 32.3548 21.3561 32.3548H20.407C19.2308 32.3558 18.0921 31.9406 17.1926 31.1829C16.293 30.4251 15.6905 29.3735 15.4916 28.2143C15.2927 27.055 15.5103 25.8628 16.1059 24.8485C16.7015 23.8342 17.6367 23.0634 18.7459 22.6722C18.8848 22.6231 19.005 22.5322 19.09 22.4119C19.175 22.2917 19.2206 22.148 19.2205 22.0007V21.2022C19.2205 20.1324 19.6455 19.1063 20.402 18.3498C21.1585 17.5933 22.1846 17.1683 23.2544 17.1683C24.3243 17.1683 25.3503 17.5933 26.1068 18.3498C26.8633 19.1063 27.2883 20.1324 27.2883 21.2022V29.8692C26.7777 29.3066 26.1551 28.8571 25.4603 28.5496C24.7656 28.242 24.0142 28.0833 23.2544 28.0836C23.0656 28.0836 22.8846 28.1586 22.7511 28.2921C22.6176 28.4256 22.5426 28.6067 22.5426 28.7955C22.5426 28.9843 22.6176 29.1653 22.7511 29.2988C22.8846 29.4323 23.0656 29.5073 23.2544 29.5073C24.3243 29.5073 25.3503 29.9323 26.1068 30.6889C26.8633 31.4454 27.2883 32.4714 27.2883 33.5413C27.2883 34.6111 26.8633 35.6372 26.1068 36.3937C25.3503 37.1502 24.3243 37.5752 23.2544 37.5752ZM35.5934 32.3548H34.6443C34.4555 32.3548 34.2744 32.4298 34.1409 32.5633C34.0074 32.6968 33.9324 32.8779 33.9324 33.0667C33.9324 33.2555 34.0074 33.4365 34.1409 33.57C34.2744 33.7035 34.4555 33.7785 34.6443 33.7785H35.5934C35.9915 33.7785 36.3888 33.7412 36.7799 33.667C36.7552 34.459 36.4978 35.2262 36.0398 35.8728C35.5818 36.5195 34.9435 37.0169 34.2045 37.303C33.4656 37.5891 32.6588 37.6513 31.8847 37.4817C31.1107 37.3122 30.4037 36.9184 29.8521 36.3495C29.3005 35.7807 28.9286 35.062 28.7828 34.2831C28.6371 33.5042 28.724 32.6997 29.0327 31.9699C29.3413 31.2401 29.8581 30.6174 30.5185 30.1794C31.1789 29.7415 31.9536 29.5077 32.746 29.5073C32.9348 29.5073 33.1158 29.4323 33.2493 29.2988C33.3828 29.1653 33.4578 28.9843 33.4578 28.7955C33.4578 28.6067 33.3828 28.4256 33.2493 28.2921C33.1158 28.1586 32.9348 28.0836 32.746 28.0836C31.9862 28.0833 31.2348 28.242 30.5401 28.5496C29.8453 28.8571 29.2227 29.3066 28.7121 29.8692V21.2022C28.7121 20.1324 29.1371 19.1063 29.8936 18.3498C30.6501 17.5933 31.6761 17.1683 32.746 17.1683C33.8158 17.1683 34.8419 17.5933 35.5984 18.3498C36.3549 19.1063 36.7799 20.1324 36.7799 21.2022V22.0007C36.7798 22.148 36.8254 22.2917 36.9104 22.4119C36.9954 22.5322 37.1156 22.6231 37.2545 22.6722C38.3637 23.0634 39.2989 23.8342 39.8945 24.8485C40.4901 25.8628 40.7077 27.055 40.5088 28.2143C40.3099 29.3735 39.7074 30.4251 38.8078 31.1829C37.9083 31.9406 36.7696 32.3558 35.5934 32.3548ZM37.2545 25.948C37.2545 26.1368 37.1795 26.3179 37.046 26.4514C36.9125 26.5849 36.7314 26.6599 36.5426 26.6599H36.068C34.9982 26.6599 33.9721 26.2349 33.2156 25.4784C32.4591 24.7219 32.0341 23.6958 32.0341 22.626V22.1514C32.0341 21.9626 32.1091 21.7815 32.2426 21.648C32.3761 21.5145 32.5572 21.4395 32.746 21.4395C32.9348 21.4395 33.1158 21.5145 33.2493 21.648C33.3828 21.7815 33.4578 21.9626 33.4578 22.1514V22.626C33.4578 23.3182 33.7328 23.9821 34.2224 24.4716C34.7119 24.9611 35.3758 25.2361 36.068 25.2361H36.5426C36.7314 25.2361 36.9125 25.3111 37.046 25.4446C37.1795 25.5781 37.2545 25.7592 37.2545 25.948ZM19.9324 26.6599H19.4578C19.269 26.6599 19.0879 26.5849 18.9544 26.4514C18.8209 26.3179 18.7459 26.1368 18.7459 25.948C18.7459 25.7592 18.8209 25.5781 18.9544 25.4446C19.0879 25.3111 19.269 25.2361 19.4578 25.2361H19.9324C20.6246 25.2361 21.2886 24.9611 21.7781 24.4716C22.2676 23.9821 22.5426 23.3182 22.5426 22.626V22.1514C22.5426 21.9626 22.6176 21.7815 22.7511 21.648C22.8846 21.5145 23.0656 21.4395 23.2544 21.4395C23.4432 21.4395 23.6243 21.5145 23.7578 21.648C23.8913 21.7815 23.9663 21.9626 23.9663 22.1514V22.626C23.9663 23.6958 23.5413 24.7219 22.7848 25.4784C22.0283 26.2349 21.0022 26.6599 19.9324 26.6599Z" fill="#8E8D8D"/>

            #     </svg>

                    
                
                
            #     </div>
            #     <div class="Frame15" style="left: 29px; top: 115px; position: absolute; justify-content: flex-start; align-items: flex-end; gap: 24px; display: inline-flex">
            #         <div id="counter" style="color: #111416; font-size: 150px; font-family:  'Source Sans Pro',sans-serif; font-weight: 700; line-height: 47.93px; word-wrap: break-word"></div>
            #         <div class="Frame9" style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 0px; display: inline-flex">
            #         <div style="color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
            #         <div style="color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">ΛΥΨΥ</div>
            #         </div>
            #     </div>
            #     </div>
            #     <script type="text/javascript">
            #         {js_code}
            #         animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #         </script>
            #     """,height = 250
            # )
            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            # )
            #st.write(kpdf['D5'][kpdf['year']==str(year_filter)])
            html(
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
                                <path d="M42.0002 27.3717C41.9987 26.1341 41.6395 24.9233 40.9659 23.8849C40.2924 22.8466 39.3331 22.025 38.2036 21.519V21.2022C38.2024 19.998 37.8029 18.8279 37.0674 17.8743C36.3319 16.9208 35.3016 16.2372 34.1371 15.9303C32.9726 15.6233 31.7393 15.7101 30.6293 16.1772C29.5193 16.6443 28.5949 17.4654 28.0002 18.5126C27.4055 17.4654 26.4811 16.6443 25.3711 16.1772C24.2611 15.7101 23.0278 15.6233 21.8633 15.9303C20.6988 16.2372 19.6685 16.9208 18.933 17.8743C18.1975 18.8279 17.798 19.998 17.7968 21.2022V21.519C16.6664 22.0233 15.7063 22.8442 15.0325 23.8826C14.3588 24.9209 14.0002 26.1322 14.0002 27.37C14.0002 28.6077 14.3588 29.819 15.0325 30.8573C15.7063 31.8957 16.6664 32.7166 17.7968 33.2209V33.5413C17.798 34.7455 18.1975 35.9156 18.933 36.8692C19.6685 37.8227 20.6988 38.5062 21.8633 38.8132C23.0278 39.1202 24.2611 39.0334 25.3711 38.5663C26.4811 38.0992 27.4055 37.2781 28.0002 36.2309C28.5949 37.2781 29.5193 38.0992 30.6293 38.5663C31.7393 39.0334 32.9726 39.1202 34.1371 38.8132C35.3016 38.5062 36.3319 37.8227 37.0674 36.8692C37.8029 35.9156 38.2024 34.7455 38.2036 33.5413V33.2209C39.3331 32.7159 40.2925 31.895 40.9661 30.8572C41.6397 29.8194 41.9989 28.609 42.0002 27.3717ZM23.2544 37.5752C22.206 37.5757 21.1986 37.168 20.4456 36.4385C19.6926 35.709 19.2532 34.7149 19.2205 33.667C19.6116 33.7412 20.0089 33.7785 20.407 33.7785H21.3561C21.5449 33.7785 21.726 33.7035 21.8595 33.57C21.993 33.4365 22.068 33.2555 22.068 33.0667C22.068 32.8779 21.993 32.6968 21.8595 32.5633C21.726 32.4298 21.5449 32.3548 21.3561 32.3548H20.407C19.2308 32.3558 18.0921 31.9406 17.1926 31.1829C16.293 30.4251 15.6905 29.3735 15.4916 28.2143C15.2927 27.055 15.5103 25.8628 16.1059 24.8485C16.7015 23.8342 17.6367 23.0634 18.7459 22.6722C18.8848 22.6231 19.005 22.5322 19.09 22.4119C19.175 22.2917 19.2206 22.148 19.2205 22.0007V21.2022C19.2205 20.1324 19.6455 19.1063 20.402 18.3498C21.1585 17.5933 22.1846 17.1683 23.2544 17.1683C24.3243 17.1683 25.3503 17.5933 26.1068 18.3498C26.8633 19.1063 27.2883 20.1324 27.2883 21.2022V29.8692C26.7777 29.3066 26.1551 28.8571 25.4603 28.5496C24.7656 28.242 24.0142 28.0833 23.2544 28.0836C23.0656 28.0836 22.8846 28.1586 22.7511 28.2921C22.6176 28.4256 22.5426 28.6067 22.5426 28.7955C22.5426 28.9843 22.6176 29.1653 22.7511 29.2988C22.8846 29.4323 23.0656 29.5073 23.2544 29.5073C24.3243 29.5073 25.3503 29.9323 26.1068 30.6888C26.8633 31.4454 27.2883 32.4714 27.2883 33.5413C27.2883 34.6111 26.8633 35.6372 26.1068 36.3937C25.3503 37.1502 24.3243 37.5752 23.2544 37.5752ZM35.5934 32.3548H34.6443C34.4555 32.3548 34.2744 32.4298 34.1409 32.5633C34.0074 32.6968 33.9324 32.8779 33.9324 33.0667C33.9324 33.2555 34.0074 33.4365 34.1409 33.57C34.2744 33.7035 34.4555 33.7785 34.6443 33.7785H35.5934C35.9915 33.7785 36.3888 33.7412 36.7799 33.667C36.7552 34.459 36.4978 35.2262 36.0398 35.8728C35.5818 36.5195 34.9435 37.0169 34.2045 37.303C33.4656 37.5891 32.6588 37.6513 31.8847 37.4817C31.1107 37.3122 30.4037 36.9184 29.8521 36.3495C29.3005 35.7807 28.9286 35.062 28.7828 34.2831C28.6371 33.5042 28.724 32.6997 29.0327 31.9699C29.3413 31.2401 29.8581 30.6174 30.5185 30.1794C31.1789 29.7415 31.9536 29.5077 32.746 29.5073C32.9348 29.5073 33.1158 29.4323 33.2493 29.2988C33.3828 29.1653 33.4578 28.9843 33.4578 28.7955C33.4578 28.6067 33.3828 28.4256 33.2493 28.2921C33.1158 28.1586 32.9348 28.0836 32.746 28.0836C31.9862 28.0833 31.2348 28.242 30.5401 28.5496C29.8453 28.8571 29.2227 29.3066 28.7121 29.8692V21.2022C28.7121 20.1324 29.1371 19.1063 29.8936 18.3498C30.6501 17.5933 31.6761 17.1683 32.746 17.1683C33.8158 17.1683 34.8419 17.5933 35.5984 18.3498C36.3549 19.1063 36.7799 20.1324 36.7799 21.2022V22.0007C36.7798 22.148 36.8254 22.2917 36.9104 22.4119C36.9954 22.5322 37.1156 22.6231 37.2545 22.6722C38.3637 23.0634 39.2989 23.8342 39.8945 24.8485C40.4901 25.8628 40.7077 27.055 40.5088 28.2143C40.3099 29.3735 39.7074 30.4251 38.8078 31.1829C37.9083 31.9406 36.7696 32.3558 35.5934 32.3548ZM37.2545 25.948C37.2545 26.1368 37.1795 26.3179 37.046 26.4514C36.9125 26.5849 36.7314 26.6599 36.5426 26.6599H36.068C34.9982 26.6599 33.9721 26.2349 33.2156 25.4784C32.4591 24.7219 32.0341 23.6958 32.0341 22.626V22.1514C32.0341 21.9626 32.1091 21.7815 32.2426 21.648C32.3761 21.5145 32.5572 21.4395 32.746 21.4395C32.9348 21.4395 33.1158 21.5145 33.2493 21.648C33.3828 21.7815 33.4578 21.9626 33.4578 22.1514V22.626C33.4578 23.3182 33.7328 23.9821 34.2224 24.4716C34.7119 24.9611 35.3758 25.2361 36.068 25.2361H36.5426C36.7314 25.2361 36.9125 25.3111 37.046 25.4446C37.1795 25.5781 37.2545 25.7592 37.2545 25.948ZM19.9324 26.6599H19.4578C19.269 26.6599 19.0879 26.5849 18.9544 26.4514C18.8209 26.3179 18.7459 26.1368 18.7459 25.948C18.7459 25.7592 18.8209 25.5781 18.9544 25.4446C19.0879 25.3111 19.269 25.2361 19.4578 25.2361H19.9324C20.6246 25.2361 21.2886 24.9611 21.7781 24.4716C22.2676 23.9821 22.5426 23.3182 22.5426 22.626V22.1514C22.5426 21.9626 22.6176 21.7815 22.7511 21.648C22.8846 21.5145 23.0656 21.4395 23.2544 21.4395C23.4432 21.4395 23.6243 21.5145 23.7578 21.648C23.8913 21.7815 23.9663 21.9626 23.9663 22.1514V22.626C23.9663 23.6958 23.5413 24.7219 22.7848 25.4784C22.0283 26.2349 21.0022 26.6599 19.9324 26.6599Z" fill="url(#paint0_linear_21_744)"/>
                                <defs>
                                <linearGradient id="paint0_linear_21_744" x1="17.4496" y1="17.2499" x2="43.5468" y2="51.7043" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                </defs>
                            </svg>
                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
                            <div>
                                <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">ΛΥΨΥ</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
        )

          
        with col3:
            #st.write('D7-Εργαζόμενοι ΕΚΟ')
            text=kpdf['D7'][kpdf['year']==str(year_filter)].iloc[0]
            # st.write('D7-Εργαζόμενοι ΕΚΟ: '+text)
            # st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΕΚΟ</h3>", unsafe_allow_html=True)
            # html(
            #                 f"""
            #                     <div class="Component3" style="width: 290px; height: 183px; padding-bottom: 24px; padding-left: 24px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); border-radius: 15px; justify-content: space-between; align-items: flex-end; gap: 24px; display: inline-flex">
            #                 <div class="Rectangle19" style="width: 329px; height: 210px; left: 0px; top: 0px; position: absolute; border-radius: 15px"></div>
            #     <div style="width: 56px; height: 56px; left: 256px; top: 19px; position: absolute">
            #                     <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">

            #                 <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
            #                 <path id="Vector" d="M42.0002 27.3717C41.9987 26.1341 41.6395 24.9233 40.9659 23.8849C40.2924 22.8466 39.3331 22.025 38.2036 21.519V21.2022C38.2024 19.998 37.8029 18.8279 37.0674 17.8743C36.3319 16.9208 35.3016 16.2372 34.1371 15.9303C32.9726 15.6233 31.7393 15.7101 30.6293 16.1772C29.5193 16.6443 28.5949 17.4654 28.0002 18.5126C27.4055 17.4654 26.4811 16.6443 25.3711 16.1772C24.2611 15.7101 23.0278 15.6233 21.8633 15.9303C20.6988 16.2372 19.6685 16.9208 18.933 17.8743C18.1975 18.8279 17.798 19.998 17.7968 21.2022V21.519C16.6664 22.0233 15.7063 22.8442 15.0325 23.8826C14.3588 24.9209 14.0002 26.1322 14.0002 27.37C14.0002 28.6077 14.3588 29.819 15.0325 30.8573C15.7063 31.8957 16.6664 32.7166 17.7968 33.2209V33.5413C17.798 34.7455 18.1975 35.9156 18.933 36.8692C19.6685 37.8227 20.6988 38.5062 21.8633 38.8132C23.0278 39.1202 24.2611 39.0334 25.3711 38.5663C26.4811 38.0992 27.4055 37.2781 28.0002 36.2309C28.5949 37.2781 29.5193 38.0992 30.6293 38.5663C31.7393 39.0334 32.9726 39.1202 34.1371 38.8132C35.3016 38.5062 36.3319 37.8227 37.0674 36.8692C37.8029 35.9156 38.2024 34.7455 38.2036 33.5413V33.2209C39.3331 32.7159 40.2925 31.895 40.9661 30.8572C41.6397 29.8194 41.9989 28.609 42.0002 27.3717ZM23.2544 37.5752C22.206 37.5757 21.1986 37.168 20.4456 36.4385C19.6926 35.709 19.2532 34.7149 19.2205 33.667C19.6116 33.7412 20.0089 33.7785 20.407 33.7785H21.3561C21.5449 33.7785 21.726 33.7035 21.8595 33.57C21.993 33.4365 22.068 33.2555 22.068 33.0667C22.068 32.8779 21.993 32.6968 21.8595 32.5633C21.726 32.4298 21.5449 32.3548 21.3561 32.3548H20.407C19.2308 32.3558 18.0921 31.9406 17.1926 31.1829C16.293 30.4251 15.6905 29.3735 15.4916 28.2143C15.2927 27.055 15.5103 25.8628 16.1059 24.8485C16.7015 23.8342 17.6367 23.0634 18.7459 22.6722C18.8848 22.6231 19.005 22.5322 19.09 22.4119C19.175 22.2917 19.2206 22.148 19.2205 22.0007V21.2022C19.2205 20.1324 19.6455 19.1063 20.402 18.3498C21.1585 17.5933 22.1846 17.1683 23.2544 17.1683C24.3243 17.1683 25.3503 17.5933 26.1068 18.3498C26.8633 19.1063 27.2883 20.1324 27.2883 21.2022V29.8692C26.7777 29.3066 26.1551 28.8571 25.4603 28.5496C24.7656 28.242 24.0142 28.0833 23.2544 28.0836C23.0656 28.0836 22.8846 28.1586 22.7511 28.2921C22.6176 28.4256 22.5426 28.6067 22.5426 28.7955C22.5426 28.9843 22.6176 29.1653 22.7511 29.2988C22.8846 29.4323 23.0656 29.5073 23.2544 29.5073C24.3243 29.5073 25.3503 29.9323 26.1068 30.6889C26.8633 31.4454 27.2883 32.4714 27.2883 33.5413C27.2883 34.6111 26.8633 35.6372 26.1068 36.3937C25.3503 37.1502 24.3243 37.5752 23.2544 37.5752ZM35.5934 32.3548H34.6443C34.4555 32.3548 34.2744 32.4298 34.1409 32.5633C34.0074 32.6968 33.9324 32.8779 33.9324 33.0667C33.9324 33.2555 34.0074 33.4365 34.1409 33.57C34.2744 33.7035 34.4555 33.7785 34.6443 33.7785H35.5934C35.9915 33.7785 36.3888 33.7412 36.7799 33.667C36.7552 34.459 36.4978 35.2262 36.0398 35.8728C35.5818 36.5195 34.9435 37.0169 34.2045 37.303C33.4656 37.5891 32.6588 37.6513 31.8847 37.4817C31.1107 37.3122 30.4037 36.9184 29.8521 36.3495C29.3005 35.7807 28.9286 35.062 28.7828 34.2831C28.6371 33.5042 28.724 32.6997 29.0327 31.9699C29.3413 31.2401 29.8581 30.6174 30.5185 30.1794C31.1789 29.7415 31.9536 29.5077 32.746 29.5073C32.9348 29.5073 33.1158 29.4323 33.2493 29.2988C33.3828 29.1653 33.4578 28.9843 33.4578 28.7955C33.4578 28.6067 33.3828 28.4256 33.2493 28.2921C33.1158 28.1586 32.9348 28.0836 32.746 28.0836C31.9862 28.0833 31.2348 28.242 30.5401 28.5496C29.8453 28.8571 29.2227 29.3066 28.7121 29.8692V21.2022C28.7121 20.1324 29.1371 19.1063 29.8936 18.3498C30.6501 17.5933 31.6761 17.1683 32.746 17.1683C33.8158 17.1683 34.8419 17.5933 35.5984 18.3498C36.3549 19.1063 36.7799 20.1324 36.7799 21.2022V22.0007C36.7798 22.148 36.8254 22.2917 36.9104 22.4119C36.9954 22.5322 37.1156 22.6231 37.2545 22.6722C38.3637 23.0634 39.2989 23.8342 39.8945 24.8485C40.4901 25.8628 40.7077 27.055 40.5088 28.2143C40.3099 29.3735 39.7074 30.4251 38.8078 31.1829C37.9083 31.9406 36.7696 32.3558 35.5934 32.3548ZM37.2545 25.948C37.2545 26.1368 37.1795 26.3179 37.046 26.4514C36.9125 26.5849 36.7314 26.6599 36.5426 26.6599H36.068C34.9982 26.6599 33.9721 26.2349 33.2156 25.4784C32.4591 24.7219 32.0341 23.6958 32.0341 22.626V22.1514C32.0341 21.9626 32.1091 21.7815 32.2426 21.648C32.3761 21.5145 32.5572 21.4395 32.746 21.4395C32.9348 21.4395 33.1158 21.5145 33.2493 21.648C33.3828 21.7815 33.4578 21.9626 33.4578 22.1514V22.626C33.4578 23.3182 33.7328 23.9821 34.2224 24.4716C34.7119 24.9611 35.3758 25.2361 36.068 25.2361H36.5426C36.7314 25.2361 36.9125 25.3111 37.046 25.4446C37.1795 25.5781 37.2545 25.7592 37.2545 25.948ZM19.9324 26.6599H19.4578C19.269 26.6599 19.0879 26.5849 18.9544 26.4514C18.8209 26.3179 18.7459 26.1368 18.7459 25.948C18.7459 25.7592 18.8209 25.5781 18.9544 25.4446C19.0879 25.3111 19.269 25.2361 19.4578 25.2361H19.9324C20.6246 25.2361 21.2886 24.9611 21.7781 24.4716C22.2676 23.9821 22.5426 23.3182 22.5426 22.626V22.1514C22.5426 21.9626 22.6176 21.7815 22.7511 21.648C22.8846 21.5145 23.0656 21.4395 23.2544 21.4395C23.4432 21.4395 23.6243 21.5145 23.7578 21.648C23.8913 21.7815 23.9663 21.9626 23.9663 22.1514V22.626C23.9663 23.6958 23.5413 24.7219 22.7848 25.4784C22.0283 26.2349 21.0022 26.6599 19.9324 26.6599Z" fill="#8E8D8D"/>

            #                 </svg>

                                
                            
                            
            #                 </div>
            #                 <div class="Frame15" style="left: 29px; top: 115px; position: absolute; justify-content: flex-start; align-items: flex-end; gap: 24px; display: inline-flex">
            #                     <div id="counter" style="color: #111416; font-size: 150px; font-family:  'Source Sans Pro',sans-serif; font-weight: 700; line-height: 47.93px; word-wrap: break-word"></div>
            #                     <div class="Frame9" style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 0px; display: inline-flex">
            #                     <div style="color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
            #                     <div style="color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">ΕΚΟ</div>
            #                     </div>
            #                 </div>
            #                 </div>
            #                 <script type="text/javascript">
            #                     {js_code}
            #                     animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #                     </script>
            #                 """,height = 250
            #             )
            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            # )
            #st.write(kpdf['D7'][kpdf['year']==str(year_filter)])
            html(
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g id="&#206;&#149;&#206;&#154;&#206;&#159;">
                                    <circle id="Ellipse 24" cx="28" cy="28" r="28" fill="white"/>
                                    <g id="Group">
                                        <path id="Vector" d="M40.9972 20.0092C40.0026 19.6677 38.5414 20.3829 37.7955 22.1856L37.484 22.963C37.0181 22.0305 36.2093 21.2839 35.1832 20.9423C35.4012 20.5072 35.5255 19.9785 35.5255 19.4497V19.0768C35.5255 17.2426 34.0329 15.75 32.1987 15.75C30.3646 15.75 28.872 17.2426 28.872 19.0768V19.4497C28.872 19.5119 28.872 19.6055 28.872 19.6677C28.6233 19.6055 28.3125 19.5433 28.0017 19.5433C27.6909 19.5433 27.3794 19.574 27.1 19.6677C27.1 19.6055 27.1 19.5119 27.1 19.4497V19.0768C27.1 17.2426 25.6074 15.75 23.7732 15.75C21.9391 15.75 20.4772 17.2426 20.4772 19.0768V19.4497C20.4772 19.9785 20.6023 20.4758 20.8195 20.9423C19.7934 21.2532 18.9539 21.9991 18.5187 22.963L18.2079 22.1856C17.462 20.3829 16.0008 19.6677 15.0055 20.0092C14.2903 20.2578 13.7001 21.0667 14.1659 22.6207L16.3116 30.0831V30.1138C17.4927 33.3162 18.7052 34.9639 19.7934 35.9277H18.4566C18.2079 35.9277 17.99 36.1457 17.99 36.3943V40.5913C17.99 40.84 18.2079 41.0579 18.4566 41.0579H37.5776C37.8262 41.0579 38.0442 40.84 38.0442 40.5913V36.3943C38.0442 36.1457 37.8262 35.9277 37.5776 35.9277H36.2407C37.3289 34.9953 38.5414 33.3477 39.7225 30.1138V30.0831L41.8682 22.6207C42.2719 21.0667 41.6817 20.2578 40.9972 20.0092ZM36.9245 24.362L35.7434 27.3158C35.4633 27.1293 35.1211 26.9735 34.7481 26.8806C34.2815 26.7563 33.7842 26.7563 33.3184 26.8185C32.8518 25.8231 32.0123 25.0772 30.9862 24.7664C31.2042 24.3313 31.3592 23.8025 31.3592 23.2738V22.9008C31.3592 22.8386 31.3592 22.7458 31.3592 22.6836C31.6393 22.7765 31.9501 22.8079 32.2609 22.8079C33.1941 22.8079 34.0329 22.4035 34.6552 21.7819C35.8363 22.0305 36.8002 23.0873 36.9245 24.362ZM28.0017 26.5698C28.9341 26.5698 29.7737 26.1654 30.3953 25.5438C31.2663 25.7303 32.0123 26.2897 32.4167 27.0978C32.3231 27.1293 32.2609 27.1914 32.168 27.2221L30.9555 27.9995C29.8051 28.7462 28.6233 29.4922 28.0017 30.9226C27.3794 29.4922 26.1983 28.7148 25.0479 27.9995L23.8354 27.2221C23.7418 27.16 23.6796 27.1293 23.5868 27.0978C23.9912 26.3212 24.7371 25.7303 25.6074 25.5438C26.229 26.1654 27.0686 26.5698 28.0017 26.5698ZM29.8051 19.4497V19.0768C29.8051 17.7706 30.8933 16.6824 32.1987 16.6824C33.5049 16.6824 34.5931 17.7706 34.5931 19.0768V19.4497C34.5931 20.7559 33.5049 21.8441 32.1987 21.8441C31.7943 21.8441 31.3906 21.7197 31.0484 21.5333C30.7997 20.9731 30.4268 20.5072 29.9295 20.165C29.8673 19.947 29.8051 19.6984 29.8051 19.4497ZM30.3953 22.8701V23.2431C30.3953 24.5485 29.3071 25.6367 28.0017 25.6367C26.6956 25.6367 25.6074 24.5485 25.6074 23.2431V22.8701C25.6074 21.564 26.6956 20.4758 28.0017 20.4758C29.3071 20.4758 30.3953 21.564 30.3953 22.8701ZM21.4104 19.0768C21.4104 17.7706 22.4986 16.6824 23.804 16.6824C25.1101 16.6824 26.1983 17.7706 26.1983 19.0768V19.4497C26.1983 19.6984 26.1668 19.9163 26.074 20.165C25.5767 20.5072 25.2037 20.9731 24.9543 21.5333C24.6128 21.7197 24.2084 21.8441 23.804 21.8441C22.4986 21.8441 21.4104 20.7866 21.4104 19.4497V19.0768ZM21.4104 21.7504C22.0013 22.3721 22.8715 22.7765 23.804 22.7765C24.1155 22.7765 24.3949 22.7458 24.7057 22.6522C24.7057 22.7143 24.7057 22.8079 24.7057 22.8701V23.2431C24.7057 23.7711 24.83 24.2998 25.0786 24.7349C24.0533 25.0772 23.2138 25.8231 22.7472 26.787C22.2806 26.6942 21.7833 26.7249 21.3167 26.8492C20.9438 26.9428 20.6023 27.0978 20.3222 27.2851L19.0782 24.362C19.2025 23.0873 20.1664 22.0305 21.4104 21.7504ZM17.2133 29.803L15.0677 22.3414C14.8505 21.564 14.9433 21.0045 15.3163 20.8802C15.8136 20.6937 16.8089 21.191 17.3377 22.5278L19.6069 28.1239C19.2961 28.9327 19.6691 29.8344 20.633 30.456L23.6489 32.3838C23.7418 32.446 23.804 32.446 23.8976 32.446C24.0533 32.446 24.2084 32.3838 24.302 32.228C24.457 32.0108 24.3949 31.7307 24.1777 31.5749L21.1617 29.6786C20.9438 29.5229 20.1978 28.9949 20.5401 28.3725C20.6951 28.0932 21.0681 27.8752 21.5032 27.7509C22.1563 27.5959 22.8094 27.6887 23.3381 28.031L24.5506 28.8084C26.1361 29.8344 27.5351 30.7047 27.5351 33.472V35.9277H21.4104C20.2285 35.2747 18.7052 33.9378 17.2133 29.803ZM18.8917 36.8609H27.5044V40.1255H18.8917V36.8609ZM37.111 40.1255H28.4676V36.8609H37.0803V40.1255H37.111ZM40.935 22.3721L38.7901 29.8344C37.2975 33.9378 35.7741 35.2747 34.5931 35.9277H28.4676V33.472C28.4676 30.7047 29.8359 29.8344 31.4528 28.8084L32.6653 28.031C33.1941 27.6887 33.8464 27.5959 34.4995 27.7509C34.966 27.8752 35.339 28.0932 35.4633 28.3725C35.8056 28.9949 35.0589 29.5229 34.8417 29.6786L31.8258 31.6064C31.6078 31.7307 31.5457 32.0415 31.7014 32.2595C31.7943 32.3838 31.9501 32.4767 32.1059 32.4767C32.1987 32.4767 32.2924 32.446 32.3545 32.4145L35.3697 30.4867C36.3336 29.8651 36.7073 28.9634 36.3958 28.1553L38.6658 22.5585C39.2252 21.2217 40.1891 20.7559 40.6864 20.9109C41.0594 21.0045 41.153 21.5954 40.935 22.3721Z" fill="url(#paint0_linear_89_478)"/>
                                    </g>
                                </g>
                                <defs>
                                    <linearGradient id="paint0_linear_89_478" x1="17.4493" y1="17.3831" x2="46.4282" y2="52.5212" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#548CEE"/>
                                    <stop offset="1" stop-color="#15E7FF"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
                            <div>
                                <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">ΕΚΟ</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
        )
            

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            # Filter the dataframe based on the selected year
            st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Εργαζόμενοι Γεν. Πληθ.</p><p  style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(% επί του Συνόλου)</p>", unsafe_allow_html=True)
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]
            # Select the value from the filtered dataframe
            d9_value = filtered_kpdf["D9"].iloc[0]
            fig=gaugeChart(d9_value,'royalblue')
            st.plotly_chart(fig,use_container_width=True)
            

        with col2:
            # Filter the dataframe based on the selected year
            st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Εργαζόμενοι ΛΥΨΥ</p><p style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(% επί του Συνόλου)</p>", unsafe_allow_html=True)
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]
            # Select the value from the filtered dataframe
            d10_value = filtered_kpdf["D10"].iloc[0]
            fig=gaugeChart(d10_value,'skyblue')

            st.plotly_chart(fig,use_container_width=True)
        with col3:
            # Filter the dataframe based on the selected year
            st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Εργαζόμενοι ΕΚΟ</p><p style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(% επί του Συνόλου)</p>", unsafe_allow_html=True)
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
           # st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Ωρες απασχολησης εργαζομένων ΛΥΨΥ</p><p style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(Μεσος Όρος)</p>", unsafe_allow_html=True)

            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            # )
            # st.metric(label="Συνολο Μελών "+str(kpdf['D1'][kpdf['year']==str(year_filter)][0]), value=int(kpdf['D1'][kpdf['year']==str(year_filter)][0]), delta=-0.5,delta_color="inverse")
            html(
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:435px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g id="&#206;&#149;&#206;&#154;&#206;&#159;">
                                    <circle id="Ellipse 24" cx="28" cy="28" r="28" fill="white"/>
                                    <g id="Group">
                                        <path id="Vector" d="M40.9972 20.0092C40.0026 19.6677 38.5414 20.3829 37.7955 22.1856L37.484 22.963C37.0181 22.0305 36.2093 21.2839 35.1832 20.9423C35.4012 20.5072 35.5255 19.9785 35.5255 19.4497V19.0768C35.5255 17.2426 34.0329 15.75 32.1987 15.75C30.3646 15.75 28.872 17.2426 28.872 19.0768V19.4497C28.872 19.5119 28.872 19.6055 28.872 19.6677C28.6233 19.6055 28.3125 19.5433 28.0017 19.5433C27.6909 19.5433 27.3794 19.574 27.1 19.6677C27.1 19.6055 27.1 19.5119 27.1 19.4497V19.0768C27.1 17.2426 25.6074 15.75 23.7732 15.75C21.9391 15.75 20.4772 17.2426 20.4772 19.0768V19.4497C20.4772 19.9785 20.6023 20.4758 20.8195 20.9423C19.7934 21.2532 18.9539 21.9991 18.5187 22.963L18.2079 22.1856C17.462 20.3829 16.0008 19.6677 15.0055 20.0092C14.2903 20.2578 13.7001 21.0667 14.1659 22.6207L16.3116 30.0831V30.1138C17.4927 33.3162 18.7052 34.9639 19.7934 35.9277H18.4566C18.2079 35.9277 17.99 36.1457 17.99 36.3943V40.5913C17.99 40.84 18.2079 41.0579 18.4566 41.0579H37.5776C37.8262 41.0579 38.0442 40.84 38.0442 40.5913V36.3943C38.0442 36.1457 37.8262 35.9277 37.5776 35.9277H36.2407C37.3289 34.9953 38.5414 33.3477 39.7225 30.1138V30.0831L41.8682 22.6207C42.2719 21.0667 41.6817 20.2578 40.9972 20.0092ZM36.9245 24.362L35.7434 27.3158C35.4633 27.1293 35.1211 26.9735 34.7481 26.8806C34.2815 26.7563 33.7842 26.7563 33.3184 26.8185C32.8518 25.8231 32.0123 25.0772 30.9862 24.7664C31.2042 24.3313 31.3592 23.8025 31.3592 23.2738V22.9008C31.3592 22.8386 31.3592 22.7458 31.3592 22.6836C31.6393 22.7765 31.9501 22.8079 32.2609 22.8079C33.1941 22.8079 34.0329 22.4035 34.6552 21.7819C35.8363 22.0305 36.8002 23.0873 36.9245 24.362ZM28.0017 26.5698C28.9341 26.5698 29.7737 26.1654 30.3953 25.5438C31.2663 25.7303 32.0123 26.2897 32.4167 27.0978C32.3231 27.1293 32.2609 27.1914 32.168 27.2221L30.9555 27.9995C29.8051 28.7462 28.6233 29.4922 28.0017 30.9226C27.3794 29.4922 26.1983 28.7148 25.0479 27.9995L23.8354 27.2221C23.7418 27.16 23.6796 27.1293 23.5868 27.0978C23.9912 26.3212 24.7371 25.7303 25.6074 25.5438C26.229 26.1654 27.0686 26.5698 28.0017 26.5698ZM29.8051 19.4497V19.0768C29.8051 17.7706 30.8933 16.6824 32.1987 16.6824C33.5049 16.6824 34.5931 17.7706 34.5931 19.0768V19.4497C34.5931 20.7559 33.5049 21.8441 32.1987 21.8441C31.7943 21.8441 31.3906 21.7197 31.0484 21.5333C30.7997 20.9731 30.4268 20.5072 29.9295 20.165C29.8673 19.947 29.8051 19.6984 29.8051 19.4497ZM30.3953 22.8701V23.2431C30.3953 24.5485 29.3071 25.6367 28.0017 25.6367C26.6956 25.6367 25.6074 24.5485 25.6074 23.2431V22.8701C25.6074 21.564 26.6956 20.4758 28.0017 20.4758C29.3071 20.4758 30.3953 21.564 30.3953 22.8701ZM21.4104 19.0768C21.4104 17.7706 22.4986 16.6824 23.804 16.6824C25.1101 16.6824 26.1983 17.7706 26.1983 19.0768V19.4497C26.1983 19.6984 26.1668 19.9163 26.074 20.165C25.5767 20.5072 25.2037 20.9731 24.9543 21.5333C24.6128 21.7197 24.2084 21.8441 23.804 21.8441C22.4986 21.8441 21.4104 20.7866 21.4104 19.4497V19.0768ZM21.4104 21.7504C22.0013 22.3721 22.8715 22.7765 23.804 22.7765C24.1155 22.7765 24.3949 22.7458 24.7057 22.6522C24.7057 22.7143 24.7057 22.8079 24.7057 22.8701V23.2431C24.7057 23.7711 24.83 24.2998 25.0786 24.7349C24.0533 25.0772 23.2138 25.8231 22.7472 26.787C22.2806 26.6942 21.7833 26.7249 21.3167 26.8492C20.9438 26.9428 20.6023 27.0978 20.3222 27.2851L19.0782 24.362C19.2025 23.0873 20.1664 22.0305 21.4104 21.7504ZM17.2133 29.803L15.0677 22.3414C14.8505 21.564 14.9433 21.0045 15.3163 20.8802C15.8136 20.6937 16.8089 21.191 17.3377 22.5278L19.6069 28.1239C19.2961 28.9327 19.6691 29.8344 20.633 30.456L23.6489 32.3838C23.7418 32.446 23.804 32.446 23.8976 32.446C24.0533 32.446 24.2084 32.3838 24.302 32.228C24.457 32.0108 24.3949 31.7307 24.1777 31.5749L21.1617 29.6786C20.9438 29.5229 20.1978 28.9949 20.5401 28.3725C20.6951 28.0932 21.0681 27.8752 21.5032 27.7509C22.1563 27.5959 22.8094 27.6887 23.3381 28.031L24.5506 28.8084C26.1361 29.8344 27.5351 30.7047 27.5351 33.472V35.9277H21.4104C20.2285 35.2747 18.7052 33.9378 17.2133 29.803ZM18.8917 36.8609H27.5044V40.1255H18.8917V36.8609ZM37.111 40.1255H28.4676V36.8609H37.0803V40.1255H37.111ZM40.935 22.3721L38.7901 29.8344C37.2975 33.9378 35.7741 35.2747 34.5931 35.9277H28.4676V33.472C28.4676 30.7047 29.8359 29.8344 31.4528 28.8084L32.6653 28.031C33.1941 27.6887 33.8464 27.5959 34.4995 27.7509C34.966 27.8752 35.339 28.0932 35.4633 28.3725C35.8056 28.9949 35.0589 29.5229 34.8417 29.6786L31.8258 31.6064C31.6078 31.7307 31.5457 32.0415 31.7014 32.2595C31.7943 32.3838 31.9501 32.4767 32.1059 32.4767C32.1987 32.4767 32.2924 32.446 32.3545 32.4145L35.3697 30.4867C36.3336 29.8651 36.7073 28.9634 36.3958 28.1553L38.6658 22.5585C39.2252 21.2217 40.1891 20.7559 40.6864 20.9109C41.0594 21.0045 41.153 21.5954 40.935 22.3721Z" fill="url(#paint0_linear_89_478)"/>
                                    </g>
                                </g>
                                <defs>
                                    <linearGradient id="paint0_linear_89_478" x1="17.4493" y1="17.3831" x2="46.4282" y2="52.5212" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#548CEE"/>
                                    <stop offset="1" stop-color="#15E7FF"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
                            <div>
                                <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 30px; word-wrap: break-word">Μεσος Όρος</div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 30px; word-wrap: break-word">Ωρες απασχολησης εργαζομένων ΛΥΨΥ</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
        )
        with col2:
            #st.write('Δ15-Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος)')
            #st.write(kpdf['D15'][kpdf['year']==str(year_filter)])
            text=kpdf['D15'][kpdf['year']==str(year_filter)].iloc[0]
            text=str(text.round())
            # st.write('Δ15-Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος): '+text)
            #st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Ωρες απασχολησης εργαζομένων ΕΚΟ</p><p style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(Μεσος Όρος)</p>", unsafe_allow_html=True)

            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center; font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            # )
            html(
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:435px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g id="&#206;&#149;&#206;&#154;&#206;&#159;">
                                    <circle id="Ellipse 24" cx="28" cy="28" r="28" fill="white"/>
                                    <g id="Group">
                                        <path id="Vector" d="M40.9972 20.0092C40.0026 19.6677 38.5414 20.3829 37.7955 22.1856L37.484 22.963C37.0181 22.0305 36.2093 21.2839 35.1832 20.9423C35.4012 20.5072 35.5255 19.9785 35.5255 19.4497V19.0768C35.5255 17.2426 34.0329 15.75 32.1987 15.75C30.3646 15.75 28.872 17.2426 28.872 19.0768V19.4497C28.872 19.5119 28.872 19.6055 28.872 19.6677C28.6233 19.6055 28.3125 19.5433 28.0017 19.5433C27.6909 19.5433 27.3794 19.574 27.1 19.6677C27.1 19.6055 27.1 19.5119 27.1 19.4497V19.0768C27.1 17.2426 25.6074 15.75 23.7732 15.75C21.9391 15.75 20.4772 17.2426 20.4772 19.0768V19.4497C20.4772 19.9785 20.6023 20.4758 20.8195 20.9423C19.7934 21.2532 18.9539 21.9991 18.5187 22.963L18.2079 22.1856C17.462 20.3829 16.0008 19.6677 15.0055 20.0092C14.2903 20.2578 13.7001 21.0667 14.1659 22.6207L16.3116 30.0831V30.1138C17.4927 33.3162 18.7052 34.9639 19.7934 35.9277H18.4566C18.2079 35.9277 17.99 36.1457 17.99 36.3943V40.5913C17.99 40.84 18.2079 41.0579 18.4566 41.0579H37.5776C37.8262 41.0579 38.0442 40.84 38.0442 40.5913V36.3943C38.0442 36.1457 37.8262 35.9277 37.5776 35.9277H36.2407C37.3289 34.9953 38.5414 33.3477 39.7225 30.1138V30.0831L41.8682 22.6207C42.2719 21.0667 41.6817 20.2578 40.9972 20.0092ZM36.9245 24.362L35.7434 27.3158C35.4633 27.1293 35.1211 26.9735 34.7481 26.8806C34.2815 26.7563 33.7842 26.7563 33.3184 26.8185C32.8518 25.8231 32.0123 25.0772 30.9862 24.7664C31.2042 24.3313 31.3592 23.8025 31.3592 23.2738V22.9008C31.3592 22.8386 31.3592 22.7458 31.3592 22.6836C31.6393 22.7765 31.9501 22.8079 32.2609 22.8079C33.1941 22.8079 34.0329 22.4035 34.6552 21.7819C35.8363 22.0305 36.8002 23.0873 36.9245 24.362ZM28.0017 26.5698C28.9341 26.5698 29.7737 26.1654 30.3953 25.5438C31.2663 25.7303 32.0123 26.2897 32.4167 27.0978C32.3231 27.1293 32.2609 27.1914 32.168 27.2221L30.9555 27.9995C29.8051 28.7462 28.6233 29.4922 28.0017 30.9226C27.3794 29.4922 26.1983 28.7148 25.0479 27.9995L23.8354 27.2221C23.7418 27.16 23.6796 27.1293 23.5868 27.0978C23.9912 26.3212 24.7371 25.7303 25.6074 25.5438C26.229 26.1654 27.0686 26.5698 28.0017 26.5698ZM29.8051 19.4497V19.0768C29.8051 17.7706 30.8933 16.6824 32.1987 16.6824C33.5049 16.6824 34.5931 17.7706 34.5931 19.0768V19.4497C34.5931 20.7559 33.5049 21.8441 32.1987 21.8441C31.7943 21.8441 31.3906 21.7197 31.0484 21.5333C30.7997 20.9731 30.4268 20.5072 29.9295 20.165C29.8673 19.947 29.8051 19.6984 29.8051 19.4497ZM30.3953 22.8701V23.2431C30.3953 24.5485 29.3071 25.6367 28.0017 25.6367C26.6956 25.6367 25.6074 24.5485 25.6074 23.2431V22.8701C25.6074 21.564 26.6956 20.4758 28.0017 20.4758C29.3071 20.4758 30.3953 21.564 30.3953 22.8701ZM21.4104 19.0768C21.4104 17.7706 22.4986 16.6824 23.804 16.6824C25.1101 16.6824 26.1983 17.7706 26.1983 19.0768V19.4497C26.1983 19.6984 26.1668 19.9163 26.074 20.165C25.5767 20.5072 25.2037 20.9731 24.9543 21.5333C24.6128 21.7197 24.2084 21.8441 23.804 21.8441C22.4986 21.8441 21.4104 20.7866 21.4104 19.4497V19.0768ZM21.4104 21.7504C22.0013 22.3721 22.8715 22.7765 23.804 22.7765C24.1155 22.7765 24.3949 22.7458 24.7057 22.6522C24.7057 22.7143 24.7057 22.8079 24.7057 22.8701V23.2431C24.7057 23.7711 24.83 24.2998 25.0786 24.7349C24.0533 25.0772 23.2138 25.8231 22.7472 26.787C22.2806 26.6942 21.7833 26.7249 21.3167 26.8492C20.9438 26.9428 20.6023 27.0978 20.3222 27.2851L19.0782 24.362C19.2025 23.0873 20.1664 22.0305 21.4104 21.7504ZM17.2133 29.803L15.0677 22.3414C14.8505 21.564 14.9433 21.0045 15.3163 20.8802C15.8136 20.6937 16.8089 21.191 17.3377 22.5278L19.6069 28.1239C19.2961 28.9327 19.6691 29.8344 20.633 30.456L23.6489 32.3838C23.7418 32.446 23.804 32.446 23.8976 32.446C24.0533 32.446 24.2084 32.3838 24.302 32.228C24.457 32.0108 24.3949 31.7307 24.1777 31.5749L21.1617 29.6786C20.9438 29.5229 20.1978 28.9949 20.5401 28.3725C20.6951 28.0932 21.0681 27.8752 21.5032 27.7509C22.1563 27.5959 22.8094 27.6887 23.3381 28.031L24.5506 28.8084C26.1361 29.8344 27.5351 30.7047 27.5351 33.472V35.9277H21.4104C20.2285 35.2747 18.7052 33.9378 17.2133 29.803ZM18.8917 36.8609H27.5044V40.1255H18.8917V36.8609ZM37.111 40.1255H28.4676V36.8609H37.0803V40.1255H37.111ZM40.935 22.3721L38.7901 29.8344C37.2975 33.9378 35.7741 35.2747 34.5931 35.9277H28.4676V33.472C28.4676 30.7047 29.8359 29.8344 31.4528 28.8084L32.6653 28.031C33.1941 27.6887 33.8464 27.5959 34.4995 27.7509C34.966 27.8752 35.339 28.0932 35.4633 28.3725C35.8056 28.9949 35.0589 29.5229 34.8417 29.6786L31.8258 31.6064C31.6078 31.7307 31.5457 32.0415 31.7014 32.2595C31.7943 32.3838 31.9501 32.4767 32.1059 32.4767C32.1987 32.4767 32.2924 32.446 32.3545 32.4145L35.3697 30.4867C36.3336 29.8651 36.7073 28.9634 36.3958 28.1553L38.6658 22.5585C39.2252 21.2217 40.1891 20.7559 40.6864 20.9109C41.0594 21.0045 41.153 21.5954 40.935 22.3721Z" fill="url(#paint0_linear_89_478)"/>
                                    </g>
                                </g>
                                <defs>
                                    <linearGradient id="paint0_linear_89_478" x1="17.4493" y1="17.3831" x2="46.4282" y2="52.5212" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#548CEE"/>
                                    <stop offset="1" stop-color="#15E7FF"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
                            <div>
                                <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 30px; word-wrap: break-word">Μεσος Όρος</div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 30px; word-wrap: break-word">Ωρες απασχολησης εργαζομένων ΕΚΟ</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
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
        # col1, col2 = st.columns(2)
        # with col1:
            #st.write('D18')
            #st.write(kpdf['D18'][kpdf['year']==str(year_filter)])
            text=str(kpdf['D18'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('D18 Ετησιες μοναδες εργασιας: '+text)
            #st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας</h3>", unsafe_allow_html=True)

            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter2("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            # )
            html(
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:435px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g id="&#206;&#149;&#206;&#154;&#206;&#159;">
                                    <circle id="Ellipse 24" cx="28" cy="28" r="28" fill="white"/>
                                    <g id="Group">
                                        <path id="Vector" d="M40.9972 20.0092C40.0026 19.6677 38.5414 20.3829 37.7955 22.1856L37.484 22.963C37.0181 22.0305 36.2093 21.2839 35.1832 20.9423C35.4012 20.5072 35.5255 19.9785 35.5255 19.4497V19.0768C35.5255 17.2426 34.0329 15.75 32.1987 15.75C30.3646 15.75 28.872 17.2426 28.872 19.0768V19.4497C28.872 19.5119 28.872 19.6055 28.872 19.6677C28.6233 19.6055 28.3125 19.5433 28.0017 19.5433C27.6909 19.5433 27.3794 19.574 27.1 19.6677C27.1 19.6055 27.1 19.5119 27.1 19.4497V19.0768C27.1 17.2426 25.6074 15.75 23.7732 15.75C21.9391 15.75 20.4772 17.2426 20.4772 19.0768V19.4497C20.4772 19.9785 20.6023 20.4758 20.8195 20.9423C19.7934 21.2532 18.9539 21.9991 18.5187 22.963L18.2079 22.1856C17.462 20.3829 16.0008 19.6677 15.0055 20.0092C14.2903 20.2578 13.7001 21.0667 14.1659 22.6207L16.3116 30.0831V30.1138C17.4927 33.3162 18.7052 34.9639 19.7934 35.9277H18.4566C18.2079 35.9277 17.99 36.1457 17.99 36.3943V40.5913C17.99 40.84 18.2079 41.0579 18.4566 41.0579H37.5776C37.8262 41.0579 38.0442 40.84 38.0442 40.5913V36.3943C38.0442 36.1457 37.8262 35.9277 37.5776 35.9277H36.2407C37.3289 34.9953 38.5414 33.3477 39.7225 30.1138V30.0831L41.8682 22.6207C42.2719 21.0667 41.6817 20.2578 40.9972 20.0092ZM36.9245 24.362L35.7434 27.3158C35.4633 27.1293 35.1211 26.9735 34.7481 26.8806C34.2815 26.7563 33.7842 26.7563 33.3184 26.8185C32.8518 25.8231 32.0123 25.0772 30.9862 24.7664C31.2042 24.3313 31.3592 23.8025 31.3592 23.2738V22.9008C31.3592 22.8386 31.3592 22.7458 31.3592 22.6836C31.6393 22.7765 31.9501 22.8079 32.2609 22.8079C33.1941 22.8079 34.0329 22.4035 34.6552 21.7819C35.8363 22.0305 36.8002 23.0873 36.9245 24.362ZM28.0017 26.5698C28.9341 26.5698 29.7737 26.1654 30.3953 25.5438C31.2663 25.7303 32.0123 26.2897 32.4167 27.0978C32.3231 27.1293 32.2609 27.1914 32.168 27.2221L30.9555 27.9995C29.8051 28.7462 28.6233 29.4922 28.0017 30.9226C27.3794 29.4922 26.1983 28.7148 25.0479 27.9995L23.8354 27.2221C23.7418 27.16 23.6796 27.1293 23.5868 27.0978C23.9912 26.3212 24.7371 25.7303 25.6074 25.5438C26.229 26.1654 27.0686 26.5698 28.0017 26.5698ZM29.8051 19.4497V19.0768C29.8051 17.7706 30.8933 16.6824 32.1987 16.6824C33.5049 16.6824 34.5931 17.7706 34.5931 19.0768V19.4497C34.5931 20.7559 33.5049 21.8441 32.1987 21.8441C31.7943 21.8441 31.3906 21.7197 31.0484 21.5333C30.7997 20.9731 30.4268 20.5072 29.9295 20.165C29.8673 19.947 29.8051 19.6984 29.8051 19.4497ZM30.3953 22.8701V23.2431C30.3953 24.5485 29.3071 25.6367 28.0017 25.6367C26.6956 25.6367 25.6074 24.5485 25.6074 23.2431V22.8701C25.6074 21.564 26.6956 20.4758 28.0017 20.4758C29.3071 20.4758 30.3953 21.564 30.3953 22.8701ZM21.4104 19.0768C21.4104 17.7706 22.4986 16.6824 23.804 16.6824C25.1101 16.6824 26.1983 17.7706 26.1983 19.0768V19.4497C26.1983 19.6984 26.1668 19.9163 26.074 20.165C25.5767 20.5072 25.2037 20.9731 24.9543 21.5333C24.6128 21.7197 24.2084 21.8441 23.804 21.8441C22.4986 21.8441 21.4104 20.7866 21.4104 19.4497V19.0768ZM21.4104 21.7504C22.0013 22.3721 22.8715 22.7765 23.804 22.7765C24.1155 22.7765 24.3949 22.7458 24.7057 22.6522C24.7057 22.7143 24.7057 22.8079 24.7057 22.8701V23.2431C24.7057 23.7711 24.83 24.2998 25.0786 24.7349C24.0533 25.0772 23.2138 25.8231 22.7472 26.787C22.2806 26.6942 21.7833 26.7249 21.3167 26.8492C20.9438 26.9428 20.6023 27.0978 20.3222 27.2851L19.0782 24.362C19.2025 23.0873 20.1664 22.0305 21.4104 21.7504ZM17.2133 29.803L15.0677 22.3414C14.8505 21.564 14.9433 21.0045 15.3163 20.8802C15.8136 20.6937 16.8089 21.191 17.3377 22.5278L19.6069 28.1239C19.2961 28.9327 19.6691 29.8344 20.633 30.456L23.6489 32.3838C23.7418 32.446 23.804 32.446 23.8976 32.446C24.0533 32.446 24.2084 32.3838 24.302 32.228C24.457 32.0108 24.3949 31.7307 24.1777 31.5749L21.1617 29.6786C20.9438 29.5229 20.1978 28.9949 20.5401 28.3725C20.6951 28.0932 21.0681 27.8752 21.5032 27.7509C22.1563 27.5959 22.8094 27.6887 23.3381 28.031L24.5506 28.8084C26.1361 29.8344 27.5351 30.7047 27.5351 33.472V35.9277H21.4104C20.2285 35.2747 18.7052 33.9378 17.2133 29.803ZM18.8917 36.8609H27.5044V40.1255H18.8917V36.8609ZM37.111 40.1255H28.4676V36.8609H37.0803V40.1255H37.111ZM40.935 22.3721L38.7901 29.8344C37.2975 33.9378 35.7741 35.2747 34.5931 35.9277H28.4676V33.472C28.4676 30.7047 29.8359 29.8344 31.4528 28.8084L32.6653 28.031C33.1941 27.6887 33.8464 27.5959 34.4995 27.7509C34.966 27.8752 35.339 28.0932 35.4633 28.3725C35.8056 28.9949 35.0589 29.5229 34.8417 29.6786L31.8258 31.6064C31.6078 31.7307 31.5457 32.0415 31.7014 32.2595C31.7943 32.3838 31.9501 32.4767 32.1059 32.4767C32.1987 32.4767 32.2924 32.446 32.3545 32.4145L35.3697 30.4867C36.3336 29.8651 36.7073 28.9634 36.3958 28.1553L38.6658 22.5585C39.2252 21.2217 40.1891 20.7559 40.6864 20.9109C41.0594 21.0045 41.153 21.5954 40.935 22.3721Z" fill="url(#paint0_linear_89_478)"/>
                                    </g>
                                </g>
                                <defs>
                                    <linearGradient id="paint0_linear_89_478" x1="17.4493" y1="17.3831" x2="46.4282" y2="52.5212" gradientUnits="userSpaceOnUse">
                                    <stop stop-color="#548CEE"/>
                                    <stop offset="1" stop-color="#15E7FF"/>
                                    </linearGradient>
                                </defs>
                            </svg>
                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
                            <div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 30px; word-wrap: break-word">Ετήσιες Μονάδες Εργασίας</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
            )
        # with col2:
        #     #st.write('D19')
        #     #st.write(kpdf['D19'][kpdf['year']==str(year_filter)])
        #     text=str(kpdf['D19'][kpdf['year']==str(year_filter)].iloc[0])
        #     # st.write('D19 Ετησιες μοναδες εργασιας: '+text)
        #    # st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας(Μέσος Όρος)</h3>", unsafe_allow_html=True)

        #     # html(
        #     #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
        #     #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
        #     #     <script type="text/javascript">
        #     #     {js_code}
        #     #     animateCounter2("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
        #     #     </script></body>
        #     #     """
        #     # )
        #     html(
        #     f"""
        #         <body>
        #             <div style="display:flex; justify-content: center; " >
        #                 <div style="width:435px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
        #                     <div style="text-align:right;">
        #                     <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
        #                         <g id="&#206;&#149;&#206;&#154;&#206;&#159;">
        #                             <circle id="Ellipse 24" cx="28" cy="28" r="28" fill="white"/>
        #                             <g id="Group">
        #                                 <path id="Vector" d="M40.9972 20.0092C40.0026 19.6677 38.5414 20.3829 37.7955 22.1856L37.484 22.963C37.0181 22.0305 36.2093 21.2839 35.1832 20.9423C35.4012 20.5072 35.5255 19.9785 35.5255 19.4497V19.0768C35.5255 17.2426 34.0329 15.75 32.1987 15.75C30.3646 15.75 28.872 17.2426 28.872 19.0768V19.4497C28.872 19.5119 28.872 19.6055 28.872 19.6677C28.6233 19.6055 28.3125 19.5433 28.0017 19.5433C27.6909 19.5433 27.3794 19.574 27.1 19.6677C27.1 19.6055 27.1 19.5119 27.1 19.4497V19.0768C27.1 17.2426 25.6074 15.75 23.7732 15.75C21.9391 15.75 20.4772 17.2426 20.4772 19.0768V19.4497C20.4772 19.9785 20.6023 20.4758 20.8195 20.9423C19.7934 21.2532 18.9539 21.9991 18.5187 22.963L18.2079 22.1856C17.462 20.3829 16.0008 19.6677 15.0055 20.0092C14.2903 20.2578 13.7001 21.0667 14.1659 22.6207L16.3116 30.0831V30.1138C17.4927 33.3162 18.7052 34.9639 19.7934 35.9277H18.4566C18.2079 35.9277 17.99 36.1457 17.99 36.3943V40.5913C17.99 40.84 18.2079 41.0579 18.4566 41.0579H37.5776C37.8262 41.0579 38.0442 40.84 38.0442 40.5913V36.3943C38.0442 36.1457 37.8262 35.9277 37.5776 35.9277H36.2407C37.3289 34.9953 38.5414 33.3477 39.7225 30.1138V30.0831L41.8682 22.6207C42.2719 21.0667 41.6817 20.2578 40.9972 20.0092ZM36.9245 24.362L35.7434 27.3158C35.4633 27.1293 35.1211 26.9735 34.7481 26.8806C34.2815 26.7563 33.7842 26.7563 33.3184 26.8185C32.8518 25.8231 32.0123 25.0772 30.9862 24.7664C31.2042 24.3313 31.3592 23.8025 31.3592 23.2738V22.9008C31.3592 22.8386 31.3592 22.7458 31.3592 22.6836C31.6393 22.7765 31.9501 22.8079 32.2609 22.8079C33.1941 22.8079 34.0329 22.4035 34.6552 21.7819C35.8363 22.0305 36.8002 23.0873 36.9245 24.362ZM28.0017 26.5698C28.9341 26.5698 29.7737 26.1654 30.3953 25.5438C31.2663 25.7303 32.0123 26.2897 32.4167 27.0978C32.3231 27.1293 32.2609 27.1914 32.168 27.2221L30.9555 27.9995C29.8051 28.7462 28.6233 29.4922 28.0017 30.9226C27.3794 29.4922 26.1983 28.7148 25.0479 27.9995L23.8354 27.2221C23.7418 27.16 23.6796 27.1293 23.5868 27.0978C23.9912 26.3212 24.7371 25.7303 25.6074 25.5438C26.229 26.1654 27.0686 26.5698 28.0017 26.5698ZM29.8051 19.4497V19.0768C29.8051 17.7706 30.8933 16.6824 32.1987 16.6824C33.5049 16.6824 34.5931 17.7706 34.5931 19.0768V19.4497C34.5931 20.7559 33.5049 21.8441 32.1987 21.8441C31.7943 21.8441 31.3906 21.7197 31.0484 21.5333C30.7997 20.9731 30.4268 20.5072 29.9295 20.165C29.8673 19.947 29.8051 19.6984 29.8051 19.4497ZM30.3953 22.8701V23.2431C30.3953 24.5485 29.3071 25.6367 28.0017 25.6367C26.6956 25.6367 25.6074 24.5485 25.6074 23.2431V22.8701C25.6074 21.564 26.6956 20.4758 28.0017 20.4758C29.3071 20.4758 30.3953 21.564 30.3953 22.8701ZM21.4104 19.0768C21.4104 17.7706 22.4986 16.6824 23.804 16.6824C25.1101 16.6824 26.1983 17.7706 26.1983 19.0768V19.4497C26.1983 19.6984 26.1668 19.9163 26.074 20.165C25.5767 20.5072 25.2037 20.9731 24.9543 21.5333C24.6128 21.7197 24.2084 21.8441 23.804 21.8441C22.4986 21.8441 21.4104 20.7866 21.4104 19.4497V19.0768ZM21.4104 21.7504C22.0013 22.3721 22.8715 22.7765 23.804 22.7765C24.1155 22.7765 24.3949 22.7458 24.7057 22.6522C24.7057 22.7143 24.7057 22.8079 24.7057 22.8701V23.2431C24.7057 23.7711 24.83 24.2998 25.0786 24.7349C24.0533 25.0772 23.2138 25.8231 22.7472 26.787C22.2806 26.6942 21.7833 26.7249 21.3167 26.8492C20.9438 26.9428 20.6023 27.0978 20.3222 27.2851L19.0782 24.362C19.2025 23.0873 20.1664 22.0305 21.4104 21.7504ZM17.2133 29.803L15.0677 22.3414C14.8505 21.564 14.9433 21.0045 15.3163 20.8802C15.8136 20.6937 16.8089 21.191 17.3377 22.5278L19.6069 28.1239C19.2961 28.9327 19.6691 29.8344 20.633 30.456L23.6489 32.3838C23.7418 32.446 23.804 32.446 23.8976 32.446C24.0533 32.446 24.2084 32.3838 24.302 32.228C24.457 32.0108 24.3949 31.7307 24.1777 31.5749L21.1617 29.6786C20.9438 29.5229 20.1978 28.9949 20.5401 28.3725C20.6951 28.0932 21.0681 27.8752 21.5032 27.7509C22.1563 27.5959 22.8094 27.6887 23.3381 28.031L24.5506 28.8084C26.1361 29.8344 27.5351 30.7047 27.5351 33.472V35.9277H21.4104C20.2285 35.2747 18.7052 33.9378 17.2133 29.803ZM18.8917 36.8609H27.5044V40.1255H18.8917V36.8609ZM37.111 40.1255H28.4676V36.8609H37.0803V40.1255H37.111ZM40.935 22.3721L38.7901 29.8344C37.2975 33.9378 35.7741 35.2747 34.5931 35.9277H28.4676V33.472C28.4676 30.7047 29.8359 29.8344 31.4528 28.8084L32.6653 28.031C33.1941 27.6887 33.8464 27.5959 34.4995 27.7509C34.966 27.8752 35.339 28.0932 35.4633 28.3725C35.8056 28.9949 35.0589 29.5229 34.8417 29.6786L31.8258 31.6064C31.6078 31.7307 31.5457 32.0415 31.7014 32.2595C31.7943 32.3838 31.9501 32.4767 32.1059 32.4767C32.1987 32.4767 32.2924 32.446 32.3545 32.4145L35.3697 30.4867C36.3336 29.8651 36.7073 28.9634 36.3958 28.1553L38.6658 22.5585C39.2252 21.2217 40.1891 20.7559 40.6864 20.9109C41.0594 21.0045 41.153 21.5954 40.935 22.3721Z" fill="url(#paint0_linear_89_478)"/>
        #                             </g>
        #                         </g>
        #                         <defs>
        #                             <linearGradient id="paint0_linear_89_478" x1="17.4493" y1="17.3831" x2="46.4282" y2="52.5212" gradientUnits="userSpaceOnUse">
        #                             <stop stop-color="#548CEE"/>
        #                             <stop offset="1" stop-color="#15E7FF"/>
        #                             </linearGradient>
        #                         </defs>
        #                     </svg>
        #                     </div>
        #                     <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
        #                     <div>
        #                         <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 30px; word-wrap: break-word">Μεσος Όρος</div>
        #                         <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 30px; word-wrap: break-word">Ετήσιες Μονάδες Εργασίας</div>
        #                     </div>
        #                 </div>
	    #             </div>
        #         <script type="text/javascript">
        #         {js_code}
        #         animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
        #         </script>
        #         </body>



        #     """,height=250
        #     )


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
             



        




def e_button5(id,kpdf,js_code,css_code):
    st.subheader("Κύκλοι εργασιών")
    colors = px.colors.qualitative.Plotly


    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    val2=float(kpdf['D24'][kpdf['year']==str(year_filter)].iloc[0])
    val29=float(kpdf['D29'][kpdf['year']==str(year_filter)].iloc[0])

        #st.write(first_alias_value)
        #st.markdown(text)
   # st.markdown("<h3 style='text-align: center; color: grey;'>Κυκλοι Εργασιών</h3>", unsafe_allow_html=True)
    # text="**"+str(val2)+"** **&#8364;**"
    # html(
    #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
    #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
    #     <script type="text/javascript">
    #     {js_code}
    #     animateCounter3test2("counter", 0, """+str(val2)+""", 1000,100);  // Increase from 0 to 100 in 1 second
    #     </script></body>
    #     """
    # )

    html(f"""<head><style>{css_code}</style></head>
<body >
 	  <div class="icon-area" style="
    display: flex;
    align-items: center;
    border-radius: 16px;
    background: linear-gradient(164deg, #548CEE 0%, #15E7FF 100%);
   padding-left: 30px;
    /* max-width: 80ch; */
    padding-top: 15px;
    padding-bottom: 15px;
"> 
<p>
<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="50" fill="white"/>
<path d="M82.3237 38.4982C82.5788 38.6039 82.8713 38.4828 82.9769 38.2276L84.699 34.0702C84.8047 33.8151 84.6835 33.5226 84.4284 33.4169C84.1733 33.3112 83.8808 33.4324 83.7751 33.6875L82.2444 37.383L78.5489 35.8523C78.2938 35.7466 78.0013 35.8678 77.8956 36.1229C77.7899 36.378 77.9111 36.6705 78.1662 36.7762L82.3237 38.4982ZM75.1355 26.9921L74.782 27.3457V27.3457L75.1355 26.9921ZM64.0913 19.6126L63.9 20.0745L64.0913 19.6126ZM38.0363 19.6126L38.2276 20.0745L38.0363 19.6126ZM26.9921 26.9921L27.3456 27.3457L26.9921 26.9921ZM19.6126 38.0363L20.0745 38.2276L19.6126 38.0363ZM82.9769 37.845C81.241 33.6541 78.6966 29.8461 75.4891 26.6385L74.782 27.3457C77.8967 30.4604 80.3674 34.1581 82.0531 38.2276L82.9769 37.845ZM75.4891 26.6385C72.2815 23.431 68.4735 20.8866 64.2827 19.1507L63.9 20.0745C67.9695 21.7602 71.6672 24.2309 74.782 27.3457L75.4891 26.6385ZM64.2827 19.1507C60.0918 17.4147 55.6 16.5213 51.0638 16.5213V17.5213C55.4687 17.5213 59.8304 18.3889 63.9 20.0745L64.2827 19.1507ZM51.0638 16.5213C46.5276 16.5213 42.0358 17.4147 37.8449 19.1507L38.2276 20.0745C42.2972 18.3889 46.6589 17.5213 51.0638 17.5213V16.5213ZM37.8449 19.1507C33.654 20.8866 29.8461 23.431 26.6385 26.6386L27.3456 27.3457C30.4603 24.2309 34.158 21.7602 38.2276 20.0745L37.8449 19.1507ZM26.6385 26.6386C23.4309 29.8461 20.8866 33.6541 19.1506 37.845L20.0745 38.2276C21.7602 34.1581 24.2309 30.4604 27.3456 27.3457L26.6385 26.6386ZM19.1506 37.845C17.4147 42.0359 16.5212 46.5276 16.5212 51.0638H17.5212C17.5212 46.659 18.3888 42.2972 20.0745 38.2276L19.1506 37.845Z" fill="url(#paint0_linear_111_332)"/>
<path d="M82.5152 64.0914L82.0533 63.9L82.5152 64.0914ZM75.1357 75.1356L75.4893 75.4891L75.1357 75.1356ZM64.0915 82.515L63.9002 82.0531L64.0915 82.515ZM38.0365 82.515L37.8451 82.977L38.0365 82.515ZM26.9923 75.1355L27.3458 74.782L26.9923 75.1355ZM19.1509 63.9C19.2565 63.6449 19.549 63.5237 19.8041 63.6294L23.9616 65.3515C24.2167 65.4572 24.3379 65.7496 24.2322 66.0048C24.1265 66.2599 23.834 66.381 23.5789 66.2754L19.8834 64.7446L18.3527 68.4401C18.247 68.6953 17.9545 68.8164 17.6994 68.7107C17.4443 68.6051 17.3231 68.3126 17.4288 68.0575L19.1509 63.9ZM85.6066 51.0638C85.6066 55.6 84.7131 60.0918 82.9772 64.2827L82.0533 63.9C83.739 59.8304 84.6066 55.4687 84.6066 51.0638H85.6066ZM82.9772 64.2827C81.2412 68.4736 78.6969 72.2815 75.4893 75.4891L74.7822 74.782C77.8969 71.6673 80.3676 67.9696 82.0533 63.9L82.9772 64.2827ZM75.4893 75.4891C72.2817 78.6967 68.4738 81.2411 64.2829 82.977L63.9002 82.0531C67.9698 80.3674 71.6675 77.8967 74.7822 74.782L75.4893 75.4891ZM64.2829 82.977C60.092 84.7129 55.6002 85.6064 51.064 85.6064V84.6064C55.4689 84.6064 59.8306 83.7388 63.9002 82.0531L64.2829 82.977ZM51.064 85.6064C46.5278 85.6064 42.036 84.7129 37.8451 82.977L38.2278 82.0531C42.2974 83.7388 46.6591 84.6064 51.064 84.6064V85.6064ZM37.8451 82.977C33.6543 81.2411 29.8463 78.6967 26.6387 75.4891L27.3458 74.782C30.4606 77.8967 34.1583 80.3674 38.2278 82.0531L37.8451 82.977ZM26.6387 75.4891C23.4312 72.2815 20.8868 68.4736 19.1509 64.2827L20.0747 63.9C21.7604 67.9696 24.2311 71.6673 27.3458 74.782L26.6387 75.4891Z" fill="url(#paint1_linear_111_332)"/>
<path d="M31.532 46.836H36.124C36.4227 44.372 36.992 42.16 37.832 40.2C38.672 38.24 39.736 36.5787 41.024 35.216C42.312 33.8533 43.8053 32.808 45.504 32.08C47.2213 31.352 49.1067 30.988 51.16 30.988C52.3547 30.988 53.456 31.1 54.464 31.324C55.472 31.5293 56.4053 31.8373 57.264 32.248C58.1413 32.6587 58.9533 33.172 59.7 33.788C60.4653 34.3853 61.1933 35.0853 61.884 35.888L61.044 36.868C60.9507 36.9613 60.8573 37.0453 60.764 37.12C60.6893 37.176 60.5773 37.204 60.428 37.204C60.2787 37.204 60.1013 37.1107 59.896 36.924C59.6907 36.7187 59.4293 36.476 59.112 36.196C58.7947 35.916 58.4027 35.608 57.936 35.272C57.488 34.9173 56.9467 34.6 56.312 34.32C55.6773 34.04 54.94 33.8067 54.1 33.62C53.2787 33.4147 52.3267 33.312 51.244 33.312C49.564 33.312 48.024 33.6107 46.624 34.208C45.2427 34.7867 44.02 35.6453 42.956 36.784C41.892 37.9227 41.0147 39.332 40.324 41.012C39.6333 42.692 39.148 44.6333 38.868 46.836H55.724V47.676C55.724 47.8813 55.6493 48.068 55.5 48.236C55.3693 48.3853 55.1547 48.46 54.856 48.46H38.7C38.644 49.3373 38.616 50.2427 38.616 51.176C38.616 51.568 38.616 51.9507 38.616 52.324C38.6347 52.6787 38.6533 53.0427 38.672 53.416H53.176V54.256C53.176 54.48 53.092 54.676 52.924 54.844C52.7747 54.9933 52.56 55.068 52.28 55.068H38.812C39.0547 57.3827 39.512 59.4173 40.184 61.172C40.856 62.9267 41.7147 64.392 42.76 65.568C43.824 66.744 45.056 67.6307 46.456 68.228C47.856 68.8253 49.396 69.124 51.076 69.124C52.2333 69.124 53.2507 69.012 54.128 68.788C55.024 68.564 55.808 68.284 56.48 67.948C57.152 67.5933 57.7213 67.22 58.188 66.828C58.6733 66.4173 59.084 66.044 59.42 65.708C59.7747 65.3533 60.064 65.064 60.288 64.84C60.5307 64.616 60.736 64.504 60.904 64.504C61.0907 64.504 61.2587 64.588 61.408 64.756L62.444 65.736C61.772 66.5947 61.044 67.3787 60.26 68.088C59.476 68.7787 58.608 69.376 57.656 69.88C56.7227 70.3653 55.696 70.7387 54.576 71C53.456 71.28 52.2333 71.42 50.908 71.42C48.7987 71.42 46.8853 71.056 45.168 70.328C43.4507 69.6 41.9573 68.536 40.688 67.136C39.4373 65.736 38.42 64.028 37.636 62.012C36.852 59.9773 36.3293 57.6627 36.068 55.068H31.532V53.416H35.928C35.9093 53.0427 35.8907 52.6787 35.872 52.324C35.872 51.9507 35.872 51.568 35.872 51.176C35.872 50.2613 35.9 49.356 35.956 48.46H31.532V46.836Z" fill="url(#paint2_linear_111_332)"/>
<defs>
<linearGradient id="paint0_linear_111_332" x1="25.0894" y1="19.218" x2="55.8368" y2="84.0486" gradientUnits="userSpaceOnUse">
<stop stop-color="#548CEE"/>
<stop offset="1" stop-color="#15E7FF"/>
</linearGradient>
<linearGradient id="paint1_linear_111_332" x1="27.681" y1="82.9097" x2="58.4283" y2="18.079" gradientUnits="userSpaceOnUse">
<stop stop-color="#548CEE"/>
<stop offset="1" stop-color="#15E7FF"/>
</linearGradient>
<linearGradient id="paint2_linear_111_332" x1="35.0653" y1="33.5811" x2="81.4848" y2="75.5521" gradientUnits="userSpaceOnUse">
<stop stop-color="#548CEE"/>
<stop offset="1" stop-color="#15E7FF"/>
</linearGradient>
</defs>
</svg>



   </p>
   <div class="column" style="display: flex;
   flex-direction: column;padding-left: 30px;
    padding-top: 30px;">
      <h3 class="icon-header" style="font-size: 18px;
      line-height: 0px;
      display: block;
      padding-right: 20px;"><div id="counter" style="text-align: left; color:white;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
        </h3>
       <p style="
    color: #002970;
    font-size: 24px;
    /* font-family: Ubuntu; */
    font-weight: 300;
    line-height: 24px;
    word-wrap: break-word;">Κύκλοι Εργασιών</p>
   </div>
    <div>
        <div class="number" style="text-align:center; font-size: 24px;padding-left:30px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">{str(val29)} %</div>
    </div>
</div>
    <script type="text/javascript">
    {js_code}
    animateCounter3test2("counter", 0, """+str(val2)+""", 1000,100);  // Increase from 0 to 100 in 1 second
    </script>
    </body>
        """,height=250)

    # html(
    #         f"""
    #             <body style="background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%);">
    #                 <div style="display:flex; justify-content: center; " >
    #                     <div style="width:310px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); display: flex;align-items: center;flex-direction: column;flex-wrap: nowrap;border: 1px solid transparent;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
    #                         <div style="text-align:right;">
    #                         <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
    #                             <g id="&#206;&#149;&#206;&#154;&#206;&#159;">
    #                                 <circle id="Ellipse 24" cx="28" cy="28" r="28" fill="white"/>
    #                                 <g id="Group">
    #                                     <path id="Vector" d="M40.9972 20.0092C40.0026 19.6677 38.5414 20.3829 37.7955 22.1856L37.484 22.963C37.0181 22.0305 36.2093 21.2839 35.1832 20.9423C35.4012 20.5072 35.5255 19.9785 35.5255 19.4497V19.0768C35.5255 17.2426 34.0329 15.75 32.1987 15.75C30.3646 15.75 28.872 17.2426 28.872 19.0768V19.4497C28.872 19.5119 28.872 19.6055 28.872 19.6677C28.6233 19.6055 28.3125 19.5433 28.0017 19.5433C27.6909 19.5433 27.3794 19.574 27.1 19.6677C27.1 19.6055 27.1 19.5119 27.1 19.4497V19.0768C27.1 17.2426 25.6074 15.75 23.7732 15.75C21.9391 15.75 20.4772 17.2426 20.4772 19.0768V19.4497C20.4772 19.9785 20.6023 20.4758 20.8195 20.9423C19.7934 21.2532 18.9539 21.9991 18.5187 22.963L18.2079 22.1856C17.462 20.3829 16.0008 19.6677 15.0055 20.0092C14.2903 20.2578 13.7001 21.0667 14.1659 22.6207L16.3116 30.0831V30.1138C17.4927 33.3162 18.7052 34.9639 19.7934 35.9277H18.4566C18.2079 35.9277 17.99 36.1457 17.99 36.3943V40.5913C17.99 40.84 18.2079 41.0579 18.4566 41.0579H37.5776C37.8262 41.0579 38.0442 40.84 38.0442 40.5913V36.3943C38.0442 36.1457 37.8262 35.9277 37.5776 35.9277H36.2407C37.3289 34.9953 38.5414 33.3477 39.7225 30.1138V30.0831L41.8682 22.6207C42.2719 21.0667 41.6817 20.2578 40.9972 20.0092ZM36.9245 24.362L35.7434 27.3158C35.4633 27.1293 35.1211 26.9735 34.7481 26.8806C34.2815 26.7563 33.7842 26.7563 33.3184 26.8185C32.8518 25.8231 32.0123 25.0772 30.9862 24.7664C31.2042 24.3313 31.3592 23.8025 31.3592 23.2738V22.9008C31.3592 22.8386 31.3592 22.7458 31.3592 22.6836C31.6393 22.7765 31.9501 22.8079 32.2609 22.8079C33.1941 22.8079 34.0329 22.4035 34.6552 21.7819C35.8363 22.0305 36.8002 23.0873 36.9245 24.362ZM28.0017 26.5698C28.9341 26.5698 29.7737 26.1654 30.3953 25.5438C31.2663 25.7303 32.0123 26.2897 32.4167 27.0978C32.3231 27.1293 32.2609 27.1914 32.168 27.2221L30.9555 27.9995C29.8051 28.7462 28.6233 29.4922 28.0017 30.9226C27.3794 29.4922 26.1983 28.7148 25.0479 27.9995L23.8354 27.2221C23.7418 27.16 23.6796 27.1293 23.5868 27.0978C23.9912 26.3212 24.7371 25.7303 25.6074 25.5438C26.229 26.1654 27.0686 26.5698 28.0017 26.5698ZM29.8051 19.4497V19.0768C29.8051 17.7706 30.8933 16.6824 32.1987 16.6824C33.5049 16.6824 34.5931 17.7706 34.5931 19.0768V19.4497C34.5931 20.7559 33.5049 21.8441 32.1987 21.8441C31.7943 21.8441 31.3906 21.7197 31.0484 21.5333C30.7997 20.9731 30.4268 20.5072 29.9295 20.165C29.8673 19.947 29.8051 19.6984 29.8051 19.4497ZM30.3953 22.8701V23.2431C30.3953 24.5485 29.3071 25.6367 28.0017 25.6367C26.6956 25.6367 25.6074 24.5485 25.6074 23.2431V22.8701C25.6074 21.564 26.6956 20.4758 28.0017 20.4758C29.3071 20.4758 30.3953 21.564 30.3953 22.8701ZM21.4104 19.0768C21.4104 17.7706 22.4986 16.6824 23.804 16.6824C25.1101 16.6824 26.1983 17.7706 26.1983 19.0768V19.4497C26.1983 19.6984 26.1668 19.9163 26.074 20.165C25.5767 20.5072 25.2037 20.9731 24.9543 21.5333C24.6128 21.7197 24.2084 21.8441 23.804 21.8441C22.4986 21.8441 21.4104 20.7866 21.4104 19.4497V19.0768ZM21.4104 21.7504C22.0013 22.3721 22.8715 22.7765 23.804 22.7765C24.1155 22.7765 24.3949 22.7458 24.7057 22.6522C24.7057 22.7143 24.7057 22.8079 24.7057 22.8701V23.2431C24.7057 23.7711 24.83 24.2998 25.0786 24.7349C24.0533 25.0772 23.2138 25.8231 22.7472 26.787C22.2806 26.6942 21.7833 26.7249 21.3167 26.8492C20.9438 26.9428 20.6023 27.0978 20.3222 27.2851L19.0782 24.362C19.2025 23.0873 20.1664 22.0305 21.4104 21.7504ZM17.2133 29.803L15.0677 22.3414C14.8505 21.564 14.9433 21.0045 15.3163 20.8802C15.8136 20.6937 16.8089 21.191 17.3377 22.5278L19.6069 28.1239C19.2961 28.9327 19.6691 29.8344 20.633 30.456L23.6489 32.3838C23.7418 32.446 23.804 32.446 23.8976 32.446C24.0533 32.446 24.2084 32.3838 24.302 32.228C24.457 32.0108 24.3949 31.7307 24.1777 31.5749L21.1617 29.6786C20.9438 29.5229 20.1978 28.9949 20.5401 28.3725C20.6951 28.0932 21.0681 27.8752 21.5032 27.7509C22.1563 27.5959 22.8094 27.6887 23.3381 28.031L24.5506 28.8084C26.1361 29.8344 27.5351 30.7047 27.5351 33.472V35.9277H21.4104C20.2285 35.2747 18.7052 33.9378 17.2133 29.803ZM18.8917 36.8609H27.5044V40.1255H18.8917V36.8609ZM37.111 40.1255H28.4676V36.8609H37.0803V40.1255H37.111ZM40.935 22.3721L38.7901 29.8344C37.2975 33.9378 35.7741 35.2747 34.5931 35.9277H28.4676V33.472C28.4676 30.7047 29.8359 29.8344 31.4528 28.8084L32.6653 28.031C33.1941 27.6887 33.8464 27.5959 34.4995 27.7509C34.966 27.8752 35.339 28.0932 35.4633 28.3725C35.8056 28.9949 35.0589 29.5229 34.8417 29.6786L31.8258 31.6064C31.6078 31.7307 31.5457 32.0415 31.7014 32.2595C31.7943 32.3838 31.9501 32.4767 32.1059 32.4767C32.1987 32.4767 32.2924 32.446 32.3545 32.4145L35.3697 30.4867C36.3336 29.8651 36.7073 28.9634 36.3958 28.1553L38.6658 22.5585C39.2252 21.2217 40.1891 20.7559 40.6864 20.9109C41.0594 21.0045 41.153 21.5954 40.935 22.3721Z" fill="url(#paint0_linear_89_478)"/>
    #                                 </g>
    #                             </g>
    #                             <defs>
    #                                 <linearGradient id="paint0_linear_89_478" x1="17.4493" y1="17.3831" x2="46.4282" y2="52.5212" gradientUnits="userSpaceOnUse">
    #                                 <stop stop-color="#548CEE"/>
    #                                 <stop offset="1" stop-color="#15E7FF"/>
    #                                 </linearGradient>
    #                             </defs>
    #                         </svg>
    #                         </div>
    #                         <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 60px;"></div>
    #                         <div>
    #                             <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Yπηρεσίες</div>
    #                             <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Κυκλοι Εργασιών</div>
    #                         </div>
    #                     </div>
	#                 </div>
    #             <script type="text/javascript">
    #             {js_code}
    #             animateCounter3test2("counter", 0, """+str(val2)+""", 1000,100);  // Increase from 0 to 100 in 1 second
    #             </script>
    #             </body>



    #         """,height=300
    #     )
   # st.markdown("<h3 style='text-align: center; color: grey;'>Yπηρεσίες</h3>", unsafe_allow_html=True)

    with st.container():
        col1, col2,col3 = st.columns(3)

        with col1:
            #st.markdown("<h3 style='text-align: center; color: grey;'>🏠 Κτηρίων & Εξ. Χώρων</h3>", unsafe_allow_html=True)

            val26=float(kpdf['D26'][kpdf['year']==str(year_filter)].iloc[0])
            
            val4=float(kpdf['D30'][kpdf['year']==str(year_filter)].iloc[0])
            

            # text26="**🏠** **"+str(val26)+"** &#8364; "

            # html(
            #         f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #         <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #         <script type="text/javascript">
            #         {js_code}
            #         animateCounter3("counter", 0, """+str(val26)+""", 1000);  // Increase from 0 to 100 in 1 second
            #         </script></body>
            #         """
            #     )
            html(
            f"""<head><style>{css_code}</style></head>
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px; display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                 <svg width="56" height="56" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="&#206;&#154;&#207;&#132;&#206;&#174;&#207;&#129;&#206;&#185;&#206;&#191;">
<circle id="Ellipse 25" cx="16" cy="16" r="16" fill="url(#paint0_linear_103_204)"/>
<path id="XMLID_1_" d="M22.2862 23H9.71458V16.0769H8.706C8.05571 16.0769 7.75227 15.2582 8.242 14.8261L14.9324 8.42967C15.5312 7.85678 16.469 7.85678 17.0678 8.42967L23.7576 14.8261C24.2479 15.2576 23.9445 16.0769 23.2936 16.0769H22.2862V23Z" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="XMLID_2_" d="M18 23H14V19.4C14 18.0746 14.8955 17 16 17C17.1045 17 18 18.0746 18 19.4V23Z" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<defs>
<linearGradient id="paint0_linear_103_204" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
<stop stop-color="#548CEE"/>
<stop offset="1" stop-color="#15E7FF"/>
</linearGradient>
</defs>
</svg>





                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Κτηρίων & Εξ. Χώρων</div>
                            </div>
                            <div>
                                <div class="number" style="text-align:center; font-size: 24px;padding-left:30px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">{str(val4)} %</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter3test2("counter", 0, """+str(val26)+""", 1000,10);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
            )



        with col2:
            #st.markdown("<h3 style='text-align: center; color: grey;'>🍴 Εστίασης</h3>", unsafe_allow_html=True)

            val27=float(kpdf['D27'][kpdf['year']==str(year_filter)].iloc[0])
            val6=float(kpdf['D31'][kpdf['year']==str(year_filter)].iloc[0])
            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter3("counter", 0, """+str(val27)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            # )
            html(
            f"""<head><style>{css_code}</style></head>
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px;  display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                          <svg width="56" height="56" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="&#206;&#149;&#207;&#131;&#207;&#132;&#206;&#175;&#206;&#177;&#207;&#131;&#206;&#183;">
<circle id="Ellipse 27" cx="16" cy="16" r="16" fill="url(#paint0_linear_103_212)"/>
<g id="Group 2">
<path id="Vector" d="M10.1502 14.2243C8.72043 12.7945 8.72043 10.5398 10.1502 9.10999L16.2545 15.2142L18.2892 17.249L21.4238 20.3836C21.9738 20.9335 21.9738 21.7584 21.4238 22.3083C20.8739 22.8583 19.884 22.8583 19.3891 22.1983L17.1344 19.3937C16.5844 18.6788 15.5946 18.4588 14.7147 18.7888L10.1502 14.2243Z" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_2" d="M18.2893 13.4544L21.2589 10.4848" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_3" d="M17.0793 16.0391C17.2993 15.9841 17.4643 15.9841 17.6843 15.9291C18.3992 15.8741 19.2241 15.4892 20.049 14.6643L22.7436 11.9696" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_4" d="M13.3398 17.4139L9.49027 20.5485C8.88535 20.9885 8.83035 21.8684 9.38028 22.3633C9.93022 22.9133 10.7551 22.8033 11.1951 22.2533L14.3297 18.3488" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_5" d="M19.7739 9L17.0242 11.6947C16.1993 12.5196 15.7594 13.3445 15.7594 14.0594C15.7594 14.2793 15.7044 14.4443 15.6494 14.6643" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
</g>
</g>
<defs>
<linearGradient id="paint0_linear_103_212" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
<stop stop-color="#548CEE"/>
<stop offset="1" stop-color="#15E7FF"/>
</linearGradient>
</defs>
</svg>

                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εστίασης</div>
                            </div>
                            <div>
                                <div class="number" style="text-align:center; font-size: 24px;padding-left:30px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">{str(val6)} %</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter3test2("counter", 0, """+str(val27)+""", 1000,10);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
            )
        with col3:
            #st.markdown("<h3 style='text-align: center; color: grey;'>💬 Λοιπές Δραστηρίοτητες</h3>", unsafe_allow_html=True)

            val28=float(kpdf['D28'][kpdf['year']==str(year_filter)].iloc[0])
            val8=float(kpdf['D32'][kpdf['year']==str(year_filter)].iloc[0])

            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter3("counter", 0, """+str(val28)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            # )
            html(
            f"""<head><style>{css_code}</style></head>
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px; display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                  <svg width="56" height="56" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="...">
<circle id="Ellipse 26" cx="16" cy="16" r="16" fill="url(#paint0_linear_103_208)"/>
<path id="Vector" d="M16 13C15.4914 13 14.9943 13.1508 14.5714 13.4334C14.1485 13.7159 13.8189 14.1175 13.6243 14.5874C13.4297 15.0573 13.3788 15.5743 13.478 16.0731C13.5772 16.5719 13.8221 17.0301 14.1817 17.3897C14.5413 17.7493 14.9995 17.9942 15.4983 18.0934C15.9971 18.1927 16.5142 18.1417 16.984 17.9471C17.4539 17.7525 17.8555 17.4229 18.1381 17C18.4206 16.5772 18.5714 16.08 18.5714 15.5714C18.5714 14.8894 18.3005 14.2354 17.8183 13.7532C17.336 13.2709 16.682 13 16 13ZM16 16.8571C15.7457 16.8571 15.4971 16.7817 15.2857 16.6405C15.0743 16.4992 14.9095 16.2984 14.8122 16.0634C14.7148 15.8285 14.6894 15.57 14.739 15.3206C14.7886 15.0712 14.9111 14.8421 15.0909 14.6623C15.2707 14.4825 15.4998 14.36 15.7492 14.3104C15.9986 14.2608 16.2571 14.2863 16.492 14.3836C16.727 14.4809 16.9278 14.6457 17.069 14.8571C17.2103 15.0686 17.2857 15.3171 17.2857 15.5714C17.2857 15.9124 17.1503 16.2394 16.9091 16.4806C16.668 16.7217 16.341 16.8571 16 16.8571ZM9.57143 13C9.06285 13 8.56569 13.1508 8.14282 13.4334C7.71995 13.7159 7.39036 14.1175 7.19574 14.5874C7.00111 15.0573 6.95019 15.5743 7.04941 16.0731C7.14863 16.5719 7.39353 17.0301 7.75315 17.3897C8.11278 17.7493 8.57096 17.9942 9.06977 18.0934C9.56858 18.1927 10.0856 18.1417 10.5555 17.9471C11.0253 17.7525 11.4269 17.4229 11.7095 17C11.992 16.5772 12.1429 16.08 12.1429 15.5714C12.1429 14.8894 11.8719 14.2354 11.3897 13.7532C10.9075 13.2709 10.2534 13 9.57143 13ZM9.57143 16.8571C9.31714 16.8571 9.06856 16.7817 8.85713 16.6405C8.64569 16.4992 8.4809 16.2984 8.38358 16.0634C8.28627 15.8285 8.26081 15.57 8.31042 15.3206C8.36003 15.0712 8.48248 14.8421 8.66229 14.6623C8.8421 14.4825 9.07119 14.36 9.3206 14.3104C9.57 14.2608 9.82852 14.2863 10.0635 14.3836C10.2984 14.4809 10.4992 14.6457 10.6405 14.8571C10.7817 15.0686 10.8571 15.3171 10.8571 15.5714C10.8571 15.9124 10.7217 16.2394 10.4806 16.4806C10.2394 16.7217 9.91242 16.8571 9.57143 16.8571ZM22.4286 13C21.92 13 21.4228 13.1508 21 13.4334C20.5771 13.7159 20.2475 14.1175 20.0529 14.5874C19.8583 15.0573 19.8073 15.5743 19.9066 16.0731C20.0058 16.5719 20.2507 17.0301 20.6103 17.3897C20.9699 17.7493 21.4281 17.9942 21.9269 18.0934C22.4257 18.1927 22.9427 18.1417 23.4126 17.9471C23.8825 17.7525 24.2841 17.4229 24.5666 17C24.8492 16.5772 25 16.08 25 15.5714C25 14.8894 24.7291 14.2354 24.2468 13.7532C23.7646 13.2709 23.1106 13 22.4286 13ZM22.4286 16.8571C22.1743 16.8571 21.9257 16.7817 21.7143 16.6405C21.5028 16.4992 21.338 16.2984 21.2407 16.0634C21.1434 15.8285 21.118 15.57 21.1676 15.3206C21.2172 15.0712 21.3396 14.8421 21.5194 14.6623C21.6992 14.4825 21.9283 14.36 22.1777 14.3104C22.4271 14.2608 22.6857 14.2863 22.9206 14.3836C23.1555 14.4809 23.3563 14.6457 23.4976 14.8571C23.6389 15.0686 23.7143 15.3171 23.7143 15.5714C23.7143 15.9124 23.5788 16.2394 23.3377 16.4806C23.0966 16.7217 22.7696 16.8571 22.4286 16.8571Z" fill="white"/>
</g>
<defs>
<linearGradient id="paint0_linear_103_208" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
<stop stop-color="#548CEE"/>
<stop offset="1" stop-color="#15E7FF"/>
</linearGradient>
</defs>
</svg>

                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Λοιπές Δραστηρίοτητες</div>
                            </div>
                             <div>
                                <div class="number" style="text-align:center; font-size: 24px;padding-left:30px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">{str(val8)} %</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter3test2("counter", 0, """+str(val28)+""", 1000,10);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
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
    st.subheader("Διαχρονική (%) μεταβολή Κύκλων Εργασιών")
    # year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    # val1=float(kpdf['D24'][kpdf['year']==str(year_filter)].iloc[0])
    # val2=float(kpdf['D29'][kpdf['year']==str(year_filter)].iloc[0])
    # val3=float(kpdf['D26'][kpdf['year']==str(year_filter)].iloc[0])
    # val4=float(kpdf['D30'][kpdf['year']==str(year_filter)].iloc[0])
    # val5=float(kpdf['D27'][kpdf['year']==str(year_filter)].iloc[0])
    # val6=float(kpdf['D31'][kpdf['year']==str(year_filter)].iloc[0])
    # val7=float(kpdf['D28'][kpdf['year']==str(year_filter)].iloc[0])
    # val8=float(kpdf['D32'][kpdf['year']==str(year_filter)].iloc[0])

    #METABOLES
    # with st.container():
    #     col1, col2,col3,col4 = st.columns(4)
    #     with col1:
    #         st.markdown("<h3 style='text-align: center; color: grey;'>% Μεταβολή Κύκλου Εργασιών</h3>", unsafe_allow_html=True)
    #         html(
    #             f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
    #             <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
    #             <script type="text/javascript">
    #             {js_code}
    #             animateCounter2("counter", 0, """+str(val1)+""", 1000);  // Increase from 0 to 100 in 1 second
    #             </script></body>
    #             """
    #                     )
    #         st.metric(label="% Μεταβολή Κύκλου Εργασιών",label_visibility="hidden", value=val1, delta=f'{val2}%')



    #     with col2:
    #         st.markdown("<h3 style='text-align: center; color: grey;'>% Μετ.Kύκλ.Εργ. Κτήρια/Εξωτερικοί Χώροι</h3>", unsafe_allow_html=True)
    #         html(
    #             f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
    #             <div id="counter" style="text-align: center; font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
    #             <script type="text/javascript">
    #             {js_code}
    #             animateCounter2("counter", 0, """+str(val3)+""", 1000);  // Increase from 0 to 100 in 1 second
    #             </script></body>
    #             """
    #                     )
    #         st.metric(label="% Μετ.Kύκλ.Εργ. Κτήρια/Εξωτ. Χώροι ", label_visibility="hidden", value=val3, delta=f'{val4}%')
    #     with col3:
    #         st.markdown("<h3 style='text-align: center; color: grey;'>% Μετ.Κύκλ.Εργ. Υπηρ. Εστίασης</h3>", unsafe_allow_html=True)
    #         html(
    #             f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
    #             <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
    #             <script type="text/javascript">
    #             {js_code}
    #             animateCounter2("counter", 0, """+str(val5)+""", 1000);  // Increase from 0 to 100 in 1 second
    #             </script></body>
    #             """
    #                     )
    #         st.metric(label="% Μετ.Κύκλ.Εργ. Υπηρ. Εστίασης",label_visibility="hidden", value=val5, delta=f'{val6}%')
    #     with col4:
    #         st.markdown("<h3 style='text-align: center; color: grey;'>% Μετ.Κύκλ.Εργ. Λοιπ. Εργασίες</h3>", unsafe_allow_html=True)
    #         html(
    #             f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
    #             <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
    #             <script type="text/javascript">
    #             {js_code}
    #             animateCounter2("counter", 0, """+str(val7)+""", 1000);  // Increase from 0 to 100 in 1 second
    #             </script></body>
    #             """
    #                     )

    #         st.metric(label="% Μετ.Kυκλ.Εργ. Λοιπές εργασίες",label_visibility="hidden", value=val7, delta=f'{val8}%')

        

    # st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Κύκλου Εργασιών</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D24'].astype(float).tolist()

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
            values =kpdf['D27'].astype(float).tolist()
            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μετ.Κύκλ.Εργ. Λοιπ. Δραστ.</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D28'].astype(float).tolist()
            fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)





def e_button7(id,kpdf,js_code,css_code):
    st.subheader("Κατανομή πλήθους με βάση το καθαρό εισόδημα")

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    val1=float(kpdf['D36_overal'][kpdf['year']==str(year_filter)].iloc[0])
    val2=float(kpdf['D36'][kpdf['year']==str(year_filter)].iloc[0])

    val3=float(kpdf['D38'][kpdf['year']==str(year_filter)].iloc[0])
    val4=float(kpdf['D40'][kpdf['year']==str(year_filter)].iloc[0])
    val5=float(kpdf['D40_metaboli'][kpdf['year']==str(year_filter)].iloc[0])

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            # st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Καθαρών αποτελεσμάτων</h3>", unsafe_allow_html=True)
            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter2("counter", 0, """+str(val1)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            #             )
            html(
            f"""<head><style>{css_code}</style></head>
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px;  display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                          <svg width="56" height="56" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="&#206;&#149;&#207;&#131;&#207;&#132;&#206;&#175;&#206;&#177;&#207;&#131;&#206;&#183;">
<circle id="Ellipse 27" cx="16" cy="16" r="16" fill="url(#paint0_linear_103_212)"/>
<g id="Group 2">
<path id="Vector" d="M10.1502 14.2243C8.72043 12.7945 8.72043 10.5398 10.1502 9.10999L16.2545 15.2142L18.2892 17.249L21.4238 20.3836C21.9738 20.9335 21.9738 21.7584 21.4238 22.3083C20.8739 22.8583 19.884 22.8583 19.3891 22.1983L17.1344 19.3937C16.5844 18.6788 15.5946 18.4588 14.7147 18.7888L10.1502 14.2243Z" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_2" d="M18.2893 13.4544L21.2589 10.4848" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_3" d="M17.0793 16.0391C17.2993 15.9841 17.4643 15.9841 17.6843 15.9291C18.3992 15.8741 19.2241 15.4892 20.049 14.6643L22.7436 11.9696" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_4" d="M13.3398 17.4139L9.49027 20.5485C8.88535 20.9885 8.83035 21.8684 9.38028 22.3633C9.93022 22.9133 10.7551 22.8033 11.1951 22.2533L14.3297 18.3488" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_5" d="M19.7739 9L17.0242 11.6947C16.1993 12.5196 15.7594 13.3445 15.7594 14.0594C15.7594 14.2793 15.7044 14.4443 15.6494 14.6643" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
</g>
</g>
<defs>
<linearGradient id="paint0_linear_103_212" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
<stop stop-color="#548CEE"/>
<stop offset="1" stop-color="#15E7FF"/>
</linearGradient>
</defs>
</svg>

                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:left; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Καθαρά αποτελέσματα</div>
                            </div>
                            <div>
                                <div class="number" style="text-align:center; font-size: 24px;padding-left:30px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">{str(val2)} %</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val1)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
            )




            # st.metric(label="% Ετήσια Μεταβολή Καθαρών αποτελεσμάτων",label_visibility="hidden", value=val1, delta=f'{val2}%')


        with col2:
            # st.markdown("<h3 style='text-align: center; color: grey;'>Αριθμοδείκτη καθαρών αποτελεσμάτων</h3>", unsafe_allow_html=True)

            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;    font-family: 'Source Sans Pro',sans-serif; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter2("counter", 0, """+str(val3)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """
            #             )

            html(
            f"""<head><style>{css_code}</style></head>
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px;  display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                          <svg width="56" height="56" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g id="&#206;&#149;&#207;&#131;&#207;&#132;&#206;&#175;&#206;&#177;&#207;&#131;&#206;&#183;">
                                <circle id="Ellipse 27" cx="16" cy="16" r="16" fill="url(#paint0_linear_103_212)"/>
                                <g id="Group 2">
                                <path id="Vector" d="M10.1502 14.2243C8.72043 12.7945 8.72043 10.5398 10.1502 9.10999L16.2545 15.2142L18.2892 17.249L21.4238 20.3836C21.9738 20.9335 21.9738 21.7584 21.4238 22.3083C20.8739 22.8583 19.884 22.8583 19.3891 22.1983L17.1344 19.3937C16.5844 18.6788 15.5946 18.4588 14.7147 18.7888L10.1502 14.2243Z" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                <path id="Vector_2" d="M18.2893 13.4544L21.2589 10.4848" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                <path id="Vector_3" d="M17.0793 16.0391C17.2993 15.9841 17.4643 15.9841 17.6843 15.9291C18.3992 15.8741 19.2241 15.4892 20.049 14.6643L22.7436 11.9696" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                <path id="Vector_4" d="M13.3398 17.4139L9.49027 20.5485C8.88535 20.9885 8.83035 21.8684 9.38028 22.3633C9.93022 22.9133 10.7551 22.8033 11.1951 22.2533L14.3297 18.3488" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                <path id="Vector_5" d="M19.7739 9L17.0242 11.6947C16.1993 12.5196 15.7594 13.3445 15.7594 14.0594C15.7594 14.2793 15.7044 14.4443 15.6494 14.6643" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                </g>
                                </g>
                                <defs>
                                <linearGradient id="paint0_linear_103_212" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                </defs>
                            </svg>

                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:left; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Αριθμοδείκτης καθαρών αποτελεσμάτων</div>
                            </div>

                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val3)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
            )

            

            # st.metric(label="Αριθμοδείκτη καθαρών αποτελεσμάτων", label_visibility="hidden",value=val3)
        with col3:
            # st.markdown("<h3 style='text-align: center; color: grey;'>Έσοδα ανά εργαζόμενο / % Ετήσια Μεταβολή</h3>", unsafe_allow_html=True)
            # html(
            #     f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
            #     <div id="counter" style="text-align: center;     font-family: 'Source Sans Pro',sans-serif;font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
            #     <script type="text/javascript">
            #     {js_code}
            #     animateCounter2("counter", 0, """+str(val4)+""", 1000);  // Increase from 0 to 100 in 1 second
            #     </script></body>
            #     """    )

            html(
            f"""<head><style>{css_code}</style></head>
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px;  display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                          <svg width="56" height="56" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g id="&#206;&#149;&#207;&#131;&#207;&#132;&#206;&#175;&#206;&#177;&#207;&#131;&#206;&#183;">
                                <circle id="Ellipse 27" cx="16" cy="16" r="16" fill="url(#paint0_linear_103_212)"/>
                                <g id="Group 2">
                                <path id="Vector" d="M10.1502 14.2243C8.72043 12.7945 8.72043 10.5398 10.1502 9.10999L16.2545 15.2142L18.2892 17.249L21.4238 20.3836C21.9738 20.9335 21.9738 21.7584 21.4238 22.3083C20.8739 22.8583 19.884 22.8583 19.3891 22.1983L17.1344 19.3937C16.5844 18.6788 15.5946 18.4588 14.7147 18.7888L10.1502 14.2243Z" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                <path id="Vector_2" d="M18.2893 13.4544L21.2589 10.4848" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                <path id="Vector_3" d="M17.0793 16.0391C17.2993 15.9841 17.4643 15.9841 17.6843 15.9291C18.3992 15.8741 19.2241 15.4892 20.049 14.6643L22.7436 11.9696" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                <path id="Vector_4" d="M13.3398 17.4139L9.49027 20.5485C8.88535 20.9885 8.83035 21.8684 9.38028 22.3633C9.93022 22.9133 10.7551 22.8033 11.1951 22.2533L14.3297 18.3488" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                <path id="Vector_5" d="M19.7739 9L17.0242 11.6947C16.1993 12.5196 15.7594 13.3445 15.7594 14.0594C15.7594 14.2793 15.7044 14.4443 15.6494 14.6643" stroke="white" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                                </g>
                                </g>
                                <defs>
                                <linearGradient id="paint0_linear_103_212" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#548CEE"/>
                                <stop offset="1" stop-color="#15E7FF"/>
                                </linearGradient>
                                </defs>
                            </svg>

                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:left; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Έσοδα ανά εργαζόμενο</div>
                            </div>
                            <div>
                                <div class="number" style="text-align:center; font-size: 24px;padding-left:30px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">{str(val5)} %</div>
                            </div>
                        </div>
	                </div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(val4)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script>
                </body>



            """,height=250
            )

            






            # st.metric(label="Έσοδα ανά εργαζόμενο / % Ετήσια Μεταβολή", label_visibility="hidden", value=val4, delta=f'{val5}%')
    
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Καθαρών Αποτελεσμάτων</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D36_overal'].astype(float).tolist()
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
    
