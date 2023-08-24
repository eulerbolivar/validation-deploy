import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


# INICIALIZAÇÃO
load_figure_template("slate")
app = dash.Dash(
    external_stylesheets=[dbc.themes.SLATE]
)
server = app.server

# INGESTÃO DE DADOS
df_data = pd.read_csv("dados_vendas.csv")
df_data["Data"] = pd.to_datetime(df_data["Data"])

# ,style={"border": "solid red 1px"}

# LAYOUT
app.layout = html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H2("NomeEmpresa", style={"font-family": "Voltaire", "font-size": "40px", "text-align": "center", "margin-top": "10px"}),
                        html.Hr(),

                        html.H5("Responsáveis:"),
                        dcc.Checklist(df_data["Responsavel"].value_counts().index, df_data["Responsavel"].value_counts().index, id="check_resp", inputStyle={"margin-right": "8px"}),
                    ], style={"height": "95vh", "margin": "15px", "padding": "10px"})
                ], sm=2),

                dbc.Col([
                    dbc.Row([
                        dbc.Col([dcc.Graph(id="controle_fig", className="graph"),], sm=4),
                        dbc.Col([dcc.Graph(id="1", className="graph"),], sm=4),
                        dbc.Col([dcc.Graph(id="2", className="graph"),], sm=4),
                    ], style={"margin": "0px"}),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id="3", className="graph"),], sm=4),
                        dbc.Col([dcc.Graph(id="4", className="graph"),], sm=4),
                        dbc.Col([dcc.Graph(id="5", className="graph"),], sm=4),
                    ], style={"margin": "0px"}),
                    
                ],style={"height": "95vh", "margin-top": "15px", "border": "solid black 1px", "border-radius": "10px"}, sm=10),
            ], ),
        ])


# CALLBACKS
@app.callback(
            Output('controle_fig', 'figure'),
            [
                Input('check_resp', 'value'),
            ]
)

def render_graphs(responsavel):

    df_filtered = df_data[df_data["Responsavel"].isin(responsavel)]
    controle = ["Tasks", "E-mail", "Follow Up", "Whatsapp", "Social Media"]
    
    df_controle = df_filtered.groupby("Responsavel")[controle].apply(np.sum).reset_index()
    fig_controle = px.bar(df_controle, x="Responsavel", y=controle)

    fig_controle.update_layout(template="slate")

    return fig_controle

# EXECUÇÃO
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
