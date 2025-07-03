# Define o limite de saques diários e o valor máximo permitido por saque
LIMITE_SAQUES_DIARIOS = 3
LIMITE_VALOR_SAQUE = 500.0

def main():
    """
    Função principal do sistema bancário.
    Exibe o menu, recebe a opção do usuário e chama as funções das operações.
    """
    # Inicializa a conta com saldo, extrato e contador de saques diários
    conta = {
        "saldo": 0.0,
        "extrato": [],
        "numero_saques_diarios": 0
    }

    # Menu de opções apresentado ao usuário
    menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

    # Loop principal do sistema, executa até o usuário escolher sair
    while True:
        opcao = input(menu)  # Recebe a opção do usuário

        if opcao == "1":
            # Opção de depósito
            try:
                valor = float(input("Informe o valor do depósito: "))  # Solicita valor do depósito
                depositar(conta, valor)  # Chama a função de depósito
            except ValueError:
                print("Valor inválido. Por favor, digite um número válido.")

        elif opcao == "2":
            # Opção de saque
            try:
                valor = float(input("Informe o valor do saque: "))  # Solicita valor do saque
                sacar(conta, valor)  # Chama a função de saque
            except ValueError:
                print("Valor inválido. Por favor, digite um número válido.")

        elif opcao == "3":
            # Opção de exibir extrato
            exibir_extrato(conta)  # Chama a função de extrato

        elif opcao == "4":
            # Opção de sair do sistema
            print("Obrigado por usar nosso sistema bancário. Volte sempre!")
            break  # Encerra o loop e o programa

        else:
            # Opção inválida
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def depositar(conta, valor):
    """
    Realiza a operação de depósito, verificando se o valor é válido.
    Atualiza o saldo e registra o depósito no extrato.
    """
    if valor <= 0:
        print("\nOperação falhou! O valor informado é inválido.")
        return

    conta["saldo"] += valor  # Adiciona o valor ao saldo
    conta["extrato"].append(f"Depósito:  {format_currency(valor)}")  # Registra no extrato
    print(f"\nDepósito de {format_currency(valor)} realizado com sucesso!")

def sacar(conta, valor):
    """
    Realiza a operação de saque, verificando limites e saldo.
    Atualiza o saldo, registra o saque no extrato e incrementa o contador de saques diários.
    """
    if conta["numero_saques_diarios"] >= LIMITE_SAQUES_DIARIOS:
        print("\nOperação falhou! Você atingiu o limite de saques diários.")
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

    conta["saldo"] -= valor  # Subtrai o valor do saldo
    conta["extrato"].append(f"Saque:    -{format_currency(valor)}")  # Registra no extrato
    conta["numero_saques_diarios"] += 1  # Incrementa o número de saques diários
    print(f"\nSaque de {format_currency(valor)} realizado com sucesso!")

def exibir_extrato(conta):
    """
    Exibe o extrato de todas as movimentações (depósitos e saques) e o saldo atual.
    """
    print("\n========== EXTRATO ==========")
    if not conta["extrato"]:
        print("Não foram realizadas movimentações.")  # Caso não haja movimentações
    else:
        for movimento in conta["extrato"]:
            print(movimento)  # Exibe cada movimentação registrada
    print(f"\nSaldo atual: {format_currency(conta['saldo'])}")  # Exibe o saldo atual
    print("=============================")

def format_currency(value):
    """
    Formata um valor numérico para o padrão monetário brasileiro (R$ xxx,xx).
    """
    return f"R$ {value:.2f}".replace('.', ',')

# Ponto de entrada do programa
if __name__ == "__main__":
    main()  # Chama a função principal para iniciar o sistema bancário  