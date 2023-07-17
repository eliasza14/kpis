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
        col1, col2 = st.columns(2)
        with col1:
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
        with col2:
            #st.write('D19')
            #st.write(kpdf['D19'][kpdf['year']==str(year_filter)])
            text=str(kpdf['D19'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('D19 Ετησιες μοναδες εργασιας: '+text)
           # st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας(Μέσος Όρος)</h3>", unsafe_allow_html=True)

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
                                <div style="text-align:center; color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 30px; word-wrap: break-word">Μεσος Όρος</div>
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

    html(f""" 
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
"> <p>
<svg width="100" height="100" viewBox="0 0 97 97" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="48.5" cy="48.5" r="48.5" fill="white"/>
<path d="M49.5474 75.9102C45.4515 75.9102 42.0635 75.1517 39.3835 73.6347C36.7035 72.1177 34.6808 69.9939 33.3155 67.2633C32.0008 64.4822 31.3435 61.2207 31.3435 57.4787V42.9156C31.3435 39.1231 32.0008 35.8616 33.3155 33.131C34.6303 30.3499 36.6276 28.2008 39.3077 26.6838C42.0383 25.1668 45.4515 24.4083 49.5474 24.4083C53.5927 24.4083 56.9553 25.0909 59.6354 26.4562C62.366 27.771 64.3886 29.5914 65.7033 31.9174C67.0181 34.2435 67.5996 36.9235 67.4479 39.9575C67.4479 40.5137 67.1951 40.7918 66.6894 40.7918H59.4837C58.9274 40.7918 58.6493 40.4884 58.6493 39.8816C58.6493 38.4658 58.3459 37.1763 57.7391 36.0133C57.1323 34.8503 56.1716 33.9401 54.8568 33.2827C53.5421 32.5748 51.7723 32.2208 49.5474 32.2208C46.3111 32.2208 43.9345 33.1563 42.4175 35.0272C40.9005 36.8476 40.142 39.5024 40.142 42.9915V57.1753C40.142 60.7656 40.9005 63.4961 42.4175 65.3671C43.9345 67.1875 46.3364 68.0977 49.6232 68.0977C52.7583 68.0977 55.0338 67.415 56.4497 66.0497C57.9161 64.6339 58.6493 62.7124 58.6493 60.2852C58.6493 59.6784 58.9527 59.375 59.5595 59.375H66.6135C67.1698 59.375 67.4479 59.6784 67.4479 60.2852C67.5996 63.4203 66.9675 66.1762 65.5516 68.5528C64.1863 70.8788 62.1384 72.6992 59.4078 74.014C56.6772 75.2781 53.3904 75.9102 49.5474 75.9102ZM25.9581 58.9199C25.503 58.9199 25.3261 58.6418 25.4272 58.0855L26.3374 54.0655C26.4385 53.6104 26.7166 53.3829 27.1717 53.3829H51.8987C52.4549 53.3829 52.6572 53.661 52.5055 54.2172L51.5953 58.2372C51.5447 58.6923 51.2666 58.9199 50.761 58.9199H25.9581ZM26.3374 49.1353C25.8317 49.1353 25.6547 48.8572 25.8064 48.3009L26.6408 44.3568C26.7419 43.9017 27.02 43.6741 27.4751 43.6741H53.6432C54.1489 43.6741 54.3512 43.9269 54.25 44.4326L53.4157 48.4526C53.3651 48.9077 53.087 49.1353 52.5814 49.1353H26.3374Z" fill="url(#paint0_linear_100_418)"/>
<defs>
<linearGradient id="paint0_linear_100_418" x1="29.0363" y1="26.3555" x2="89.6567" y2="88.9601" gradientUnits="userSpaceOnUse">
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
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px; display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
                            <div style="text-align:right;">
                 

<svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="&#206;&#163;&#207;&#133;&#206;&#189;&#206;&#181;&#207;&#132;&#206;&#177;&#206;&#185;&#207;&#129;&#206;&#185;&#207;&#131;&#207;&#132;&#206;&#173;&#207;&#130;">
<rect width="56" height="56" rx="5" fill="white"/>
<circle id="Ellipse 24" cx="28" cy="28" r="28" fill="url(#paint0_linear_93_809)"/>
<g id="Group 1">
<path id="Vector" d="M23.5938 20.4511C22.467 20.4511 22.1204 20.4819 21.9446 20.5083C21.6486 20.5522 21.3922 20.7376 21.2559 21.0043L17.6718 28.0501C17.5018 28.3835 17.5494 28.7864 17.7919 29.0714C18.0256 29.3469 18.0879 29.4143 18.1561 29.4861C18.192 29.5235 18.2323 29.5667 18.4447 29.8165C18.4586 29.8319 18.4718 29.8473 18.4865 29.862C18.5019 29.8781 18.5165 29.8927 18.5319 29.9089C18.5568 29.8664 18.5832 29.8253 18.6118 29.7858C18.655 29.7279 18.7099 29.6759 18.77 29.629C18.7751 29.618 18.7788 29.607 18.7839 29.596C18.8294 29.522 18.8755 29.448 18.9209 29.374C18.981 29.3 19.0492 29.237 19.1246 29.1843C18.7026 28.689 18.9568 29.0106 18.4982 28.4707L22.0823 21.4248C22.3146 21.3904 22.9073 21.3786 23.5938 21.3786C23.7857 21.3786 23.9857 21.3794 24.1865 21.3808C24.2378 21.3237 24.2949 21.2717 24.3565 21.227C24.4275 20.8995 24.673 20.5837 24.9829 20.4628C24.5272 20.4562 24.04 20.4511 23.5938 20.4511Z" fill="#467EE0"/>
<path id="Vector_2" d="M38.4812 31.3112C38.4065 30.6371 38.0006 30.2349 37.7017 29.9902C37.4833 29.8114 37.2709 29.6239 37.0467 29.4253C36.9434 29.3345 36.8408 29.2436 36.7375 29.1535C36.5697 29.0077 36.4019 28.8619 36.2342 28.7169C35.9323 28.4546 35.6312 28.193 35.3301 27.93C35.1367 27.7608 34.944 27.5901 34.7513 27.4201C34.5432 27.2369 34.3285 27.0472 34.1153 26.8611C33.9673 26.7321 33.8179 26.6046 33.6736 26.4816C33.5483 26.3753 33.4193 26.2654 33.2955 26.1577C32.9321 25.842 32.5629 25.5196 32.2068 25.2075L31.9907 25.0185C31.6258 24.6998 31.2617 24.3803 30.8968 24.0602C30.8221 23.9942 30.3385 23.5444 29.7099 22.9568C29.6777 22.9905 29.644 23.022 29.6088 23.0506C29.252 23.337 28.8183 23.2828 28.471 23.0667C29.3158 23.8579 30.1722 24.6573 30.2858 24.7569C30.6506 25.0771 31.0155 25.3972 31.3804 25.7167C31.8163 26.0976 32.2508 26.4786 32.6874 26.8574C32.9585 27.0933 33.2347 27.3234 33.5058 27.5593C33.9117 27.9139 34.3139 28.2729 34.7198 28.6275C35.1887 29.0378 35.659 29.4444 36.1287 29.8532C36.4569 30.1389 36.7785 30.432 37.1148 30.7075C37.3456 30.8972 37.5251 31.1031 37.5603 31.4137C37.5837 31.6233 37.5866 31.8277 37.4687 32.0079C37.3485 32.1918 37.1983 32.3479 37.0159 32.4783C36.8642 32.5874 36.6408 32.6439 36.4159 32.6439C36.1814 32.6439 35.944 32.5823 35.7821 32.4526C35.4576 32.1925 35.1095 31.9618 34.7711 31.7207C34.2765 31.3683 33.7805 31.0188 33.2867 30.6664C32.7101 30.2547 32.135 29.8407 31.5591 29.4283C31.165 29.1462 30.7679 28.8678 30.3766 28.5813C30.2228 28.4685 30.0623 28.3894 29.8696 28.3645C29.8455 28.3615 29.822 28.3601 29.7986 28.3601C29.5202 28.3601 29.3062 28.5777 29.3341 28.8649C29.3553 29.0832 29.4652 29.2517 29.6374 29.377C30.0704 29.6913 30.5078 30.0012 30.9437 30.3126C31.3115 30.5749 31.6822 30.8357 32.0493 31.0994C32.6039 31.498 33.1548 31.9002 33.7095 32.2988C34.1293 32.5999 34.5505 32.9003 34.974 33.1955C35.385 33.4827 35.4209 33.9121 35.2444 34.285C35.0846 34.622 34.8048 34.7795 34.5058 34.7795C34.3366 34.7795 34.1615 34.729 33.9981 34.6323C33.5124 34.3429 33.0684 33.9817 32.6054 33.6534C32.009 33.23 31.4111 32.808 30.8148 32.3838C30.2558 31.9867 29.6967 31.5903 29.1429 31.1874C29.0132 31.0928 28.8813 31.0401 28.7267 31.0401C28.7055 31.0401 28.6842 31.0408 28.6622 31.043C28.4219 31.065 28.2893 31.158 28.2227 31.3749C28.1552 31.594 28.2219 31.8123 28.4007 31.942C29.2777 32.5794 30.1546 33.2161 31.0324 33.852C31.576 34.2469 32.1233 34.6367 32.6632 35.0367C32.8391 35.1664 32.9226 35.3591 32.9365 35.5774C32.9526 35.8236 32.8632 36.036 32.7116 36.2228C32.5306 36.447 32.3006 36.5657 32.0581 36.5657C31.9071 36.5657 31.7511 36.5196 31.5987 36.4243C31.3613 36.2763 31.1364 36.1078 30.9078 35.9459C30.6638 35.7745 30.4235 35.5972 30.1796 35.4265C29.8257 35.1796 29.4682 34.9392 29.115 34.6916C28.6322 34.3531 28.1538 34.0095 27.6702 33.671C27.5677 33.5992 27.471 33.5641 27.3779 33.5641C27.2548 33.5641 27.1398 33.6263 27.0299 33.7487C26.8401 33.959 26.8438 34.2659 27.0438 34.4235C27.2893 34.6169 27.5391 34.8044 27.7889 34.9913C28.4014 35.4506 29.0154 35.9078 29.6279 36.3672C29.7473 36.4566 29.7656 36.5445 29.7033 36.6815C29.5326 37.0647 29.1963 37.2486 28.8329 37.2486C28.7282 37.2486 28.6212 37.2332 28.5157 37.2031C28.2967 37.1409 28.101 36.9973 27.8944 36.8925C27.8842 36.8866 27.8226 36.8397 27.7274 36.765C27.7288 36.7738 27.731 36.7811 27.7325 36.7899C27.7728 37.0588 27.6673 37.3269 27.5105 37.5387C27.4754 37.5856 27.4329 37.6288 27.386 37.6684C27.4211 37.6911 27.4431 37.7028 27.4732 37.7182C27.5178 37.7409 27.5699 37.7709 27.6263 37.8032C27.7941 37.9006 28.0021 38.0215 28.2622 38.0955C28.4505 38.149 28.6425 38.1761 28.8329 38.1761C29.5839 38.1761 30.2426 37.7482 30.5495 37.0603C30.5774 36.9995 30.5994 36.9386 30.6169 36.8778C30.773 36.9892 30.9335 37.1028 31.1078 37.2112C31.4031 37.3951 31.7313 37.4925 32.0581 37.4925C32.5863 37.4925 33.0742 37.2486 33.4325 36.806C33.7263 36.4434 33.875 36.0243 33.8655 35.5913C34.0736 35.6675 34.2897 35.7063 34.5058 35.7063C35.1887 35.7063 35.7785 35.3232 36.0825 34.6814C36.2576 34.3099 36.3082 33.9238 36.2444 33.5648C36.3008 33.5692 36.3587 33.5707 36.4159 33.5707C36.8459 33.5707 37.2503 33.4505 37.5559 33.2322C37.8299 33.0366 38.0614 32.7955 38.2438 32.5164C38.5259 32.0856 38.5193 31.646 38.4812 31.3112Z" fill="#467EE0"/>
<path id="Vector_3" d="M28.8034 19.1477C28.3162 19.1477 27.8356 19.2136 27.3572 19.3118C26.7059 19.4459 26.0948 19.5536 25.5234 19.8928C25.464 19.9272 24.0603 20.5595 23.1701 21.5537C22.9701 21.9069 22.773 22.2622 22.5789 22.6183C22.5466 22.6769 22.5246 22.7465 22.5173 22.8124C22.477 23.1839 22.4463 23.556 22.4045 23.9275C22.3686 24.2521 22.3561 24.5847 22.2719 24.8975C22.1774 25.2485 22.0221 25.5847 21.8785 25.921C21.7839 26.1445 21.7825 26.3577 21.9026 26.5621C22.1254 26.9416 22.4697 27.146 22.9005 27.1907C23.0185 27.2032 23.1364 27.209 23.2544 27.209C23.5679 27.209 23.8786 27.1651 24.179 27.0676C24.5746 26.9409 24.9153 26.7057 25.2164 26.4192C25.5234 26.1276 25.7776 25.795 25.9688 25.4162C26.1168 25.1239 26.2223 24.8191 26.2765 24.4931C26.3073 24.3092 26.3146 24.1121 26.448 23.9575C26.5029 23.8953 26.5483 23.8264 26.6033 23.7634C26.8429 23.4894 27.1425 23.2945 27.4971 23.2395C27.6158 23.2212 27.7352 23.2124 27.8547 23.2124C28.1279 23.2124 28.4005 23.2608 28.6642 23.3597C28.802 23.411 28.9353 23.4674 29.0401 23.5817C29.2181 23.7736 29.3998 23.9641 29.591 24.1429C29.8167 24.3546 30.0533 24.5532 30.2856 24.7569C30.6504 25.077 31.0153 25.3972 31.3802 25.7166C31.8161 26.0976 32.2505 26.4786 32.6872 26.8574C32.9583 27.0933 33.2345 27.3233 33.5056 27.5592C33.9115 27.9138 34.3137 28.2728 34.7196 28.6274C35.1885 29.0377 35.6588 29.4443 36.1285 29.8532C36.4567 30.1389 36.7783 30.4319 37.1146 30.7074C37.1227 30.7148 37.1322 30.7177 37.1432 30.7177C37.2604 30.7177 37.5285 30.3389 37.8429 29.892C38.0993 29.5271 38.3711 29.0253 38.5491 28.6157C38.5726 28.5615 38.5755 28.478 38.5513 28.4252C38.3557 27.9966 38.1528 27.5717 37.9491 27.1468C37.6289 26.4756 37.3058 25.8067 36.9849 25.1364C36.6523 24.4404 36.3211 23.7436 35.9893 23.0469C35.7834 22.6139 35.5775 22.1801 35.3694 21.7479C35.1284 21.2467 34.8859 20.7456 34.6434 20.2452C34.6097 20.1749 34.5621 20.1463 34.4763 20.1404C34.003 20.1075 33.5276 20.0826 33.0587 20.0174C32.7363 19.9727 32.4213 19.8723 32.1062 19.7873C31.6615 19.6679 31.2212 19.5338 30.7757 19.4166C30.1859 19.2613 29.5844 19.1704 28.9756 19.1506C28.9177 19.1484 28.8606 19.1477 28.8034 19.1477ZM28.8034 20.013C28.8518 20.013 28.8994 20.0137 28.947 20.0152C29.4797 20.0327 30.0211 20.1126 30.5552 20.254C30.7853 20.3141 31.0226 20.3815 31.2512 20.4467C31.4564 20.5053 31.6688 20.5661 31.8813 20.6233C31.9458 20.6401 32.0102 20.6584 32.0747 20.6767C32.3473 20.7522 32.6286 20.8306 32.9392 20.8746C33.3107 20.9258 33.6785 20.9537 34.0367 20.9779L34.0704 21.0475C34.2441 21.4057 34.417 21.764 34.5892 22.1223C34.7503 22.4571 34.9093 22.7919 35.069 23.1267L35.2082 23.419C35.3247 23.6637 35.4412 23.9085 35.5577 24.1524C35.7724 24.6052 35.9878 25.0572 36.2046 25.51C36.3651 25.8463 36.527 26.1826 36.6889 26.5189C36.8486 26.8522 37.0091 27.1863 37.1688 27.5197C37.3249 27.8457 37.4846 28.1805 37.6414 28.5183C37.4882 28.8326 37.3014 29.1571 37.1344 29.3945C37.1095 29.4304 37.0816 29.4707 37.0516 29.5125C37.0362 29.4993 37.0208 29.4854 37.0054 29.4714C36.9029 29.3806 36.8003 29.2905 36.697 29.2004C36.5292 29.0546 36.3614 28.9088 36.1937 28.763C35.8918 28.5014 35.59 28.2391 35.2888 27.9761C35.0954 27.8069 34.9027 27.6369 34.71 27.4662C34.502 27.283 34.2873 27.094 34.0741 26.9079C33.9268 26.779 33.7774 26.6515 33.6331 26.5284C33.5078 26.4222 33.3796 26.3123 33.2543 26.2046C32.8909 25.8881 32.5216 25.565 32.1641 25.2529L31.9502 25.0653C31.5853 24.7459 31.2204 24.4264 30.8563 24.107C30.7889 24.0477 30.7215 23.989 30.6541 23.9304C30.4885 23.7868 30.3325 23.652 30.183 23.5121C29.9947 23.3355 29.813 23.1421 29.6753 22.9941C29.4211 22.7194 29.1148 22.6043 28.9676 22.5494C28.61 22.4153 28.2356 22.3472 27.8547 22.3472C27.692 22.3472 27.5279 22.3596 27.366 22.3845C26.8319 22.4659 26.3432 22.7465 25.9512 23.1949C25.9044 23.2483 25.867 23.2982 25.8362 23.3377C25.8208 23.3582 25.8032 23.3809 25.7952 23.3905C25.5168 23.7121 25.4648 24.0674 25.434 24.2792C25.4303 24.3033 25.4274 24.3275 25.423 24.351C25.3849 24.5788 25.3109 24.8001 25.1966 25.0265C25.0559 25.3049 24.8625 25.562 24.6208 25.7921C24.3797 26.0207 24.1482 26.1687 23.9137 26.2441C23.7086 26.3101 23.4866 26.3438 23.2544 26.3438C23.1679 26.3438 23.0785 26.3394 22.9891 26.3299C22.8426 26.3152 22.7598 26.2676 22.7012 26.1987C22.7151 26.1665 22.7283 26.1342 22.7422 26.1027C22.8749 25.795 23.0119 25.4771 23.1078 25.1217C23.1899 24.8169 23.217 24.5173 23.2419 24.2535C23.2492 24.1729 23.2566 24.0975 23.2646 24.0235C23.2866 23.8235 23.3064 23.6235 23.3247 23.43C23.3394 23.2798 23.3547 23.1253 23.3709 22.9743C23.532 22.6769 23.7013 22.3721 23.8749 22.0651C24.3255 21.5867 25.0244 21.1024 25.8545 20.6943C25.9014 20.6716 25.93 20.657 25.9652 20.6364C26.3689 20.3969 26.8414 20.3002 27.388 20.1888L27.5316 20.1595C28.018 20.0591 28.4217 20.013 28.8034 20.013Z" fill="#467EE0"/>
<g id="Clip path group">
<mask id="mask0_93_809" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="16" y="28" width="13" height="11">
<g id="1278aba829">
<path id="Vector_4" d="M16.7192 28.5007H28.4006V38.7278H16.7192V28.5007Z" fill="white"/>
</g>
</mask>
<g mask="url(#mask0_93_809)">
<g id="Group">
<path id="Vector_5" d="M24.8291 36.1701C24.8459 36.1701 24.8635 36.1715 24.8811 36.1737C25.0269 36.1913 25.1536 36.2814 25.2181 36.4133C25.284 36.5496 25.276 36.6668 25.2731 36.7115C25.2709 36.7716 25.2657 36.828 25.2613 36.8822C25.254 36.9665 25.2467 37.0529 25.2562 37.1035C25.2884 37.2786 25.3917 37.4361 25.569 37.5863C25.8152 37.7943 26.0343 37.8779 26.2797 37.8603C26.3537 37.8544 26.4131 37.8273 26.4805 37.7687C26.7244 37.5548 27.3626 36.7884 27.4835 36.5635C27.5157 36.5034 27.5472 36.4148 27.5025 36.258C27.4087 35.9239 27.1941 35.6946 26.8482 35.5554C26.5427 35.4338 26.3955 35.4924 26.2922 35.5664C26.1801 35.6462 26.0672 35.6514 26.0284 35.6521C25.9009 35.6638 25.7749 35.6184 25.6848 35.5283C25.5918 35.436 25.5456 35.3063 25.5588 35.1759L25.5595 35.1671C25.561 35.126 25.5639 35.0491 25.5983 34.9627C25.6658 34.7934 25.7097 34.5495 25.4577 34.167C25.2591 33.8659 24.991 33.682 24.6371 33.6036C24.3931 33.5501 24.2034 33.5787 24.0217 33.6981C23.9946 33.7164 23.9653 33.734 23.9272 33.756L23.8744 33.7875C23.7169 33.882 23.5162 33.8666 23.3755 33.7487C23.2341 33.6314 23.1821 33.4373 23.2465 33.2651C23.4392 32.7479 23.3279 32.35 22.8861 31.9742C22.4377 31.5932 22.0274 31.5449 21.5541 31.8167C21.3812 31.9163 21.1629 31.8841 21.0252 31.7397C20.8882 31.5954 20.8669 31.3749 20.9746 31.2071C21.3329 30.651 21.2926 30.1887 20.8501 29.7528C20.4112 29.3205 19.9592 29.2568 19.4295 29.5543C18.9034 30.1484 18.7481 30.3353 18.6807 30.4159L18.6499 30.4525C18.5591 30.5602 18.4697 30.6693 18.3796 30.7792C18.2286 30.9631 18.0726 31.1536 17.9085 31.3375C17.7026 31.5668 17.6052 31.7669 17.592 31.9859C17.5707 32.3339 17.6814 32.6255 17.9305 32.8783C18.1334 33.0834 18.3759 33.2021 18.6741 33.2409C18.8902 33.2695 19.0866 33.2285 19.2756 33.1171C19.3181 33.0922 19.3642 33.0585 19.4221 33.016C19.4558 32.9911 19.4917 32.9655 19.5313 32.9376C19.6793 32.8336 19.8756 32.8329 20.0251 32.9354C20.1738 33.038 20.2434 33.2219 20.1995 33.3977C20.1958 33.4102 20.1936 33.4212 20.1921 33.4292C20.1841 33.4659 20.1724 33.5208 20.1423 33.5831C20.0515 33.7684 20.05 33.9655 20.1365 34.1846C20.3086 34.6205 20.6075 34.8931 21.0501 35.0176C21.379 35.1107 21.623 35.0726 21.8399 34.8953C21.8706 34.8704 21.8977 34.852 21.9263 34.833C21.9388 34.8242 21.9527 34.8147 21.9703 34.8029C22.1146 34.7033 22.3051 34.7004 22.4516 34.7956C22.5989 34.8909 22.6736 35.0652 22.6421 35.2381C22.6384 35.2572 22.6363 35.274 22.6341 35.2887C22.626 35.3392 22.6172 35.4023 22.5879 35.4741C22.5373 35.5986 22.5469 35.7378 22.6223 35.9693C22.7498 36.362 23.2282 36.787 23.7374 36.795C24.0122 36.7972 24.1909 36.7181 24.3338 36.5232C24.3748 36.4675 24.4173 36.4184 24.4547 36.3752C24.4686 36.3584 24.4825 36.3422 24.4972 36.3254C24.58 36.2265 24.7016 36.1701 24.8291 36.1701ZM26.213 38.7277C25.7874 38.7277 25.3932 38.5702 25.0115 38.2471C24.7543 38.0303 24.5734 37.7826 24.473 37.5079C24.2539 37.6134 24.0034 37.6647 23.7242 37.6603C22.9 37.6478 22.0545 37.0229 21.7988 36.2367C21.7659 36.1342 21.7336 36.0199 21.7131 35.8968C21.4369 35.9569 21.1365 35.9415 20.8149 35.8506C20.1152 35.6536 19.6024 35.1876 19.332 34.5033C19.2741 34.3575 19.2368 34.211 19.2192 34.0659C19.0082 34.1172 18.7884 34.1282 18.562 34.0989C18.0726 34.0351 17.6528 33.8285 17.315 33.4856C16.8952 33.06 16.6923 32.5229 16.7282 31.9332C16.7538 31.5178 16.9289 31.1346 17.263 30.7602C17.4154 30.5902 17.559 30.4159 17.7107 30.2298C17.8037 30.1177 17.896 30.0048 17.9898 29.8935L18.0162 29.862C18.0946 29.7682 18.2565 29.574 18.8272 28.9293C18.8565 28.8963 18.8902 28.8678 18.9276 28.8451C19.8214 28.3058 20.7204 28.4099 21.4574 29.1367C21.9446 29.6165 22.1461 30.1873 22.0567 30.7792C22.5359 30.7595 23.0048 30.9397 23.4466 31.3148C23.9235 31.7207 24.1777 32.1999 24.2012 32.7274C24.399 32.7002 24.6078 32.7105 24.8239 32.7589C25.3998 32.8863 25.8562 33.1992 26.1793 33.6901C26.3845 34.0007 26.4958 34.3121 26.5134 34.6198C26.72 34.6161 26.9398 34.6601 27.1699 34.7524C27.7655 34.9905 28.1685 35.4301 28.3355 36.0235C28.4315 36.3635 28.4015 36.6837 28.2454 36.9731C28.0483 37.3401 27.3259 38.1783 27.0497 38.42C26.8424 38.6017 26.605 38.7036 26.3435 38.7233C26.3002 38.7263 26.2563 38.7277 26.213 38.7277Z" fill="#467EE0"/>
</g>
</g>
</g>
<path id="Vector_6" d="M19.7957 33.7238C19.6983 33.7238 19.6001 33.6915 19.5188 33.6241C19.3356 33.471 19.3107 33.1977 19.4631 33.0146L21.0082 31.1602C21.1614 30.9771 21.4346 30.9522 21.6178 31.1053C21.801 31.2577 21.8259 31.531 21.6735 31.7141L20.1283 33.5685C20.0426 33.671 19.9195 33.7238 19.7957 33.7238Z" fill="#467EE0"/>
<path id="Vector_7" d="M22.206 35.5781C22.1108 35.5781 22.0155 35.5473 21.9357 35.4836C21.7496 35.3341 21.7188 35.0616 21.8683 34.8755L23.3519 33.0212C23.5006 32.8343 23.7731 32.8043 23.9592 32.9537C24.1461 33.1032 24.1768 33.375 24.0274 33.5618L22.5438 35.4162C22.458 35.5224 22.3328 35.5781 22.206 35.5781Z" fill="#467EE0"/>
<path id="Vector_8" d="M24.7394 37.1232C24.6457 37.1232 24.5512 37.0932 24.4713 37.0302C24.2845 36.8814 24.2522 36.6096 24.401 36.4221L25.5754 34.9392C25.7234 34.7516 25.9959 34.7201 26.1828 34.8681C26.3703 35.0169 26.4018 35.2887 26.2538 35.4762L25.0794 36.9591C24.9937 37.0668 24.8677 37.1232 24.7394 37.1232Z" fill="#467EE0"/>
<path id="Vector_9" d="M19.6791 18.5301C19.5846 18.5301 19.5553 18.5594 19.5143 18.6422C19.3553 18.9653 19.1861 19.3045 18.997 19.6796C18.6659 20.3339 18.334 20.9882 18.0006 21.6417C17.9017 21.8358 17.8021 22.03 17.7025 22.2234C17.5757 22.4688 17.449 22.7143 17.3244 22.9604C17.2497 23.1092 17.1764 23.2586 17.1039 23.4088C17.0328 23.5554 16.9617 23.7012 16.8885 23.8462C16.6767 24.2668 16.4599 24.6917 16.2496 25.1027L16.1514 25.2947C16.0606 25.4712 15.9705 25.6478 15.8796 25.8244C15.7507 26.0749 15.6217 26.3255 15.4935 26.5768C15.4129 26.7365 15.3331 26.8962 15.2532 27.0567C15.1345 27.2941 15.0122 27.5402 14.8862 27.782C14.8437 27.8648 14.8656 27.9871 14.9308 28.0289C15.081 28.1234 15.2444 28.2062 15.4173 28.2941L15.6921 28.4348C16.076 28.6311 16.4723 28.8341 16.8643 29.0209C16.9156 29.0451 16.9911 29.059 17.057 29.0561C17.0958 29.0546 17.1493 29.0524 17.2292 28.8883C17.4731 28.3894 17.7266 27.886 17.9728 27.3996L18.1516 27.0435C18.4336 26.4837 18.7157 25.9247 19 25.3665C19.1853 25.0016 19.3714 24.6375 19.5575 24.2733C19.7956 23.8059 20.0345 23.3385 20.2719 22.8703C20.4272 22.5641 20.581 22.2578 20.7342 21.9509C20.8587 21.7032 20.9825 21.4556 21.1078 21.208C21.3298 20.7676 21.5664 20.3002 21.8031 19.8438C21.8624 19.7287 21.8632 19.5815 21.7313 19.5097C21.6221 19.4511 21.5115 19.3954 21.3943 19.3368C21.3371 19.3082 21.28 19.2796 21.2236 19.251C21.1129 19.1946 21.0023 19.1375 20.8917 19.0811C20.6374 18.9507 20.3752 18.8159 20.1158 18.6884C20.0718 18.6671 20.0279 18.6437 19.9847 18.6195C19.9158 18.5829 19.8125 18.5272 19.7788 18.5301L19.7465 18.5331L19.7136 18.5309C19.7011 18.5301 19.6894 18.5301 19.6791 18.5301ZM17.0409 29.9213C16.8489 29.9213 16.657 29.8796 16.4936 29.8019C16.0892 29.61 15.6869 29.4041 15.2979 29.2048L15.0254 29.0656C14.8429 28.9726 14.6539 28.8766 14.47 28.7608C14.026 28.4817 13.8692 27.8633 14.1183 27.3827C14.2407 27.1475 14.3616 26.905 14.4788 26.6706C14.5594 26.5087 14.64 26.3467 14.722 26.1856C14.8503 25.9328 14.9799 25.6808 15.1096 25.428C15.2005 25.2522 15.2906 25.0763 15.3807 24.9005L15.4789 24.7085C15.6891 24.2983 15.9053 23.8748 16.1155 23.4572C16.1873 23.3158 16.2562 23.1729 16.3258 23.0308C16.3991 22.8799 16.4745 22.7238 16.5529 22.5699C16.6782 22.3216 16.8057 22.0739 16.9332 21.827C17.0321 21.6344 17.1317 21.4417 17.2299 21.249C17.5625 20.5962 17.8937 19.9427 18.2248 19.2891C18.4124 18.917 18.5802 18.5807 18.7377 18.2605C18.934 17.8605 19.2864 17.6502 19.7334 17.6656C20.011 17.6509 20.233 17.7704 20.3964 17.859C20.4294 17.8766 20.4631 17.8949 20.4968 17.911C20.7627 18.0422 21.0294 18.1792 21.2873 18.3118C21.3972 18.3682 21.5064 18.4239 21.6163 18.4796C21.6712 18.5081 21.7262 18.5353 21.7811 18.5631C21.8991 18.6224 22.0214 18.6832 22.143 18.7492C22.6779 19.0386 22.8625 19.6804 22.5716 20.2416C22.3372 20.6951 22.1108 21.142 21.88 21.5985C21.7555 21.8446 21.6316 22.0923 21.5078 22.3392C21.354 22.6469 21.1994 22.9546 21.0433 23.2616C20.806 23.7305 20.5671 24.1986 20.3283 24.6668C20.1422 25.0309 19.9568 25.3943 19.7715 25.7592C19.4879 26.316 19.2058 26.8743 18.9245 27.4325L18.745 27.7893C18.501 28.2729 18.2483 28.774 18.0065 29.2685C17.7523 29.788 17.3676 29.9103 17.09 29.9206C17.0731 29.9213 17.057 29.9213 17.0409 29.9213Z" fill="#467EE0"/>
<g id="Clip path group_2">
<mask id="mask1_93_809" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="33" y="17" width="9" height="13">
<g id="5437f3b491">
<path id="Vector_10" d="M33.4683 17.5H41.9999V29.8605H33.4683V17.5Z" fill="white"/>
</g>
</mask>
<g mask="url(#mask1_93_809)">
<g id="Group_2">
<path id="Vector_11" d="M36.4149 18.3814C36.1446 18.5037 35.8698 18.6341 35.6039 18.7609L35.3723 18.8708C35.2698 18.9191 35.1679 18.9682 35.0661 19.0173C34.8698 19.1118 34.6668 19.2093 34.4631 19.3023C34.3796 19.3397 34.3203 19.4833 34.3386 19.5368C34.3737 19.6408 34.4265 19.7492 34.4822 19.8643L34.4961 19.8921C34.6104 20.128 34.7254 20.3639 34.8397 20.5998C35.0009 20.9281 35.1606 21.257 35.3189 21.5867C35.4134 21.7845 35.5064 21.986 35.5958 22.1802C35.6786 22.3597 35.7607 22.5384 35.8456 22.7165C35.9585 22.9546 36.0742 23.1912 36.1892 23.4279C36.2969 23.6484 36.4046 23.8696 36.5101 24.0909C36.6464 24.3752 36.7805 24.6602 36.9146 24.9444C37.0267 25.1833 37.1395 25.4221 37.2531 25.661C37.497 26.1724 37.7417 26.6837 37.9864 27.1959L38.4568 28.1798C38.5718 28.4201 38.6868 28.6604 38.8011 28.9007C38.8202 28.9366 38.9162 28.9791 38.9579 28.9711C39.1697 28.8949 39.3594 28.8187 39.5331 28.7381C39.9807 28.5307 40.3492 28.3534 40.6914 28.1805C40.8298 28.1102 40.9881 28.0245 41.1075 27.9241C41.1412 27.8963 41.1405 27.815 41.1229 27.7769C40.8914 27.2838 40.6525 26.7841 40.4218 26.2998L40.232 25.9013C39.9162 25.239 39.6005 24.5759 39.2832 23.9136C39.1528 23.6396 39.0209 23.3663 38.8898 23.093C38.7447 22.7912 38.5997 22.4901 38.4553 22.1882C38.2363 21.7303 38.0187 21.2717 37.8011 20.813L37.4377 20.0489C37.1996 19.547 36.9607 19.0452 36.7241 18.5426C36.6501 18.3843 36.5966 18.3653 36.5365 18.3645C36.5153 18.3682 36.4926 18.3711 36.4706 18.3733C36.4523 18.3755 36.4281 18.3784 36.4149 18.3814ZM38.9506 29.8363C38.574 29.8363 38.1828 29.6151 38.0201 29.2729C37.9058 29.0333 37.7908 28.793 37.6758 28.5535L37.2054 27.5688C36.9607 27.0574 36.716 26.5453 36.4721 26.0324C36.3578 25.7928 36.2449 25.5533 36.1314 25.313C35.998 25.0302 35.8647 24.7466 35.7299 24.4638C35.6244 24.2448 35.5181 24.0257 35.4112 23.8066C35.2954 23.5678 35.1782 23.3289 35.0639 23.0886C34.9775 22.9069 34.8939 22.7245 34.8097 22.5421C34.7218 22.3501 34.6309 22.1523 34.5386 21.9604C34.3818 21.6329 34.2221 21.3061 34.0624 20.9793C33.9473 20.7427 33.8316 20.5061 33.7173 20.2687L33.7034 20.2408C33.6389 20.1075 33.5722 19.9698 33.5195 19.8159C33.3546 19.3302 33.6221 18.7345 34.1041 18.5147C34.2998 18.4253 34.499 18.3301 34.691 18.237C34.795 18.188 34.8983 18.1381 35.0024 18.089L35.2317 17.9799C35.505 17.8495 35.7878 17.7154 36.0698 17.5879C36.1812 17.5374 36.2867 17.5249 36.3636 17.5147C36.3819 17.5125 36.4003 17.5103 36.4178 17.5073L36.4515 17.5007L36.486 17.5C36.8025 17.4905 37.2369 17.6004 37.5073 18.174C37.7432 18.6759 37.9813 19.177 38.2194 19.6774L38.5828 20.4423C38.7997 20.9002 39.0173 21.3574 39.2356 21.8153C39.3799 22.1164 39.5243 22.4175 39.6693 22.7179C39.8012 22.9919 39.9331 23.2659 40.0642 23.5399C40.3807 24.203 40.6972 24.866 41.013 25.5291L41.2028 25.9276C41.4343 26.4119 41.6731 26.9138 41.9061 27.4091C42.0687 27.7563 42.038 28.2729 41.6636 28.5872C41.4768 28.7439 41.2643 28.8597 41.0819 28.952C40.7302 29.1301 40.3536 29.3118 39.8964 29.5235C39.6986 29.6151 39.4862 29.7015 39.2444 29.7872C39.1506 29.8209 39.051 29.8363 38.9506 29.8363Z" fill="#467EE0"/>
</g>
</g>
</g>
</g>
</g>
<defs>
<linearGradient id="paint0_linear_93_809" x1="6.89862" y1="3.61356" x2="71.9428" y2="74.8993" gradientUnits="userSpaceOnUse">
<stop stop-color="#C7D7F4" stop-opacity="0.56"/>
<stop offset="1" stop-color="#60EFFF" stop-opacity="0.55"/>
</linearGradient>
</defs>
</svg>


                            </div>
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Κτηρίων & Εξ. Χώρων</div>
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
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px;  display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
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
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εστίασης</div>
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
            f"""
                <body>
                    <div style="display:flex; justify-content: center; " >
                        <div style="width:310px; display: flex;align-items: flex-start;flex-direction: column;flex-wrap: nowrap;border: 1px solid #6E7279;border-radius: 16px;padding-top: 12px; padding-bottom: 12px; padding-left:24px; padding-right:24px;">
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
                            <div id="counter" style="text-align: left; color:black;font-family:'Source Sans Pro',sans-serif;font-weight: bold; font-size: 45px;"></div>
                            <div>
                                <div style="text-align:center; color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Λοιπές Δραστηρίοτητες</div>
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
    
