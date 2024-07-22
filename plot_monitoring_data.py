import plotly.graph_objs as go
import pandas as pd
import logging
from extract_data import extract_data
from logging_config import configurar_logging

configurar_logging()
logger = logging.getLogger(__name__)

def plot_monitoring_data():
    df = extract_data()

    # Verificar los datos extraídos
    logger.debug(f"Extracted DataFrame: \n{df}")

    # Convertir los campos de fecha y hora a datetime
    df['start_time'] = pd.to_datetime(df['start_time'], format="%Y-%m-%d %H:%M:%S")
    df['end_time'] = pd.to_datetime(df['end_time'], format="%Y-%m-%d %H:%M:%S")

    # Verificar los datos después de la conversión
    logger.debug(f"Converted start_time data: \n{df['start_time']}")
    logger.debug(f"Converted end_time data: \n{df['end_time']}")
    logger.debug(f"Dtypes after conversion: \n{df.dtypes}")

    # Asegurarse de que no hay datos nulos
    logger.debug(f"Any NaT values in start_time: {df['start_time'].isnull().any()}")
    logger.debug(f"Any NaT values in end_time: {df['end_time'].isnull().any()}")

    # Simular duraciones significativas para visualización si es necesario
    df['duration'] = df['duration'].apply(lambda x: x if x > 0 else 0.001)
    logger.debug(f"Durations after adjustment: \n{df['duration']}")

    # Crear las barras
    bars = []
    for i, row in df.iterrows():
        bars.append(go.Bar(
            x=[row['start_time']],
            y=[row['duration']],
            text=str(i+1),  # ID correlativo
            textposition='outside',
            marker_color='rgba(0, 0, 255, 0.5)' if i % 2 == 0 else 'rgba(0, 255, 255, 0.6)',
            name=row['dag_id'],
            width=1000 * 60 * 5  # Ancho de las barras en milisegundos (5 minutos)
        ))

    # Configurar el layout del gráfico
    layout = go.Layout(
        title='Duración de Ejecución de Tareas por DAG',
        xaxis=dict(
            title='Fecha y Hora de Inicio',
            tickformat='%Y-%m-%d %H:%M:%S',
            tickangle=-45
        ),
        yaxis=dict(
            title='Duración (segundos)'
        ),
        barmode='group'
    )

    # Crear la figura y mostrarla
    fig = go.Figure(data=bars, layout=layout)
    fig.show()

if __name__ == "__main__":
    plot_monitoring_data()
