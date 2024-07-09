import streamlit as st
import tempfile
from pathlib import Path
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Conversor de Texto em Áudio OpenAI", page_icon="🤖")
st.title('🤖💬 Conversor de Texto em Áudio OpenAI')

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.markdown("[Pegue aqui sua chave OpenAI API](https://platform.openai.com/account/api-keys)")
    if openai_api_key:
        client = OpenAI(api_key=openai_api_key)
     model_selection = st.radio("Qualidade:", ("tts-1", "tts-1-hd"))
    if st.button("Reiniciar"):
        st.session_state.clear()
        st.experimental_rerun()
    if st.button("Limpar Conversa"):
        if "messages" in st.session_state:
            del st.session_state["messages"]
        st.experimental_rerun()
# Área principal para entrada de texto e controles
texto_usuario = st.text_area("Digite ou cole o texto aqui:", max_chars=4096)
velocidade_voz = st.slider("Velocidade da voz:", 0.25, 4.0, 1.0)
vozes_disponiveis = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

if openai_import_success and openai_api_key:
    client = OpenAI(api_key=openai_api_key)
    st.success("API key configurada com sucesso!")
else:
    st.warning('Por favor, insira sua chave OpenAI API na barra lateral.')

# Função para converter texto em áudio
def converter_texto_em_audio(voice):
    if not openai_import_success:
        st.error("A biblioteca OpenAI não está disponível. Por favor, instale-a e reinicie o aplicativo.")
        return
    if not client:
        st.error("Por favor, forneça uma chave API OpenAI válida.")
        return
    if not texto_usuario:
        st.error("Por favor, insira algum texto para converter.")
        return
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_path = Path(temp_file.name)
        
        response = client.audio.speech.create(
            model=model_selection,
            voice=voice,
            input=texto_usuario,
            speed=velocidade_voz
        )
        
        response.stream_to_file(temp_path)
        
        with open(temp_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="Download audio",
                data=audio_bytes,
                file_name="narration.mp3",
                mime="audio/mp3",
            )
        
        # Limpar o arquivo temporário
        temp_path.unlink()
        
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")

# Botões para seleção de voz
if openai_import_success:
    cols = st.columns(3)
    for idx, voz in enumerate(vozes_disponiveis):
        with cols[idx % 3]:
            st.button(f"Voz {voz.capitalize()}", on_click=converter_texto_em_audio, args=(voz,), key=f"btn_{voz}")

    # Link para amostras de voz
    st.markdown("Confira as [amostras de voz](https://platform.openai.com/docs/guides/text-to-speech) disponíveis.")
else:
    st.warning("Funcionalidades desativadas devido a problemas na importação da biblioteca OpenAI.")
