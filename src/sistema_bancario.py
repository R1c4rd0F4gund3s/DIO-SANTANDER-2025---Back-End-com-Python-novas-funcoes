import getpass
from datetime import datetime

# Limites e constantes do sistema
LIMITE_SAQUES_DIARIOS = 3
LIMITE_VALOR_SAQUE = 500.0
AGENCIA_PADRAO = "0001"

# Estruturas globais
usuarios = []
contas = []

def formatar_data(data_str):
    """Converte string DD/MM/AAAA em datetime, pedindo novamente se inválida."""
    while True:
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
            return data
        except ValueError:
            data_str = input("Data inválida! Digite novamente (DD/MM/AAAA): ").strip()

def formatar_data_str(data):
    """Converte datetime para string DD/MM/AAAA."""
    return data.strftime("%d/%m/%Y")

def formatar_cpf(cpf):
    """Formata o CPF para XXX.XXX.XXX-XX."""
    cpf_numeros = ''.join(filter(str.isdigit, cpf)).zfill(11)
    return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"

def validar_dados_usuario(dados):
    """Exibe dados e permite confirmação/correção pelo usuário."""
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
    """Cria novo usuário, valida dados e adiciona senha."""
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
    """Cria uma nova conta corrente para o usuário informado."""
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

def menu_cadastro_conta(usuario):
    """
    Menu para o usuário após o cadastro, permitindo listar contas, criar nova conta ou sair para tela de login.
    """
    while True:
        print(f"\n=== Menu de Contas para {usuario['nome']} ===")
        print("[1] Listar Contas")
        print("[2] Nova Conta")
        print("[3] Voltar para Login")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            print("\n--- Contas cadastradas ---")
            encontrou = False
            for conta in contas:
                if conta["usuario"] == usuario:
                    encontrou = True
                    print(f"Agência: {conta['agencia']} | Conta: {conta['numero']}")
            if not encontrou:
                print("Nenhuma conta cadastrada para este usuário.")
        elif opcao == "2":
            conta = criar_conta_corrente(usuario)
            print(f"Nova conta criada! Agência: {conta['agencia']} | Conta: {conta['numero']}")
        elif opcao == "3":
            print("Voltando para tela de login...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def autenticar_usuario():
    """
    Autentica o usuário pelo número da agência, conta e senha.
    Se não existir, oferece opção de cadastro e menu de contas.
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
                    menu_cadastro_conta(usuario)
            elif opc == "N":
                print("Tente novamente.")
            else:
                print("Opção inválida.")

def menu_usuario(conta):
    """Exibe o menu principal para o usuário autenticado."""
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
    """Realiza depósito, atualiza saldo e extrato."""
    if valor <= 0:
        print("\nOperação falhou! O valor informado é inválido.")
        return conta["saldo"], conta["extrato"]
    conta["saldo"] += valor
    conta["extrato"].append(f"Depósito:  {format_currency(valor)}")
    print(f"\nDepósito de {format_currency(valor)} realizado com sucesso!")
    return conta["saldo"], conta["extrato"]

def sacar(conta, valor):
    """Realiza saque, verifica limites e saldo, atualiza extrato."""
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
    """Exibe o extrato de movimentações e saldo atual."""
    print("\n========== EXTRATO ==========")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimento in extrato:
            print(movimento)
    print(f"\nSaldo atual: {format_currency(saldo)}")
    print("=============================")

def format_currency(value):
    """Formata valor para padrão monetário brasileiro."""
    return f"R$ {value:.2f}".replace('.', ',')

def main():
    """Função principal: autentica e exibe menu principal."""
    while True:
        conta = autenticar_usuario()
        if conta:
            menu_usuario(conta)
        sair = input("Deseja encerrar o sistema? (S/N): ").strip().upper()
        if sair == "S":
            print("Obrigado por usar nosso sistema bancário. Volte sempre!")
            break

if __name__ == "__main__":
    main()