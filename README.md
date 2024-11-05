# Sistema de Gerenciamento de Colaboradores
Este projeto é uma interface gráfica desenvolvida em Python com o uso de customtkinter e Firestore (Firebase) para gerenciar colaboradores dentro de uma instituição. A aplicação permite o login de usuários pré-cadastrados e oferece funcionalidades para cadastrar, visualizar e demitir colaboradores.

## Funcionalidades
### Login
Descrição: O sistema permite o login de usuários pré-cadastrados no Firestore, garantindo que apenas usuários autenticados acessem as funcionalidades internas.
Como usar: Na tela inicial, insira seu e-mail e senha cadastrados. Clique em "Entrar". Em caso de dados incorretos, uma mensagem de erro será exibida.
Cadastro de Colaborador
Descrição: Usuários autenticados podem cadastrar novos colaboradores no sistema, inserindo informações básicas do colaborador, como nome, cargo e departamento.
Como usar: Acesse a opção de cadastro de colaborador. Preencha os campos necessários e clique em "Cadastrar".
Status da função update_verify: A função de verificação e atualização do colaborador está em manutenção e será ajustada para integrar com a nova tela frame_register.
Visualização de Colaboradores
Descrição: Visualize a lista de colaboradores cadastrados com detalhes como nome, cargo e departamento.
Como usar: Navegue até a opção "Listar Colaboradores" para exibir uma tabela com todos os colaboradores cadastrados.
Demitir Colaborador
Descrição: É possível demitir colaboradores, removendo-os do sistema.
Como usar: Na lista de colaboradores, selecione o colaborador desejado e clique em "Demitir". Essa ação remove o colaborador do banco de dados.
## Estrutura do Código
A interface foi estruturada com classes para manter a separação das responsabilidades e facilitar a manutenção. Abaixo está uma visão geral:

### Classe App: Gerencia a interface principal e os métodos de login.
Funções principais:
login(): Autentica o usuário com base nas credenciais armazenadas no Firestore.
window_home(): Interface da tela inicial pós-login, onde as opções de gerenciamento estão disponíveis.
register_verify(): Função para cadastrar um novo colaborador.
open_list_frame(): Exibe a tabela com os colaboradores cadastrados.
dismiss_verify(): Função para demitir o colaborador selecionado.

## Requisitos
Python 3.11+
Firebase Admin SDK configurado e autenticado
customtkinter: Biblioteca para customização de interface em Tkinter
Instalação
Clone este repositório.

## Instale as dependências com:

bash
Copy code
pip install customtkinter firebase-admin
Configure o Firebase Admin SDK com as credenciais JSON.

## Execute a aplicação:

bash
Copy code
python nome_do_arquivo.py

## Notas Adicionais
A função update_verify, responsável pela verificação e atualização dos dados de colaboradores no registro, está em manutenção devido à recente atualização da tela frame_register. Essa funcionalidade será ajustada em breve para otimizar o processo de atualização dos colaboradores.