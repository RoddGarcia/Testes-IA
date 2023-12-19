import speech_recognition as sr
import os
import json

def reconhecer_fala():
    # Carregar dados de reconhecimento do arquivo JSON
    with open('recog.json') as f:
        dados = json.load(f)

    print(dados) 

    # Inicializar o reconhecedor
    reconhecedor = sr.Recognizer()

    # Usar o microfone como fonte de áudio
    with sr.Microphone() as fonte:
        print("Diga algo:")
        reconhecedor.adjust_for_ambient_noise(fonte) 
        audio = reconhecedor.listen(fonte, timeout=5)

    try:
        os.system('cls')
        print("Reconhecendo...")
        texto = reconhecedor.recognize_google(audio)
        print("Você disse:", texto.upper())

        # Verificar se o texto reconhecido corresponde a alguma frase registrada
        for i in dados.get("Recog", []):
            if texto.upper() in i.get("phrase", "").upper():
                if "command::" in i.get("answer", ""):
                    os.system(i.get("answer", "").replace("command::", ""))
                else:
                    print(i.get("answer", ""))
            else:
                print()

    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
    except sr.RequestError as e:
        print(f"Não foi possível obter resultados da API de Reconhecimento de Fala do Google; {e}")

if __name__ == "__main__":
    reconhecer_fala()
