import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Defina a chave em uma variável de ambiente: GOOGLE_API_KEY
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "Defina a variável GOOGLE_API_KEY no arquivo .env antes de executar."
    )

client = genai.Client(api_key=API_KEY)

def executar_poc_suporte(origem_manuais):
    system_instruction = (
        "Você é um assistente técnico especialista. Use o arquivo fornecido para responder "
        "as dúvidas dos clientes. Se a resposta não estiver no manual, diga educadamente "
        "que não encontrou a informação e que um especialista humano será acionado."
    )

    if isinstance(origem_manuais, str) and os.path.isdir(origem_manuais):
        caminhos_manuais = [
            os.path.join(origem_manuais, nome)
            for nome in sorted(os.listdir(origem_manuais))
            if os.path.isfile(os.path.join(origem_manuais, nome))
        ]
        if not caminhos_manuais:
            raise RuntimeError(f"A pasta '{origem_manuais}' não possui arquivos para carregar.")
    elif isinstance(origem_manuais, str):
        caminhos_manuais = [origem_manuais]
    else:
        caminhos_manuais = origem_manuais

    arquivos_contexto = []
    for caminho in caminhos_manuais:
        # Upload de cada arquivo para a API
        print(f"Fazendo upload do manual: {caminho}...")
        arquivo = client.files.upload(file=caminho)
        arquivos_contexto.append(arquivo)

    print("\n✓ Manuais prontos. Iniciando chat (digite 'sair' para encerrar).")

    # Mantemos histórico simples para contexto entre mensagens
    history = []

    while True:
        pergunta = input("\nCliente (WhatsApp): ")
        if pergunta.lower() in ["sair", "exit"]:
            break

        contents = list(arquivos_contexto)
        contents.extend(history)
        contents.append(pergunta)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system_instruction),
        )

        history.extend([pergunta, response.text])
        print(f"\nIA Especialista: {response.text}")

# Execute passando a pasta com os manuais
executar_poc_suporte("manuais")