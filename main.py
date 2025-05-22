from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
import openai
from dotenv import load_dotenv
import os
from tiny_api import processar_comando_tiny

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    form = await request.form()
    msg = form.get('Body')
    resp = MessagingResponse()

    # Integração com IA + Tiny
    resposta = processar_comando_tiny(msg)

    resp.message(resposta)
    return PlainTextResponse(str(resp))

# Estrutura do Projeto

# main.py - Ponto de entrada principal da API WhatsApp
import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from handlers import processar_mensagem

# Verifica se o módulo ssl está disponível
try:
    import ssl
except ImportError:
    sys.stderr.write("[ERRO] Módulo 'ssl' não encontrado. Verifique sua instalação do Python.\n")
    sys.exit(1)

load_dotenv()

app = FastAPI()

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    user_msg = form.get('Body')
    sender_number = form.get('From')

    resposta_texto = processar_mensagem(user_msg, sender_number)

    twilio_resp = MessagingResponse()
    twilio_resp.message(resposta_texto)
    return PlainTextResponse(str(twilio_resp), status_code=200)
