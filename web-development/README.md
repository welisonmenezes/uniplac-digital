# Guideline Web Development

## Banco de dados

- O SGBD escolhido para o projeto é o MariaDB versão 10.1.3 ou superior.
- Site do MariaDB: <https://mariadb.org/>.
- A instalação utilizada pelo time de desenvolvimento é a versão integrada com o XAMPP 7.3.2.
- Site do XAMPP: <https://www.apachefriends.org/pt_br/index.html>.


## Problemas com o upload de imagem (Solução)

Ao tentar salvar uma imagem na base64 no banco de dados nos deparamos com o problema de limite de tamanho do arquivo de log, por algum motivo o MariaDB tenta escrever no log quando há problema.

Também tivemos contratempos com o tamanho máximo em bytes de uma única instrução que o MariaDB está configurado para executar por padrão. Em ambas as situações é emitido um erro, que no caso do Python e do PHPMyAdmin, era silenciso.

Após algumas boas horas de pesquisa descobrimos que q solução estava em checar o arquivo my.ini e definir valores adequados para os seguintes campos: innodb_log_file_size e max_allowed_packet.

Veja como configuramos em nosso ambiente:

`innodb_log_file_size = 100M`

`max_allowed_packet = 100M`