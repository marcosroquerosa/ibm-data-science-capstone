# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Launch site options for the dropdown (ALL + each site in the data)
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site} for site in sorted(spacex_df['Launch Site'].unique())
]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=site_options,
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: str(i) for i in range(0, 10001, 2500)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # total successful launches (sum of class) contributed by each site
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total Success Launches By Site')
        return fig
    # success (class=1) vs. failure (class=0) counts for the selected site
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    outcome_counts = filtered_df['class'].value_counts().reset_index()
    outcome_counts.columns = ['class', 'count']
    outcome_counts['Outcome'] = outcome_counts['class'].map({1: 'Success', 0: 'Failure'})
    fig = px.pie(outcome_counts, values='count', names='Outcome',
                 title=f'Total Success Launches for site {entered_site}',
                 color='Outcome', color_discrete_map={'Success': '#2ca02c', 'Failure': '#d62728'})
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]
    if entered_site == 'ALL':
        title = 'Correlation between Payload and Success for all Sites'
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        title = f'Correlation between Payload and Success for site {entered_site}'
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category', title=title,
                     hover_data=['Booster Version'])
    return fig


# Run the app
if __name__ == '__main__':
    app.run()
