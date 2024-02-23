# https://github.com/gtellapolinario/Text-to-voice/streamlit_app.py
# Aplicativo streamlit text to speech openai 
import os
import tempfile
import openai
import requests
import streamlit as st

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


st.title('#### 🤖💬 Conversor de Texto em Áudio OpenAI')

texto_usuario = st.text_area("Digite ou cole o texto aqui:", max_chars=4096)

if 'OPENAI_API_KEY' in st.secrets:
    st.success('API key already provided!', icon='✅')
    openai.api_key = st.secrets['OPENAI_API_KEY']
else:
    openai.api_key = st.text_input('Digite sua chave de API:', type='password')

velocidade_voz = st.slider("Velocidade da voz:", 0.25, 4.0, 1.0)
vozes_disponiveis = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

client = openai.api_key
# Função para converter texto em áudio
def converter_texto_em_audio(voice):
    if texto_usuario and openai.api_key:
        response = openai.Audio.create(
            model="tts-1",
            voice=voice,
            input=texto_usuario,
            speed=velocidade_voz
        )
        # Verifica se a resposta é bem-sucedida e reproduz o áudio
        if response.status_code == 200:
            audio_bytes = response.content
            if len(audio_bytes) > 0:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    fp.write(audio_bytes)
                    fp.seek(0)
                    st.audio(fp.name, format="audio/mp3")
                    # Reset file pointer for download
                    fp.seek(0)
                    # Create a download button for the audio file
                    st.download_button(
                        label="Download audio",
                        data=fp.read(),
                        file_name="narration.mp3",
                        mime="audio/mp3",
                    )
                os.unlink(fp.name)  # Clean up the temporary file
            else:
                st.error("Não foi possível gerar o áudio. Por favor, tente novamente.")

# Botões para seleção de voz
for voz in vozes_disponiveis:
    st.button(f"Converter usando voz {voz.capitalize()}", on_click=converter_texto_em_audio, args=(voz,))

# Link para amostras de voz
st.markdown("Confira as [amostras de voz](https://platform.openai.com/docs/guides/text-to-speech) disponíveis.")


