

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas DataFrame
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create the dropdown options for Launch Site selection
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df["Launch Site"].unique()]

# Define the layout of the application
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown', options=launch_sites, value='ALL',
                 placeholder="Select a Launch Site here", searchable=True),
    html.Br(),

    dcc.Graph(id='success-pie-chart'),

    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider', min=min_payload, max=max_payload, step=1000,
                     value=[min_payload, max_payload],
                     marks={i: str(i) for i in range(0, int(max_payload) + 1000, 1000)}),

    dcc.Graph(id='success-payload-scatter-chart')
])

# Define callback to update success-pie-chart based on site selection
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['class'] == 1]
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site', 
            title='Total Success Launches By All Sites'
        )
        return fig
    else:
        specific_site = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            specific_site,
            names='class',
            title='Launch status by: ' + entered_site
        )
        return fig

# Define callback to update success-payload-scatter-chart based on site and payload range selection
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Payload Success Scatter Plot'
        )
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)', y='class', color='Booster Version Category',
            title='Payload Success Scatter Plot for ' + selected_site
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
