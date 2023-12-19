# TO DO:
# MELHORAR SISTEMAS DE ADICIONAR
# ADIciONAR SISTEMA DE PESQUISA NO GOOGLE

import speech_recognition as sr
import os
import json
import time

def reconhecer_fala():
    # Carregar dados de reconhecimento do arquivo JSON
    with open('recog.json') as f:
        dados = json.load(f)

    print(dados) 

    # Inicializar o reconhecedor
    reconhecedor = sr.Recognizer()

    while True:
        try:
            # Usar o microfone como fonte de áudio
            with sr.Microphone() as fonte:
                print("Diga algo em inglês:")
                reconhecedor.adjust_for_ambient_noise(fonte) 
                audio = reconhecedor.listen(fonte, timeout=5)

            os.system('cls')  # Limpar a tela (apenas para sistemas Windows)
            print("Te escutando...")
            texto = reconhecedor.recognize_google(audio)
            print("Você disse:", texto.upper())

            # Verificar se o texto reconhecido corresponde a alguma frase registrada
            texto_encontrado = False

            for i in dados.get("Recog", []):
                if texto.upper() in i.get("phrase", "").upper():
                    texto_encontrado = True
                    if "command::" in i.get("answer", ""):
                        os.system(i.get("answer", "").replace("command::", ""))
                    if "command::exit" in i.get("answer", ""):
                        print('Okay! Bye!')
                        quit()
                        break
                    else:
                        print(i.get("answer", ""))
                    break  # Sair do loop assim que uma correspondência for encontrada

            if not texto_encontrado:
                print("Texto não foi encontrado no banco de dados. Deseja adicioná-lo?")
                with sr.Microphone() as fonte_adicional:
                    audio_adicional = reconhecedor.listen(fonte_adicional, timeout=5)

                novo_texto = reconhecedor.recognize_google(audio_adicional).upper()

                if novo_texto == "YES":
                    time.sleep(1)
                    print("Diga o que deve ser adicionado...")

                    with sr.Microphone() as fonte_adicional:
                        audio_adicional = reconhecedor.listen(fonte_adicional, timeout=5)

                    novo_texto = reconhecedor.recognize_google(audio_adicional).upper()
                    
                    novo_registro = {"phrase": texto.upper(), "answer": f"{novo_texto}"}

                    # Abrir o arquivo em modo de adição para adicionar novos comandos sem apagar os antigos
                    with open('to_add.txt', 'a') as arquivo:
                        json.dump(novo_registro, arquivo, indent=2)
                        arquivo.write('\n')  # Adicionar uma nova linha para separar entradas

                    print("Texto foi adicionado.")
                elif novo_texto == "NO":
                    print("Texto não será adicionado.")
                else:
                    print("Comando não reconhecido. Sem detalhes.")

        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
        except sr.RequestError as e:
            print(f"Não foi possível obter resultados da API de Reconhecimento de Fala do Google; {e}")

if __name__ == "__main__":
    reconhecer_fala()
