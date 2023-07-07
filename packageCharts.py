import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#GAUGE CHART

def gaugeChart(value,color):
        # Create the figure and gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': '%'}
        ))

        # Customize the appearance of the gauge chart
        fig.update_traces(
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': color,'thickness': 0.7},
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

        return fig

def stackedChart(columns,kpdf,legend_labels,xaxis_title,yaxis_title):
    # Create the stacked bar plot using Plotly
    kpdf_selected = kpdf[columns]

    fig = go.Figure()
    legend_labels=legend_labels
    # legend_labels = ['Γενικού Πληθυσμού', 'ΛΥΨΥ', 'ΕΚΟ']
    
    for i, col in enumerate(columns):
        fig.add_trace(go.Bar(
             
            name=legend_labels[i],  # Use the corresponding label
            x=kpdf['year'].apply(str),
            y=kpdf_selected[col],
            text=kpdf[col],
            textposition='inside'
        ))
    # Update the layout
    fig.update_layout(barmode='stack', xaxis_title=xaxis_title,yaxis_title=yaxis_title,legend=dict(
    orientation="h",  # Horizontal legends
    yanchor="bottom",
    y=1.02,
    xanchor="center",
    x=0.5
    ),height=600, width=800)

    return fig
        

