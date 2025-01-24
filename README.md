# Sistema de Gerenciamento de Serviços

Este projeto é um sistema de gerenciamento de serviços desenvolvido com **Python** e **Flask**, que permite gerenciar clientes, serviços e agendamentos. Além disso, ele inclui autenticação de usuários e validação de formulários.

## Funcionalidades

- Cadastro, edição e exclusão de **clientes**.
- Cadastro, edição e exclusão de **serviços**.
- Gerenciamento de **agendamentos** (criação, edição e exclusão).
- **Autenticação de usuários** com suporte a login e logout.
- Senhas criptografadas utilizando **Flask-Bcrypt**.
- Sistema de mensagens de feedback utilizando **Flask Flash**.
- Restrições de acesso a páginas com **Flask-Login**.
- Banco de dados utilizando **SQLite**.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **Flask-SQLAlchemy**: ORM para interagir com o banco de dados.
- **Flask-WTF**: Validação de formulários.
- **Flask-Bcrypt**: Criptografia de senhas.
- **Flask-Login**: Gerenciamento de autenticação de usuários.
- **HTML/CSS**: Interface básica.
- **SQLite**: Banco de dados.

## Requisitos

Certifique-se de ter o **Python 3.10 ou superior** instalado em sua máquina.

### Dependências do projeto:
Instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt

Dependências principais:

Flask

Flask-SQLAlchemy

Flask-WTF

Flask-Bcrypt

Flask-Login


Configuração e Uso

1. Clone este repositório:

git clone git@github.com:Jon-dev67/Gerenciamento-.git
cd Gerenciamento-


2. Configure o ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate


3. Configure o banco de dados:

A configuração está definida para usar um banco SQLite localizado no arquivo geren_servicos.db.

No primeiro uso, as tabelas serão criadas automaticamente.



4. Inicie o servidor Flask:

python app_gerenciamento/app_servicos.py


5. Acesse o sistema no navegador:

URL padrão: http://127.0.0.1:5000




Rotas Principais

/ - Página inicial.

/login - Página de login.

/logout - Logout.

/clientes - Gerenciamento de clientes.

/servicos - Gerenciamento de serviços.

/Agendar - Lista de agendamentos.

/agendamentos - Formulário para criar novos agendamentos.

/cad_cliente - Cadastro de clientes.

/cad_usuario - Cadastro de novos usuários.


Estrutura de Pastas

Gerenciamento-
├── app_gerenciamento/
│   ├── app_servicos.py          # Arquivo principal da aplicação
│   ├── static/                  # Arquivos estáticos (imagens, CSS, etc.)
│   ├── templates/               # Templates HTML
│   ├── instance/
│   │   └── geren_servicos.db    # Banco de dados SQLite
│   ├── tests/                   # Arquivos de teste
├── README.md                    # Documentação do projeto
├── requirements.txt             # Dependências do projeto

Próximas Melhorias

Adicionar paginação para listas de clientes e agendamentos.

Melhorar a interface do usuário com frameworks CSS, como Bootstrap.

Implementar funcionalidade de recuperação de senha.

Adicionar suporte para múltiplos idiomas.


Contribuições

Sinta-se à vontade para contribuir com este projeto. Envie um pull request ou abra uma issue com sugestões de melhorias ou correções.

Licença

Este projeto é de uso pessoal e educacional. Caso deseje usar comercialmente, entre em contato com o autor.


---

Autor

Jon-dev67
GitHub: Jon-dev67
