import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend no interactivo para servidores
import matplotlib.pyplot as plt
import os
from datetime import datetime
from flask import current_app


# ============================================================
# MODELO SIR
# ============================================================
def run_sir_model(population, beta, gamma, days, max_points=1000):
    """
    Ejecuta el modelo SIR y devuelve listas S, I, R.
    """

    # Condición inicial: 1 infectado, resto susceptibles
    S = [population - 1]
    I = [1]
    R = [0]

    # Validación para evitar explosiones de puntos
    if days < 1:
        days = 1

    # Número de puntos para el gráfico
    num_points = min(max_points, max(100, int(days * 500)))

    # Tiempo continuo para el gráfico dinámico
    t_values = np.linspace(0, days, num_points)

    # Simulación discreta día a día para datos numéricos
    for _ in range(days):
        new_infected = beta * S[-1] * I[-1] / population
        new_recovered = gamma * I[-1]

        S.append(S[-1] - new_infected)
        I.append(I[-1] + new_infected - new_recovered)
        R.append(R[-1] + new_recovered)

    return S, I, R, t_values


# ============================================================
# GRÁFICO DINÁMICO (PLOTLY) PARA LA VISTA DE ANÁLISIS
# ============================================================
def generate_sir_plot_html(population, beta, gamma, days):
    S, I, R, t_values = run_sir_model(population, beta, gamma, days)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t_values,
        y=np.interp(t_values, range(len(S)), S),
        mode='lines',
        name='Susceptibles (S)'
    ))

    fig.add_trace(go.Scatter(
        x=t_values,
        y=np.interp(t_values, range(len(I)), I),
        mode='lines',
        name='Infectados (I)'
    ))

    fig.add_trace(go.Scatter(
        x=t_values,
        y=np.interp(t_values, range(len(R)), R),
        mode='lines',
        name='Recuperados (R)'
    ))

    fig.update_layout(
        title="Modelo SIR – Propagación de la enfermedad",
        xaxis_title="Tiempo (días)",
        yaxis_title="Población",
        template="plotly_white",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return pio.to_html(fig, full_html=False), S, I, R


# ============================================================
# GRÁFICO ESTÁTICO (MATPLOTLIB) PARA EL REPORTE PDF
# ============================================================
def generate_sir_plot_image(population, beta, gamma, days):
    S, I, R, t_values = run_sir_model(population, beta, gamma, days)

    # Carpeta absoluta donde Flask sirve archivos estáticos
    folder = os.path.join(current_app.root_path, "static", "static_plots")
    os.makedirs(folder, exist_ok=True)

    filename = f"sir_plot_{datetime.now().timestamp()}.png"

    # Ruta absoluta (para guardar y para WeasyPrint)
    absolute_path = os.path.join(folder, filename)

    # Ruta relativa (para url_for)
    relative_path = f"static_plots/{filename}"

    # Generar gráfico
    plt.figure(figsize=(6, 4))
    plt.plot(t_values, np.interp(t_values, range(len(S)), S), label="Susceptibles (S)")
    plt.plot(t_values, np.interp(t_values, range(len(I)), I), label="Infectados (I)")
    plt.plot(t_values, np.interp(t_values, range(len(R)), R), label="Recuperados (R)")
    plt.xlabel("Tiempo (días)")
    plt.ylabel("Población")
    plt.title("Modelo SIR – Propagación de la enfermedad")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(absolute_path, bbox_inches="tight")
    plt.close()

    return absolute_path, relative_path, S, I, R
