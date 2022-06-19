# Import required libraries
import pandas as pd
import dash # Ver 2.5.1 which requires the following imports.
from dash import html
# import dash_html_components as html
from dash import dcc
# import dash_core_components as dcc

# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output


import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv", index_col = 0)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# figpie = px.pie(spacex_df, values= 'class', names='Launch Site', title='total successful launches by launch site')
# figscat1  = px.scatter(spacex_df, x= 'Payload Mass (kg)', y = 'class',  color = 'Booster Version Category', title='Correlation between Payload and Success for Site')
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                                'font-size': 40}),
            # TASK 1: Add a dropdown list to enable Launch Site selection
            # The default select value is for ALL sites
            dcc.Dropdown(options = [{'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, {'label': 'KSC LC-39A','value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}], searchable=True,
                          placeholder = 'Select a Launch Site here',  multi= False, value='ALL', id='site-dropdown'),
            
            
            
            
            html.Br(),

            # TASK 2: Add a pie chart to show the total successful launches count for all sites
            # If a specific launch site was selected, show the Success vs. Failed counts for the site
            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br(),

            html.P("Payload range (Kg):"),
            # TASK 3: Add a slider to select payload range
            dcc.RangeSlider(min = min_payload, max = max_payload, step = 1000,
                            value = [min_payload, max_payload],
                            # marks = {0:'0 kg', 5000:'5000 kg'},
                            id='payload-slider'),
# marks = {0:{'label':'0','style':{'color': 'black', 'font-size':'40px'}},
# 2500:{'label':'2500','style':{'color': 'black', 'font-size':'40px'}}, 5000:'5000', 7500:'7500', 10000:'10000'}
            # TASK 4: Add a scatter chart to show the correlation between payload and launch success
            html.Div(dcc.Graph(id='success-payload-scatter-chart')),
            ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property= 'figure'),
                Input(component_id='site-dropdown', component_property='value'))

def get_pie(site = 'ALL'):
    if site == 'ALL':
        figure = px.pie(spacex_df, values= 'class', names='Launch Site', title='total successful launches by launch site')
    else:
        df_mask = spacex_df.query('`Launch Site` == @site')
        figure = px.pie(df_mask, names = 'class', title= 'total successful launches for site ' + site)

    return figure
    


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# add callback decorator
@app.callback( Output(component_id='success-payload-scatter-chart', component_property= 'figure'),
                [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property='value')])

def get_graph(site = 'ALL', slideval =[min_payload, max_payload]):

    if site == 'ALL':
        df_mask = spacex_df.query('`Payload Mass (kg)` < @slideval[1] & `Payload Mass (kg)` > @slideval[0]')
        figure = px.scatter(df_mask, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title='Correlation between Payload and Success for all Sites')
    else:
        df_mask1 = spacex_df.query('`Launch Site` == @site & `Payload Mass (kg)` < @slideval[1] & `Payload Mass (kg)` > @slideval[0]')
        figure = px.scatter(df_mask1, x= 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title='Correlation between Payload and Success for Site')

    return figure

# Run the app
if __name__ == '__main__':
    app.run_server()
