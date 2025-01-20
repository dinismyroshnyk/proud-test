# Instruções
## Configuração do ambiente virtual
Abre o terminal aqui no diretório proud.page, e muda (cd) para o diretório backend (de maior nível, o que contém os diretórios backend e proud)  
*OU*  
Abre o terminal no diretório backend

Estando o terminal no diretório backend, cria o ambiente virtual:  
`python -m venv projectenv`  
**Nota:** O nome 'projectenv' é para ser igual para todos nós, porque assim o .gitignore necessita apenas de uma única linha para os ambientes virtuais de todos.

## Configuração das variáveis de ambiente
Ainda no mesmo diretório backend que anteriormente, cria um ficheiro .env e coloca (por agora) as tuas variáveis pessoais de ligação à base de dados.  
Para isto deves criar uma base de dados local, chama-lhe o que quiseres, e no ficheiro .env o conteúdo deve ser o seguinte:  
**DB_NAME=nome_bd**  
**DB_USER=user**  
**DB_PASSWORD=password**  
**DB_HOST=localhost**  
**DB_PORT=5432**

**De notar:** Não se utilizam plicas ou aspas e não devem haver espaços antes ou depois do igual. O 'nome_bd' deve ser o nome da base de dados criada. O 'user' e a 'password' é o que tens configurado no postgresql no teu pc, provavelmente é postgres para ambos.<br> Estes dados são apenas enquanto não temos os dados para a base de dados remota, depois trocamos para esses.  

## Autenticação para o github
Enquanto método de autenticação para o github, se o login normal estiver a resultar em código 403, experimenta utilizar um PAT (Personal Access Token).
Para isso tens de:
1. Ir ao github, clicar na foto de perfil no canto superior direito e depois no menu que aparece clicar em settings.
2. Nas settings, dá scroll nas tabs à esquerda, a última deve ser 'Developer Settings', clica nessa opção.
3. Nas developer settings, deves ter uma tab de Personal Access Token, clica e depois clica em Tokens (Classic).
4. Depois clica em generate new token > generate new token (classic).
5. Talvez tenhas de usar alguma forma de autenticação, como uma passkey ou assim. Configuras o prazo do token e defines que tem acesso à opção repo (que selecionada, também seleciona as sub opções).
6. Quando for gerado, copia-o e guarda-o no teu pc numa nota chamada token.txt ou algo assim, porque quando saíres dessa página onde ele é apresentado, não o voltas ver.
7. Utilizá-lo quando te autenticares ao tentar dar push para o repositório remoto.

## Conclusão
Com isto deves poder dar push (para origin:dev e não origin:main !!) sem problemas.
