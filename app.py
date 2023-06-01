from dash import Dash, html,dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

hurtos = pd.read_csv('https://drive.google.com/uc?export=download&id=1FvzVgsyJEiQGevrS1DVyPfY_88AuluQ4', dayfirst=True)

app.layout = dbc.Container(
    [
        html.H1("Comparación municipios"),
        html.Label("Seleccione municipio 1"),
        dcc.Dropdown(hurtos['DEPARTAMENTO'].unique(),'ANTIOQUIA',id ="departamento_1"),
        html.Label("Seleccione municipio 2"),
        dcc.Dropdown(hurtos['DEPARTAMENTO'].unique(),'BOGOTÁ D.C.',id ="departamento_2"),
        html.Div(id="output")
    ]
)

@callback(
    Output("output", "children"),
    Input("departamento_1", "value"),
    Input("departamento_2", "value"),
)

def comparar(departamento_1, departamento_2):
    hurtos["FECHA"] = pd.to_datetime(hurtos["FECHA HECHO"], format="%d/%m/%Y")
    
    hurto_1 = hurtos.query("DEPARTAMENTO == @departamento_1")
    hurto_2 = hurtos.query("DEPARTAMENTO == @departamento_2")
    
    
    return dcc.Graph(
        figure={
            "data":
                [
                    go.Bar(
                        x = hurto_1["FECHA"],
                        y = hurto_1["CANTIDAD"],
                        name = departamento_1,
                        width=0.5,
                        offset=0.2
                        
                    ),
                    go.Bar(
                        x = hurto_2["FECHA"],
                        y = hurto_2["CANTIDAD"],
                        name = departamento_2,
                        width=0.5,
                        offset=-0.2
                    
                    )
                ],
            "layout": go.Layout(
                    title="Cantidad de hurtos entre dos departamentos",
                    xaxis = {"title": "Fecha"},
                    yaxis = {"title": "Cantidad de hurtos"},
                    barmode="group",
                )
        }
    )


if __name__ == "__main__":
    app.run_server(debug=True)
