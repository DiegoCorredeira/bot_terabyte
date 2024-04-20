
## Monitoramento de preços TerabyteShop

O código fornecido é um sistema de monitoramento de preços que verifica regularmente o preço de vários produtos em sites de comércio eletrônico e armazena essas informações em um banco de dados. Ele também permite pesquisar por produtos específicos no banco de dados.

### Funcionalidades Principais

1. Monitoramento de Preços: O código verifica regularmente o preço de vários produtos em sites de comércio eletrônico e atualiza o banco de dados com as informações mais recentes. Se o preço atingir o menor ou o maior valor registrado, uma notificação é enviada usando o serviço Pushbullet.

2. Armazenamento de Dados: As informações do produto, como URL, nome, preço atual, menor preço registrado e maior preço registrado, são armazenadas em um banco de dados SQLite chamado "precos.db".

3. Pesquisa de Produtos: É possível pesquisar por produtos específicos no banco de dados, fornecendo o nome do produto desejado. Os resultados são exibidos, incluindo as informações relevantes do produto.

### Dependências

Para executar o código, você precisa ter as seguintes dependências instaladas:

- Python 3.x: O código é escrito em Python e requer uma versão 3.x para ser executado.

- Selenium: É uma biblioteca utilizada para interagir com o navegador da web e extrair informações das páginas da web. Pode ser instalada usando o comando `pip install selenium`.

- ChromeDriver: É um executável necessário para que o Selenium funcione com o Google Chrome. O ChromeDriverManager pode ser usado para baixar e gerenciar automaticamente a versão correta do ChromeDriver. Para instalá-lo, use o comando `pip install webdriver_manager`.

- Pushbullet: É uma biblioteca para enviar notificações push para dispositivos usando o serviço Pushbullet. Pode ser instalada usando o comando `pip install pushbullet.py`.

- SQLite: É um banco de dados embutido que armazena as informações dos produtos. Não requer instalação separada, pois é incluído na biblioteca padrão do Python.

### Como Executar o Código

Para executar o código, siga as etapas abaixo:

1. Instale as dependências mencionadas acima usando os comandos `pip install selenium`, `pip install webdriver_manager` e `pip install pushbullet.py`.

2. Certifique-se de ter o Google Chrome instalado em seu sistema. O ChromeDriver requer o Google Chrome para funcionar corretamente. Você pode fazer o download do Chrome em https://www.google.com/chrome/.

3. Copie o código fornecido para um arquivo Python com a extensão ".py", como "monitorar_precos.py".

4. Abra o arquivo Python em um editor de texto ou ambiente de desenvolvimento integrado (IDE).

5. Modifique a seção `urls_por_categoria` no código para adicionar as URLs dos produtos que deseja monitorar. Certifique-se de associar cada URL a uma categoria relevante.

6. Salve o arquivo Python modificado.

7. No terminal ou prompt de comando, navegue até o diretório onde o arquivo Python está localizado.

8. Execute o arquivo Python usando o comando `python monitorar_precos.py`.

9. O código começará a monitorar os preços dos produtos e ex

ibirá informações relevantes no console. Se algum preço atingir o menor ou o maior valor registrado, uma notificação será enviada usando o serviço Pushbullet.

10. Para pesquisar por um produto específico no banco de dados, chame a função `pesquisar_produto` e passe o nome do produto como argumento. O código exibirá os resultados da pesquisa no console.


-> No momento atual, o projeto encontra-se em manutenção 
