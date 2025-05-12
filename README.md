## Chat Seguro com Interface Gráfica em Python

Este é um projeto de chat em grupo e mensagens privadas usando **sockets**, com interface gráfica em **Tkinter**, **suporte a emojis**, e **criptografia com Fernet (symmetric key encryption)**.

## Funcionalidades

- Interface gráfica amigável com abas para chats públicos e privados
- Escolha de nome de usuário ao entrar
- Mensagens privadas com o comando `/msg NOME mensagem`
- Emojis integrados no campo de entrada
- Exibição de todas as mensagens enviadas e recebidas
- Criptografia ponto-a-ponto usando `cryptography.fernet`

## Segurança

Todas as mensagens são criptografadas com uma chave Fernet trocada no momento da conexão com o servidor. O conteúdo transmitido não pode ser lido por terceiros.

## Estrutura
├── server.py # Código do servidor com suporte a múltiplos clientes
├── client.py # Cliente com interface gráfica e criptografia
├── README.md # Este arquivo

## Requisitos
- Python 3.8+
- Bibliotecas:
  - `cryptography`
  - `tkinter` (padrão com Python)

Para instalar dependências:
pip install cryptography

## Como executar
1. Inicie o servidor
python server.py
2. Execute o cliente (em outra aba ou outro computador na mesma rede)
python client.py

## Exemplo de mensagem privada
Digite na aba "Geral":
/msg João Olá, João! Tudo bem?
Se "João" estiver conectado, a mensagem será enviada diretamente para ele.

## Notas
O servidor distribui a chave simétrica (Fernet) no momento da conexão.
As mensagens são criptografadas e descriptografadas pelo cliente.
Por simplicidade, o sistema de autenticação ainda não foi implementado.
