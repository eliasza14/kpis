import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit.components.v1 import html

from packageKPS import *
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
    
    
       
    





    
    </style>"""
    st.markdown(css_style, unsafe_allow_html=True)

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

    response = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getkoispe").text)
    response2 = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getemployment").text)
    response3 = json.loads(requests.get("https://app.koispesupport.gr/koispe/api/getfinancial").text)


    # response = json.loads(requests.get("https://cmtprooptiki.gr/api/getkoisenew.json").text)
    # response2 = json.loads(requests.get("https://cmtprooptiki.gr/api/getemploymentcmt.json").text)
    # response3 = json.loads(requests.get("https://cmtprooptiki.gr/api/getfinancial.json").text)

    df=pd.json_normalize(response, max_level=2)
    st.write(df)

    df['year'] = df['year'].map(lambda x: str(x) if pd.notnull(x) else None)

    st.write(df)

    df['year'] = df['year'].apply(format_year)
    st.write(df)

    df2=pd.json_normalize(response2, max_level=2,dtype={"year": str})
    df2['year']=df2['year'].astype(str)
    df2['year'] = df2['year'].apply(format_year)

    df3=pd.json_normalize(response3, max_level=2,dtype={"year": str})
    df3['year']=df3['year'].astype(str)

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
    ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό / Επιχειρηματικότητα",expanded=True)
    with ad_expander:
        selected_option1 = st.radio("Επιλέξτε:", ["Συνεταιριστές","Εργαζόμενοι", "Ώρες Απασχόλησης", "Ετήσιες Μονάδες Εργασίας","Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος", "% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος", "Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος"])
    
    # selected_option3 = st.sidebar.button("Αναλυτικός Πίνακας Δεδομένων")

    # ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό")


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

        html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(val)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )






def ad_button2(id,kpdf,js_code):
    st.subheader("Εργαζόμενοι")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            
            text=str(kpdf['D3'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('Δ3-Εργαζόμενοι Γενικού Πληθυσμού: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι Γεν. Πληθυσμού</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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

            # Create the figure and gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=d9_value,
                domain={'x': [0, 1], 'y': [0, 1]},
                number={'suffix': '%'}
            ))

            # Customize the appearance of the gauge chart
            fig.update_traces(
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "royalblue",'thickness': 0.7},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 100], 'color': 'whitesmoke'},
                        ]
                    },  # Set the range for the gauge axis
                title_font={'size': 10,'color': 'gray'},  # Set the title font size
                number_font={'size': 40},  # Set the number font size
            )
            fig.update_layout(
                height=170,  # Adjust the height of the chart
                width=200,   # Adjust the width of the chart
                margin=dict(l=0, r=0, t=12, b=5, autoexpand=True),  # Adjust the top margin value

                paper_bgcolor="white",
                font={'color': "gray", 'family': "Arial"}
            )
            st.plotly_chart(fig,use_container_width=True)
            

        with col2:
            # Filter the dataframe based on the selected year
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΛΥΨΥ (% επί του Συνόλου)</h3>", unsafe_allow_html=True)

            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]

            # Select the value from the filtered dataframe
            d10_value = filtered_kpdf["D10"].iloc[0]

            # Create the figure and gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=d10_value,
                domain={'x': [0, 1], 'y': [0, 1]},
                number={'suffix': '%'}
            ))

            # Customize the appearance of the gauge chart
            fig.update_traces(
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "skyblue",'thickness': 0.7},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 100], 'color': 'whitesmoke'},
                        ]
                    },  # Set the range for the gauge axis
                title_font={'size': 10,'color': 'gray'},  # Set the title font size
                number_font={'size': 40},  # Set the number font size
            )
            fig.update_layout(
                height=170,  # Adjust the height of the chart
                width=200,   # Adjust the width of the chart
                # margin=dict(l=0, r=0, t=30, b=0, autoexpand=True),  # Set the margin to auto
                margin=dict(l=0, r=0, t=12, b=5, autoexpand=True),  # Adjust the top margin value

                paper_bgcolor="white",
                font={'color': "gray", 'family': "Arial"}
            )
            
            st.plotly_chart(fig,use_container_width=True)
        with col3:
            # Filter the dataframe based on the selected year
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΕΚΟ (% επί του Συνόλου)</h3>", unsafe_allow_html=True)

            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]

            # Select the value from the filtered dataframe
            d11_value = filtered_kpdf["D11"].iloc[0]

            # Create the figure and gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=d11_value,
                domain={'x': [0, 1], 'y': [0, 1]},
                # title={'text': "Εργαζόμενοι ΕΚΟ (% επί του Συνόλου Εργαζομένων ΚοιΣΠΕ)"},
                number={'suffix': '%'},
                
            ))
            

            # Customize the appearance of the gauge chart
            fig.update_traces(
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "red",'thickness': 0.7},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 100], 'color': 'whitesmoke'},
                        ]
                    },  # Set the range for the gauge axis
                title_font={'size': 10,'color': 'gray'},  # Set the title font size
                number_font={'size': 40},  # Set the number font size
            )
            fig.update_layout(
                height=170,  # Adjust the height of the chart
                width=200,   # Adjust the width of the chart
                paper_bgcolor="white",
                # margin=dict(l=0, r=0, t=30, b=0, autoexpand=True),  # Set the margin to auto
                margin=dict(l=0, r=0, t=12, b=5, autoexpand=True),  # Adjust the top margin value

                font={'color': "gray", 'family': "Arial"}
            )
            # fig.update_layout(paper_bgcolor = "white", font = {'color': "gray", 'family': "Arial"})
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
                kpdf_selected = kpdf[columns]
                # Create the stacked bar plot using Plotly
                fig = go.Figure()
                legend_labels = ['Γενικού Πληθυσμού', 'ΛΥΨΥ', 'ΕΚΟ']
                for i, col in enumerate(columns):
                    fig.add_trace(go.Bar(
                        name=legend_labels[i],  # Use the corresponding label
                        x=kpdf['year'].apply(str),
                        y=kpdf_selected[col],
                        text=kpdf[col],
                        textposition='inside'
                    ))
                # Update the layout
                fig.update_layout(barmode='stack', xaxis_title='Έτος',yaxis_title='% επι του Συνόλου',legend=dict(
                orientation="h",  # Horizontal legends
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),height=600, width=800)

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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D12'].tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                # title='Μεταβολή ωρών απασχόλησης ΛΥΨΥ',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            #st.write('Δ13-Ωρες απασχολησης εργαζομένων ΕΚΟ')
            st.markdown("<h3 style='text-align: center; color: grey;'>% Μεταβολή Ωρών Απασχόλησης ΕΚΟ</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D13'].tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig,use_container_width=True)
        
          

   

# def ad_button3(id,kpdf):
#     st.subheader("button3 Submenu")
#     st.write("Content of button3")
#     with st.container():
#         col1, col2,col3 = st.columns(3)
#         with col1:
#             st.write('D18')
#             st.write(kpdf['D18'])

#         with col2:
#             st.write('D19')
#             st.write(kpdf['D19'])
#         with col3:
#             st.write('D20')
#             st.write(kpdf['D20'])

#     with st.container():
#         col1, col2,col3 = st.columns(3)
#         with col1:
#             st.write('D21')
#             st.write(kpdf['D21'])

#         with col2:
#             st.write('D22')
#             st.write(kpdf['D22'])

#         with col3:
#             st.write('D23')
#             st.write(kpdf['D23'])


          






def ad_button4(id,kpdf,js_code):
    st.subheader("Ετήσιες Μονάδες Εργασίας")
    
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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

                layout = go.Layout(
                    yaxis=dict(title='Values', rangemode='nonnegative'),
                    yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                    height=400,  # Set the height of the chart
                    width=400,  # Set the width of the chart
                    legend=dict(
                        orientation='h',
                        yanchor='top',
                        y=1.1,
                        xanchor='center',
                        x=0.5
                    ),
                    margin=dict(l=0, r=0, t=30, b=0, autoexpand=True)  # Set the margin to auto
                )

                fig = go.Figure(layout=layout)
                fig.add_trace(go.Pie(
                    labels=['(%) Μ.Ε. ΛΥΨΥ επι του συνόλου', ' '],
                    values=[val, 100 - val],
                    hole=0.85,
                    textinfo='none',
                    marker_colors=['rgb(135 206 235)', 'rgb(240,240,240)'],
                ))
                fig.update_layout(annotations=[dict(text=str(val) + "%", font_size=40, showarrow=False)])
                fig.update_layout(showlegend=True)  # Show the legend
                fig.update_layout(legend=dict(
                    orientation='h',
                    yanchor='top',
                    y=1.1,
                    xanchor='center',
                    x=0.5
                ))
                st.plotly_chart(fig, use_container_width=True)


        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετήσιες Μονάδες Εργασίας ΕΚΟ % επί του Συνόλου</h3>", unsafe_allow_html=True)

            val2=float(kpdf['D23'][kpdf['year']==str(year_filter)].iloc[0])
            layout = go.Layout(
            yaxis=dict(title='Values', rangemode='nonnegative'),
            yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
            height=400,  # Set the height of the chart
            width=400,  # Set the width of the chart
            legend=dict(
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='center',
                x=0.5
            ),
            margin=dict(l=0, r=0, t=30, b=0, autoexpand=True)  # Set the margin to auto
            )
            fig = go.Figure(layout=layout)
            fig.add_trace(go.Pie(
                labels=['(%) Μ.Ε. ΕΚΟ επι του συνόλου', ' '],
                values=[val2,100-val2],
                hole=0.85,
                textinfo='none',
                marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
            ))
            fig.update_layout(annotations=[dict(text=str(val2) + "%", font_size=40, showarrow=False)])
            fig.update_layout(showlegend=True)  # Show the legend
            fig.update_layout(legend=dict(
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='center',
                x=0.5
            ))
            st.plotly_chart(fig,use_container_width=True)

    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Μονάδων Εργασίας ΛΥΨΥ</h3>", unsafe_allow_html=True)
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D18_lipsi'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Μ.Ε. ΛΥΨΥ')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='% Μεταβολή', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                yaxis=dict(title='Αρ.Μονάδων Εργασίας ΛΥΨΥ', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μεταβολή Μονάδων Εργασίας ΕΚΟ</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D18_eko'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Μ.Ε. ΕΚΟ')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='% Μεταβολή', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                yaxis=dict(title='Αρ.Μονάδων Εργασίας ΕΚΟ', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig,use_container_width=True)


    with st.container():
         col1, col2,col3 = st.columns(3)
         with col1:
             pass
         with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>Διαχρονική Κατανομή Μονάδων Εργασίας ΚοιΣΠΕ</h3>", unsafe_allow_html=True)

            # Select the relevant columns
            columns = ['D22', 'D23', 'D22_23_g']
            kpdf_selected = kpdf[columns]
            # Create the stacked bar plot using Plotly
            fig = go.Figure()
            legend_labels = ['Μ.Ε. ΛΥΨΥ', 'Μ.Ε. ΕΚΟ', 'Μ.Ε. Γεν.Πληθ.']
            for i, col in enumerate(columns):
                fig.add_trace(go.Bar(
                    name=legend_labels[i],  # Use the corresponding label
                    x=kpdf['year'].apply(str),
                    y=kpdf_selected[col],
                    text=kpdf[col],
                    textposition='inside'
                ))
            # Update the layout
            fig.update_layout(barmode='stack', xaxis_title='Έτος',yaxis_title='% επι του Συνόλου',legend=dict(
            orientation="h",  # Horizontal legends
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
            ),height=600, width=800)

            
            # Show the plot
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
        <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                    <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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

            fig = go.Figure(data=[go.Pie(labels=labels, values=[val26,val27,val28])])

            fig.update_traces(
                marker=dict(colors=colors),  # Assign colors from the color palette to the pie slices
                textinfo='percent+label'
            )

            # Update the layout
            fig.update_layout(
                legend=dict(
                    orientation="h",  # Horizontal legend
                    yanchor="bottom",    # Anchor legend to the top
                    y=1.1,           # Adjust the distance of the legend from the pie chart
                    bgcolor='rgba(255, 255, 255, 0)',  # Set legend background color as transparent
                    traceorder='normal'  # Maintain the order of the legend labels
                )
            )
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
            kpdf_selected = kpdf[columns]
            # Create the stacked bar plot using Plotly


            fig = go.Figure()
            legend_labels = ['Κτηρια & Εξ.Χώροι ','Εστίαση','Λοιπές Δραστηριότητες']
            for i, col in enumerate(columns):
                fig.add_trace(go.Bar(
                    name=legend_labels[i],  # Use the corresponding label
                    x=kpdf['year'].apply(str),
                    y=kpdf_selected[col],
                    text=kpdf[col],
                    textposition='inside',
                    marker=dict(color=colors[i])  # Assign a color from the color palette

                ))
            # Update the layout
            fig.update_layout(barmode='stack', xaxis_title='Έτος',yaxis_title='Συχνότητα',legend=dict(
            orientation="h",  # Horizontal legends
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0)',  # Set legend background color as transparent
            traceorder='normal'  # Maintain the order of the legend labels
            ),height=600, width=800)


            # Update the layout
            fig.update_layout(barmode='stack', xaxis_title='Έτος',yaxis_title='Συχνότητα')
            # Show the plot
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μετ.Kύκλ.Εργ. Κτήρια/Εξωτ. Χώροι</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D26'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
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

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center; color: grey;'>% Ετήσια Μετ.Κύκλ.Εργ. Λοιπ. Δραστ.</h3>", unsafe_allow_html=True)

            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D28'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 50px; background-color: #f1f1f1; width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
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

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig,use_container_width=True)
        with col2:

            st.markdown("<h3 style='text-align: center; color: grey;'>Συμμετοχή (%) Επιδοτήσεων στα έσοδα / Ετος</h3>", unsafe_allow_html=True)

             
            val39=float(kpdf['D39'][kpdf['year']==str(year_filter)].iloc[0])
            layout = go.Layout(
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=400,  # Set the height of the chart
                width=400,  # Set the width of the chart
                legend=dict(
                    orientation='h',
                    yanchor='top',
                    y=1.1,
                    xanchor='center',
                    x=0.5
                ),
                margin=dict(l=0, r=0, t=30, b=0, autoexpand=True)  # Set the margin to auto
            )
            fig = go.Figure(layout=layout)
            fig.add_trace(go.Pie(
                labels=['% Συμμετοχή Επιδοτήσεων', ' '],
                values=[val39,100-val39],
                hole=0.85,
                textinfo='none',
                marker_colors=['rgb(135 206 235)', 'rgb(240,240,240)'],
            ))
            fig.update_layout(annotations=[dict(text=str(val39) + "%", font_size=40, showarrow=False)])
            fig.update_layout(showlegend=True)  # Show the legend
            fig.update_layout(legend=dict(
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='center',
                x=0.5
            ))
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
    
