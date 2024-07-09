import os
import tempfile
import openai
import streamlit as st

st.set_page_config(page_title="Conversor de Texto em Áudio OpenAI", page_icon="🤖")

st.title('🤖💬 Conversor de Texto em Áudio OpenAI')

# Move API key input to main area
openai_api_key = st.text_input("OpenAI API Key", type="password")
st.markdown("[Pegue aqui sua chave OpenAI API](https://platform.openai.com/account/api-keys)")

texto_usuario = st.text_area("Digite ou cole o texto aqui:", max_chars=4096)

# Sidebar
with st.sidebar:
    model_selection = st.radio("Qualidade:", ("tts-1", "tts-1-hd"))
    if st.button("Reiniciar"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]
        st.experimental_rerun()

st.sidebar.title("Sobre o Projeto")
st.sidebar.markdown("""
                 Conversor de texto em áudio com a api Openai.
            #
            - **GitHub:** [Link do projeto](https://github.com/gtellapolinario/Text-to-voice)
            ######
            - [Obsidian-Publish](https://dr-guilhermeapolinario.com)
            ######
            - [Exemplos de gravação](https://dr-guilhermeapolinario.com/2.+%C3%81reas/Aprendizado/Exemplos+de+voz+api+Openai)
            *by* Dr. Guilherme Apolinário
                
                """)

velocidade_voz = st.slider("Velocidade da voz:", 0.25, 4.0, 1.0)
vozes_disponiveis = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Set API key
if openai_api_key:
    openai.api_key = openai_api_key
    st.success('API key provided!', icon='✅')
else:
    st.warning('Please enter your OpenAI API key.', icon='⚠️')

# Função para converter texto em áudio
def converter_texto_em_audio(voice):
    if not openai_api_key:
        st.error("Please provide an OpenAI API key.")
        return
    if not texto_usuario:
        st.error("Please enter some text to convert.")
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
        st.error(f"An error occurred: {str(e)}")

# Botões para seleção de voz
for voz in vozes_disponiveis:
    st.button(f"Converter usando voz {voz.capitalize()}", on_click=converter_texto_em_audio, args=(voz,))

# Link para amostras de voz
st.markdown("Confira as [amostras de voz](https://platform.openai.com/docs/guides/text-to-speech) disponíveis.")
