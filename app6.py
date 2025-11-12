import streamlit as st
import numpy as np
import joblib


st.set_page_config(layout="wide")
st.title("Interface para o modelo RandomForest")
st.markdown("Use a barra lateral para inserir os parâmetros do modelo")

st.sidebar.header("Parâmetros do Modelo")

st.sidebar.subheader("Parâmetros de 0 a 1")
parametro_1_value = st.sidebar.number_input(
    "Contagem da flag PSH",
    min_value=0,
    max_value=1,
   # value=0.5,
    step=1,
    help = "Exemplo: Taxa de Juros, Nivel de satisfação"
)


parametro_2_value = st.sidebar.number_input(
    "Contagem da flag URG",
    min_value=0,
    max_value=1,
   # value=0.5,
    step=1,
    help = "Exemplo: Taxa de Juros, Nivel de satisfação"
)

st.sidebar.subheader("Parâmetros de 0 a infinito")

lista = ["Porta de Destino", "Comprimento mínimo do pacote de retorno", "Comprimento médio do pacote de retorno", "Pacotes de Retorno por Segundo", "Comprimento mínimo do pacote",  "Tamanho médio do segmento de ida (Forward)", "Tamanho médio do segmento de retorno (Backward)", "Tamanho mínimo do segmento de ida"]        
lista2 = ["Porta de Destino", "Comprimento mínimo do pacote de retorno", "Comprimento médio do pacote de retorno", "Pacotes de Retorno por Segundo", "Comprimento mínimo do pacote", "Contagem da flag PSH", "Contagem da flag URG",  "Tamanho médio do segmento de ida (Forward)", "Tamanho médio do segmento de retorno (Backward)", "Tamanho mínimo do segmento de ida"]

params_inf = {}
for i in range(0, 8):
    params_inf[lista[i]] = st.sidebar.number_input(
        lista[i],
        min_value=0.0,
        value=float(i * 10),
        step=1.0,
        help="Use o mini_value=0.0 para garantir que sejam valores positivos"
    )
    
X_input = [
    params_inf["Porta de Destino"],
    params_inf["Comprimento mínimo do pacote de retorno"],
    params_inf["Comprimento médio do pacote de retorno"],
    params_inf["Pacotes de Retorno por Segundo"],
    params_inf["Comprimento mínimo do pacote"],
    parametro_1_value,
    parametro_2_value,
    params_inf["Tamanho médio do segmento de ida (Forward)"],
    params_inf["Tamanho médio do segmento de retorno (Backward)"],
    params_inf["Tamanho mínimo do segmento de ida"]
]
    
st.subheader("Entrada de Dados Atual")

data = {
    "Parametros": [f"{lista2[i]}" for i in range(10)],
    "Valor de Entrada": X_input
}

st.table(data)

col_empty, col_btn = st.columns([4, 1])
with col_btn:
        # Coloca o botão 'Detectar' em uma posição de destaque
        detect_button = st.button("🔎 Classificar", type="primary", use_container_width=True, disabled=(X_input is None))

try:
    if detect_button:
        model = joblib.load("model.joblib")
        X_input = np.array(X_input)
        X_input_reshaped = X_input.reshape(1, -1)
        prev = model.predict(X_input_reshaped)
        
        if prev[0] == 0:
            st.success("✅ O modelo previu que o tráfego é NORMAL.")
        else:
            st.error("⚠️ O modelo previu que o tráfego é ANÔMALO.")
        st.metric(label="Previsão do modelo", value=f"{prev[0]}")
    
except Exception as e:
    st.error(f"Erro ao simular o modelo: {e}")
    st.warning("Verifica se as bibliotecas a entrada do modelo")