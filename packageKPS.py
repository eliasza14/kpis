import json
import pandas as pd


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


def get_data_from_json(kdata):
    kpdf=kdata[['koispe_id','year']]
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
    kpdf['D24']=kdata['report.turnover_total']
    #search for kad starts from .81

    matching_columns = kdata.columns[kdata.columns.str.startswith("report.kad.81.")]
    print(matching_columns)

    kdata[matching_columns] = kdata[matching_columns].astype(float)

    kpdf['D26'] = kdata.apply(lambda row: calculate_d26_d27(row, matching_columns), axis=1)
    #search for kad starts from .56
    matching_columns2 = kdata.columns[kdata.columns.str.startswith("report.kad.56.")]
    kdata[matching_columns2] = kdata[matching_columns2].astype(float)
    
    kpdf['D27'] = kdata.apply(lambda row: calculate_d26_d27(row, matching_columns2), axis=1)

    kpdf['D28'] = kdata['report.turnover_other']

    #% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος
    kpdf['D29'] = round((kdata['report.turnover_total'].astype(float).pct_change()*100),1)

    kpdf['D30'] = round((kpdf['D26'].astype(float).pct_change()*100),1)
    kpdf['D31'] = round((kpdf['D27'].astype(float).pct_change()*100),1)
    kpdf['D32'] = round((kpdf['D28'].astype(float).pct_change()*100),1)
    kpdf['D36'] = round((kdata['report.overall'].astype(float).pct_change()*100),1)
    kpdf['D38'] = round(((kdata['report.overall'].astype(float))/(kdata['report.turnover_total'].astype(float))),1)
    kpdf['D39'] = round(((kdata['report.grants'].astype(float))/(kdata['report.turnover_total'].astype(float))*100),1)
    kpdf['D40'] = round(((kdata['report.turnover_total'].astype(float))/(kdata['profile.sum_eme_kispe'].astype(float))),1)
    #Extra diktes
    kpdf['D18_lipsi']=kdata['profile.eme.sum']
    kpdf['D18_eko']=kdata['profile.eme_eko.sum']
    kpdf['D18_general']=kdata['profile.eme_general.sum']
    kpdf['D22_23_g']=round(((kdata['profile.eme_general.sum'].astype(float))/(kdata['profile.sum_eme_kispe'].astype(float))*100),1)
    kpdf['D36_overal']=kdata['report.overall'].astype(float)
    kpdf['D40_metaboli']=round((kpdf['D40'].astype(float).pct_change()*100),1)
    return kpdf