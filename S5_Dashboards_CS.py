import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from S4_Graficos_CS import graph1, data
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from ArchivoConstantes_CS import data_query2


""""
DASHBOARDS
"""

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#E6FFFA",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("ClaroShop", className="display-4"),
        html.Hr(),
        html.P(
            "Visualización de Datos", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Dashboard 1", href="/page-1", active="exact"),
                dbc.NavLink("Dashboard 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url",
                                                         "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H1('PROYECTO FINAL:', style={'color': '#008080'}),
            html.H1('Aplicación del proceso ETL para la tienda Claro Shop.', style={'color': '#008080'}),
            html.Br(),
            html.H2("Objetivo General:", style={'color': '#2F4F4F'}),
            html.P('El objetivo principal de este proyecto es aplicar el porceso de ETL a los ofertas de la tienda en línea '
                   '“Claro Shop”; desarrollando e implementando un programa de web scraping que recopile sus ofertas vigentes, '
                   'para posteriormente transformar esos datos y presentarlos en un dashboard, facilitando de esa manera su '
                   'análisis detallado y su utilidad en la toma de decisiones informadas para nuestro cliente que es competencia '
                   'de Claro Shop. ', style={'text-align': 'justify'}),
            html.Br(),
            html.H2("Cursos:", style={'color': '#2F4F4F'}),
            html.P("Programación para la Extracción de Datos | Administración de Proyectos."),
            html.Br(),
            html.H3("Elaborado Por:", style={'color': '#2F4F4F'}),
            html.P("-Argüelles Aguilera Karla Daniela"),
            html.P("-Jacinto Cano Ana Beatriz"),
            html.P("-Marina Cazares Kattherine Guadalupe"),
            html.P("-Martínez Pérez Rubí Belén"),
            html.P("-Morales López Yajaira Sucet"),
            html.Br(),
            html.H3("GitHub:", style={'color': '#2F4F4F'}),
            html.A("Proyecto-Programacion5to", href="https://github.com/Proyecto-Programacion5to")
        ])
    elif pathname == "/page-1":
        graph = graph1()
        return html.Div([
            html.H1('"Cantidad de Productos con Descuento por Clasificación"',  style={'color': '#008080', 'textAlign': 'center'}),
            html.Br(),
            html.H2("Análisis:", style={'color': '#2F4F4F'}),
            html.P('Esta gráfica nos permite ver que las clasificaciones  "Hogar y Jardín", "Deportes y Ocio" y "Electrónica y Tecnología" '
                   'son en donde estan la mayoría de los productos con descuento. A la competencia estos datos le proporcionarán ideas para '
                   'establecer precios competitivos, realizar ofertas similares, expander su inventario,  identificar brechas en el mercado, '
                   'desarrollar nuevos productos y/o reorientar sus estrategias comerciales en las categorías con más o menos productos en descuento, '
                   'según a la competencia le convenga.', style={'text-align': 'justify'}),
            html.Br(),
            graph
        ])
    elif pathname == "/page-2":




"""
SEGUNDO MENU
"""

if __name__ == "__main__":
    app.run_server(port=8888)

