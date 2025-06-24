LIMITE_SAQUES_DIARIOS = 3
LIMITE_VALOR_SAQUE = 500.0

def main():
    """
    Função principal do sistema bancário.
    Exibe o menu, recebe a opção do usuário e chama as funções das operações.
    """
    conta = {
        "saldo": 0.0,
        "extrato": [],
        "numero_saques_diarios": 0
    }

    menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

    while True:
        opcao = input(menu)

        if opcao == "1":
            try:
                valor = float(input("Informe o valor do depósito: "))
                depositar(conta, valor)
            except ValueError:
                print("Valor inválido. Por favor, digite um número válido.")

        elif opcao == "2":
            try:
                valor = float(input("Informe o valor do saque: "))
                sacar(conta, valor)
            except ValueError:
                print("Valor inválido. Por favor, digite um número válido.")

        elif opcao == "3":
            exibir_extrato(conta)

        elif opcao == "4":
            print("Obrigado por usar nosso sistema bancário. Volte sempre!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def depositar(conta, valor):
    """
    Realiza a operação de depósito, verificando se o valor é válido.
    """
    if valor <= 0:
        print("\nOperação falhou! O valor informado é inválido.")
        return

    conta["saldo"] += valor
    conta["extrato"].append(f"Depósito:  {format_currency(valor)}")
    print(f"\nDepósito de {format_currency(valor)} realizado com sucesso!")

def sacar(conta, valor):
    """
    Realiza a operação de saque, verificando limites e saldo.
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

    conta["saldo"] -= valor
    conta["extrato"].append(f"Saque:    -{format_currency(valor)}")
    conta["numero_saques_diarios"] += 1
    print(f"\nSaque de {format_currency(valor)} realizado com sucesso!")

def exibir_extrato(conta):
    """
    Exibe o extrato de todas as movimentações (depósitos e saques) e o saldo atual.
    """
    print("\n========== EXTRATO ==========")
    if not conta["extrato"]:
        print("Não foram realizadas movimentações.")
    else:
        for movimento in conta["extrato"]:
            print(movimento)
    print(f"\nSaldo atual: {format_currency(conta['saldo'])}")
    print("=============================")

def format_currency(value):
    """
    Formata um valor numérico para o padrão monetário brasileiro (R$ xxx.xx).
    """
    return f"R$ {value:.2f}".replace('.', ',')

if __name__ == "__main__":
    main()