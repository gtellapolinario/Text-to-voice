import os
import tempfile
from pathlib import Path

import streamlit as st
from openai import OpenAI
from pydub import AudioSegment

st.set_page_config(page_title="Conversor de Texto em Áudio OpenAI",
                   page_icon="🤖")

my_secret = os.environ['OPENAI_API_KEY']

# Configuração da barra lateral
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    model_selection = st.radio("Qualidade:",
                               ("tts-1", "tts-1-hd", "gpt-4o-mini-tts"))
    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()
    if st.button("Limpar Conversa"):
        if "messages" in st.session_state:
            del st.session_state["messages"]
        st.rerun()

texto_usuario = st.text_area("Digite ou cole o texto aqui:")
velocidade_voz = st.slider("Velocidade da voz:", 0.25, 4.0, 1.0)
vozes_disponiveis = [
    'alloy', 'echo', 'fable', 'onyx',
    'nova', 'shimmer', "ash", 'ballad',
    'coral', 'sage']

def split_text(text, max_length=4096):
    """
    Divide o texto em chunks de tamanho máximo especificado.
    Tenta dividir no último espaço antes do limite para evitar cortar palavras.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_length
        if end >= len(text):
            chunks.append(text[start:])
            break
        last_space = text.rfind(' ', start, end)
        if last_space == -1 or last_space < start:
            last_space = end
        chunks.append(text[start:last_space])
        start = last_space
    return chunks

def converter_texto_em_audio(voice):
    if openai_api_key is not None:
        client = OpenAI(api_key=openai_api_key)
    else:
        st.error("Por favor, insira sua chave API OpenAI na barra lateral.")
        return
    if not texto_usuario.strip():
        st.error("Por favor, insira algum texto para converter.")
        return
    try:
        chunks = split_text(texto_usuario, max_length=4096)
        st.info(f"Texto dividido em {len(chunks)} partes.")

        audio_segments = []

        for idx, chunk in enumerate(chunks):
            st.write(f"Processando parte {idx + 1} de {len(chunks)}...")
            with tempfile.NamedTemporaryFile(delete=False,
                                             suffix=".mp3") as temp_file:
                temp_path = Path(temp_file.name)
            with client.audio.speech.with_streaming_response.create(
                    model=model_selection,
                    voice=voice,
                    input=chunk,
                    speed=velocidade_voz,
            ) as response:
                response.stream_to_file(temp_path)
            # Carregar o segmento de áudio usando pydub
            segment = AudioSegment.from_mp3(temp_path)
            audio_segments.append(segment)

            # Remover o arquivo temporário
            temp_path.unlink()

        if audio_segments:
            # Concatenar todos os segmentos
            audio_completo = audio_segments[0]
            for segment in audio_segments[1:]:
                audio_completo += segment

            # Exportar o áudio completo para um arquivo temporário
            with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".mp3") as final_audio_file:
                final_audio_path = Path(final_audio_file.name)
            audio_completo.export(final_audio_path, format="mp3")

            with open(final_audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(
                    label="Download audio",
                    data=audio_bytes,
                    file_name="narration.mp3",
                    mime="audio/mp3",
                )
            final_audio_path.unlink()
        else:
            st.error("Nenhum áudio foi gerado.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")

cols = st.columns(3)
for idx, voz in enumerate(vozes_disponiveis):
    with cols[idx % 3]:
        st.button(f"Voz {voz.capitalize()}",
                  on_click=converter_texto_em_audio,
                  args=(voz, ),
                  key=f"btn_{voz}",
                  type="primary")
