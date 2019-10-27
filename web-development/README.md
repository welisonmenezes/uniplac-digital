# Guideline Web Development

## Estrutura de diretório

A aplicação em si encontra-se no diretório application/

No diretório database/ encontra-se o dump do banco de dados atualizado.


## Usuários para testes:

Foram cadastrados 4 usuários, cada qual com um nível de permissão. Estes são:

- login: admin, senha: 123456, permissão: Administrador (Nível 1);
- login: editor, senha: 123456, permissão: Editor (Nível 2);
- login: author, senha: 123456, permissão: Autor (Nível 3);
- login: user, senha: 123456, permissão: Usuário (Nível 4)


## Banco de dados

- O SGBD escolhido para o projeto é o MariaDB versão 10.1.3 ou superior.
- Site do MariaDB: <https://mariadb.org/>.
- A instalação utilizada pelo time de desenvolvimento é a versão integrada com o XAMPP 7.3.2.
- Site do XAMPP: <https://www.apachefriends.org/pt_br/index.html>.


## Problemas com o upload de imagem (Solução)

Caso haja problema com o upload de imagem, talvez seja necessário aumentar os valores dos seguintes campos no arquivo my.ini: innodb_log_file_size e max_allowed_packet.

Abaixo segue o exemplo de como implementamos em nosso ambiente:

`innodb_log_file_size = 100M`

`max_allowed_packet = 100M`


## Dependências da aplicação

A aplicação está sendo rodada com Python 3.7.4. As dependências do aplicação estão descritas no arquivo application/requirements.txt.

A instalação de todas as dependências podem ser realizadas pelo seguinte commando executado a partir do diretório application/:

`pip install -r requirements.txt`


#### Qualquer dúvida, estamos à disposição.