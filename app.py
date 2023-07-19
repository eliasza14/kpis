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
    st.write(df.dtypes)

    st.write(df)

    df['year'] = df['year'].map(lambda x: str(x) if pd.notnull(x) else None)
    df['year'] = df['year'].str.split('.').str[0]
    df['year'] = df['year'].astype(str)
    df['year'] = df['year'].str.replace(',', '')
    st.write(df.dtypes)

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
    st.write(merged)
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
<path d="M82.1323 38.9602C82.6426 39.1715 83.2275 38.9292 83.4389 38.419L86.883 30.1041C87.0944 29.5938 86.8521 29.0089 86.3418 28.7975C85.8316 28.5862 85.2466 28.8285 85.0353 29.3387L81.9738 36.7297L74.5828 33.6683C74.0725 33.4569 73.4876 33.6992 73.2762 34.2095C73.0649 34.7197 73.3072 35.3047 73.8174 35.516L82.1323 38.9602ZM75.1355 26.9921L74.4284 27.6992L74.4284 27.6992L75.1355 26.9921ZM64.0913 19.6126L63.7086 20.5365L63.7086 20.5365L64.0913 19.6126ZM38.0363 19.6126L38.419 20.5365L38.419 20.5365L38.0363 19.6126ZM26.9921 26.9921L27.6992 27.6992L27.6992 27.6992L26.9921 26.9921ZM19.6126 38.0363L20.5365 38.419L20.5365 38.419L19.6126 38.0363ZM83.4389 37.6536C81.6778 33.4021 79.0966 29.539 75.8426 26.285L74.4284 27.6992C77.4967 30.7675 79.9306 34.4101 81.5911 38.419L83.4389 37.6536ZM75.8426 26.285C72.5886 23.031 68.7256 20.4498 64.474 18.6887L63.7086 20.5365C67.7175 22.197 71.3601 24.6309 74.4284 27.6992L75.8426 26.285ZM64.474 18.6887C60.2224 16.9277 55.6656 16.0213 51.0638 16.0213V18.0213C55.403 18.0213 59.6997 18.8759 63.7086 20.5365L64.474 18.6887ZM51.0638 16.0213C46.4619 16.0213 41.9051 16.9277 37.6536 18.6887L38.419 20.5365C42.4279 18.8759 46.7246 18.0213 51.0638 18.0213V16.0213ZM37.6536 18.6887C33.402 20.4498 29.539 23.031 26.285 26.285L27.6992 27.6992C30.7675 24.6309 34.41 22.197 38.419 20.5365L37.6536 18.6887ZM26.285 26.285C23.031 29.539 20.4497 33.4021 18.6887 37.6536L20.5365 38.419C22.197 34.4101 24.6309 30.7675 27.6992 27.6992L26.285 26.285ZM18.6887 37.6536C16.9276 41.9052 16.0212 46.462 16.0212 51.0638H18.0212C18.0212 46.7246 18.8759 42.4279 20.5365 38.419L18.6887 37.6536Z" fill="url(#paint0_linear_111_332)"/>
<path d="M64.0915 82.515L63.7088 81.5912L63.7088 81.5912L64.0915 82.515ZM38.0365 82.515L38.4192 81.5912L38.4192 81.5912L38.0365 82.515ZM26.9923 75.1355L26.2852 75.8427L26.2852 75.8427L26.9923 75.1355ZM18.6889 63.7087C18.9003 63.1984 19.4852 62.9561 19.9955 63.1675L28.3104 66.6116C28.8206 66.823 29.0629 67.4079 28.8516 67.9182C28.6402 68.4284 28.0553 68.6707 27.545 68.4594L20.154 65.3979L17.0925 72.7889C16.8812 73.2992 16.2962 73.5415 15.786 73.3301C15.2757 73.1188 15.0334 72.5338 15.2448 72.0236L18.6889 63.7087ZM86.1066 51.0638C86.1066 55.6657 85.2002 60.2225 83.4391 64.474L81.5913 63.7087C83.2519 59.6998 84.1066 55.403 84.1066 51.0638H86.1066ZM83.4391 64.474C81.6781 68.7256 79.0968 72.5887 75.8428 75.8427L74.4286 74.4284C77.4969 71.3602 79.9308 67.7176 81.5913 63.7087L83.4391 64.474ZM75.8428 75.8427C72.5888 79.0967 68.7258 81.6779 64.4742 83.4389L63.7088 81.5912C67.7178 79.9306 71.3603 77.4967 74.4286 74.4284L75.8428 75.8427ZM64.4742 83.4389C60.2227 85.2 55.6659 86.1064 51.064 86.1064V84.1064C55.4032 84.1064 59.6999 83.2517 63.7088 81.5912L64.4742 83.4389ZM51.064 86.1064C46.4622 86.1064 41.9054 85.2 37.6538 83.4389L38.4192 81.5912C42.4281 83.2517 46.7248 84.1064 51.064 84.1064V86.1064ZM37.6538 83.4389C33.4022 81.6779 29.5392 79.0967 26.2852 75.8427L27.6994 74.4284C30.7677 77.4967 34.4103 79.9306 38.4192 81.5912L37.6538 83.4389ZM26.2852 75.8427C23.0312 72.5887 20.45 68.7256 18.6889 64.474L20.5367 63.7087C22.1972 67.7176 24.6311 71.3602 27.6994 74.4284L26.2852 75.8427Z" fill="url(#paint1_linear_111_332)"/>
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
    <p>{val2}</p>
      <p>{str(val2)}</p>
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
<g id="&#206;&#173;&#207;&#131;&#206;&#191;&#206;&#180;&#206;&#177; &#206;&#177;&#206;&#189;&#206;&#177; &#206;&#181;&#207;&#129;&#206;&#179;&#206;&#177;&#206;&#182;&#207;&#140;&#206;&#188;&#206;&#181;&#206;&#189;&#206;&#191;">
<circle id="Ellipse 33" cx="16" cy="16" r="16" fill="url(#paint0_linear_111_338)"/>
<g id="Camada 2">
<g id="Camada 1">
<path id="Vector" d="M23.6667 13.6667H22.6667V12.6667C22.6667 12.5783 22.6315 12.4935 22.569 12.431C22.5065 12.3685 22.4217 12.3333 22.3333 12.3333H21.3333V11.3333C21.3333 11.2449 21.2982 11.1601 21.2357 11.0976C21.1732 11.0351 21.0884 11 21 11H8.33333C8.24493 11 8.16014 11.0351 8.09763 11.0976C8.03512 11.1601 8 11.2449 8 11.3333V17.94C8 18.0284 8.03512 18.1132 8.09763 18.1757C8.16014 18.2382 8.24493 18.2733 8.33333 18.2733H9.33333V19.2733C9.33333 19.3617 9.36845 19.4465 9.43096 19.509C9.49348 19.5715 9.57826 19.6067 9.66667 19.6067H10.6667V20.6067C10.6667 20.6951 10.7018 20.7799 10.7643 20.8424C10.8268 20.9049 10.9116 20.94 11 20.94H23.6667C23.7551 20.94 23.8399 20.9049 23.9024 20.8424C23.9649 20.7799 24 20.6951 24 20.6067V14C24 13.9116 23.9649 13.8268 23.9024 13.7643C23.8399 13.7018 23.7551 13.6667 23.6667 13.6667ZM18.5333 17.6067H10.8C10.7263 17.0668 10.4779 16.566 10.0926 16.1807C9.70735 15.7955 9.2065 15.547 8.66667 15.4733V13.8C9.2065 13.7263 9.70735 13.4779 10.0926 13.0926C10.4779 12.7074 10.7263 12.2065 10.8 11.6667H18.5333C18.607 12.2065 18.8555 12.7074 19.2407 13.0926C19.626 13.4779 20.1268 13.7263 20.6667 13.8V15.4733C20.1268 15.547 19.626 15.7955 19.2407 16.1807C18.8555 16.566 18.607 17.0668 18.5333 17.6067ZM20.6667 16.14V17.6067H19.1933C19.2624 17.2422 19.4401 16.9071 19.703 16.6453C19.9659 16.3836 20.3019 16.2074 20.6667 16.14ZM20.6667 11.6667V13.14C20.3009 13.0721 19.9644 12.895 19.7014 12.632C19.4383 12.369 19.2612 12.0324 19.1933 11.6667H20.6667ZM8.66667 11.6667H10.14C10.0721 12.0324 9.89499 12.369 9.63197 12.632C9.36895 12.895 9.03239 13.0721 8.66667 13.14V11.6667ZM8.66667 16.14C9.03148 16.2074 9.36739 16.3836 9.63031 16.6453C9.89324 16.9071 10.0709 17.2422 10.14 17.6067H8.66667V16.14ZM10 18.28H21C21.0884 18.28 21.1732 18.2449 21.2357 18.1824C21.2982 18.1199 21.3333 18.0351 21.3333 17.9467V13H22V18.94H10V18.28ZM23.3333 20.28H11.3333V19.6133H22.3333C22.4217 19.6133 22.5065 19.5782 22.569 19.5157C22.6315 19.4532 22.6667 19.3684 22.6667 19.28V14.3333H23.3333V20.28Z" fill="white"/>
<path id="Vector_2" d="M14.6667 12.3733C14.2198 12.3733 13.7828 12.5059 13.4112 12.7542C13.0395 13.0025 12.7498 13.3555 12.5788 13.7685C12.4077 14.1814 12.363 14.6358 12.4502 15.0742C12.5374 15.5126 12.7526 15.9153 13.0687 16.2314C13.3847 16.5475 13.7874 16.7627 14.2258 16.8499C14.6642 16.9371 15.1186 16.8924 15.5316 16.7213C15.9446 16.5502 16.2975 16.2606 16.5459 15.8889C16.7942 15.5173 16.9267 15.0803 16.9267 14.6333C16.925 14.0345 16.6863 13.4607 16.2629 13.0372C15.8394 12.6138 15.2656 12.3751 14.6667 12.3733ZM14.6667 16.2267C14.3516 16.2267 14.0436 16.1332 13.7815 15.9581C13.5195 15.7831 13.3153 15.5342 13.1947 15.2431C13.0741 14.9519 13.0425 14.6316 13.104 14.3225C13.1655 14.0134 13.3173 13.7295 13.5401 13.5067C13.7629 13.2838 14.0468 13.1321 14.3559 13.0706C14.665 13.0091 14.9853 13.0407 15.2765 13.1613C15.5676 13.2819 15.8165 13.4861 15.9915 13.7481C16.1666 14.0101 16.2601 14.3182 16.2601 14.6333C16.261 14.8431 16.2204 15.051 16.1407 15.2451C16.061 15.4392 15.9438 15.6156 15.7958 15.7643C15.6477 15.913 15.4718 16.0309 15.278 16.1114C15.0843 16.1919 14.8765 16.2333 14.6667 16.2333V16.2267Z" fill="white"/>
</g>
</g>
</g>
<defs>
<linearGradient id="paint0_linear_111_338" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
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
                animateCounter3test2("counter", 0, """+str(val1)+""", 1000,10);  // Increase from 0 to 100 in 1 second
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
<g id="&#206;&#145;&#207;&#129;&#206;&#185;&#206;&#184;&#206;&#188;&#206;&#191;&#206;&#180;&#206;&#181;&#206;&#175;&#206;&#186;&#207;&#132;&#206;&#183;&#207;&#130;" clip-path="url(#clip0_111_384)">
<circle id="Ellipse 34" cx="16" cy="16" r="16" fill="url(#paint0_linear_111_384)"/>
<path id="Arrow 1" d="M11.7025 24.5475C11.8668 24.7118 12.1332 24.7118 12.2975 24.5475L14.975 21.87C15.1393 21.7057 15.1393 21.4393 14.975 21.275C14.8107 21.1107 14.5443 21.1107 14.38 21.275L12 23.655L9.61998 21.275C9.45568 21.1107 9.18928 21.1107 9.02498 21.275C8.86067 21.4393 8.86067 21.7057 9.02498 21.87L11.7025 24.5475ZM11.5793 9.52439L11.5793 24.25H12.4207L12.4207 9.52439H11.5793Z" fill="white"/>
<path id="Arrow 2" d="M19.0292 6.7025C18.8649 6.53819 18.5985 6.53819 18.4342 6.7025L15.7567 9.38002C15.5924 9.54432 15.5924 9.81071 15.7567 9.97502C15.921 10.1393 16.1874 10.1393 16.3517 9.97502L18.7317 7.595L21.1117 9.97502C21.276 10.1393 21.5424 10.1393 21.7067 9.97502C21.871 9.81071 21.871 9.54432 21.7067 9.38002L19.0292 6.7025ZM19.1524 24.25L19.1524 7L18.311 7L18.311 24.25L19.1524 24.25Z" fill="white"/>
</g>
<defs>
<linearGradient id="paint0_linear_111_384" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
<stop stop-color="#548CEE"/>
<stop offset="1" stop-color="#15E7FF"/>
</linearGradient>
<clipPath id="clip0_111_384">
<rect width="32" height="32" fill="white"/>
</clipPath>
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
<path d="M32 16C32 24.8366 24.8366 32 16 32C7.16344 32 0 24.8366 0 16C0 7.16344 7.16344 0 16 0C24.8366 0 32 7.16344 32 16Z" fill="url(#paint0_linear_111_385)"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M21.8833 6.05604C21.976 6.05948 22.0483 6.13738 22.0449 6.23004L21.989 7.74005C21.9855 7.83272 21.9076 7.90505 21.815 7.90162C21.7223 7.89819 21.65 7.82029 21.6534 7.72763L21.6943 6.62267L17.242 10.757H11.5247L7.20473 14.0801L7 13.8139L11.4105 10.4212H17.1101L21.4658 6.3766L20.3609 6.33568C20.2682 6.33224 20.1959 6.25435 20.1993 6.16168C20.2027 6.06902 20.2806 5.99669 20.3733 6.00012L21.8833 6.05604Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M7.44696 16.9349C7.3512 17.0158 7.32561 17.0815 7.32561 17.1274C7.32561 17.1732 7.3512 17.239 7.44696 17.3198C7.54197 17.4001 7.6891 17.4796 7.88516 17.5497C8.27585 17.6892 8.8263 17.7786 9.44211 17.7786C10.0579 17.7786 10.6084 17.6892 10.9991 17.5497C11.1951 17.4796 11.3422 17.4001 11.4372 17.3198C11.533 17.239 11.5586 17.1732 11.5586 17.1274C11.5586 17.0815 11.533 17.0158 11.4372 16.9349C11.3422 16.8547 11.1951 16.7751 10.9991 16.7051C10.6084 16.5655 10.0579 16.4761 9.44211 16.4761C8.8263 16.4761 8.27585 16.5655 7.88516 16.7051C7.6891 16.7751 7.54197 16.8547 7.44696 16.9349ZM7.77564 16.3984C8.20989 16.2433 8.79908 16.1505 9.44211 16.1505C10.0851 16.1505 10.6743 16.2433 11.1086 16.3984C11.325 16.4757 11.5116 16.5716 11.6473 16.6861C11.7822 16.8 11.8842 16.9485 11.8842 17.1274C11.8842 17.3063 11.7822 17.4547 11.6473 17.5686C11.5116 17.6832 11.325 17.779 11.1086 17.8563C10.6743 18.0114 10.0851 18.1042 9.44211 18.1042C8.79908 18.1042 8.20989 18.0114 7.77564 17.8563C7.55923 17.779 7.37256 17.6832 7.23689 17.5686C7.10197 17.4547 7 17.3063 7 17.1274C7 16.9485 7.10197 16.8 7.23689 16.6861C7.37256 16.5716 7.55923 16.4757 7.77564 16.3984Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M7.16281 17.4326C7.25272 17.4326 7.32561 17.5055 7.32561 17.5954V18.5714C7.32561 18.6173 7.35121 18.684 7.44693 18.7648C7.54191 18.845 7.689 18.9246 7.88503 18.9946C8.27568 19.1341 8.82613 19.2235 9.44211 19.2235C10.0581 19.2235 10.6085 19.1341 10.9992 18.9946C11.1952 18.9246 11.3423 18.845 11.4373 18.7648C11.533 18.684 11.5586 18.6182 11.5586 18.5723V17.5963C11.5586 17.5064 11.6315 17.4326 11.7214 17.4326C11.8113 17.4326 11.8842 17.5055 11.8842 17.5954V18.5714C11.8842 18.7503 11.7823 18.8996 11.6474 19.0136C11.5117 19.1281 11.3251 19.224 11.1087 19.3012C10.6745 19.4563 10.0853 19.5491 9.44211 19.5491C8.79893 19.5491 8.20973 19.4563 7.77552 19.3012C7.55912 19.224 7.37248 19.1281 7.23683 19.0136C7.10192 18.8996 7 18.7512 7 18.5723V17.5963C7 17.5064 7.07289 17.4326 7.16281 17.4326Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M7.16281 18.8775C7.25272 18.8775 7.32561 18.9504 7.32561 19.0403V20.0163C7.32561 20.0623 7.35121 20.1289 7.44693 20.2097C7.54191 20.2899 7.689 20.3695 7.88503 20.4395C8.27568 20.579 8.82613 20.6684 9.44211 20.6684C10.0581 20.6684 10.6085 20.579 10.9992 20.4395C11.1952 20.3695 11.3423 20.2899 11.4373 20.2097C11.533 20.1289 11.5586 20.0631 11.5586 20.0172V19.0412C11.5586 18.9513 11.6315 18.8775 11.7214 18.8775C11.8113 18.8775 11.8842 18.9504 11.8842 19.0403V20.0163C11.8842 20.1952 11.7823 20.3445 11.6474 20.4585C11.5117 20.573 11.3251 20.6689 11.1087 20.7462C10.6745 20.9012 10.0853 20.994 9.44211 20.994C8.79893 20.994 8.20973 20.9012 7.77552 20.7462C7.55912 20.6689 7.37248 20.573 7.23683 20.4585C7.10192 20.3445 7 20.1961 7 20.0172V19.0412C7 18.9513 7.07289 18.8775 7.16281 18.8775Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M7.16281 20.3225C7.25272 20.3225 7.32561 20.3953 7.32561 20.4853V21.4612C7.32561 21.5072 7.35121 21.5738 7.44693 21.6546C7.54191 21.7348 7.689 21.8144 7.88503 21.8844C8.27568 22.0239 8.82613 22.1133 9.44211 22.1133C10.0581 22.1133 10.6085 22.0239 10.9992 21.8844C11.1952 21.8144 11.3423 21.7348 11.4373 21.6546C11.533 21.5738 11.5586 21.508 11.5586 21.4621V20.4861C11.5586 20.3962 11.6315 20.3225 11.7214 20.3225C11.8113 20.3225 11.8842 20.3953 11.8842 20.4853V21.4612C11.8842 21.6401 11.7823 21.7894 11.6474 21.9034C11.5117 22.018 11.3251 22.1138 11.1087 22.1911C10.6745 22.3462 10.0853 22.4389 9.44211 22.4389C8.79893 22.4389 8.20973 22.3462 7.77552 22.1911C7.55912 22.1138 7.37248 22.018 7.23683 21.9034C7.10192 21.7894 7 21.641 7 21.4621V20.4861C7 20.3962 7.07289 20.3225 7.16281 20.3225Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M13.6743 14.0451C13.5785 14.1259 13.5529 14.1917 13.5529 14.2375C13.5529 14.2834 13.5785 14.3491 13.6743 14.43C13.7693 14.5102 13.9164 14.5898 14.1125 14.6598C14.5031 14.7994 15.0536 14.8888 15.6694 14.8888C16.2852 14.8888 16.8357 14.7994 17.2263 14.6598C17.4224 14.5898 17.5695 14.5102 17.6645 14.43C17.7603 14.3491 17.7859 14.2834 17.7859 14.2375C17.7859 14.1917 17.7603 14.1259 17.6645 14.0451C17.5695 13.9649 17.4224 13.8853 17.2263 13.8153C16.8357 13.6757 16.2852 13.5863 15.6694 13.5863C15.0536 13.5863 14.5031 13.6757 14.1125 13.8153C13.9164 13.8853 13.7693 13.9649 13.6743 14.0451ZM14.0029 13.5086C14.4372 13.3535 15.0264 13.2607 15.6694 13.2607C16.3124 13.2607 16.9016 13.3535 17.3359 13.5086C17.5523 13.5859 17.7389 13.6817 17.8746 13.7963C18.0095 13.9102 18.1115 14.0586 18.1115 14.2375C18.1115 14.4164 18.0095 14.5649 17.8746 14.6788C17.7389 14.7933 17.5523 14.8892 17.3359 14.9665C16.9016 15.1216 16.3124 15.2144 15.6694 15.2144C15.0264 15.2144 14.4372 15.1216 14.0029 14.9665C13.7865 14.8892 13.5999 14.7933 13.4642 14.6788C13.3293 14.5649 13.2273 14.4164 13.2273 14.2375C13.2273 14.0586 13.3293 13.9102 13.4642 13.7963C13.5999 13.6817 13.7865 13.5859 14.0029 13.5086Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M13.3901 14.5428C13.48 14.5428 13.5529 14.6157 13.5529 14.7056V15.6816C13.5529 15.7275 13.5785 15.7941 13.6742 15.875C13.7692 15.9552 13.9163 16.0348 14.1123 16.1048C14.503 16.2443 15.0534 16.3337 15.6694 16.3337C16.2854 16.3337 16.8358 16.2443 17.2265 16.1048C17.4225 16.0348 17.5696 15.9552 17.6646 15.875C17.7603 15.7941 17.7859 15.7284 17.7859 15.6825V14.7065C17.7859 14.6166 17.8588 14.5428 17.9487 14.5428C18.0386 14.5428 18.1115 14.6157 18.1115 14.7056V15.6816C18.1115 15.8605 18.0096 16.0098 17.8747 16.1237C17.739 16.2383 17.5524 16.3341 17.336 16.4114C16.9018 16.5665 16.3126 16.6593 15.6694 16.6593C15.0262 16.6593 14.437 16.5665 14.0028 16.4114C13.7864 16.3341 13.5998 16.2383 13.4641 16.1237C13.3292 16.0098 13.2273 15.8613 13.2273 15.6825V14.7065C13.2273 14.6166 13.3002 14.5428 13.3901 14.5428Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M13.3901 15.9877C13.48 15.9877 13.5529 16.0606 13.5529 16.1505V17.1265C13.5529 17.1724 13.5785 17.239 13.6742 17.3199C13.7692 17.4001 13.9163 17.4797 14.1123 17.5497C14.503 17.6892 15.0534 17.7786 15.6694 17.7786C16.2854 17.7786 16.8358 17.6892 17.2265 17.5497C17.4225 17.4797 17.5696 17.4001 17.6646 17.3199C17.7603 17.239 17.7859 17.1733 17.7859 17.1274V16.1514C17.7859 16.0615 17.8588 15.9877 17.9487 15.9877C18.0386 15.9877 18.1115 16.0606 18.1115 16.1505V17.1265C18.1115 17.3054 18.0096 17.4547 17.8747 17.5686C17.739 17.6832 17.5524 17.779 17.336 17.8563C16.9018 18.0114 16.3126 18.1042 15.6694 18.1042C15.0262 18.1042 14.437 18.0114 14.0028 17.8563C13.7864 17.779 13.5998 17.6832 13.4641 17.5686C13.3292 17.4547 13.2273 17.3063 13.2273 17.1274V16.1514C13.2273 16.0615 13.3002 15.9877 13.3901 15.9877Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M13.3901 17.4326C13.48 17.4326 13.5529 17.5055 13.5529 17.5954V18.5714C13.5529 18.6173 13.5785 18.684 13.6742 18.7648C13.7692 18.845 13.9163 18.9246 14.1123 18.9946C14.503 19.1341 15.0534 19.2235 15.6694 19.2235C16.2854 19.2235 16.8358 19.1341 17.2265 18.9946C17.4225 18.9246 17.5696 18.845 17.6646 18.7648C17.7603 18.684 17.7859 18.6182 17.7859 18.5723V17.5963C17.7859 17.5064 17.8588 17.4326 17.9487 17.4326C18.0386 17.4326 18.1115 17.5055 18.1115 17.5954V18.5714C18.1115 18.7503 18.0096 18.8996 17.8747 19.0136C17.739 19.1281 17.5524 19.224 17.336 19.3012C16.9018 19.4563 16.3126 19.5491 15.6694 19.5491C15.0262 19.5491 14.437 19.4563 14.0028 19.3012C13.7864 19.224 13.5998 19.1281 13.4641 19.0136C13.3292 18.8996 13.2273 18.7512 13.2273 18.5723V17.5963C13.2273 17.5064 13.3002 17.4326 13.3901 17.4326Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M13.3901 18.8775C13.48 18.8775 13.5529 18.9504 13.5529 19.0403V20.0163C13.5529 20.0623 13.5785 20.1289 13.6742 20.2097C13.7692 20.2899 13.9163 20.3695 14.1123 20.4395C14.503 20.579 15.0534 20.6684 15.6694 20.6684C16.2854 20.6684 16.8358 20.579 17.2265 20.4395C17.4225 20.3695 17.5696 20.2899 17.6646 20.2097C17.7603 20.1289 17.7859 20.0631 17.7859 20.0172V19.0412C17.7859 18.9513 17.8588 18.8775 17.9487 18.8775C18.0386 18.8775 18.1115 18.9504 18.1115 19.0403V20.0163C18.1115 20.1952 18.0096 20.3445 17.8747 20.4585C17.739 20.573 17.5524 20.6689 17.336 20.7462C16.9018 20.9012 16.3126 20.994 15.6694 20.994C15.0262 20.994 14.437 20.9012 14.0028 20.7462C13.7864 20.6689 13.5998 20.573 13.4641 20.4585C13.3292 20.3445 13.2273 20.1961 13.2273 20.0172V19.0412C13.2273 18.9513 13.3002 18.8775 13.3901 18.8775Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M13.3901 20.3225C13.48 20.3225 13.5529 20.3953 13.5529 20.4853V21.4612C13.5529 21.5072 13.5785 21.5738 13.6742 21.6546C13.7692 21.7348 13.9163 21.8144 14.1123 21.8844C14.503 22.0239 15.0534 22.1133 15.6694 22.1133C16.2854 22.1133 16.8358 22.0239 17.2265 21.8844C17.4225 21.8144 17.5696 21.7348 17.6646 21.6546C17.7603 21.5738 17.7859 21.508 17.7859 21.4621V20.4861C17.7859 20.3962 17.8588 20.3225 17.9487 20.3225C18.0386 20.3225 18.1115 20.3953 18.1115 20.4853V21.4612C18.1115 21.6401 18.0096 21.7894 17.8747 21.9034C17.739 22.018 17.5524 22.1138 17.336 22.1911C16.9018 22.3462 16.3126 22.4389 15.6694 22.4389C15.0262 22.4389 14.437 22.3462 14.0028 22.1911C13.7864 22.1138 13.5998 22.018 13.4641 21.9034C13.3292 21.7894 13.2273 21.641 13.2273 21.4621V20.4861C13.2273 20.3962 13.3002 20.3225 13.3901 20.3225Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M19.9018 11.1553C19.806 11.2361 19.7804 11.3018 19.7804 11.3477C19.7804 11.3936 19.806 11.4593 19.9018 11.5402C19.9968 11.6204 20.1439 11.7 20.34 11.77C20.7307 11.9095 21.2811 11.999 21.8969 11.999C22.5127 11.999 23.0632 11.9095 23.4539 11.77C23.6499 11.7 23.7971 11.6204 23.8921 11.5402C23.9878 11.4593 24.0134 11.3936 24.0134 11.3477C24.0134 11.3018 23.9878 11.2361 23.8921 11.1553C23.7971 11.075 23.6499 10.9955 23.4539 10.9254C23.0632 10.7859 22.5127 10.6965 21.8969 10.6965C21.2811 10.6965 20.7307 10.7859 20.34 10.9254C20.1439 10.9955 19.9968 11.075 19.9018 11.1553ZM20.2305 10.6188C20.6647 10.4637 21.2539 10.3709 21.8969 10.3709C22.54 10.3709 23.1292 10.4637 23.5634 10.6188C23.7798 10.6961 23.9665 10.7919 24.1022 10.9065C24.2371 11.0204 24.339 11.1688 24.339 11.3477C24.339 11.5266 24.2371 11.6751 24.1022 11.789C23.9665 11.9035 23.7798 11.9994 23.5634 12.0767C23.1292 12.2317 22.54 12.3246 21.8969 12.3246C21.2539 12.3246 20.6647 12.2317 20.2305 12.0767C20.0141 11.9994 19.8274 11.9035 19.6917 11.789C19.5568 11.6751 19.4548 11.5266 19.4548 11.3477C19.4548 11.1688 19.5568 11.0204 19.6917 10.9065C19.8274 10.7919 20.0141 10.6961 20.2305 10.6188Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M19.6176 11.653C19.7076 11.653 19.7804 11.7259 19.7804 11.8158V12.7918C19.7804 12.8377 19.806 12.9043 19.9018 12.9852C19.9967 13.0654 20.1438 13.1449 20.3399 13.215C20.7305 13.3545 21.281 13.4439 21.8969 13.4439C22.5129 13.4439 23.0634 13.3545 23.454 13.215C23.65 13.1449 23.7971 13.0654 23.8921 12.9852C23.9878 12.9043 24.0134 12.8386 24.0134 12.7926V11.8167C24.0134 11.7268 24.0863 11.653 24.1762 11.653C24.2662 11.653 24.339 11.7259 24.339 11.8158V12.7918C24.339 12.9707 24.2371 13.12 24.1022 13.2339C23.9666 13.3485 23.7799 13.4443 23.5635 13.5216C23.1293 13.6767 22.5401 13.7695 21.8969 13.7695C21.2538 13.7695 20.6646 13.6767 20.2304 13.5216C20.014 13.4443 19.8273 13.3485 19.6917 13.2339C19.5568 13.12 19.4548 12.9715 19.4548 12.7926V11.8167C19.4548 11.7268 19.5277 11.653 19.6176 11.653Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M19.6176 13.0979C19.7076 13.0979 19.7804 13.1708 19.7804 13.2607V14.2367C19.7804 14.2826 19.806 14.3492 19.9018 14.4301C19.9967 14.5103 20.1438 14.5899 20.3399 14.6599C20.7305 14.7994 21.281 14.8888 21.8969 14.8888C22.5129 14.8888 23.0634 14.7994 23.454 14.6599C23.65 14.5899 23.7971 14.5103 23.8921 14.4301C23.9878 14.3492 24.0134 14.2835 24.0134 14.2375V13.2616C24.0134 13.1717 24.0863 13.0979 24.1762 13.0979C24.2662 13.0979 24.339 13.1708 24.339 13.2607V14.2367C24.339 14.4156 24.2371 14.5649 24.1022 14.6788C23.9666 14.7934 23.7799 14.8892 23.5635 14.9665C23.1293 15.1216 22.5401 15.2144 21.8969 15.2144C21.2538 15.2144 20.6646 15.1216 20.2304 14.9665C20.014 14.8892 19.8273 14.7934 19.6917 14.6788C19.5568 14.5649 19.4548 14.4164 19.4548 14.2375V13.2616C19.4548 13.1717 19.5277 13.0979 19.6176 13.0979Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M19.6176 14.5428C19.7076 14.5428 19.7804 14.6157 19.7804 14.7056V15.6816C19.7804 15.7275 19.806 15.7941 19.9018 15.875C19.9967 15.9552 20.1438 16.0348 20.3399 16.1048C20.7305 16.2443 21.281 16.3337 21.8969 16.3337C22.5129 16.3337 23.0634 16.2443 23.454 16.1048C23.65 16.0348 23.7971 15.9552 23.8921 15.875C23.9878 15.7941 24.0134 15.7284 24.0134 15.6825V14.7065C24.0134 14.6166 24.0863 14.5428 24.1762 14.5428C24.2662 14.5428 24.339 14.6157 24.339 14.7056V15.6816C24.339 15.8605 24.2371 16.0098 24.1022 16.1237C23.9666 16.2383 23.7799 16.3341 23.5635 16.4114C23.1293 16.5665 22.5401 16.6593 21.8969 16.6593C21.2538 16.6593 20.6646 16.5665 20.2304 16.4114C20.014 16.3341 19.8273 16.2383 19.6917 16.1237C19.5568 16.0098 19.4548 15.8614 19.4548 15.6825V14.7065C19.4548 14.6166 19.5277 14.5428 19.6176 14.5428Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M19.6176 15.9877C19.7076 15.9877 19.7804 16.0606 19.7804 16.1505V17.1265C19.7804 17.1724 19.806 17.239 19.9018 17.3199C19.9967 17.4001 20.1438 17.4797 20.3399 17.5497C20.7305 17.6892 21.281 17.7786 21.8969 17.7786C22.5129 17.7786 23.0634 17.6892 23.454 17.5497C23.65 17.4797 23.7971 17.4001 23.8921 17.3199C23.9878 17.239 24.0134 17.1733 24.0134 17.1274V16.1514C24.0134 16.0615 24.0863 15.9877 24.1762 15.9877C24.2662 15.9877 24.339 16.0606 24.339 16.1505V17.1265C24.339 17.3054 24.2371 17.4547 24.1022 17.5686C23.9666 17.6832 23.7799 17.779 23.5635 17.8563C23.1293 18.0114 22.5401 18.1042 21.8969 18.1042C21.2538 18.1042 20.6646 18.0114 20.2304 17.8563C20.014 17.779 19.8273 17.6832 19.6917 17.5686C19.5568 17.4547 19.4548 17.3063 19.4548 17.1274V16.1514C19.4548 16.0615 19.5277 15.9877 19.6176 15.9877Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M19.6176 17.4326C19.7076 17.4326 19.7804 17.5055 19.7804 17.5954V18.5714C19.7804 18.6173 19.806 18.684 19.9018 18.7648C19.9967 18.845 20.1438 18.9246 20.3399 18.9946C20.7305 19.1341 21.281 19.2235 21.8969 19.2235C22.5129 19.2235 23.0634 19.1341 23.454 18.9946C23.65 18.9246 23.7971 18.845 23.8921 18.7648C23.9878 18.684 24.0134 18.6182 24.0134 18.5723V17.5963C24.0134 17.5064 24.0863 17.4326 24.1762 17.4326C24.2662 17.4326 24.339 17.5055 24.339 17.5954V18.5714C24.339 18.7503 24.2371 18.8996 24.1022 19.0136C23.9666 19.1281 23.7799 19.224 23.5635 19.3012C23.1293 19.4563 22.5401 19.5491 21.8969 19.5491C21.2538 19.5491 20.6646 19.4563 20.2304 19.3012C20.014 19.224 19.8273 19.1281 19.6917 19.0136C19.5568 18.8996 19.4548 18.7512 19.4548 18.5723V17.5963C19.4548 17.5064 19.5277 17.4326 19.6176 17.4326Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M19.6176 18.8775C19.7076 18.8775 19.7804 18.9504 19.7804 19.0404V20.0163C19.7804 20.0623 19.806 20.1289 19.9018 20.2097C19.9967 20.2899 20.1438 20.3695 20.3399 20.4395C20.7305 20.579 21.281 20.6684 21.8969 20.6684C22.5129 20.6684 23.0634 20.579 23.454 20.4395C23.65 20.3695 23.7971 20.2899 23.8921 20.2097C23.9878 20.1289 24.0134 20.0631 24.0134 20.0172V19.0412C24.0134 18.9513 24.0863 18.8775 24.1762 18.8775C24.2662 18.8775 24.339 18.9504 24.339 19.0404V20.0163C24.339 20.1952 24.2371 20.3445 24.1022 20.4585C23.9666 20.573 23.7799 20.6689 23.5635 20.7462C23.1293 20.9012 22.5401 20.994 21.8969 20.994C21.2538 20.994 20.6646 20.9012 20.2304 20.7462C20.014 20.6689 19.8273 20.573 19.6917 20.4585C19.5568 20.3445 19.4548 20.1961 19.4548 20.0172V19.0412C19.4548 18.9513 19.5277 18.8775 19.6176 18.8775Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M19.6176 20.3225C19.7076 20.3225 19.7804 20.3953 19.7804 20.4853V21.4612C19.7804 21.5072 19.806 21.5738 19.9018 21.6546C19.9967 21.7348 20.1438 21.8144 20.3399 21.8844C20.7305 22.0239 21.281 22.1133 21.8969 22.1133C22.5129 22.1133 23.0634 22.0239 23.454 21.8844C23.65 21.8144 23.7971 21.7348 23.8921 21.6546C23.9878 21.5738 24.0134 21.508 24.0134 21.4621V20.4861C24.0134 20.3962 24.0863 20.3225 24.1762 20.3225C24.2662 20.3225 24.339 20.3953 24.339 20.4853V21.4612C24.339 21.6401 24.2371 21.7894 24.1022 21.9034C23.9666 22.018 23.7799 22.1138 23.5635 22.1911C23.1293 22.3462 22.5401 22.4389 21.8969 22.4389C21.2538 22.4389 20.6646 22.3462 20.2304 22.1911C20.014 22.1138 19.8273 22.018 19.6917 21.9034C19.5568 21.7894 19.4548 21.641 19.4548 21.4621V20.4861C19.4548 20.3962 19.5277 20.3225 19.6176 20.3225Z" fill="white"/>
<defs>
<linearGradient id="paint0_linear_111_385" x1="3.94207" y1="2.06489" x2="41.1102" y2="42.7996" gradientUnits="userSpaceOnUse">
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
                animateCounter3test2("counter", 0, """+str(val4)+""", 1000,10);  // Increase from 0 to 100 in 1 second
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
    
