import streamlit as st
import requests
from streamlit_option_menu import option_menu
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit.components.v1 import html
import base64
import io
from packageKPS import *
from packageCharts import *
from html_shortcuts import *
from PIL import Image



def main():
 

    
    #st.write(home())
    st.set_page_config(
        page_title="Koispe Dashboard",
        page_icon="✅",
        layout="wide",
    )    

    
 

    with open( "style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


    #st.markdown(css_style, unsafe_allow_html=True)

            # Load the JavaScript function code
    with open("animated_counter.js", "r") as file:
            js_code = file.read()

    with open("style2.css", "r") as file:
            css_code = file.read()
    st.sidebar.image("https://koispesupport.gr/wp-content/uploads/2023/06/Logo-Koispe-203x90.png", width=100)


    # st.sidebar.title("KPI's Dashboard")
    id=get_url_params()
    # st.write("URL ID FROM VIDAVO:",id)
    # st.write("ID from Flask application: ",id)


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


    kpdf=get_data_from_json(id)
    # kpdf=kpdf.fillna(0)
 

    # st.title("Πίνακας Δεικτών")
    # st.write(kpdf)

        # 1. as sidebar menu
    with st.sidebar:

        selected_option1 = option_menu("Μενού", ["Συνεταιριστές","Εργαζόμενοι", "Ώρες Απασχόλησης", "Ετήσιες Μονάδες Εργασίας","Κύκλοι εργασιών", 
                                                 "Διαχρονική (%) μεταβολή Κύκλων Εργασιών", "Κατανομή πλήθους με βάση το καθαρό εισόδημα","Αναλυτικός Πίνακας Δεικτών"],
                            icons=['people', 'person-gear','clock-history','person-workspace','cash-stack','graph-up-arrow','piggy-bank','table'],
                            menu_icon="cast", default_index=1,
                            
                            styles={
                                "menu-title":{"display":"none"},
                                "icon": {"font-size": "25px"}, 

                                "container": {"padding": "0!important", "background-color": "#D3ECFA", "color": "#ffffff"},
                                "nav-link": {"font-family": "Roboto","font-style": "normal","font-weight": "700","line-height": "220%" ,"background-color": "#D3ECFA", "color": "#004BCF", "text-align": "left", "margin": "0px", "--hover-color": "#004BCF"},
                                "nav-link-selected": {"color": "#ffffff", "background-color": "#004BCF"},
                            }
                            )
        

    # Empty container for the right side content
    content_container = st.empty()
        
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
    elif selected_option1=="Κύκλοι εργασιών":
        e_button5(id,kpdf,js_code,css_code)
    elif selected_option1=="Διαχρονική (%) μεταβολή Κύκλων Εργασιών":
        e_button6(id,kpdf,js_code)
    elif selected_option1=="Κατανομή πλήθους με βάση το καθαρό εισόδημα":
        e_button7(id,kpdf,js_code,css_code)    
    elif selected_option1=="Αναλυτικός Πίνακας Δεικτών":
        e_button8(id,kpdf,js_code,css_code)  
        

def ad_button1(id,kpdf,js_code):
    st.subheader("Συνεταιριστές")

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist(),index=len(kpdf['year'])-1)
    
    with st.container():

        val=kpdf['D1'][kpdf['year']==str(year_filter)].iloc[0]
        # st.markdown("<h3 style='text-align: center; color: grey;'>Συνεταιριστές Κατηγορίας Α</h3>", unsafe_allow_html=True)  
        html_content1 = html_button1(js_code, val)
        html(html_content1,height=250)



def ad_button2(id,kpdf,js_code):
    st.subheader("Εργαζόμενοι")
    #colors = px.colors.qualitative.Plotly
    # legend_labels = ['Γενικού Πληθυσμού', 'ΛΥΨΥ', 'ΕΚΟ']
    colors = ['#618abb','#00235e','#F0894F']
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist(),index=len(kpdf['year'])-1)

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            
            text=str(kpdf['D3'][kpdf['year']==str(year_filter)].iloc[0])
            html_content2 = html_button2(js_code, text)
            html(html_content2,height=250)

        with col2:

            text=kpdf['D5'][kpdf['year']==str(year_filter)].iloc[0]
            html_content3 = html_button3(js_code, text)
            html(html_content3,height=250)
          
        with col3:
            #st.write('D7-Εργαζόμενοι ΕΚΟ')
            text=kpdf['D7'][kpdf['year']==str(year_filter)].iloc[0]
            html_content4 = html_button4(js_code, text)
            html(html_content4,height=250)

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            # Filter the dataframe based on the selected year
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι Γεν. Πληθ.</h3><h3 style='text-align: center; color: grey;'>(% επί του Συνόλου)</h3>", unsafe_allow_html=True)
            # st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Εργαζόμενοι Γεν. Πληθ.</p><p  style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(% επί του Συνόλου)</p>", unsafe_allow_html=True)
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]
            # Select the value from the filtered dataframe
            d9_value = filtered_kpdf["D9"].iloc[0]
            # fig=gaugeChart(d9_value,'royalblue')
            fig=donut_pct_Chart(d9_value,'#618abb', 'rgb(240,240,240)',['% Γεν. Πληθυσμού', ' '])
            st.plotly_chart(fig,use_container_width=True)
            

        with col2:
            # Filter the dataframe based on the selected year
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΛΥΨΥ</h3><h3 style='text-align: center; color: grey;'>(% επί του Συνόλου)</h3>", unsafe_allow_html=True)
            # st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Εργαζόμενοι ΛΥΨΥ</p><p style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(% επί του Συνόλου)</p>", unsafe_allow_html=True)
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]
            # Select the value from the filtered dataframe
            d10_value = filtered_kpdf["D10"].iloc[0]
            # fig=gaugeChart(d10_value,'skyblue')
            fig=donut_pct_Chart(d10_value,'#00235e', 'rgb(240,240,240)',['% ΛΥΨΥ', ' '])
            st.plotly_chart(fig,use_container_width=True)
        with col3:
            # Filter the dataframe based on the selected year
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΕΚΟ</h3><h3 style='text-align: center; color: grey;'>(% επί του Συνόλου)</h3>", unsafe_allow_html=True)
            # st.markdown("<p style='text-align: center; color: black; font-size:24px; font-family:Roboto;'>Εργαζόμενοι ΕΚΟ</p><p style='text-align: center; color: black; font-size:18px; font-family:Roboto;'>(% επί του Συνόλου)</p>", unsafe_allow_html=True)
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]
            # Select the value from the filtered dataframe
            d11_value = filtered_kpdf["D11"].iloc[0]
            # fig=gaugeChart(d11_value,'red')
            fig=donut_pct_Chart(d11_value,'#F0894F', 'rgb(240,240,240)',['% ΕΚΟ', ' '])
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
                fig=stackedChart(columns,kpdf,legend_labels,'Έτος','% επί του Συνόλου',colors)
                # Show the plot
                st.plotly_chart(fig, use_container_width=True)
            with col3:
                pass


def ad_button3(id,kpdf,js_code):
    st.subheader("Ωρες απασχόλησης")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist(),index=len(kpdf['year'])-1)
   
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #st.write('Δ14-Ωρες απασχολησης εργαζομένων ΛΥΨΥ(Μεσος Όρος)')
            text=kpdf['D14'][kpdf['year']==str(year_filter)].iloc[0]
            text=str(text.round())
            html_content5 = html_button5(js_code, text)
            html(html_content5,height=250)

        with col2:
            #st.write('Δ15-Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος)')
            #st.write(kpdf['D15'][kpdf['year']==str(year_filter)])
            text=kpdf['D15'][kpdf['year']==str(year_filter)].iloc[0]
            text=str(text.round())
            html_content6 = html_button6(js_code, text)
            html(html_content6,height=250)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #st.write('Δ12-Ωρες απασχολησης εργαζομένων ΛΥΨΥ')
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μεταβολή Ωρών Απασχόλησης ΛΥΨΥ</h3>", unsafe_allow_html=True)
            categories=kpdf['year'].tolist()
            values =kpdf['D12'].tolist()
            line_labels=kpdf['D16'].tolist()
            fig=pctChangeV2(categories,values,line_labels,'Ώρες Απασχόλησης ΛΥΨΥ','Ώρες Απασχόλησης')
            # fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            #st.write('Δ13-Ωρες απασχολησης εργαζομένων ΕΚΟ')
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μεταβολή Ωρών Απασχόλησης ΕΚΟ</h3>", unsafe_allow_html=True)
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D13'].tolist()
            line_labels=kpdf['D17'].tolist()
            fig=pctChangeV2(categories,values,line_labels,'Ώρες Απασχόλησης ΕΚΟ','Ώρες Απασχόλησης')
            # fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)
        

def ad_button4(id,kpdf,js_code):
    st.subheader("Ετήσιες Μονάδες Εργασίας")
    colors = ['#00235e','#F0894F','#618abb']
    # legend_labels = ['Μ.Ε. ΛΥΨΥ', 'Μ.Ε. ΕΚΟ', 'Μ.Ε. Γεν.Πληθ.']

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist(),index=len(kpdf['year'])-1)

    with st.container():

            text=str(kpdf['D18'][kpdf['year']==str(year_filter)].iloc[0])
            html_content7 = html_button7(js_code, text)
            html(html_content7,height=250)


    with st.container():
        col1, col2 =st.columns(2)
        
        with col1:
            # Create the layout with two y-axes
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας ΛΥΨΥ % επί του Συνόλου</h3>", unsafe_allow_html=True)
            val = float(kpdf['D22'][kpdf['year'] == str(year_filter)].iloc[0])
            fig=donut_pct_Chart(val,'#00235e', 'rgb(240,240,240)',['(%) Μ.Ε. ΛΥΨΥ επί του συνόλου', ' '])
            st.plotly_chart(fig, use_container_width=True)


        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας ΕΚΟ % επί του Συνόλου</h3>", unsafe_allow_html=True)
            val2=float(kpdf['D23'][kpdf['year']==str(year_filter)].iloc[0])
            fig=donut_pct_Chart(val2,'#F0894F','rgb(240,240,240)',['(%) Μ.Ε. ΕΚΟ επί του συνόλου', ' '])
            st.plotly_chart(fig,use_container_width=True)

    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Μονάδων Εργασίας ΛΥΨΥ</h3>", unsafe_allow_html=True)
            categories=kpdf['year'].tolist()
            values =kpdf['D18_lipsi'].tolist()
            line_labels=kpdf['D20'].tolist()
            fig=pctChangeV2(categories,values,line_labels,'Αρ.Μονάδων Εργασίας ΛΥΨΥ','Μ.Ε. ΛΥΨΥ')
            # fig=pctChangeChart(values,categories,'Αρ.Μονάδων Εργασίας ΛΥΨΥ','Ποσοστιαία μεταβολή','% Μεταβολή','Μ.Ε. ΛΥΨΥ')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Μονάδων Εργασίας ΕΚΟ</h3>", unsafe_allow_html=True)
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D18_eko'].astype(float).tolist()
            line_labels=kpdf['D21'].tolist()
            fig=pctChangeV2(categories,values,line_labels,'Αρ.Μονάδων Εργασίας ΕΚΟ','Μ.Ε. ΕΚΟ')
            # fig=pctChangeChart(values,categories,'Αρ.Μονάδων Εργασίας ΕΚΟ','Ποσοστιαία μεταβολή','% Μεταβολή','Μ.Ε. ΕΚΟ')
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
            fig=stackedChart(columns,kpdf,legend_labels,'Έτος','% επί του Συνόλου',colors)
            st.plotly_chart(fig, use_container_width=True)
         with col3:
            pass
             

def e_button5(id,kpdf,js_code,css_code):
    st.subheader("Κύκλοι εργασιών")
    colors = ['#00235e','#F0894F','#618abb']
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist(),index=len(kpdf['year'])-1)
    val2=float(kpdf['D24'][kpdf['year']==str(year_filter)].iloc[0])
    val29=float(kpdf['D29'][kpdf['year']==str(year_filter)].iloc[0])
    html_content8 = html_button8(js_code, val2,css_code,val29)
    html(html_content8,height=250)
    with st.container():
        col1, col2,col3 = st.columns(3)

        with col1:
            #st.markdown("<h3 style='text-align: center; color: grey;'>🏠 Κτηρίων & Εξ. Χώρων</h3>", unsafe_allow_html=True)
            val26=float(kpdf['D26'][kpdf['year']==str(year_filter)].iloc[0])
            val4=float(kpdf['D30'][kpdf['year']==str(year_filter)].iloc[0])
            html_content9= html_button9(js_code, val4,css_code,val26)
            html(html_content9,height=250)

        with col2:

            val27=float(kpdf['D27'][kpdf['year']==str(year_filter)].iloc[0])
            val6=float(kpdf['D31'][kpdf['year']==str(year_filter)].iloc[0])
            html_content10= html_button10(js_code, val6,css_code,val27)
            html(html_content10,height=250)
        with col3:

            val28=float(kpdf['D28'][kpdf['year']==str(year_filter)].iloc[0])
            val8=float(kpdf['D32'][kpdf['year']==str(year_filter)].iloc[0])   
            html_content11= html_button11(js_code, val8,css_code,val28)
            html(html_content11,height=250)
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            pass
        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Ποσοστό επί του Συνόλου ανά Κατηγορία Κύκλου Εργασιών</h3>", unsafe_allow_html=True)

            labels = ['Κτίρια & Εξ.Χώροι ','Εστίαση','Λοιπές Δραστηριότητες']
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
            legend_labels = ['Κτίρια & Εξ.Χώροι ','Εστίαση','Λοιπές Δραστηριότητες']
            kpdf_selected = kpdf[columns]
            # Create the stacked bar plot using Plotly
            fig=stackedChart2(columns,kpdf,legend_labels,'Έτος','Συχνότητα',colors)
            st.plotly_chart(fig,use_container_width=True)
        with col3:
            pass
   

def e_button6(id,kpdf,js_code):
    st.subheader("Διαχρονική (%) μεταβολή Κύκλων Εργασιών")
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Κύκλου Εργασιών</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D24'].astype(float).tolist()
            line_labels=kpdf['D29'].tolist()
            fig=pctChangeV2(categories,values,line_labels,'Κύκλοι Εργασιών','Κυκλ.Εργασιών')
            # fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μετ.Kύκλ.Εργ. Κτίρια/Εξωτ. Χώροι</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D26'].astype(int).tolist()
            line_labels=kpdf['D30'].tolist()

            fig=pctChangeV2(categories,values,line_labels,'Κύκλοι Εργασιών','Κτ/Εξωτ. Χώροι')

            # fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
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
            line_labels=kpdf['D31'].tolist()


            fig=pctChangeV2(categories,values,line_labels,'Κύκλοι Εργασιών','Υπηρ. Εστίασης')

            # fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μετ.Κύκλ.Εργ. Λοιπ. Δραστ.</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()

            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D28'].astype(float).tolist()
            line_labels=kpdf['D32'].tolist()
            fig=pctChangeV2(categories,values,line_labels,'Κύκλοι Εργασιών','Λοιπ. Δραστ.')

            # fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)

def e_button7(id,kpdf,js_code,css_code):
    st.subheader("Κατανομή πλήθους με βάση το καθαρό εισόδημα")

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist(),index=len(kpdf['year'])-1)
    val1=float(kpdf['D36_overal'][kpdf['year']==str(year_filter)].iloc[0])
    val2=float(kpdf['D36'][kpdf['year']==str(year_filter)].iloc[0])

    val3=float(kpdf['D38'][kpdf['year']==str(year_filter)].iloc[0])
    val4=float(kpdf['D40'][kpdf['year']==str(year_filter)].iloc[0])
    val5=float(kpdf['D40_metaboli'][kpdf['year']==str(year_filter)].iloc[0])

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            html_content12= html_button12(js_code, val1,css_code,val2)
            html(html_content12,height=250)
        with col2:
            html_content13= html_button13(js_code, val3,css_code)
            html(html_content13,height=250)

        with col3:
            html_content14= html_button14(js_code, val4,css_code,val5)
            html(html_content14,height=250)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Καθαρών Αποτελεσμάτων</h3>", unsafe_allow_html=True)
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D36_overal'].astype(float).tolist()
            line_labels=kpdf['D36'].tolist()
            fig=pctChangeV2(categories,values,line_labels,'Καθαρά Αποτελέσματα','Καθ. Αποτελέσμ.')
            # fig=pctChangeChart(values,categories,'Values','Ποσοστιαία μεταβολή','Percentage Change','Values')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Συμμετοχή (%) Επιδοτήσεων στα έσοδα</h3>", unsafe_allow_html=True)
            val39=float(kpdf['D39'][kpdf['year']==str(year_filter)].iloc[0])
            fig=donut_pct_Chart(val39,'#00235e', 'rgb(240,240,240)',['% Συμμετοχή Επιδοτήσεων', ' '])
            st.plotly_chart(fig, use_container_width=True)
        

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        col1,col2,col3 = st.columns(3)  
        with col1:
            pass
        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Αριθμοδείκτης Καθαρών Αποτελεσμάτων / Έτος</h3>", unsafe_allow_html=True)

            fig = px.area(kpdf, x=kpdf['year'].astype(int), y='D38', markers=True)

            # Update the line color
            fig.update_traces(line=dict(color='#00235e'))

            # Update the area color
            fig.update_traces(fillcolor='#618abb', fill='tozeroy')

            fig.update_layout(
                xaxis=dict(
                    title='Έτος',
                    tickmode='linear',
                    tickfont=dict( size=20 ),
                    dtick=1
                ),
                yaxis=dict(
                    title='Αριθμοδείκτης Καθαρών Αποτελεσμάτων'
                )
            )

            st.plotly_chart(fig, use_container_width=True)
        with col3:
            pass

def e_button8(id,kpdf,js_code,css_code):
    st.subheader("Αναλυτικός Πίνακας Δεικτών")
    kpdf_filtered=kpdf.loc[:, ~kpdf.columns.isin(['D36_overal', 'D18_lipsi','D18_eko','D18_general','D22_23_g','D40_metaboli'])]
    # st.write(kpdf.loc[:, ~kpdf.columns.isin(['D36_overal', 'D18_lipsi','D18_eko','D18_general','D22_23_g','D40_metaboli'])])
   # Get the current column names in a list
    current_cols = kpdf_filtered.columns.tolist()

    # Create a dictionary to map old column names to new column names
    new_cols = {}
    found_year = False

    # Enumerate through the current column names and rename them accordingly
    for old_col in current_cols:
        if old_col == 'year':
            found_year = True
            new_cols[old_col] = old_col  # Keep 'year' column unchanged
        elif found_year:
            new_cols[old_col] = f'Δ{len(new_cols) - 1}'  # Start enumeration from 1 after 'year'
        else:
            new_cols[old_col] = old_col  # Keep columns before 'year' unchanged

    # Rename the columns using the .rename() method
    kpdf_filtered.rename(columns=new_cols, inplace=True)

    st.write(kpdf_filtered)
    csv = convert_df(kpdf_filtered)

    st.subheader("Υπόμνημα Δεικτών")
    st.markdown("""
        <table border="1" cellpadding="0" cellspacing="0" style="font-family:Roboto; color:black;">
            <tr> <th style="border:solid 1px black;font-weight: bold;">Α/Α</th> <th style="border:solid 1px black;font-weight: bold;">Δείκτης</th> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ1</td> <td style="border:solid 1px black;font-weight: bold;">Συνεταιριστές κατηγορίας Α</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ2</td> <td style="border:solid 1px black;font-weight: bold;">Εργαζόμενοι Γενικού Πληθυσμού</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ3</td> <td style="border:solid 1px black;font-weight: bold;">Εργαζόμενοι ΛΥΨΥ</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ4</td> <td style="border:solid 1px black;font-weight: bold;">Εργαζόμενοι ΕΚΟ</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ5</td> <td style="border:solid 1px black;font-weight: bold;">Εργαζόμενοι Γενικού Πληθυσμού (% επί του συνόλου των εργαζομένων της ΚοιΣΠΕ)</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ6</td> <td style="border:solid 1px black;font-weight: bold;">Εργαζόμενοι ΛΥΨΥ (% επί του συνόλου των εργαζομένων της ΚοιΣΠΕ)</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ7</td> <td style="border:solid 1px black;font-weight: bold;">Εργαζόμενοι ΕΚΟ (% επί του συνόλου των εργαζομένων της ΚοιΣΠΕ)</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ8</td> <td style="border:solid 1px black;font-weight: bold;">Ώρες απασχολησης εργαζόμενων ΛΥΨΥ</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ9</td> <td style="border:solid 1px black;font-weight: bold;">Ώρες απασχολησης εργαζόμενων ΕΚΟ</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ10</td> <td style="border:solid 1px black;font-weight: bold;">Ώρες απασχολησης εργαζόμενων ΛΥΨΥ (Μέσος Όρος)</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ11</td> <td style="border:solid 1px black;font-weight: bold;">Ώρες απασχολησης εργαζόμενων ΕΚΟ (Μέσος Όρος)</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ12</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή ωρών απασχόλησης ΛΥΨΥ</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ13</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή ωρών απασχόλησης ΕΚΟ</td> </tr> 
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ14</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσιες Μονάδες Εργασίας</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ15</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή Ετησίων Μονάδων Εργασίας ΛΥΨΥ</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ16</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή Ετησίων Μονάδων Εργασίας ΕΚΟ</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ17</td> <td style="border:solid 1px black;font-weight: bold;">Ετησίες (%) Μονάδες Εργασίας ΛΥΨΥ ως προς το σύνολο</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ18</td> <td style="border:solid 1px black;font-weight: bold;">Ετησίες (%) Μονάδες Εργασίας ΕΚΟ ως προς το σύνολο</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ19</td> <td style="border:solid 1px black;font-weight: bold;">Κύκλοι Εργασιών</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ20</td> <td style="border:solid 1px black;font-weight: bold;">Κύκλοι Εργασιών δραστηριοτήτων παροχής υπηρεσιών σε κτίρια και εξωτερικούς χώρους</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ21</td> <td style="border:solid 1px black;font-weight: bold;">Κύκλοι Εργασιών δραστηριοτήτων υπηρεσιών εστίασης</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ22</td> <td style="border:solid 1px black;font-weight: bold;">Κύκλοι Εργασιών λοιπών δραστηριοτήτων</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ23</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή Κύκλου Εργασιών</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ24</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή Κύκλου Εργασιών δραστηριοτήτων παροχής υπηρεσιών σε κτίρια και εξωτερικούς χώρους</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ25</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή Κύκλου Εργασιών δραστηριοτήτων υπηρεσιών εστίασης</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ26</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή Κύκλου Εργασιών λοιπών δραστηριοτήτων</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ27</td> <td style="border:solid 1px black;font-weight: bold;">Ετήσια (%) μεταβολή καθαρών αποτελεσμάτων</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ28</td> <td style="border:solid 1px black;font-weight: bold;">Αριθμοδείκτης καθαρών αποτελεσμάτων</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ29</td> <td style="border:solid 1px black;font-weight: bold;">Συμμετοχή (%) επιδοτήσεων στα έσοδα</td> </tr>
            <tr> <td style="border:solid 1px black;font-weight: bold;">Δ30</td> <td style="border:solid 1px black;font-weight: bold;">Έσοδα ανά εργαζόμενο</td> </tr>
        </table>
        <br>
    """,unsafe_allow_html=True)

    st.download_button(
    label="Λήψη Πίνακα Δεικτών",
    data=csv,
    file_name='kpis_table.csv',
    mime='text/csv',
    )


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
    
