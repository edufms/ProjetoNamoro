import streamlit as st
import os
from PIL import Image
import json
import datetime
import time

st.set_page_config(page_title="Slideshow do Casal", layout="centered")

# 📌 Captura ID da URL
id_unico = st.query_params.get("id", [None])

if not id_unico:
    st.error("ID não fornecido na URL.")
    st.stop()

# 📂 Caminho das imagens
caminho_pasta = os.path.join("imagens", id_unico)

if not os.path.exists(caminho_pasta):
    st.error("Nenhuma imagem encontrada para este casal.")
    st.stop()

# 🖼️ Lista de imagens
imagens = sorted([
    os.path.join(caminho_pasta, img)
    for img in os.listdir(caminho_pasta)
    if img.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
])

if not imagens:
    st.error("Não há imagens válidas.")
    st.stop()

# 🔁 Inicializa session_state
if "foto_idx" not in st.session_state:
    st.session_state.foto_idx = 0
if "ultima_execucao" not in st.session_state:
    st.session_state.ultima_execucao = time.time()

# 🕒 Tempo de relacionamento
try:
    with open("pares.json", "r") as f:
        dados = json.load(f)
        data_str = dados.get(id_unico, {}).get("data")
        if data_str:
            data_namoro = datetime.datetime.strptime(data_str, "%Y-%m-%d")
            agora = datetime.datetime.now()
            delta = agora - data_namoro

            anos = delta.days // 365
            meses = (delta.days % 365) // 30
            dias = (delta.days % 365) % 30
            horas = delta.seconds // 3600

            st.markdown(f"💖 Estão juntos há: **{anos} anos, {meses} meses, {dias} dias e {horas} horas**.")
except:
    st.warning("Erro ao carregar a data de início do namoro.")

# 🖼️ Exibe imagem atual
img_atual = imagens[st.session_state.foto_idx]
st.image(Image.open(img_atual), use_container_width=True)

# ⏱️ Avança imagem automaticamente a cada 3 segundos
tempo_atual = time.time()
if tempo_atual - st.session_state.ultima_execucao >= 3:  # 3 segundos
    st.session_state.foto_idx = (st.session_state.foto_idx + 1) % len(imagens)
    st.session_state.ultima_execucao = tempo_atual
    st.experimental_rerun()
