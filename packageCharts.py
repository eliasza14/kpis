import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

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


def stackedChart(columns, kpdf, legend_labels, xaxis_title, yaxis_title, colors):
    # Create the stacked bar plot using Plotly
    kpdf_selected = kpdf[columns]

    fig = go.Figure()

    for i, col in enumerate(columns):
        fig.add_trace(go.Bar(
            name=legend_labels[i],  # Use the corresponding label
            x=kpdf['year'].astype(int),
            y=kpdf_selected[col],
            # text=kpdf[col],
            # textposition='inside',  # 'inside' places the text at the center of the bars
            marker=dict(color=colors[i]),  # Assign a color from the color palette
            # textfont=dict(size=14, color='red')  # Set the font size and color for the labels
        ))
    
    # Add values at the center and middle of each stacked bar
    for j in range(len(kpdf)):
        cumulative_height = 0
        for i, col in enumerate(columns):
            val = kpdf_selected[col].iloc[j]
            cumulative_height += val
            fig.add_annotation(x=kpdf['year'].iloc[j], y=cumulative_height - val / 2,
                               text=f"<b>{str(round(val, 1))}%</b>", showarrow=False,
                               font=dict(family='Roboto',color='white', size=16), xanchor='center', yanchor='middle')
    
    # Update the layout
    fig.update_layout(
        barmode='stack',
        xaxis=dict(
            title=xaxis_title,
            tickmode='linear',  # Display linear sequence of ticks
            dtick=1,  # Specify tick interval as 1 for integer values
            tickfont=dict(size=25)
        ),
        yaxis=dict(title=yaxis_title),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        width=800
    )

    return fig

# def stackedChart(columns,kpdf,legend_labels,xaxis_title,yaxis_title,colors):
#     # Create the stacked bar plot using Plotly
#     kpdf_selected = kpdf[columns]

#     fig = go.Figure()
#     legend_labels=legend_labels
#     # legend_labels = ['Γενικού Πληθυσμού', 'ΛΥΨΥ', 'ΕΚΟ']
    
#     for i, col in enumerate(columns):
#         fig.add_trace(go.Bar(
             
#             name=legend_labels[i],  # Use the corresponding label
#             x=kpdf['year'].astype(int),
#             y=kpdf_selected[col],
#             text=kpdf[col],
#             textposition='inside',
#             marker=dict(color=colors[i])  # Assign a color from the color palette

#         ))
#      # Update the layout
#     fig.update_layout(
#         barmode='stack',
#         xaxis=dict(
#             title=xaxis_title,
#             tickmode='linear',  # Display linear sequence of ticks
#             dtick=1  # Specify tick interval as 1 for integer values
#         ),
#         yaxis=dict(title=yaxis_title),
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="center",
#             x=0.5
#         ),
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         height=600,
#         width=800
#     )

#     return fig



def pctChangeV2(categories, values, line_labels, yaxis_title, legend_bar):
    categories = list(map(int, categories))

    # Create the bar plot
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=values, name=legend_bar, marker_color='steelblue'))

    # Create the line plot with labels
    line_trace = go.Scatter(x=categories, y=values, name='% Μεταβολή', mode='lines', line_color='red')
    fig.add_trace(line_trace)

    # Add labels between the years with dynamic y-positioning
    y_offset = max(values) * 0.1 # Adjust this value to change the vertical offset
    for i in range(len(categories) - 1):
        label = line_labels[i + 1]
        if not pd.isna(label):
            x_label = [categories[i], categories[i + 1]]
            y_label = [values[i], values[i + 1]]
            fig.add_annotation(x=sum(x_label) / 2, y=sum(y_label) / 2 + y_offset, text=f"{label} %", showarrow=False,
                               font=dict(color='red', size=15))  # Adjust the font size as needed

    # Add values at the center of each bar
    for i in range(len(values)):
        fig.add_annotation(x=categories[i], y=values[i] / 2, text=str(round((values[i]), 1)), showarrow=False,
                           font=dict(color='white', size=15), xanchor='center', yanchor='middle')

    # Set the layout
    fig.update_layout(
        xaxis=dict(
            title='Έτος',
            tickmode='linear',
            dtick=1
        ),
        yaxis_title=yaxis_title,
    )
    return fig









# def pctChangeV2(categories,values,line_labels,yaxis_title,legend_bar):
    
#     categories=list(map(int, categories))
#     # Create the bar plot
#     fig = go.Figure()
#     fig.add_trace(go.Bar(x=categories, y=values, name=legend_bar, marker_color='steelblue'))

#     # Create the line plot with labels from 'd16' column
#     line_trace = go.Scatter(x=categories, y=values, name='% Μεταβολή', mode='lines', line_color='red')
#     fig.add_trace(line_trace)

#     # Add labels between the years
#     for i in range(len(categories) - 1):
#         label = line_labels[i + 1]
#         if not pd.isna(label):
#             x_label = [categories[i], categories[i + 1]]
#             y_label = [values[i],values[i + 1]]
#             fig.add_annotation(x=sum(x_label) / 2, y=sum(y_label) / 2 + 1, text=f"{label} %", showarrow=False,
#                             font=dict(color='red', size=15))  # Adjust the font size as needed

#     # Add d12 values at the center of each bar
#     for i in range(len(values)):
#         fig.add_annotation(x=categories[i], y=values[i] / 2, text=str(round((values[i]),1)), showarrow=False,
#                         font=dict(color='white', size=15), xanchor='center', yanchor='middle')

#     # Set the layout
#     fig.update_layout(
#         xaxis=dict(
#             title='Έτος',
#             tickmode='linear',
#             dtick=1
#         ),
#         yaxis_title=yaxis_title,
#     )
#     return fig


def pctChangeChart(values, categories, yaxis_title, yaxis2_title, line_legend, bar_trace_legend):
    # Calculate percentage change
    percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

    # Create the bar trace
    bar_trace = go.Bar(x=categories, y=values, name=bar_trace_legend)

    # Create the line trace
    line_trace = go.Scatter(x=categories[1:], y=percentage_change, name=line_legend, mode='lines+markers', yaxis='y2')

    # Create the layout with two y-axes
    layout = go.Layout(
        # title='Μεταβολή ωρών απασχόλησης ΛΥΨΥ',
        yaxis=dict(title=yaxis_title, rangemode='nonnegative'),
        yaxis2=dict(title=yaxis2_title, overlaying='y', side='right', showgrid=False),
        height=600,  # Set the height of the chart
        width=400  # Set the width of the chart
    )

    # Convert categories to integers
    categories_int = [int(category) for category in categories]

    # Update the x-axis tick values to integers
    layout.update(xaxis=dict(tickmode='array', tickvals=categories_int))

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
            x=categories[i + 1], y=percentage_change[i],
            text=f"{percentage_change[i]:.2f}%",
            showarrow=False,
            font=dict(color='red', size=12),
            xanchor='center', yanchor='bottom'
        )

    return fig








# def pctChangeChart(values,categories,yaxis_title,yaxis2_title,line_legend,bar_trace_legend):
#     # Calculate percentage change
#     percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

#     # Create the bar trace
#     bar_trace = go.Bar(x=categories, y=values, name=bar_trace_legend)

#     # Create the line trace
#     line_trace = go.Scatter(x=categories[1:], y=percentage_change, name=line_legend, mode='lines+markers', yaxis='y2')

#     # Create the layout with two y-axes
#     layout = go.Layout(
#         # title='Μεταβολή ωρών απασχόλησης ΛΥΨΥ',
#         yaxis=dict(title=yaxis_title, rangemode='nonnegative'),
#         yaxis2=dict(title=yaxis2_title, overlaying='y', side='right', showgrid=False),
#         height=600,  # Set the height of the chart
#         width=400  # Set the width of the chart
#     )

#     # Create the figure
#     fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

#     # Add labels to the bars
#     for i in range(len(categories)):
#         fig.add_annotation(
#             x=categories[i], y=values[i],
#             text=str(values[i]),
#             showarrow=False,
#             font=dict(color='black', size=12),
#             xanchor='center', yanchor='bottom'
#         )

#     # Add labels to the percentage change
#     for i in range(len(percentage_change)):
#         fig.add_annotation(
#             x=categories[i+1], y=percentage_change[i],
#             text=f"{percentage_change[i]:.2f}%",
#             showarrow=False,
#             font=dict(color='red', size=12),
#             xanchor='center', yanchor='bottom'
#         )

#     return fig

def donut_pct_Chart(val,color1,color2,labels):

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
    labels=labels,
    values=[val, 100 - val],
    hole=0.85,
    textinfo='none',
    marker_colors=[color1, color2],
    direction='clockwise',  # Set the direction to clockwise for right-side starting
    sort=False, 


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

    return fig


def pieChart(labels,values,colors):

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

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

    return fig


def stackedChart2(columns,kpdf,legend_labels,xaxis_title,yaxis_title,colors):
    # Create the stacked bar plot using Plotly
    kpdf_selected = kpdf[columns]

    fig = go.Figure()
    legend_labels=legend_labels
    # legend_labels = ['Γενικού Πληθυσμού', 'ΛΥΨΥ', 'ΕΚΟ']
    
    for i, col in enumerate(columns):
        fig.add_trace(go.Bar(
             
            name=legend_labels[i],  # Use the corresponding label
            x=kpdf['year'].astype(int),
            y=kpdf_selected[col],
            text=kpdf[col],
            textposition='inside',
            marker=dict(color=colors[i])  # Assign a color from the color palette

        ))
    # Update the layout
    fig.update_layout(
        barmode='stack',
        xaxis=dict(
            title=xaxis_title,
            tickmode='linear',
            dtick=1
        ),
        yaxis=dict(title=yaxis_title),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0)',
            traceorder='normal'
        ),
        height=600,
        width=800
    )

    return fig
     
     


        

