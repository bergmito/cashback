Projeto Cashback
  Utiliza o framework Flask, com o ORM SQLAlchemy (neste exemplo está em uso o banco de dados MySQL).
  
Para instalar as dependências 
  pip install -r requirements.txt

Instruções para execução do app:
  1) Altere, no arquivo setup.py, o usuário, senha e o caminho para o banco de dados.
  2) Execute o setup.py para gerar a estrutura do banco.
  3) Altere no arquivo session_management.py o usuário, senha e o caminho para o banco de dados.
  4) Para iniciar a aplicação execute python main.py
  
Instruções para teste
  1) Execute o comando: python -m unittest
  
Lembrando que para o funcionamento dos testes e da aplicação, é necessário que
o caminho, usuário e senha do servidor de banco de dados MySQL estejam corretos.
