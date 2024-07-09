import os
import tempfile
import openai
import streamlit as st

st.set_page_config(page_title="Conversor de Texto em Áudio OpenAI", page_icon="🤖")
st.title('🤖💬 Conversor de Texto em Áudio OpenAI')

# Sidebar para entrada de chave API e seleção de modelo
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.markdown("[Pegue aqui sua chave OpenAI API](https://platform.openai.com/account/api-keys)")
    model_selection = st.radio("Qualidade:", ("tts-1", "tts-1-hd"))
    if st.button("Reiniciar"):
        st.session_state.clear()
        st.experimental_rerun()
    if st.button("Limpar Conversa"):
        if "messages" in st.session_state:
            del st.session_state["messages"]
        st.experimental_rerun()

st.sidebar.title("")
st.sidebar.markdown("""
#
                ## Sobre o Projeto
                ### Conversor de texto em áudio com a api Openai.
            #
            - **GitHub:** [Link do projeto](https://github.com/gtellapolinario/Text-to-voice)
            ######
            - [Exemplos de gravação](https://dr-guilhermeapolinario.com/2.+%C3%81reas/Aprendizado/Exemplos+de+voz+api+Openai)
            *by* Dr. Guilherme Apolinário
                
                """)

# Área principal para entrada de texto e controles
texto_usuario = st.text_area("Digite ou cole o texto aqui:", max_chars=4096)
velocidade_voz = st.slider("Velocidade da voz:", 0.25, 4.0, 1.0)
vozes_disponiveis = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Set API key
if openai_api_key:
    openai.api_key = openai_api_key
    st.success("API key configurada com sucesso!")
else:
    st.warning('Por favor, insira sua chave OpenAI API na barra lateral.')

# Função para converter texto em áudio
def converter_texto_em_audio(voice):
    if not openai_api_key:
        st.error("Por favor, forneça uma chave API OpenAI válida.")
        return
    if not texto_usuario:
        st.error("Por favor, insira algum texto para converter.")
        return
    
    try:
        response = openai.audio.speech.create(
            model=model_selection,
            voice=voice,
            input=texto_usuario,
            speed=velocidade_voz
        )
        
        # Get the audio content
        audio_content = response.content
        
        if audio_content:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                fp.write(audio_content)
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
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")

# Botões para seleção de voz
cols = st.columns(3)
for idx, voz in enumerate(vozes_disponiveis):
    with cols[idx % 3]:
        st.button(f"Voz {voz.capitalize()}", on_click=converter_texto_em_audio, args=(voz,), key=f"btn_{voz}")

# Link para amostras de voz
st.markdown("Confira as [amostras de voz](https://platform.openai.com/docs/guides/text-to-speech) disponíveis.")
