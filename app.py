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
            html(
                f"""
                    <div class="Component3" style="width: 290px; height: 183px; padding-bottom: 24px; padding-left: 24px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); border-radius: 15px; justify-content: space-between; align-items: flex-end; gap: 24px; display: inline-flex">
                <div class="Rectangle19" style="width: 329px; height: 210px; left: 0px; top: 0px; position: absolute; border-radius: 15px"></div>
                <div style="width: 56px; height: 56px; left: 256px; top: 19px; position: absolute">
                    <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">

                <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
                <path id="Vector" d="M42.0002 27.3717C41.9987 26.1341 41.6395 24.9233 40.9659 23.8849C40.2924 22.8466 39.3331 22.025 38.2036 21.519V21.2022C38.2024 19.998 37.8029 18.8279 37.0674 17.8743C36.3319 16.9208 35.3016 16.2372 34.1371 15.9303C32.9726 15.6233 31.7393 15.7101 30.6293 16.1772C29.5193 16.6443 28.5949 17.4654 28.0002 18.5126C27.4055 17.4654 26.4811 16.6443 25.3711 16.1772C24.2611 15.7101 23.0278 15.6233 21.8633 15.9303C20.6988 16.2372 19.6685 16.9208 18.933 17.8743C18.1975 18.8279 17.798 19.998 17.7968 21.2022V21.519C16.6664 22.0233 15.7063 22.8442 15.0325 23.8826C14.3588 24.9209 14.0002 26.1322 14.0002 27.37C14.0002 28.6077 14.3588 29.819 15.0325 30.8573C15.7063 31.8957 16.6664 32.7166 17.7968 33.2209V33.5413C17.798 34.7455 18.1975 35.9156 18.933 36.8692C19.6685 37.8227 20.6988 38.5062 21.8633 38.8132C23.0278 39.1202 24.2611 39.0334 25.3711 38.5663C26.4811 38.0992 27.4055 37.2781 28.0002 36.2309C28.5949 37.2781 29.5193 38.0992 30.6293 38.5663C31.7393 39.0334 32.9726 39.1202 34.1371 38.8132C35.3016 38.5062 36.3319 37.8227 37.0674 36.8692C37.8029 35.9156 38.2024 34.7455 38.2036 33.5413V33.2209C39.3331 32.7159 40.2925 31.895 40.9661 30.8572C41.6397 29.8194 41.9989 28.609 42.0002 27.3717ZM23.2544 37.5752C22.206 37.5757 21.1986 37.168 20.4456 36.4385C19.6926 35.709 19.2532 34.7149 19.2205 33.667C19.6116 33.7412 20.0089 33.7785 20.407 33.7785H21.3561C21.5449 33.7785 21.726 33.7035 21.8595 33.57C21.993 33.4365 22.068 33.2555 22.068 33.0667C22.068 32.8779 21.993 32.6968 21.8595 32.5633C21.726 32.4298 21.5449 32.3548 21.3561 32.3548H20.407C19.2308 32.3558 18.0921 31.9406 17.1926 31.1829C16.293 30.4251 15.6905 29.3735 15.4916 28.2143C15.2927 27.055 15.5103 25.8628 16.1059 24.8485C16.7015 23.8342 17.6367 23.0634 18.7459 22.6722C18.8848 22.6231 19.005 22.5322 19.09 22.4119C19.175 22.2917 19.2206 22.148 19.2205 22.0007V21.2022C19.2205 20.1324 19.6455 19.1063 20.402 18.3498C21.1585 17.5933 22.1846 17.1683 23.2544 17.1683C24.3243 17.1683 25.3503 17.5933 26.1068 18.3498C26.8633 19.1063 27.2883 20.1324 27.2883 21.2022V29.8692C26.7777 29.3066 26.1551 28.8571 25.4603 28.5496C24.7656 28.242 24.0142 28.0833 23.2544 28.0836C23.0656 28.0836 22.8846 28.1586 22.7511 28.2921C22.6176 28.4256 22.5426 28.6067 22.5426 28.7955C22.5426 28.9843 22.6176 29.1653 22.7511 29.2988C22.8846 29.4323 23.0656 29.5073 23.2544 29.5073C24.3243 29.5073 25.3503 29.9323 26.1068 30.6889C26.8633 31.4454 27.2883 32.4714 27.2883 33.5413C27.2883 34.6111 26.8633 35.6372 26.1068 36.3937C25.3503 37.1502 24.3243 37.5752 23.2544 37.5752ZM35.5934 32.3548H34.6443C34.4555 32.3548 34.2744 32.4298 34.1409 32.5633C34.0074 32.6968 33.9324 32.8779 33.9324 33.0667C33.9324 33.2555 34.0074 33.4365 34.1409 33.57C34.2744 33.7035 34.4555 33.7785 34.6443 33.7785H35.5934C35.9915 33.7785 36.3888 33.7412 36.7799 33.667C36.7552 34.459 36.4978 35.2262 36.0398 35.8728C35.5818 36.5195 34.9435 37.0169 34.2045 37.303C33.4656 37.5891 32.6588 37.6513 31.8847 37.4817C31.1107 37.3122 30.4037 36.9184 29.8521 36.3495C29.3005 35.7807 28.9286 35.062 28.7828 34.2831C28.6371 33.5042 28.724 32.6997 29.0327 31.9699C29.3413 31.2401 29.8581 30.6174 30.5185 30.1794C31.1789 29.7415 31.9536 29.5077 32.746 29.5073C32.9348 29.5073 33.1158 29.4323 33.2493 29.2988C33.3828 29.1653 33.4578 28.9843 33.4578 28.7955C33.4578 28.6067 33.3828 28.4256 33.2493 28.2921C33.1158 28.1586 32.9348 28.0836 32.746 28.0836C31.9862 28.0833 31.2348 28.242 30.5401 28.5496C29.8453 28.8571 29.2227 29.3066 28.7121 29.8692V21.2022C28.7121 20.1324 29.1371 19.1063 29.8936 18.3498C30.6501 17.5933 31.6761 17.1683 32.746 17.1683C33.8158 17.1683 34.8419 17.5933 35.5984 18.3498C36.3549 19.1063 36.7799 20.1324 36.7799 21.2022V22.0007C36.7798 22.148 36.8254 22.2917 36.9104 22.4119C36.9954 22.5322 37.1156 22.6231 37.2545 22.6722C38.3637 23.0634 39.2989 23.8342 39.8945 24.8485C40.4901 25.8628 40.7077 27.055 40.5088 28.2143C40.3099 29.3735 39.7074 30.4251 38.8078 31.1829C37.9083 31.9406 36.7696 32.3558 35.5934 32.3548ZM37.2545 25.948C37.2545 26.1368 37.1795 26.3179 37.046 26.4514C36.9125 26.5849 36.7314 26.6599 36.5426 26.6599H36.068C34.9982 26.6599 33.9721 26.2349 33.2156 25.4784C32.4591 24.7219 32.0341 23.6958 32.0341 22.626V22.1514C32.0341 21.9626 32.1091 21.7815 32.2426 21.648C32.3761 21.5145 32.5572 21.4395 32.746 21.4395C32.9348 21.4395 33.1158 21.5145 33.2493 21.648C33.3828 21.7815 33.4578 21.9626 33.4578 22.1514V22.626C33.4578 23.3182 33.7328 23.9821 34.2224 24.4716C34.7119 24.9611 35.3758 25.2361 36.068 25.2361H36.5426C36.7314 25.2361 36.9125 25.3111 37.046 25.4446C37.1795 25.5781 37.2545 25.7592 37.2545 25.948ZM19.9324 26.6599H19.4578C19.269 26.6599 19.0879 26.5849 18.9544 26.4514C18.8209 26.3179 18.7459 26.1368 18.7459 25.948C18.7459 25.7592 18.8209 25.5781 18.9544 25.4446C19.0879 25.3111 19.269 25.2361 19.4578 25.2361H19.9324C20.6246 25.2361 21.2886 24.9611 21.7781 24.4716C22.2676 23.9821 22.5426 23.3182 22.5426 22.626V22.1514C22.5426 21.9626 22.6176 21.7815 22.7511 21.648C22.8846 21.5145 23.0656 21.4395 23.2544 21.4395C23.4432 21.4395 23.6243 21.5145 23.7578 21.648C23.8913 21.7815 23.9663 21.9626 23.9663 22.1514V22.626C23.9663 23.6958 23.5413 24.7219 22.7848 25.4784C22.0283 26.2349 21.0022 26.6599 19.9324 26.6599Z" fill="#8E8D8D"/>

                </svg>

                    
                
                
                </div>
                <div class="Frame15" style="left: 29px; top: 115px; position: absolute; justify-content: flex-start; align-items: flex-end; gap: 24px; display: inline-flex">
                    <div id="counter" style="color: #111416; font-size: 150px; font-family:  'Source Sans Pro',sans-serif; font-weight: 700; line-height: 47.93px; word-wrap: break-word"></div>
                    <div class="Frame9" style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 0px; display: inline-flex">
                    <div style="color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
                    <div style="color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Γεν. Πληθυσμού</div>
                    </div>
                </div>
                </div>
                <script type="text/javascript">
                    {js_code}
                    animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                    </script>
                """,height = 250
            )
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

        with col2:
            
            text=kpdf['D5'][kpdf['year']==str(year_filter)].iloc[0]
            # st.write('Δ5-Εργαζόμενοι ΛΥΨΥ: '+text)
            # st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΛΥΨΥ</h3>", unsafe_allow_html=True)
            html(
                f"""
                    <div class="Component3" style="width: 290px; height: 183px; padding-bottom: 24px; padding-left: 24px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); border-radius: 15px; justify-content: space-between; align-items: flex-end; gap: 24px; display: inline-flex">
                <div class="Rectangle19" style="width: 329px; height: 210px; left: 0px; top: 0px; position: absolute; border-radius: 15px"></div>
                <div style="width: 56px; height: 56px; left: 256px; top: 19px; position: absolute">
                    <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">

                <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
                <path id="Vector" d="M42.0002 27.3717C41.9987 26.1341 41.6395 24.9233 40.9659 23.8849C40.2924 22.8466 39.3331 22.025 38.2036 21.519V21.2022C38.2024 19.998 37.8029 18.8279 37.0674 17.8743C36.3319 16.9208 35.3016 16.2372 34.1371 15.9303C32.9726 15.6233 31.7393 15.7101 30.6293 16.1772C29.5193 16.6443 28.5949 17.4654 28.0002 18.5126C27.4055 17.4654 26.4811 16.6443 25.3711 16.1772C24.2611 15.7101 23.0278 15.6233 21.8633 15.9303C20.6988 16.2372 19.6685 16.9208 18.933 17.8743C18.1975 18.8279 17.798 19.998 17.7968 21.2022V21.519C16.6664 22.0233 15.7063 22.8442 15.0325 23.8826C14.3588 24.9209 14.0002 26.1322 14.0002 27.37C14.0002 28.6077 14.3588 29.819 15.0325 30.8573C15.7063 31.8957 16.6664 32.7166 17.7968 33.2209V33.5413C17.798 34.7455 18.1975 35.9156 18.933 36.8692C19.6685 37.8227 20.6988 38.5062 21.8633 38.8132C23.0278 39.1202 24.2611 39.0334 25.3711 38.5663C26.4811 38.0992 27.4055 37.2781 28.0002 36.2309C28.5949 37.2781 29.5193 38.0992 30.6293 38.5663C31.7393 39.0334 32.9726 39.1202 34.1371 38.8132C35.3016 38.5062 36.3319 37.8227 37.0674 36.8692C37.8029 35.9156 38.2024 34.7455 38.2036 33.5413V33.2209C39.3331 32.7159 40.2925 31.895 40.9661 30.8572C41.6397 29.8194 41.9989 28.609 42.0002 27.3717ZM23.2544 37.5752C22.206 37.5757 21.1986 37.168 20.4456 36.4385C19.6926 35.709 19.2532 34.7149 19.2205 33.667C19.6116 33.7412 20.0089 33.7785 20.407 33.7785H21.3561C21.5449 33.7785 21.726 33.7035 21.8595 33.57C21.993 33.4365 22.068 33.2555 22.068 33.0667C22.068 32.8779 21.993 32.6968 21.8595 32.5633C21.726 32.4298 21.5449 32.3548 21.3561 32.3548H20.407C19.2308 32.3558 18.0921 31.9406 17.1926 31.1829C16.293 30.4251 15.6905 29.3735 15.4916 28.2143C15.2927 27.055 15.5103 25.8628 16.1059 24.8485C16.7015 23.8342 17.6367 23.0634 18.7459 22.6722C18.8848 22.6231 19.005 22.5322 19.09 22.4119C19.175 22.2917 19.2206 22.148 19.2205 22.0007V21.2022C19.2205 20.1324 19.6455 19.1063 20.402 18.3498C21.1585 17.5933 22.1846 17.1683 23.2544 17.1683C24.3243 17.1683 25.3503 17.5933 26.1068 18.3498C26.8633 19.1063 27.2883 20.1324 27.2883 21.2022V29.8692C26.7777 29.3066 26.1551 28.8571 25.4603 28.5496C24.7656 28.242 24.0142 28.0833 23.2544 28.0836C23.0656 28.0836 22.8846 28.1586 22.7511 28.2921C22.6176 28.4256 22.5426 28.6067 22.5426 28.7955C22.5426 28.9843 22.6176 29.1653 22.7511 29.2988C22.8846 29.4323 23.0656 29.5073 23.2544 29.5073C24.3243 29.5073 25.3503 29.9323 26.1068 30.6889C26.8633 31.4454 27.2883 32.4714 27.2883 33.5413C27.2883 34.6111 26.8633 35.6372 26.1068 36.3937C25.3503 37.1502 24.3243 37.5752 23.2544 37.5752ZM35.5934 32.3548H34.6443C34.4555 32.3548 34.2744 32.4298 34.1409 32.5633C34.0074 32.6968 33.9324 32.8779 33.9324 33.0667C33.9324 33.2555 34.0074 33.4365 34.1409 33.57C34.2744 33.7035 34.4555 33.7785 34.6443 33.7785H35.5934C35.9915 33.7785 36.3888 33.7412 36.7799 33.667C36.7552 34.459 36.4978 35.2262 36.0398 35.8728C35.5818 36.5195 34.9435 37.0169 34.2045 37.303C33.4656 37.5891 32.6588 37.6513 31.8847 37.4817C31.1107 37.3122 30.4037 36.9184 29.8521 36.3495C29.3005 35.7807 28.9286 35.062 28.7828 34.2831C28.6371 33.5042 28.724 32.6997 29.0327 31.9699C29.3413 31.2401 29.8581 30.6174 30.5185 30.1794C31.1789 29.7415 31.9536 29.5077 32.746 29.5073C32.9348 29.5073 33.1158 29.4323 33.2493 29.2988C33.3828 29.1653 33.4578 28.9843 33.4578 28.7955C33.4578 28.6067 33.3828 28.4256 33.2493 28.2921C33.1158 28.1586 32.9348 28.0836 32.746 28.0836C31.9862 28.0833 31.2348 28.242 30.5401 28.5496C29.8453 28.8571 29.2227 29.3066 28.7121 29.8692V21.2022C28.7121 20.1324 29.1371 19.1063 29.8936 18.3498C30.6501 17.5933 31.6761 17.1683 32.746 17.1683C33.8158 17.1683 34.8419 17.5933 35.5984 18.3498C36.3549 19.1063 36.7799 20.1324 36.7799 21.2022V22.0007C36.7798 22.148 36.8254 22.2917 36.9104 22.4119C36.9954 22.5322 37.1156 22.6231 37.2545 22.6722C38.3637 23.0634 39.2989 23.8342 39.8945 24.8485C40.4901 25.8628 40.7077 27.055 40.5088 28.2143C40.3099 29.3735 39.7074 30.4251 38.8078 31.1829C37.9083 31.9406 36.7696 32.3558 35.5934 32.3548ZM37.2545 25.948C37.2545 26.1368 37.1795 26.3179 37.046 26.4514C36.9125 26.5849 36.7314 26.6599 36.5426 26.6599H36.068C34.9982 26.6599 33.9721 26.2349 33.2156 25.4784C32.4591 24.7219 32.0341 23.6958 32.0341 22.626V22.1514C32.0341 21.9626 32.1091 21.7815 32.2426 21.648C32.3761 21.5145 32.5572 21.4395 32.746 21.4395C32.9348 21.4395 33.1158 21.5145 33.2493 21.648C33.3828 21.7815 33.4578 21.9626 33.4578 22.1514V22.626C33.4578 23.3182 33.7328 23.9821 34.2224 24.4716C34.7119 24.9611 35.3758 25.2361 36.068 25.2361H36.5426C36.7314 25.2361 36.9125 25.3111 37.046 25.4446C37.1795 25.5781 37.2545 25.7592 37.2545 25.948ZM19.9324 26.6599H19.4578C19.269 26.6599 19.0879 26.5849 18.9544 26.4514C18.8209 26.3179 18.7459 26.1368 18.7459 25.948C18.7459 25.7592 18.8209 25.5781 18.9544 25.4446C19.0879 25.3111 19.269 25.2361 19.4578 25.2361H19.9324C20.6246 25.2361 21.2886 24.9611 21.7781 24.4716C22.2676 23.9821 22.5426 23.3182 22.5426 22.626V22.1514C22.5426 21.9626 22.6176 21.7815 22.7511 21.648C22.8846 21.5145 23.0656 21.4395 23.2544 21.4395C23.4432 21.4395 23.6243 21.5145 23.7578 21.648C23.8913 21.7815 23.9663 21.9626 23.9663 22.1514V22.626C23.9663 23.6958 23.5413 24.7219 22.7848 25.4784C22.0283 26.2349 21.0022 26.6599 19.9324 26.6599Z" fill="#8E8D8D"/>

                </svg>

                    
                
                
                </div>
                <div class="Frame15" style="left: 29px; top: 115px; position: absolute; justify-content: flex-start; align-items: flex-end; gap: 24px; display: inline-flex">
                    <div id="counter" style="color: #111416; font-size: 150px; font-family:  'Source Sans Pro',sans-serif; font-weight: 700; line-height: 47.93px; word-wrap: break-word"></div>
                    <div class="Frame9" style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 0px; display: inline-flex">
                    <div style="color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
                    <div style="color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">ΛΥΨΥ</div>
                    </div>
                </div>
                </div>
                <script type="text/javascript">
                    {js_code}
                    animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                    </script>
                """,height = 250
            )
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


          
        with col3:
            #st.write('D7-Εργαζόμενοι ΕΚΟ')
            text=kpdf['D7'][kpdf['year']==str(year_filter)].iloc[0]
            # st.write('D7-Εργαζόμενοι ΕΚΟ: '+text)
            # st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΕΚΟ</h3>", unsafe_allow_html=True)
            html(
                            f"""
                                <div class="Component3" style="width: 290px; height: 183px; padding-bottom: 24px; padding-left: 24px; background: linear-gradient(138deg, rgba(198.55, 215.22, 244.37, 0.56) 0%, rgba(96, 239, 255, 0.55) 100%); border-radius: 15px; justify-content: space-between; align-items: flex-end; gap: 24px; display: inline-flex">
                            <div class="Rectangle19" style="width: 329px; height: 210px; left: 0px; top: 0px; position: absolute; border-radius: 15px"></div>
                <div style="width: 56px; height: 56px; left: 256px; top: 19px; position: absolute">
                                <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">

                            <circle id="Ellipse 24" cx="27.8947" cy="27.8947" r="27.8947" fill="white"/>
                            <path id="Vector" d="M42.0002 27.3717C41.9987 26.1341 41.6395 24.9233 40.9659 23.8849C40.2924 22.8466 39.3331 22.025 38.2036 21.519V21.2022C38.2024 19.998 37.8029 18.8279 37.0674 17.8743C36.3319 16.9208 35.3016 16.2372 34.1371 15.9303C32.9726 15.6233 31.7393 15.7101 30.6293 16.1772C29.5193 16.6443 28.5949 17.4654 28.0002 18.5126C27.4055 17.4654 26.4811 16.6443 25.3711 16.1772C24.2611 15.7101 23.0278 15.6233 21.8633 15.9303C20.6988 16.2372 19.6685 16.9208 18.933 17.8743C18.1975 18.8279 17.798 19.998 17.7968 21.2022V21.519C16.6664 22.0233 15.7063 22.8442 15.0325 23.8826C14.3588 24.9209 14.0002 26.1322 14.0002 27.37C14.0002 28.6077 14.3588 29.819 15.0325 30.8573C15.7063 31.8957 16.6664 32.7166 17.7968 33.2209V33.5413C17.798 34.7455 18.1975 35.9156 18.933 36.8692C19.6685 37.8227 20.6988 38.5062 21.8633 38.8132C23.0278 39.1202 24.2611 39.0334 25.3711 38.5663C26.4811 38.0992 27.4055 37.2781 28.0002 36.2309C28.5949 37.2781 29.5193 38.0992 30.6293 38.5663C31.7393 39.0334 32.9726 39.1202 34.1371 38.8132C35.3016 38.5062 36.3319 37.8227 37.0674 36.8692C37.8029 35.9156 38.2024 34.7455 38.2036 33.5413V33.2209C39.3331 32.7159 40.2925 31.895 40.9661 30.8572C41.6397 29.8194 41.9989 28.609 42.0002 27.3717ZM23.2544 37.5752C22.206 37.5757 21.1986 37.168 20.4456 36.4385C19.6926 35.709 19.2532 34.7149 19.2205 33.667C19.6116 33.7412 20.0089 33.7785 20.407 33.7785H21.3561C21.5449 33.7785 21.726 33.7035 21.8595 33.57C21.993 33.4365 22.068 33.2555 22.068 33.0667C22.068 32.8779 21.993 32.6968 21.8595 32.5633C21.726 32.4298 21.5449 32.3548 21.3561 32.3548H20.407C19.2308 32.3558 18.0921 31.9406 17.1926 31.1829C16.293 30.4251 15.6905 29.3735 15.4916 28.2143C15.2927 27.055 15.5103 25.8628 16.1059 24.8485C16.7015 23.8342 17.6367 23.0634 18.7459 22.6722C18.8848 22.6231 19.005 22.5322 19.09 22.4119C19.175 22.2917 19.2206 22.148 19.2205 22.0007V21.2022C19.2205 20.1324 19.6455 19.1063 20.402 18.3498C21.1585 17.5933 22.1846 17.1683 23.2544 17.1683C24.3243 17.1683 25.3503 17.5933 26.1068 18.3498C26.8633 19.1063 27.2883 20.1324 27.2883 21.2022V29.8692C26.7777 29.3066 26.1551 28.8571 25.4603 28.5496C24.7656 28.242 24.0142 28.0833 23.2544 28.0836C23.0656 28.0836 22.8846 28.1586 22.7511 28.2921C22.6176 28.4256 22.5426 28.6067 22.5426 28.7955C22.5426 28.9843 22.6176 29.1653 22.7511 29.2988C22.8846 29.4323 23.0656 29.5073 23.2544 29.5073C24.3243 29.5073 25.3503 29.9323 26.1068 30.6889C26.8633 31.4454 27.2883 32.4714 27.2883 33.5413C27.2883 34.6111 26.8633 35.6372 26.1068 36.3937C25.3503 37.1502 24.3243 37.5752 23.2544 37.5752ZM35.5934 32.3548H34.6443C34.4555 32.3548 34.2744 32.4298 34.1409 32.5633C34.0074 32.6968 33.9324 32.8779 33.9324 33.0667C33.9324 33.2555 34.0074 33.4365 34.1409 33.57C34.2744 33.7035 34.4555 33.7785 34.6443 33.7785H35.5934C35.9915 33.7785 36.3888 33.7412 36.7799 33.667C36.7552 34.459 36.4978 35.2262 36.0398 35.8728C35.5818 36.5195 34.9435 37.0169 34.2045 37.303C33.4656 37.5891 32.6588 37.6513 31.8847 37.4817C31.1107 37.3122 30.4037 36.9184 29.8521 36.3495C29.3005 35.7807 28.9286 35.062 28.7828 34.2831C28.6371 33.5042 28.724 32.6997 29.0327 31.9699C29.3413 31.2401 29.8581 30.6174 30.5185 30.1794C31.1789 29.7415 31.9536 29.5077 32.746 29.5073C32.9348 29.5073 33.1158 29.4323 33.2493 29.2988C33.3828 29.1653 33.4578 28.9843 33.4578 28.7955C33.4578 28.6067 33.3828 28.4256 33.2493 28.2921C33.1158 28.1586 32.9348 28.0836 32.746 28.0836C31.9862 28.0833 31.2348 28.242 30.5401 28.5496C29.8453 28.8571 29.2227 29.3066 28.7121 29.8692V21.2022C28.7121 20.1324 29.1371 19.1063 29.8936 18.3498C30.6501 17.5933 31.6761 17.1683 32.746 17.1683C33.8158 17.1683 34.8419 17.5933 35.5984 18.3498C36.3549 19.1063 36.7799 20.1324 36.7799 21.2022V22.0007C36.7798 22.148 36.8254 22.2917 36.9104 22.4119C36.9954 22.5322 37.1156 22.6231 37.2545 22.6722C38.3637 23.0634 39.2989 23.8342 39.8945 24.8485C40.4901 25.8628 40.7077 27.055 40.5088 28.2143C40.3099 29.3735 39.7074 30.4251 38.8078 31.1829C37.9083 31.9406 36.7696 32.3558 35.5934 32.3548ZM37.2545 25.948C37.2545 26.1368 37.1795 26.3179 37.046 26.4514C36.9125 26.5849 36.7314 26.6599 36.5426 26.6599H36.068C34.9982 26.6599 33.9721 26.2349 33.2156 25.4784C32.4591 24.7219 32.0341 23.6958 32.0341 22.626V22.1514C32.0341 21.9626 32.1091 21.7815 32.2426 21.648C32.3761 21.5145 32.5572 21.4395 32.746 21.4395C32.9348 21.4395 33.1158 21.5145 33.2493 21.648C33.3828 21.7815 33.4578 21.9626 33.4578 22.1514V22.626C33.4578 23.3182 33.7328 23.9821 34.2224 24.4716C34.7119 24.9611 35.3758 25.2361 36.068 25.2361H36.5426C36.7314 25.2361 36.9125 25.3111 37.046 25.4446C37.1795 25.5781 37.2545 25.7592 37.2545 25.948ZM19.9324 26.6599H19.4578C19.269 26.6599 19.0879 26.5849 18.9544 26.4514C18.8209 26.3179 18.7459 26.1368 18.7459 25.948C18.7459 25.7592 18.8209 25.5781 18.9544 25.4446C19.0879 25.3111 19.269 25.2361 19.4578 25.2361H19.9324C20.6246 25.2361 21.2886 24.9611 21.7781 24.4716C22.2676 23.9821 22.5426 23.3182 22.5426 22.626V22.1514C22.5426 21.9626 22.6176 21.7815 22.7511 21.648C22.8846 21.5145 23.0656 21.4395 23.2544 21.4395C23.4432 21.4395 23.6243 21.5145 23.7578 21.648C23.8913 21.7815 23.9663 21.9626 23.9663 22.1514V22.626C23.9663 23.6958 23.5413 24.7219 22.7848 25.4784C22.0283 26.2349 21.0022 26.6599 19.9324 26.6599Z" fill="#8E8D8D"/>

                            </svg>

                                
                            
                            
                            </div>
                            <div class="Frame15" style="left: 29px; top: 115px; position: absolute; justify-content: flex-start; align-items: flex-end; gap: 24px; display: inline-flex">
                                <div id="counter" style="color: #111416; font-size: 150px; font-family:  'Source Sans Pro',sans-serif; font-weight: 700; line-height: 47.93px; word-wrap: break-word"></div>
                                <div class="Frame9" style="flex-direction: column; justify-content: flex-start; align-items: flex-start; gap: 0px; display: inline-flex">
                                <div style="color: #8E8D8D; font-size: 12px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">Εργαζόμενοι</div>
                                <div style="color: #6E7279; font-size: 24px; font-family:  'Source Sans Pro',sans-serif; font-weight: 300; line-height: 24px; word-wrap: break-word">ΕΚΟ</div>
                                </div>
                            </div>
                            </div>
                            <script type="text/javascript">
                                {js_code}
                                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                                </script>
                            """,height = 250
                        )
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
            st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Ωρες απασχολησης εργαζομένων ΛΥΨΥ</p><p style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(Μεσος Όρος)</p>", unsafe_allow_html=True)

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
            st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Ωρες απασχολησης εργαζομένων ΕΚΟ</p><p style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(Μεσος Όρος)</p>", unsafe_allow_html=True)

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
    
