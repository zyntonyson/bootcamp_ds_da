import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, ttest_ind
import seaborn as sns

sns.set_theme(style="whitegrid")

def simulador_ttest(d, alpha, n):
    m1 =135
    std =19
    m2 =m1+d
    num_experimentos =1000
    rechazos = 0
    for _ in range(num_experimentos):
        a = np.random.normal(m1, std, n)
        b = np.random.normal(m2, std, n)
        _, p = ttest_ind(a, b)
        if p < alpha:
            rechazos += 1

    x = np.linspace(min(m1, m2) - 3*std, max(m1, m2) + 3*std, 500)
    y1 = norm.pdf(x, m1, std / np.sqrt(n))
    y2 = norm.pdf(x, m2, std / np.sqrt(n))

    idx = np.where(y1 + y2 > 0.01 * max(y1.max(), y2.max()))[0]
    x_start, x_end = x[idx[0]], x[idx[-1]]

    z_alpha = norm.ppf(1 - alpha)
    t_crit = m1 + z_alpha * (std / np.sqrt(n))
    beta = norm.cdf(t_crit, loc=m2, scale=std / np.sqrt(n))

    fig1, ax1 = plt.subplots(figsize=(9, 4.5))
    ax1.plot(x, y1, label='Control (M1)', color='blue')
    ax1.plot(x, y2, label='Test (M2)', color='green')
    ax1.axvline(m1, linestyle='--', color='blue')
    ax1.axvline(m2, linestyle='--', color='green')
    #ax1.axvline(t_crit, linestyle=':', color='black')
    ax1.fill_between(x, y1, where=(x > t_crit), color='blue', alpha=0.2, label='Alpha')
    ax1.fill_between(x, y2, where=(x < t_crit), color='green', alpha=0.2, label='Beta')
    ax1.set_xlim(x_start, x_end)
    ax1.set_ylim(bottom=0)
    ax1.set_title(f"Distribuciones bajo H0 y H1| α = {alpha:.2f},  D = {abs(m1 - m2):.2f}")
    ax1.set_xlabel("Valor observado")
    ax1.set_ylabel("Densidad")
    ax1.legend()
    fig1.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(4.5, 4.5))
    ax2.pie([rechazos, num_experimentos - rechazos],
            labels=["Rechaza H0", "No Rechaza H0"],
            colors=["lightcoral", "lightgray"],
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops=dict(width=0.5))
    ax2.set_title(f"Rechazo H0 en {num_experimentos} pruebas")
    fig2.tight_layout()

    return fig1, fig2

st.title("📊 Simulador para pruebas T")
st.markdown("Ajusta los parámetros y observa los efectos en las distribuciones, errores α/β y rechazo de hipótesis.")

with st.sidebar:
    d = st.slider("Diferencia entre las medias", 0, 20, 20, 1)
    alpha = st.slider("Alpha (nivel de significancia)", 0.01, 0.1, 0.05, 0.01)
    n = st.slider("Tamaño de muestra por grupo", 100, 1000, 100, 100)

if st.button("Simular"):
    fig1, fig2 = simulador_ttest(d, alpha, n)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.pyplot(fig1)
    with col2:
        st.pyplot(fig2)
