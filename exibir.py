import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image
import time
import urllib.parse

st.set_page_config(page_title="Amor em Fotos", layout="centered")

query_params = st.experimental_get_query_params()
id_unico = query_params.get("id", [None])[0]

if not id_unico:
    st.error("Parâmetro inválido na URL.")
        st.stop()

        # Carrega dados
        with open("pares.json", "r") as f:
            dados = json.load(f)

            casal = dados.get(id_unico)

            if not casal:
                st.error("Casal não encontrado.")
                    st.stop()

                    st.title(f"{casal['nome']}")
                    data_namoro = datetime.strptime(casal["data"], "%Y-%m-%d")

                    # Tempo juntos
                    agora = datetime.now()
                    diferenca = agora - data_namoro

                    anos = diferenca.days // 365
                    meses = (diferenca.days % 365) // 30
                    dias = (diferenca.days % 365) % 30
                    horas = diferenca.seconds // 3600

                    st.subheader(f"Juntos há {anos} anos, {meses} meses, {dias} dias e {horas} horas.")

                    # Slideshow
                    st.subheader("Nossas Memórias 💖")

                    fotos = casal["fotos"]

                    # Slideshow simples com intervalo
                    for img_path in fotos:
                        img = Image.open(img_path)
                            st.image(img, use_column_width=True)
                                time.sleep(1.5)