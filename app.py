import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Función para calcular el payoff de la estrategia
def calcular_payoff(precio_subyacente, strike_price, prima_call, cantidad_opciones, monto_garantizado, monto_opciones, intereses_renta_fija):
    # Payoff de las opciones (cada lote equivale a 100 acciones)
    if precio_subyacente <= strike_price:
        payoff_total = -monto_opciones + intereses_renta_fija  # Resultado negativo
    else:
        payoff_opciones = (precio_subyacente - strike_price) * cantidad_opciones * 100
        payoff_total = intereses_renta_fija + payoff_opciones  # Payoff total
    
    return payoff_total

# Inputs del usuario usando Streamlit
st.title('Estrategia de Capital Garantizado')

precio_subyacente = st.number_input('Precio actual del activo subyacente:', value=3680.0)
strike_price = st.number_input('Precio de ejercicio (strike price) de las opciones call:', value=3858.1)
prima_call = st.number_input('Prima de la opción call:', value=290.0)
monto_invertir = st.number_input('Monto total que deseas invertir:', value=100000000.0)
tasa_interes = st.number_input('Tasa de interés anual de las letras (en decimal, por ejemplo 0.05 para 5%):', value=0.443)
vencimiento = st.number_input('Vencimiento de las opciones y las letras (en días):', value=72)
porcentaje_garantizado = st.number_input('Porcentaje de capital garantizado (por ejemplo, 0.90 para 90%):', value=0.9)

# Cantidad garantizada
monto_garantizado = monto_invertir * porcentaje_garantizado
# Cantidad invertida en letras
monto_letras = monto_garantizado / ((1 + tasa_interes) ** (vencimiento / 365))
# Intereses de la renta fija
intereses_renta_fija = monto_garantizado - monto_letras
# Cantidad restante para comprar opciones call
monto_restante = monto_invertir - monto_letras
# Cantidad de opciones call a comprar
cantidad_opciones = int(monto_restante // (prima_call * 100))
# Monto invertido en opciones call
monto_opciones = cantidad_opciones * prima_call * 100

# Mostrar los detalles de la estrategia
st.subheader('Detalles de la Estrategia')
st.write(f'Cantidad destinada a comprar opciones call: {monto_restante:.2f} ARS')
st.write(f'Intereses generados por la renta fija: {intereses_renta_fija:.2f} ARS')
st.write(f'Cantidad de opciones call compradas: {cantidad_opciones}')

# Rango de precios del activo subyacente al vencimiento
cambios_porcentuales = np.arange(-30, 31, 2)  # de -30% a 30% en pasos de 2%
precios_futuros = np.round(precio_subyacente * (1 + cambios_porcentuales / 100), 2)
payoffs = [calcular_payoff(precio, strike_price, prima_call, cantidad_opciones, monto_garantizado, monto_opciones, intereses_renta_fija) for precio in precios_futuros]

# Calcular el retorno en porcentaje
retornos = [np.round(payoff / monto_invertir * 100, 2) for payoff in payoffs]

# Crear la tabla
tabla = pd.DataFrame({
    'Cambio %': cambios_porcentuales,
    'Subyacente': precios_futuros,
    'Payoff a Vencimiento': np.round(payoffs, 2),
    'Return %': retornos
})

# Mostrar la tabla en Streamlit
st.subheader('Tabla de Resultados')
st.write(tabla)

# Crear la figura de la tabla con matplotlib
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('tight')
ax.axis('off')
tabla_mpl = pd.plotting.table(ax, tabla, loc='center', cellLoc='center', colWidths=[0.15]*len(tabla.columns))

# Ajustar el tamaño de la fuente de la tabla y la escala de las celdas
tabla_mpl.auto_set_font_size(False)
tabla_mpl.set_fontsize(10)
tabla_mpl.scale(1.5, 1.5)  # Aumentar el tamaño de las celdas

# Mostrar la figura en Streamlit
st.pyplot(fig)
