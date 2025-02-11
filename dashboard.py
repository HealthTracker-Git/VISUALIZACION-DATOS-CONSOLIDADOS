# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 12:25:55 2025

@author: osmor
"""


# PARA TODOS LOS AÑOS CON UN RESPECTIVO CODIGOPRESTACION

import pandas as pd
import plotly.express as px
import plotly.io as pio

# Configurar el renderizador para mostrar el gráfico en el navegador
pio.renderers.default = "browser"

# Ruta del archivo CSV
file_path = r"C:\Users\osmor\Downloads\SECCIÓN-A-CONSULTAS-MÉDICAS.csv"

# **Leer el CSV con delimitador correcto**
df = pd.read_csv(file_path, delimiter=";", dtype={'MES': str, 'ANO': int, 'CODIGOPRESTACION': str, 'TOTAL': float})

# **Verificar que las columnas ahora sean correctas**
print("Columnas después de corregir delimitador:")
print(df.columns)

# **Eliminar espacios en blanco en nombres de columnas**
df.columns = df.columns.str.strip()

# **Verificar si las columnas clave existen después del ajuste**
columnas_interes = ['MES', 'ANO', 'CODIGOPRESTACION', 'TOTAL']
for col in columnas_interes:
    if col not in df.columns:
        print(f"⚠️ Advertencia: La columna '{col}' no está en el archivo CSV.")

# **Si todas las columnas existen, continuar con el procesamiento**
if all(col in df.columns for col in columnas_interes):
    df = df[columnas_interes]

    # Convertir MES a nombre del mes para mejor visualización
    meses_dict = {
        "1": "Enero", "2": "Febrero", "3": "Marzo", "4": "Abril", "5": "Mayo",
        "6": "Junio", "7": "Julio", "8": "Agosto", "9": "Septiembre", "10": "Octubre",
        "11": "Noviembre", "12": "Diciembre"
    }
    df['MES'] = df['MES'].astype(str).map(meses_dict)

    # Ordenar los meses correctamente
    df['MES'] = pd.Categorical(df['MES'], categories=[
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
        "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ], ordered=True)

    # **Agrupar los datos por MES, AÑO y CODIGOPRESTACION, sumando el TOTAL**
    df_agrupado = df.groupby(['MES', 'ANO', 'CODIGOPRESTACION'], as_index=False)['TOTAL'].sum()

    # **Diagnóstico: Ver datos agrupados**
    print("Datos agrupados (primeras filas):")
    print(df_agrupado.head())

    # **Verificar valores únicos de CODIGOPRESTACION**
    print("Códigos de prestación únicos:", df_agrupado['CODIGOPRESTACION'].unique())

    # **Seleccionar un código específico para visualizar**
    codigo_seleccionado = "3020201"  # Puedes cambiarlo por otro código de tu interés

    # **Filtrar por el código de prestación**
    df_filtrado = df_agrupado[df_agrupado['CODIGOPRESTACION'] == codigo_seleccionado]

    # **Verificar si df_filtrado tiene datos**
    if df_filtrado.empty:
        print(f"⚠️ Advertencia: No hay datos para el código de prestación {codigo_seleccionado}")
    else:
        print("Datos filtrados:")
        print(df_filtrado.head())

        # **Crear gráfico interactivo**
        fig = px.line(
            df_filtrado,
            x="MES",
            y="TOTAL",
            color="ANO",  # Diferenciar los años por color
            title=f"Evolución Mensual de Consultas Médicas para Código {codigo_seleccionado} (2009-2023)",
            markers=True
        )

        # **Mostrar gráfico interactivo**
        fig.show()
else:
    print("⛔ No se puede continuar porque faltan columnas en el CSV.")

    
    #%%
    

# **Mostrar gráfico interactivo**
import plotly.io as pio
pio.renderers.default = "browser"  # Esto abrirá el gráfico en el navegador

fig.show()





#%%

# CON DASH

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Ruta del archivo CSV
file_path = r"C:\Users\osmor\Downloads\SECCIÓN-A-CONSULTAS-MÉDICAS.csv"

# **Leer el CSV con delimitador correcto**
df = pd.read_csv(file_path, delimiter=";", dtype={'MES': str, 'ANO': int, 'CODIGOPRESTACION': str, 'TOTAL': float})

# **Eliminar espacios en blanco en nombres de columnas**
df.columns = df.columns.str.strip()

# **Convertir MES a nombre del mes para mejor visualización**
meses_dict = {
    "1": "Enero", "2": "Febrero", "3": "Marzo", "4": "Abril", "5": "Mayo",
    "6": "Junio", "7": "Julio", "8": "Agosto", "9": "Septiembre", "10": "Octubre",
    "11": "Noviembre", "12": "Diciembre"
}
df['MES'] = df['MES'].astype(str).map(meses_dict)

# **Ordenar los meses correctamente**
df['MES'] = pd.Categorical(df['MES'], categories=[
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
], ordered=True)

# **Agrupar los datos por MES, AÑO y CODIGOPRESTACION, sumando el TOTAL**
df_agrupado = df.groupby(['MES', 'ANO', 'CODIGOPRESTACION'], as_index=False)['TOTAL'].sum()

# **Obtener la lista única de códigos de prestación**
codigos_prestacion_unicos = sorted(df_agrupado['CODIGOPRESTACION'].unique())

# **Inicializar la app de Dash**
app = dash.Dash(__name__)

# **Diseño de la aplicación**
app.layout = html.Div([
    html.H1("Evolución de Consultas Médicas", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Selecciona Código de Prestación:"),
        dcc.Dropdown(
            id='filtro-codigo',
            options=[{'label': codigo, 'value': codigo} for codigo in codigos_prestacion_unicos],
            value=codigos_prestacion_unicos[0],  # Primer código por defecto
            clearable=False
        ),
    ], style={'width': '50%', 'margin': 'auto'}),

    # Gráfico de evolución
    dcc.Graph(id='grafico-evolucion')
])

# **Callback para actualizar el gráfico según el código seleccionado**
@app.callback(
    Output('grafico-evolucion', 'figure'),
    [Input('filtro-codigo', 'value')]
)
def actualizar_grafico(codigo_seleccionado):
    df_filtrado = df_agrupado[df_agrupado['CODIGOPRESTACION'] == codigo_seleccionado]

    # Crear gráfico
    fig = px.line(
        df_filtrado, 
        x="MES", 
        y="TOTAL",
        color="ANO",  # Diferenciar los años por color
        title=f"Evolución Mensual de Consultas Médicas para Código {codigo_seleccionado}",
        markers=True
    )
    
    return fig

# **Ejecutar la app**
if __name__ == '__main__':
    app.run_server(debug=True)


   
    
    import webbrowser
webbrowser.open("http://127.0.0.1:8050/")

