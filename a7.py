# FIFA World Cup Winners Dashboard
# Hosted at: [Your Render Deployment Link]

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Create dataset
world_cup_data = [
    (1930, "Uruguay", "Argentina"), (1934, "Italy", "Czechoslovakia"), (1938, "Italy", "Hungary"), 
    (1950, "Uruguay", "Brazil"), (1954, "Germany", "Hungary"), (1958, "Brazil", "Sweden"),
    (1962, "Brazil", "Czechoslovakia"), (1966, "England", "Germany"),
    (1970, "Brazil", "Italy"), (1974, "Germany", "Netherlands"), (1978, "Argentina", "Netherlands"), 
    (1982, "Italy", "Germany"), (1986, "Argentina", "Germany"), 
    (1990, "Germany", "Argentina"), (1994, "Brazil", "Italy"), (1998, "France", "Brazil"),
    (2002, "Brazil", "Germany"), (2006, "Italy", "France"),
    (2010, "Spain", "Netherlands"), (2014, "Germany", "Argentina"), (2018, "France", "Croatia"), (2022, "Argentina", "France")
]

df = pd.DataFrame(world_cup_data, columns=["Year", "Winner", "Runner-up"])
win_counts = df["Winner"].value_counts().reset_index()
win_counts.columns = ["Country", "Wins"]

# Get a list of all countries
all_countries = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv")
all_countries = all_countries[["COUNTRY"]]
all_countries.columns = ["Country"]

# Merge with win_counts to include countries with 0 wins
win_counts = all_countries.merge(win_counts, on="Country", how="left").fillna(0)
win_counts["Wins"] = win_counts["Wins"].astype(int)

# Define color scale
color_scale = [
    (0, "gray"),
    (0.01, "yellow"),  # >0 wins → yellow
    (1, "red")  # Max wins → red
]

# Create Choropleth Map
fig = px.choropleth(
    win_counts, locations="Country", locationmode="country names",
    color="Wins", hover_name="Country",
    color_continuous_scale=color_scale, title="FIFA World Cup Wins by Country"
)

# Dash App
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),
    dcc.Graph(figure=fig),
    html.Label("Select a Country to View Wins:"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in win_counts["Country"].unique()],
        value="Brazil",
    ),
    html.Div(id="country-output"),
    html.Label("Select a Year to View Winner & Runner-up:"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": y, "value": y} for y in df["Year"].unique()],
        value=2022,
    ),
    html.Div(id="year-output")
])

@app.callback(
    dash.Output("country-output", "children"),
    [dash.Input("country-dropdown", "value")]
)
def update_country(selected_country):
    wins = win_counts.loc[win_counts["Country"] == selected_country, "Wins"].values[0]
    return f"{selected_country} has won {wins} times."

@app.callback(
    dash.Output("year-output", "children"),
    [dash.Input("year-dropdown", "value")]
)
def update_year(selected_year):
    row = df[df["Year"] == selected_year].iloc[0]
    return f"{row['Year']}: Winner - {row['Winner']}, Runner-up - {row['Runner-up']}"

if __name__ == "__main__":
    app.run_server(debug=True)