# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("Week 3\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'}, {
                                    'label': spacex_df['Launch Site'].unique()[0], 'value': spacex_df['Launch Site'].unique()[0]}, {
                                    'label': spacex_df['Launch Site'].unique()[1], 'value': spacex_df['Launch Site'].unique()[1]}, {
                                    'label': spacex_df['Launch Site'].unique()[2], 'value': spacex_df['Launch Site'].unique()[2]}, {
                                    'label': spacex_df['Launch Site'].unique()[3], 'value': spacex_df['Launch Site'].unique()[3]}],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.H1('Pie Chart'),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider', min=0, max=10000, step=1000, marks={i: str(i) for i in range(0, 10001, 2500)},
                                    value=[min_payload, max_payload]
),
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success

    html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site', 'class']]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
                     names='Launch Site',
                     title='Total Sucess Launches By Site')
    else:
        fig = px.pie(filtered_df[filtered_df['Launch Site'] == entered_site].value_counts().reset_index().replace({'class': {0: 'Fail', 1: 'Success'}}), values=0,
                     names='class',
                     title=f'Total Sucess Launches By {entered_site}')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(site, payload):
    filtered_df = spacex_df[['Launch Site', 'class',
                             'Payload Mass (kg)', 'Booster Version']]
    pd.set_option('mode.chained_assignment', None)
    filtered_df['Booster Version'] = filtered_df['Booster Version'].str.split(
        ' ', expand=True)[1]
    low, high = payload
    # There are some error when using int value row True or False statement checking on my pandas version, have tried to fix it but didn't find the solution. Came up
    # with alternative of using isin method
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)'].isin(
        list(range(low, high+1, 1)))]
    if site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version",
        )
    else:
        fig = px.scatter(
            filtered_df[filtered_df['Launch Site'] == site],
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version"
        )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
