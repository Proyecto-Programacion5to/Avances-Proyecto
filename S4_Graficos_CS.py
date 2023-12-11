import plotly.express as px
import pandas as pd
from dash import dcc
from PF_ArchivoConstantes_CS import data_query1, data_query2

def graph1():
    #LEER CSV
    query1 = pd.read_csv(data_query1)
    #GRAFICO DE COLUMAS CON QUERY 1
    columns = ["Celulares y Telefonia", "Electronica y Tecnologia", "Videojuegos", "Hogar y Jardin", "Deportes y Ocio",
               "Ferreteria y Autos", "Salud Belleza y Cuidado Personal"]
    fig_bar = px.bar(query1, x=columns, y="Cantidad",
                     color=columns)
    fig_bar.update_layout(xaxis_title="Clasificaciones")
    return dcc.Graph(figure=fig_bar)

#def graph2():


#SEGUNDO GRAFICO
def loadData(filename):
    data = pd.read_csv(filepath_or_buffer=data_query2, sep=",")
    data = data.iloc[:, 1:]
    return data

data = loadData(data_query2)



