import dash
import pandas as pd
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/dWLwgP.css"]
tickFont = {'size': 9, 'color': 'rgb(30,30,30)'}

def loadData(filename):
    data = pd.read_csv("Query2.csv", sep=",")
    data = data.iloc[:, 1:]
    return data

data = loadData("Query2.csv")

clasificacion = data['Clsificacion'].unique()
clasificacion.sort()
options = [{'label': c, 'value': c} for c in clasificacion]

app = dash.Dash()
app.title = 'Descuentos Dashboard'

app.layout = html.Div([
    html.H1('Descuentos por producto'),
    html.Div(
        dcc.Dropdown(
            id='clasification_picker',
            options=options,
            value='celulares-y-telefonia-li'
        ),
        style={'width': '35%'}
    ),
    dcc.Graph(
        id='descuentos_product',
        config={'displayModeBar': False}
    )
])

@app.callback(Output(component_id='descuentos_product', component_property='figure'),
              [Input(component_id='clasification_picker', component_property='value')])
def update_chart(selected_clasification):
    filter_dt = data[data["Clsificacion"] == selected_clasification]
    fig = go.Figure(data=[go.Scatter(
        x=filter_dt['Producto'],
        y=filter_dt['Descuento'],
        mode='lines+markers',
        marker=dict(color='firebrick')
    )])
    fig.update_layout(title='Descuentos por producto {}'.format(selected_clasification),
                      xaxis=dict(tickangle=-90, ticktext=filter_dt['Producto'], tickfont=tickFont, type='category'))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
