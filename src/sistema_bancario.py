import getpass
from datetime import datetime

# Define o limite de saques diários e o valor máximo permitido por saque
LIMITE_SAQUES_DIARIOS = 3
LIMITE_VALOR_SAQUE = 500.0
AGENCIA_PADRAO = "0001"  # Número fixo da agência

# Listas globais para armazenar usuários e contas
usuarios = []
contas = []

def formatar_data(data_str):
    """
    Recebe uma string no formato DD/MM/AAAA e retorna uma data formatada.
    Se inválida, solicita novamente.
    """
    while True:
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
            return data
        except ValueError:
            data_str = input("Data inválida! Digite novamente (DD/MM/AAAA): ").strip()

def formatar_data_str(data):
    """
    Recebe um objeto datetime e retorna string no formato DD/MM/AAAA.
    """
    return data.strftime("%d/%m/%Y")

def formatar_cpf(cpf):
    """
    Formata o CPF para o padrão XXX.XXX.XXX-XX.
    """
    cpf_numeros = ''.join(filter(str.isdigit, cpf)).zfill(11)
    return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"

def validar_dados_usuario(dados):
    """
    Exibe os dados informados e pede confirmação ao usuário.
    Permite alteração caso o usuário informe que estão incorretos.
    """
    while True:
        print("\nConfira os dados informados:")
        print(f"Nome: {dados['nome']}")
        print(f"Data de nascimento: {formatar_data_str(dados['nascimento'])}")
        print(f"CPF: {formatar_cpf(dados['cpf'])}")
        print(f"Endereço: {dados['endereco']}")
        confirma = input("Os dados estão corretos? (S/N): ").strip().upper()
        if confirma == "S":
            return dados
        elif confirma == "N":
            print("\nVamos corrigir os dados.")
            dados['nome'] = input("Nome completo: ").strip()
            nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
            dados['nascimento'] = formatar_data(nascimento)
            logradouro = input("Logradouro: ").strip()
            numero = input("Número: ").strip()
            bairro = input("Bairro: ").strip()
            cidade = input("Cidade: ").strip()
            estado = input("Estado (sigla): ").strip().upper()
            dados['endereco'] = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"
        else:
            print("Opção inválida. Digite S para sim ou N para não.")

def criar_usuario():
    """
    Cria um novo usuário (cliente do banco), incluindo senha.
    Solicita nome, data de nascimento, CPF, endereço e senha.
    Garante que o CPF seja único entre os usuários.
    Valida os dados antes de cadastrar.
    """
    print("\n=== Cadastro de Usuário ===")
    while True:
        cpf = input("CPF (XXX.XXX.XXX-XX): ").strip()
        if any(formatar_cpf(u["cpf"]) == formatar_cpf(cpf) for u in usuarios):
            print("Já existe usuário com esse CPF.")
            return None
        break
    nome = input("Nome completo: ").strip()
    nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
    nascimento_dt = formatar_data(nascimento)
    logradouro = input("Logradouro: ").strip()
    numero = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    estado = input("Estado (sigla): ").strip().upper()
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"
    senha = getpass.getpass("Crie uma senha para acesso: ").strip()
    dados = {
        "nome": nome,
        "nascimento": nascimento_dt,
        "cpf": cpf,
        "endereco": endereco,
        "senha": senha
    }
    dados = validar_dados_usuario(dados)
    usuarios.append(dados)
    print("Usuário criado com sucesso!")
    return dados

def criar_conta_corrente(usuario):
    """
    Cria uma nova conta corrente vinculada a um usuário existente.
    O número da conta é exclusivo e a agência é fixa.
    """
    numero_conta = len(contas) + 1
    conta = {
        "agencia": AGENCIA_PADRAO,
        "numero": numero_conta,
        "usuario": usuario,
        "saldo": 0.0,
        "extrato": [],
        "numero_saques_diarios": 0
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Agência: {conta['agencia']} Conta: {conta['numero']}")
    return conta

def autenticar_usuario():
    """
    Autentica o usuário pelo número da agência, conta e senha.
    Se não existir, oferece opção de cadastro.
    """
    while True:
        print("\n=== Login no Sistema Bancário ===")
        agencia = input("Agência: ").strip()
        numero = input("Conta: ").strip()
        senha = getpass.getpass("Senha: ").strip()
        conta = next((c for c in contas if c["agencia"] == agencia and str(c["numero"]) == numero), None)
        if conta and conta["usuario"]["senha"] == senha:
            print(f"\nBem-vindo(a), {conta['usuario']['nome']}!")
            return conta
        else:
            print("\nConta ou senha inválidos.")
            opc = input("Deseja se cadastrar no sistema? (S/N): ").strip().upper()
            if opc == "S":
                usuario = criar_usuario()
                if usuario:
                    conta = criar_conta_corrente(usuario)
                    print(f"Seus dados de acesso:\nAgência: {conta['agencia']} | Conta: {conta['numero']}")
                    return conta
            elif opc == "N":
                print("Tente novamente.")
            else:
                print("Opção inválida.")

def menu_usuario(conta):
    """
    Exibe o menu principal para o usuário autenticado.
    """
    while True:
        menu = f"""
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

Agência: {conta['agencia']} | Conta: {conta['numero']} | Titular: {conta['usuario']['nome']}
CPF: {formatar_cpf(conta['usuario']['cpf'])} | Nascimento: {formatar_data_str(conta['usuario']['nascimento'])}
=> """
        opcao = input(menu)

        if opcao == "1":
            try:
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = depositar(conta, valor)
                print(f"Saldo atual: {format_currency(saldo)} | Últimas movimentações: {extrato[-3:]}")
            except ValueError:
                print("Valor inválido. Por favor, digite um número válido.")
        elif opcao == "2":
            try:
                valor = float(input("Informe o valor do saque: "))
                sacar(conta, valor)
            except ValueError:
                print("Valor inválido. Por favor, digite um número válido.")
        elif opcao == "3":
            exibir_extrato(conta["saldo"], extrato=conta["extrato"])
        elif opcao == "4":
            print("Saindo da conta. Até logo!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def depositar(conta, valor):
    """
    Realiza a operação de depósito, verificando se o valor é válido.
    Atualiza o saldo e registra o depósito no extrato.
    Retorna saldo e extrato (resumido se necessário).
    """
    if valor <= 0:
        print("\nOperação falhou! O valor informado é inválido.")
        return conta["saldo"], conta["extrato"]
    conta["saldo"] += valor
    conta["extrato"].append(f"Depósito:  {format_currency(valor)}")
    print(f"\nDepósito de {format_currency(valor)} realizado com sucesso!")
    return conta["saldo"], conta["extrato"]

def sacar(conta, valor):
    """
    Realiza a operação de saque, verificando limites e saldo.
    Atualiza o saldo, registra o saque no extrato e incrementa o contador de saques diários.
    Exibe saldo e extrato após o saque.
    """
    if conta["numero_saques_diarios"] >= LIMITE_SAQUES_DIARIOS:
        print(f"\nOperação falhou! Limite de saques diários atingido ({conta['numero_saques_diarios']}/{LIMITE_SAQUES_DIARIOS}).")
        return
    if valor > LIMITE_VALOR_SAQUE:
        print(f"\nOperação falhou! O valor do saque excede o limite de {format_currency(LIMITE_VALOR_SAQUE)}.")
        return
    if valor > conta["saldo"]:
        print("\nOperação falhou! Não será possível sacar o dinheiro por falta de saldo.")
        return
    if valor <= 0:
        print("\nOperação falhou! O valor informado é inválido.")
        return
    conta["saldo"] -= valor
    conta["extrato"].append(f"Saque:    -{format_currency(valor)}")
    conta["numero_saques_diarios"] += 1
    print(f"\nSaque de {format_currency(valor)} realizado com sucesso!")
    print(f"Saques efetuados: {conta['numero_saques_diarios']}/{LIMITE_SAQUES_DIARIOS}")
    exibir_extrato(conta["saldo"], extrato=conta["extrato"])

def exibir_extrato(saldo, *, extrato):
    """
    Exibe o extrato de todas as movimentações (depósitos e saques) e o saldo atual.
    Recebe saldo por posição e extrato como argumento nomeado.
    """
    print("\n========== EXTRATO ==========")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimento in extrato:
            print(movimento)
    print(f"\nSaldo atual: {format_currency(saldo)}")
    print("=============================")

def format_currency(value):
    """
    Formata um valor numérico para o padrão monetário brasileiro (R$ xxx,xx).
    """
    return f"R$ {value:.2f}".replace('.', ',')

def main():
    """
    Função principal do sistema bancário.
    Solicita autenticação antes de exibir o menu principal.
    """
    while True:
        conta = autenticar_usuario()
        if conta:
            menu_usuario(conta)
        sair = input("Deseja encerrar o sistema? (S/N): ").strip().upper()
        if sair == "S":
            print("Obrigado por usar nosso sistema bancário. Volte sempre!")
            break

# Ponto de entrada do programa
if __name__ == "__main__":
    main()