# https://github.com/gtellapolinario/Text-to-voice/streamlit_app.py
# Aplicativo streamlit text to speech openai 

import streamlit as st
from openai import OpenAI


# Configuração da barra lateral com informações fixas
st.sidebar.title("Sobre o Projeto")
st.sidebar.info("""
            Este projeto foi desenvolvido por Dr. Guilherme Apolinário, médico com interesse em tecnologia aplicada à saúde.
            - **GitHub:** [Link do projeto](https://github.com/gtellapolinario/Text-to-voice)
            - [Obsidian-Publish](https://dr-guilhermeapolinario.com)
            - [Exemplos de gravação](https://dr-guilhermeapolinario.com/2.+%C3%81reas/Aprendizado/Exemplos+de+voz+api+Openai)
                """)

st.sidebar.title("Informações")
st.sidebar.info(""" 
            Aplicativo de conversão direta de texto para áudio, utilizando a API da OpenAI. 
            É necessário inserir a chave da API que você copia em sua conta OpenAI. 
            Para copiar a chave acesso o site: [OpenAI API Keys](https://platform.openai.com/api-keys)
            """)

st.title("Conversor de Texto em Áudio")

# Campo para inserção da chave da API
chave_api = st.text_input("Insira sua chave da API da OpenAI:", type="password")

# Inicializa o cliente da OpenAI se a chave da API for fornecida
if chave_api:
    client = OpenAI(api_key=chave_api)

    # Campo de entrada de texto
    texto_usuario = st.text_area("Digite ou cole o texto aqui:", max_chars=4096)

    # Seletor de velocidade
    velocidade_voz = st.slider("Velocidade da voz:", 0.25, 4.0, 1.0)

    # Voze disponíveis da API
    vozes_disponiveis = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    # Função para converter texto em áudio
    def converter_texto_em_audio(voice):
        if texto_usuario:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=texto_usuario,
                speed=velocidade_voz
            )
            
            # Salvar e reproduzir o áudio
            audio_file_path = "output.mp3"
            response.stream_to_file(audio_file_path)
            st.audio(audio_file_path, format='audio/mp3')

    # Botões para seleção de voz
    for voz in vozes_disponiveis:
        st.button(f"Converter usando voz {voz.capitalize()}", on_click=converter_texto_em_audio, args=(voz,))

    # Link para amostras de voz
    st.markdown("Confira as [amostras de voz](https://platform.openai.com/docs/guides/text-to-speech) disponíveis.")
else:
    st.warning("Por favor, insira sua chave da API da OpenAI para usar o aplicativo.")
