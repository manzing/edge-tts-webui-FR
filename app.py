import gradio as gr
import edge_tts
import asyncio
import os
# https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4
SUPPORTED_VOICES = {
    'Vivienne': 'fr-FR-VivienneMultilingualNeural',
    'Denise': 'fr-FR-DeniseNeural',
    'Eloise': 'fr-FR-EloiseNeural',
    'Remy': 'fr-FR-RemyMultilingualNeural',
    'Henri': 'fr-FR-HenriNeural'
}

# Modification de voix
def changeVoice(voices):
    example = SUPPORTED_VOICES[voices]
    example_file = os.path.join(os.path.dirname(__file__), "example/"+example+".mp3")
    return example_file

# Text to Speech
async def textToSpeech(text, voices, rate, volume):
    output_file = "output.mp3"
    voices = SUPPORTED_VOICES[voices]
    if (rate >= 0):
        rates = rate = "+" + str(rate) + "%"
    else:
        rates = str(rate) + "%"
    if (volume >= 0):
        volumes = "+" + str(volume) + "%"
    else:
        volumes = str(volume) + "%"
    communicate = edge_tts.Communicate(text,
                                       voices,
                                       rate=rates,
                                       volume=volumes,
                                       proxy=None)
    await communicate.save(output_file)
    audio_file = os.path.join(os.path.dirname(__file__), "output.mp3")
    if (os.path.exists(audio_file)):
        return audio_file
    else:
        raise gr.Error("La création a échoué！")
        return FileNotFoundError


# Effacer le texte et rendu
def clearSpeech():
    output_file = os.path.join(os.path.dirname(__file__), "output.mp3")
    if (os.path.exists(output_file)):
        os.remove(output_file)
    return None, None


with gr.Blocks(css="style.css", title="Text To Speech") as demo:
    gr.Markdown("""
    # Text-to-Speech FR
    Conversion texte en audio vocal avec edge-tts
    """)
    with gr.Row():
        with gr.Column():
            text = gr.TextArea(label="Entrez votre texte", elem_classes="text-area")
            btn = gr.Button("Convertir en audio vocal", elem_id="submit-btn")
        with gr.Column():
            voices = gr.Dropdown(choices=[
                "Vivienne", "Denise", "Eloise", "Remy",
                "Henri"
            ],
                                 value="Vivienne",
                                 label="Modèle de voix",
                                 info="Choix du modèle vocal FR (France)",
                                 interactive=True)
            
            example = gr.Audio(label="Exemple",
                              value="example/fr-FR-VivienneMultilingualNeural.mp3",
                              interactive=False,
                              elem_classes="example")

            voices.change(fn=changeVoice,inputs=voices,outputs=example)
            rate = gr.Slider(-100,
                             100,
                             step=1,
                             value=0,
                             label="Vitesse de parole",
                             info="Accélérer ou ralentir la voix",
                             interactive=True)
            
            volume = gr.Slider(-100,
                               100,
                               step=1,
                               value=0,
                               label="Volume",
                               info="Augmenter ou baisser le volume audio",
                               interactive=True)
            audio = gr.Audio(label="Sortie",
                             interactive=False,
                             elem_classes="audio")
            clear = gr.Button("Effacer", elem_id="clear-btn")
            btn.click(fn=textToSpeech,
                      inputs=[text, voices, rate, volume],
                      outputs=[audio])
            clear.click(fn=clearSpeech, outputs=[text, audio])

if __name__ == "__main__":
    demo.launch()
