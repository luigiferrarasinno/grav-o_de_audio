#pip install sounddevice
#pip install scipy
#pip install soundfile
#pip install SpeechRecognition


import sounddevice as sd
import soundfile as sf
import speech_recognition as sr


fs = 44100 
duracao_segmento = 10 * 60  
duracao_total = 2 * 60 * 60 
texto_transcrito = ""

for i in range(0, duracao_total, duracao_segmento):
    print(f"Gravando segmento {i//duracao_segmento + 1}...")
    gravacao = sd.rec(int(duracao_segmento * fs), samplerate=fs, channels=1)
    sd.wait()

   
    sf.write(f'segmento_{i//duracao_segmento + 1}.wav', gravacao, fs)
    
    
    audio_gravado, _ = sf.read(f'segmento_{i//duracao_segmento + 1}.wav')

  
    recognizer = sr.Recognizer()
    with sr.AudioFile(f'segmento_{i//duracao_segmento + 1}.wav') as source:
        audio_data = recognizer.record(source)
        try:
            resultado = recognizer.recognize_google(audio_data, show_all=True, language='pt-BR')
            if len(resultado['alternative']) > 0:
                texto_transcrito += resultado['alternative'][0]['transcript'] + "\n"
        except sr.UnknownValueError:
            print("O reconhecimento de fala não conseguiu entender o áudio.")
        except sr.RequestError as e:
            print("Erro durante o reconhecimento de fala; {0}".format(e))


with open('texto_transcrito.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write(texto_transcrito)

print("Gravação concluída! O texto transcrito foi salvo em 'texto_transcrito.txt'.")
