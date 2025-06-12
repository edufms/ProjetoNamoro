import streamlit as st
import os
from PIL import Image
import json
import datetime

st.set_page_config(page_title="Slideshow do Casal", layout="centered")

# 📌 Captura o ID da URL (ex: ?id=abc123)
id_unico = st.query_params.get("id", [None])[0]

if not id_unico:
    st.error("ID não fornecido na URL.")
    st.stop()

# 📂 Caminho para as imagens do casal
caminho_pasta = os.path.join("imagens", id_unico)

if not os.path.exists(caminho_pasta):
    st.error("Nenhuma imagem encontrada para este casal.")
    st.stop()

# 📷 Lista de imagens
imagens = sorted([
    os.path.join(caminho_pasta, img)
    for img in os.listdir(caminho_pasta)
    if img.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
])

if not imagens:
    st.error("Não há imagens válidas nesta pasta.")
    st.stop()

# 🔁 Inicializa índice no session_state
if "foto_idx" not in st.session_state:
    st.session_state.foto_idx = 0

# ▶️ Slideshow com botões
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("⬅️"):
        st.session_state.foto_idx = (st.session_state.foto_idx - 1) % len(imagens)

with col3:
    if st.button("➡️"):
        st.session_state.foto_idx = (st.session_state.foto_idx + 1) % len(imagens)

# 🖼️ Exibe imagem atual
img_atual = imagens[st.session_state.foto_idx]
st.image(Image.open(img_atual), use_container_width=True)

# 🕒 Tempo juntos
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
        else:
            st.warning("Data de início do namoro não encontrada.")
except Exception as e:
    st.warning(f"Erro ao carregar a data: {e}")
