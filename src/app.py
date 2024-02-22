from dash import Dash, html
import dash_bootstrap_components as dbc


# Variable that contains the external_stylesheet to use (ie.Flatly styling from dash bootstrap components (dbc))
external_stylesheets = [dbc.themes.LITERA]

# Variable that contains the meta tags (to ensure responsive design)
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__,external_stylesheets=external_stylesheets,meta_tags=meta_tags)

# Define the three rows of the app layout 

#style={"textAlign":"center", "color":"green","font-weight": "bold","font":"Times New Roman", "font-family":"Copperplate"}
#style={"color": "green", "fontSize": 20, "font-weight":"bold", "font-family":"Copperplate"}
# #"In one single page, learn about what students who graduated from your exact course went on to do after graduation,\
#                          how much they get paid and how satisfied they are with their current job.\
#                          Our goal at GRAD:ME! is to make post-graduation seem less scary and we hope that this dashboard will help,\
#                          even just a little :)", id="third_paragraph_row1"
# html.P("Here, you will find all the info you need in ONE SINGLE page!", id="third_paragraph_row1")
row_one = html.Div(
    # dbc.Row([
    #     dbc.Col([html.H1("GRAD:ME! Dashboard", id='app_header'), 
    #              html.P("Are you a final year undergraduate student? Getting nervous about the next steps as graduation approaches?\
    #                     Tired of browsing tens of different websites to get reliable information regarding post-graduation life?", id="first_paragraph_row1"),
    #              html.P("Welcome to GRAD:ME! Dashboard !",id="second_paragraph_row1", style={"font-weight":"bold"}),
    #              ], width={"size": 12}),
    # ]),
        dbc.Row([
        dbc.Col([html.H1("Welcome to GRAD:ME! Dashboard", id='app_header'), 
                 html.P("Find all the infomation you need regarding employment prospects after graduation in ONE SINGLE PAGE !", id="first_paragraph_row1"),
                 ], width={"size": 12}),
    ]),
)

row_two = html.Div(
    dbc.Row([
        dbc.Col(children=[dbc.Label("Select your course"), 
                          dbc.Select(id="type-dropdown",
                                     # id uniquely identifies the element, will be needed later
                                     options=[
                                         {"label": "COURSE 1", "value": "course"},
                                         # The value is in the format of the column heading in the data
                                         {"label": "COURSE 2", "value": "course"},
                                         {"label": "COURSE 3", "value": "course"},
                                         {"label": "COURSE 4", "value": "course"},
                                     ],
                                     value="COURSE 1",  # The default selection,
                                     #id="course_name_selector"
                                     ),
                          ], width=4),
        dbc.Col(children=[dbc.Label("Select your study mode"), 
                          dbc.RadioItems(
                            options=[
                                {"label": "Full-Time", "value": 1},
                                {"label": "Part-Time", "value": 2}
                            ],
                            value=1,
                            id="kis_mode_selector")],
                            width=4),
        dbc.Col(children=[dbc.Label("Select your kis level"), 
                    dbc.RadioItems(
                    options=[
                        {"label": "3", "value": 3},
                        {"label": "4", "value": 4}
                    ],
                    value=3,
                    id="kis_level_selector")],
                    width=4)
    ]),
)
row_three = html.Div(
    dbc.Row([
        dbc.Col(children=[
            html.Img(src=app.get_asset_url('map-placeholder.png'), className="img-fluid"),
        ], width=8),
        dbc.Col(children=[
            dbc.Card(
                [
                    dbc.CardImg(src=app.get_asset_url('logos/2022_Beijing.jpg'), top=True, style={"width": "200px"}),
                    dbc.CardBody(
                        [
                            html.H4("TownName 2026", className="card-title"),
                            html.P(
                                "Highlights of the paralympic event will go here. This will be a sentence or two.",
                                className="card-text",
                            ),
                            html.P(
                                "Number of athletes: XX",
                                className="card-text",
                            ),
                            html.P(
                                "Number of events: XX",
                                className="card-text",
                            ),
                            html.P(
                                "Number of countries: XX",
                                className="card-text",
                            ),
                        ]
                    ),
                ],
                style={"width": "18rem"},
            )

        ], width=4),
    ], align="start")
)

# Add an HTML layout to the Dash app.
# The layout is wrapped in a DBC Container()
app.layout = dbc.Container([
    row_one,
    row_two,
    row_three
])

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
    # Runs on port 8050 by default. If you have a port conflict, add the parameter port=   e.g. port=8051
