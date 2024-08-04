import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_filtering import filter_csv

all_crime_data = filter_csv()

# Dash app
app = dash.Dash(__name__)

# layout
app.layout = html.Div([
    html.H1("Toronto Crime Map"),

    # Dropdown to select crime type!!
    dcc.Dropdown(
        id='crime-type-dropdown',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Auto Theft', 'value': 'Auto Theft'},
            {'label': 'Assault', 'value': 'Assault'},
            {'label': 'Robbery', 'value': 'Robbery'}
        ],
        value='All',
        multi=True
    ),

    # Date range picker # cool feature on how we can make this calander shit thing where user can select daysss
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date='2014-01-01',
        end_date='2024-01-15',
        display_format='YYYY-MM-DD'
    ),

    # heatmap
    dcc.Graph(id='heatmap-graph')
])

# updating heatmap based on user
@app.callback(
    Output('heatmap-graph', 'figure'),
    [
        Input('crime-type-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ]
)
def update_heatmap(selected_crime_types, start_date, end_date):
    # Filter data based on the selected crime types
    if 'All' not in selected_crime_types:
        filtered_data = all_crime_data[all_crime_data['MCI_CATEGORY'].isin(selected_crime_types)]
    else:
        filtered_data = all_crime_data

    # Filter data based on the selected date range
    filtered_data = filtered_data[(filtered_data['DATE'] >= start_date) & (filtered_data['DATE'] <= end_date)]

    # Create the heatmap
    fig = px.scatter_mapbox(filtered_data, lat='LAT_WGS84', lon='LONG_WGS84', color='MCI_CATEGORY',
                            hover_name='MCI_CATEGORY',
                            hover_data={'LAT_WGS84': False, 'LONG_WGS84': False, 'MCI_CATEGORY': False, 'DATE': True,'PREMISES_TYPE':True},
                            zoom=12, height=650,
                            color_discrete_map={'Theft': 'blue', 'Assault': 'red', 'Robbery': 'green'})
    fig.update_layout(mapbox_style="open-street-map", mapbox_center_lat=43.65107, mapbox_center_lon=-79.347015)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
