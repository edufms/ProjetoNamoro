import streamlit as st
import qrcode
from datetime import datetime
import uuid
import os
import json

st.title("Nosso Amor em Fotos")

if "uuid" not in st.session_state:
    st.session_state.uuid = str(uuid.uuid4())

    # Cria pasta se não existir
    os.makedirs("imagens", exist_ok=True)

    nome = st.text_input("Digite o nome do casal (Ex: Ana e João)")
    data_namoro = st.date_input("Data de início do namoro")
    fotos = st.file_uploader("Envie até 6 fotos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if st.button("Gerar Página com QR Code"):
        if not nome or not data_namoro or not fotos:
                st.warning("Preencha todos os campos e envie as fotos.")
                    else:
                            id_unico = st.session_state.uuid
                                    pasta = f"imagens/{id_unico}"
                                            os.makedirs(pasta, exist_ok=True)

                                                    caminhos = []
                                                            for i, foto in enumerate(fotos[:6]):
                                                                        caminho = os.path.join(pasta, f"{i}.jpg")
                                                                                    with open(caminho, "wb") as f:
                                                                                                    f.write(foto.getbuffer())
                                                                                                                caminhos.append(caminho)

                                                                                                                        # Salva dados
                                                                                                                                dados = {
                                                                                                                                            "nome": nome,
                                                                                                                                                        "data": str(data_namoro),
                                                                                                                                                                    "fotos": caminhos
                                                                                                                                                                            }

                                                                                                                                                                                    if os.path.exists("pares.json"):
                                                                                                                                                                                                with open("pares.json", "r") as f:
                                                                                                                                                                                                                all_data = json.load(f)
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                    all_data = {}

                                                                                                                                                                                                                                            all_data[id_unico] = dados
                                                                                                                                                                                                                                                    with open("pares.json", "w") as f:
                                                                                                                                                                                                                                                                json.dump(all_data, f)

                                                                                                                                                                                                                                                                        url = f"https://seusite.com/exibir.py?id={id_unico}"  # ou "http://localhost:8501/exibir?id=..."

                                                                                                                                                                                                                                                                                qr = qrcode.make(url)
                                                                                                                                                                                                                                                                                        st.image(qr, caption="Escaneie para ver a página do casal")
                                                                                                                                                                                                                                                                                                st.markdown(f"[Ou clique aqui para abrir]({url})")