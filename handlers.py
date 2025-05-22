# handlers.py - Lógica de roteamento e IA
import openai
from auth import verificar_autenticacao
from tiny_api import listar_produtos, cadastrar_pedido_exemplo
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def processar_mensagem(msg: str, telefone: str) -> str:
    autenticado, nome = verificar_autenticacao(telefone, msg)
    if not autenticado:
        return "Olá! Para continuar, envie seu CNPJ ou código de funcionário para autenticação."

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Você é um atendente da empresa do usuário {nome}, respondendo comandos sobre produtos e pedidos."},
            {"role": "user", "content": msg}
        ]
    )
    texto = resposta['choices'][0]['message']['content'].lower()

    if "listar produtos" in texto:
        return listar_produtos()
    elif "fazer pedido" in texto:
        return cadastrar_pedido_exemplo()
    else:
        return texto
    
    memoria_conversas = {}

def processar_mensagem(msg, telefone):
    autorizado, nome = verificar_autenticacao(telefone, msg)
    if not autorizado:
        return "Envie seu CNPJ ou código de funcionário para continuar."

    if telefone not in memoria_conversas:
        memoria_conversas[telefone] = [
            {"role": "system", "content": f"Você é o atendente virtual da empresa {nome}."}
        ]

    # Adiciona a mensagem do usuário ao histórico
    memoria_conversas[telefone].append({"role": "user", "content": msg})

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=memoria_conversas[telefone][-10:]  # envia só as 10 últimas mensagens
        )
        conteudo = resposta.choices[0].message.content
        # Adiciona a resposta da IA à memória
        memoria_conversas[telefone].append({"role": "assistant", "content": conteudo})
        return conteudo
    except Exception as e:
        return "Ocorreu um erro ao consultar a IA. Tente novamente mais tarde."
