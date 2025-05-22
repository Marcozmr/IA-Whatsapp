auth.py - #Autenticação de usuários por CNPJ ou código de funcionário
usuarios_permitidos = {
    "12345678000100": "VIVA 7 MAQUINAS",
    "FUNC001": "Funcionário teste",
    "FUNC002": "Funcionário Welyngton bassi",
    "FUNC003": "Funcionário Marcos vinicius",
    "FUNC004":  "Funcionario marlon",
    "FUNC005": "Funcionário Marcio",
    "FUNC006": "Funcionário Vinicius",
}

def verificar_autenticacao(telefone: str, msg: str):
    for codigo, nome in usuarios_permitidos.items():
        if codigo in msg:
            return True, nome
    if telefone in usuarios_permitidos:
        return True, usuarios_permitidos[telefone]
    return False, ""