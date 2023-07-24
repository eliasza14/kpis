import json
import pandas as pd
import streamlit as st
import requests
import numpy as np






def calculate_percentage_change(old_value2, new_value2):

    old_value=float(old_value2)
    new_value=float(new_value2)
    st.write(old_value)
    st.write(new_value)
    if old_value > 0 and new_value > 0:
        percentage_change = (new_value - old_value) / old_value
    elif old_value < 0 and new_value < 0:
        percentage_change = (old_value - new_value) / abs(old_value)

    elif old_value > 0 and new_value < 0:
        percentage_change = (new_value - old_value) / old_value

    elif old_value < 0 and new_value > 0:
        percentage_change = (new_value - old_value) / abs(old_value)

    else:
        # Handle the case when both old_value and new_value are zero
        percentage_change = np.nan
    return round((float(percentage_change)*100),1)
# def calculate_percentage_change_d36(old_value2, new_value2):
#     old_value=float(old_value2)
#     new_value=float(new_value2)
#     st.write(old_value)
#     st.write(new_value)
#     if old_value > 0 and new_value > 0:
#         percentage_change = (new_value - old_value) / old_value
#         # st.write("result")
#         # st.write(percentage_change)
#     elif old_value < 0 and new_value < 0:
#         percentage_change = (old_value - new_value) / abs(old_value)
#     elif old_value > 0 and new_value < 0:
#         percentage_change = (new_value - old_value) / old_value
#     elif old_value < 0 and new_value > 0:
#         percentage_change = (new_value - old_value) / abs(old_value)
#     else:
#         # Handle the case when both old_value and new_value are zero
#         percentage_change = 0.0
#     st.write("result2")
#     st.write(percentage_change)

#     return round(percentage_change*100,1)


def calculate_d26_d27(row,matching_columns):
    
    values = row[matching_columns]
    column_sum = values.sum()
    d26=column_sum
    return d26






# def calculate_d19(row):
#     d18=row['D18']
#     d3 = row['D3']
#     d5 = row['D5']
#     d7 = row['D7']
#     return round((float(d18) / (int(d3) + int(d5) + int(d7))),1)



def calculate_d15(row):    
    d7 = row['D7']
    d13 = row['D13']
  
    return round(float(d13) / int(d7),1)




def calculate_d14(row):    
    d5 = row['D5']
    d12 = row['D12']
  
    return round(float(d12) / int(d5),1)



def calculate_d11(row):    
    d3 = row['D3']
    d5 = row['D5']
    d7 = row['D7']
    return round((int(d7) / (int(d3) + int(d5) + int(d7))*100),1)

def calculate_d10(row):    
    d3 = row['D3']
    d5 = row['D5']
    d7 = row['D7']
    return round((int(d5) / (int(d3) + int(d5) + int(d7))*100),1)

def calculate_d9(row):    
    d3 = row['D3']
    d5 = row['D5']
    d7 = row['D7']
    return round((int(d3) / (int(d3) + int(d5) + int(d7))*100),1)


def format_year(year):
    return "{:d}".format(year)  # Removes the comma separator
# @st.experimental_memo
@st.cache_data 
def get_data_from_json(id):
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
    
    kdata=kdata.sort_values(by=['year'], ascending=True)
    kdata=kdata.reset_index(drop=True)



    #Try
    kpdf=kdata[['koispe_id','year']]
    kpdf=kpdf.sort_values(by=['year'], ascending=True)
    
    print("Test kpdf")
    print(kpdf)

    # kpdf['year']=kpdf['year'].astype(str)
    kpdf['D1'] = kdata['profile.meli_a']
    kpdf['D3'] = kdata['profile.employee_general.sum']
    kpdf['D5'] = kdata['profile.employee.sum']
    kpdf['D7'] = kdata['profile.eko.sum']
    #Calculation from function
    kpdf['D9']=kpdf.apply(calculate_d9, axis=1)
    kpdf['D10']=kpdf.apply(calculate_d10, axis=1)
    kpdf['D11']=kpdf.apply(calculate_d11, axis=1)
    #ores apasxolisis
    kpdf['D12']=(kdata['profile.eme.sum'].astype(float))*2080
    kpdf['D13']=(kdata['profile.eme_eko.sum'].astype(float))*2080
    kpdf['D14']=kpdf.apply(calculate_d14, axis=1)
    kpdf['D15']=kpdf.apply(calculate_d15, axis=1)
    kpdf['D16']=round((kpdf['D12'].pct_change() * 100),1)
    kpdf['D17']=round((kpdf['D13'].pct_change() * 100),1)
    #etisies monades ergasias
    kpdf['D18']=kdata['profile.sum_eme_kispe'].astype(float)
    # kpdf['D19']=kpdf.apply(calculate_d19, axis=1)
    kpdf['D20']=round((kdata['profile.eme.sum'].astype(float).pct_change()*100),1)
    kpdf['D21']=round((kdata['profile.eme_eko.sum'].astype(float).pct_change()*100),1)
    kpdf['D22']=round(((kdata['profile.eme.sum'].astype(float))/(kdata['profile.sum_eme_kispe'].astype(float))*100),1)
    kpdf['D23']=round(((kdata['profile.eme_eko.sum'].astype(float))/(kdata['profile.sum_eme_kispe'].astype(float))*100),1)


    #Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος
    kpdf['D24']=kdata['report.turnover_total'].astype(float)
    #search for kad starts from .81

    matching_columns = kdata.columns[kdata.columns.str.startswith("report.kad.81.")]
    print(matching_columns)

    kdata[matching_columns] = kdata[matching_columns].astype(float)

    kpdf['D26'] = kdata.apply(lambda row: calculate_d26_d27(row, matching_columns), axis=1)
    #search for kad starts from .56
    matching_columns2 = kdata.columns[kdata.columns.str.startswith("report.kad.56.")]
    kdata[matching_columns2] = kdata[matching_columns2].astype(float)
    
    kpdf['D27'] = kdata.apply(lambda row: calculate_d26_d27(row, matching_columns2), axis=1)

    kpdf['D28'] = kdata['report.turnover_other'].astype(float)

    #% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος
    kpdf['D29'] = round((kdata['report.turnover_total'].astype(float).pct_change()*100),1)

    kpdf['D30'] = round((kpdf['D26'].astype(float).pct_change()*100),1)
    kpdf['D31'] = round((kpdf['D27'].astype(float).pct_change()*100),1)
    kpdf['D32'] = round((kpdf['D28'].astype(float).pct_change()*100),1)
    kpdf['D36_overal']=kdata['report.overall'].astype(float)

    #D36 fixing code
    # kpdf['D36'] = round((kdata['report.overall'].astype(float).pct_change()*100),1)
    st.write(kdata)

    st.write(kdata['report.overall'])
    # kdata=kdata.sort_values(by=['year'], ascending=True)
    # kpdf['D36'] = kpdf.apply(lambda row: calculate_percentage_change_d36(row['D36_overal'], kpdf.loc[row.name + 1, 'D36_overal']), axis=1)
# Calculate the percentage change for each row using the custom function
    kpdf['D36'] = kpdf.apply(lambda row: calculate_percentage_change( kpdf.loc[row.name - 1, 'D36_overal'],row['D36_overal'])
                            if row.name != 0 else np.nan, axis=1)
    # for i in range(len(kpdf['D36_overal'])):
    #     if kpdf['D36_overal'][i] > 0 and kpdf['D36_overal'][i+1] > 0:
    #         percentage_change = (kpdf['D36_overal'][i+1] - kpdf['D36_overal'][i]) / kpdf['D36_overal'][i]
    #         # st.write("result")
    #         # st.write(percentage_change)
    #     elif kpdf['D36_overal'][i] < 0 and kpdf['D36_overal'][i+1] < 0:
    #         percentage_change = (kpdf['D36_overal'][i] - kpdf['D36_overal'][i+1]) / abs(kpdf['D36_overal'][i])
    #     elif kpdf['D36_overal'][i] > 0 and kpdf['D36_overal'][i+1] < 0:
    #         percentage_change = (kpdf['D36_overal'][i+1] - kpdf['D36_overal'][i]) / kpdf['D36_overal'][i]
    #     elif kpdf['D36_overal'][i] < 0 and kpdf['D36_overal'][i+1] > 0:
    #         percentage_change = (kpdf['D36_overal'][i+1] - kpdf['D36_overal'][i]) / abs(kpdf['D36_overal'][i])
    #     else:
    #         # Handle the case when both old_value and new_value are zero
    #         percentage_change = 0.0
    #     st.write("mesa sto for")
    #     st.write(percentage_change)
    # st.write(percentage_change)

    # kpdf['D36'] = kdata.apply(lambda row: calculate_percentage_change_d36(row['report.overall'], kdata.loc[row.name - 1, 'report.overall']), axis=1)
    # x=calculate_percentage_change_d36( float(kdata['report.overall'][0]),float(kdata['report.overall'][1]))


    kpdf['D38'] = round(((kdata['report.overall'].astype(float))/(kdata['report.turnover_total'].astype(float))),2)
    kpdf['D39'] = round(((kdata['report.grants'].astype(float))/(kdata['report.turnover_total'].astype(float))*100),2)
    kpdf['D40'] = round(((kdata['report.turnover_total'].astype(float))/(kdata['profile.sum_eme_kispe'].astype(float))),2)
    #Extra diktes
    kpdf['D18_lipsi']=kdata['profile.eme.sum'].astype(float)
    kpdf['D18_eko']=kdata['profile.eme_eko.sum'].astype(float)
    kpdf['D18_general']=kdata['profile.eme_general.sum'].astype(float)
    kpdf['D22_23_g']=round(((kdata['profile.eme_general.sum'].astype(float))/(kdata['profile.sum_eme_kispe'].astype(float))*100),1)
    kpdf['D40_metaboli']=round((kpdf['D40'].astype(float).pct_change()*100),1)
    return kpdf