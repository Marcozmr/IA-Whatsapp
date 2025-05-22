import openai
import requests
import os

def processar_comando_tiny(msg: str) -> str:
    # Interpreta comando com IA
    resposta_ia = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente integrado ao ERP Tiny."},
            {"role": "user", "content": msg}
        ]
    )["choices"][0]["message"]["content"]

    # Exemplo: busca clientes se IA entendeu isso
    if "listar clientes" in resposta_ia.lower():
        return listar_clientes_tiny()
    else:
        return resposta_ia

def listar_clientes_tiny():
    url = "https://api.tiny.com.br/api2/cliente.listar.php"
    params = {
        "token": os.getenv("TINY_API_TOKEN"),
        "formato": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "clientes" in data.get("retorno", {}):
        nomes = [c["cliente"]["nome"] for c in data["retorno"]["clientes"]]
        return "Clientes:\n" + "\n".join(nomes)
    return "Não foi possível listar os clientes."

# tiny_api.py - Integração com ERP Tiny
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TINY_API_TOKEN = os.getenv("TINY_API_TOKEN")
BASE_URL = "https://api.tiny.com.br/api2/"

def listar_produtos():
    params = {"token": TINY_API_TOKEN, "formato": "json"}
    resp = requests.get(BASE_URL + "produtos.listar.php", params=params)
    data = resp.json()
    try:
        produtos = data['retorno']['produtos']
        nomes = [p['produto']['descricao'] for p in produtos]
        return "Produtos disponíveis:\n" + "\n".join(nomes[:10])
    except:
        return "Erro ao buscar produtos no Tiny."

def cadastrar_pedido_exemplo():
    pedido = {
        "pedido": {
            "data_pedido": "21/05/2025",
            "cliente": {"nome": "Cliente WhatsApp"},
            "itens": [
                {"item": {"descricao": "Produto A", "quantidade": 1, "valor_unitario": 100}},
                {"item": {"descricao": "Produto B", "quantidade": 2, "valor_unitario": 50}}
            ]
        }
    }
    params = {"token": TINY_API_TOKEN, "formato": "json"}
    resp = requests.post(BASE_URL + "pedido.incluir.php", params=params, json=pedido)
    if resp.status_code == 200:
        return "Pedido cadastrado com sucesso!"
    return "Erro ao cadastrar pedido."
