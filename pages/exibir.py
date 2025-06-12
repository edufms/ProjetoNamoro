import streamlit as st
import os
from PIL import Image
import json
import datetime
import base64

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

# 🔄 Converter imagens para base64
def get_image_as_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 🖼️ Lista de imagens base64
imagens_base64 = [get_image_as_base64(img) for img in imagens]

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

            casal = dados.get(id_unico, {}).get("nome")
            st.markdown(f"# {casal}")
            st.markdown(f"💖 Estão juntos há: **{anos} anos, {meses} meses, {dias} dias e {horas} horas**.")
        else:
            st.warning("Data de início do namoro não encontrada.")
except Exception as e:
    st.warning(f"Erro ao carregar a data: {e}")

# 🖼️ Criação do carrossel automático com HTML + JS
html = """
<div id="slideshow" style="text-align:center">
  <img id="slide-img" src="data:image/jpeg;base64,{first_img}" style="width:100%; max-height:400px; object-fit:contain; border-radius:16px">
</div>
<script>
  const imagens = [{imagens_list}];
  let idx = 0;
  const slide = document.getElementById("slide-img");
  setInterval(() => {{
    idx = (idx + 1) % imagens.length;
    slide.src = "data:image/jpeg;base64," + imagens[idx];
  }}, 3000);
</script>
""".format(
    first_img=imagens_base64[0],
    imagens_list=",".join([f'"{img}"' for img in imagens_base64]))

st.components.v1.html(html, height=420)

