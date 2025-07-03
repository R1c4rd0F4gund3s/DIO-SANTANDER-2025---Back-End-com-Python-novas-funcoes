# 💳 Sistema Bancário Moderno em Python

Este é o protótipo da primeira versão de um novo sistema bancário desenvolvido em Python. O objetivo é modernizar as operações do banco, oferecendo funcionalidades básicas como **depósito**, **saque**, **extrato**, **cadastro de usuários** e **criação de contas correntes**.

## 🚀 Funcionalidades Implementadas

- **💰 Depósito**: Permite adicionar fundos à conta do usuário.  
  - Agora recebe argumentos apenas por posição e retorna saldo e extrato resumido.

- **🏧 Saque**:
  - Limite de 3 saques diários.
  - Limite máximo de R$ 500,00 por saque.
  - Verificação de saldo para evitar saques não autorizados.
  - Todos os saques são registrados para exibição no extrato.
  - Exibe o número de saques efetuados e o limite de saques após cada operação.
  - Mostra saldo e extrato após o saque.

- **📄 Extrato**:
  - Lista todas as transações (depósitos e saques).
  - Exibe o saldo atual da conta.
  - Mensagem específica para extratos sem movimentações.
  - Formatação de valores monetários no padrão `R$ xxx,xx`.
  - Recebe argumentos por posição (saldo) e nomeados (extrato).

- **🧑‍💼 Cadastro de Usuário**:
  - Permite criar um novo usuário informando nome, data de nascimento, CPF (com máscara e zeros à esquerda) e endereço completo.
  - Garante que o CPF seja único entre os usuários.
  - **🔒 Agora o usuário define uma senha de acesso no momento do cadastro.**
  - **📅 O campo de data de nascimento é tratado como data e sempre exibido no formato DD/MM/AAAA.**
  - **🆗 Antes de finalizar o cadastro, o sistema exibe os dados para confirmação e permite correção.**

- **🏦 Criação de Conta Corrente**:
  - Permite criar uma conta corrente vinculada a um usuário já cadastrado.
  - O número da agência é fixo ("0001") e o número da conta é exclusivo.
  - Um usuário pode ter mais de uma conta.
  - **🔗 Ao cadastrar um novo usuário, uma conta corrente é criada automaticamente.**
  - **📢 O sistema informa agência e número da conta ao usuário após o cadastro.**
  - **🗂️ Novo menu de contas:** Após o cadastro, o usuário pode listar todas as suas contas, criar novas contas ou voltar para a tela de login.

- **🔑 Login Seguro**:
  - O acesso ao sistema é feito informando agência, número da conta e senha.
  - Caso a conta não exista, o sistema oferece a opção de cadastro.
  - **🔄 Após o cadastro, o usuário pode acessar o menu de contas para gerenciar suas contas antes de voltar ao login.**

- **📝 Validação e Máscaras**:
  - O CPF é sempre apresentado com a máscara `XXX.XXX.XXX-XX`.
  - Data de nascimento sempre apresentada como `DD/MM/AAAA`.

## 🗂️ Estrutura do Projeto
![Fluxograma](/../../blob/main/images/fluxograma_sistema_bancario.png)

## 🖥️ Como Executar

1. Clone este repositório:

   ```bash
   git clone https://github.com/R1c4rd0F4gund3s/sistema_bancario.git