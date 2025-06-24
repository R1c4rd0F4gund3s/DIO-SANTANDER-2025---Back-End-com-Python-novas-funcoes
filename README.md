# Sistema Bancário Moderno em Python

Este é o protótipo da primeira versão de um novo sistema bancário desenvolvido em Python. O objetivo é modernizar as operações do banco, oferecendo funcionalidades básicas como **depósito**, **saque** e **extrato**.

## Funcionalidades Implementadas

- **Depósito**: Permite adicionar fundos à conta do usuário.

- **Saque**:
  - Limite de 3 saques diários.
  - Limite máximo de R$ 500,00 por saque.
  - Verificação de saldo para evitar saques não autorizados.
  - Todos os saques são registrados para exibição no extrato.

- **Extrato**:
  - Lista todas as transações (depósitos e saques).
  - Exibe o saldo atual da conta.
  - Mensagem específica para extratos sem movimentações.
  - Formatação de valores monetários no padrão `R$ xxx.xx`.

## Estrutura do Projeto
![Fluxograma](https://github.com/R1c4rd0F4gund3s/DIO-SANTANDER-2025---Back-End-com-Python/blob/main/images/fluxograma_sistema_bancario.png)
