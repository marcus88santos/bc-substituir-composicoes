# Automação para Exclusão e Atualização das Composições de um Orçamento
![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)  

<br />
Esta aplicação automatiza a etapa de exclusão e substituição de composições de um orçamento, pré-determinadas em uma planilha do Excel. A aplicação integra o uso de navegação automatizada em páginas web para acessar e manipular informações de orçamentos em uma plataforma específica. O sistema foi desenvolvido para otimizar o processo de gestão de composições e encargos, garantindo eficiência e precisão nas alterações necessárias.
<br />

Duração de cada ciclo de formatação:<br />
>~~cerca de 15 min~~<br />
>**alguns segundos**

## :hammer: Funcionalidades

- **Leitura e Processamento de Planilhas Excel**: Leitura de planilhas contendo dados de composições a serem alteradas ou removidas.
- **Automação de Navegação Web**: Acesso automatizado à plataforma de orçamentos via Selenium WebDriver.
- **Substituição e Exclusão de Composições**: Alteração de composições existentes com base em um conjunto de regras definidas e exclusão de composições obsoletas.
- **Verificação de Encargos Remanescentes**: Identificação de encargos que ainda necessitam de ajustes após a realização das alterações.


## :page_facing_up: Estrutura do Código

   - Uso de variáveis de ambiente para garantir segurança e flexibilidade na configuração de credenciais e caminhos de arquivos.
   - Automação com Selenium para replicar interações humanas com a interface web de forma eficiente.
   - Tratamento de exceções para lidar com possíveis falhas durante a navegação e manipulação de dados.
   - Estruturação modular do código para garantir que cada funcionalidade seja facilmente extensível e reutilizável.

O código é dividido em várias etapas:

### 1. `functions.py`

Este arquivo contém funções responsáveis por manipular e processar planilhas Excel para obter as composições que devem ser alteradas ou removidas:

- `read_sheet(file)`: Lê as informações da planilha e identifica colunas como status, código a substituir, base, novo tipo, novo código e nova base.
- `get_changes(folder, file)`: Processa a planilha de alterações e retorna uma lista de mudanças.
- `get_orcamento(folder, title)`: Lê o orçamento diretamente de um arquivo de texto.

### 2. `functionsBrowser.py`

Responsável por interagir com o navegador e manipular as informações na plataforma de orçamentos online:

- `open_browser()`: Inicializa o navegador com opções de configuração.
- `login(browser)`: Realiza login na plataforma utilizando credenciais armazenadas em variáveis de ambiente.
- `navegate_to(url, browser)`: Navega até uma URL específica.
- `get_encargos(browser)`: Retorna uma lista de composições que ainda possuem encargos a serem ajustados.
- `do_changes(browser, changes)`: Aplica as mudanças de acordo com as regras definidas na planilha.

### 3. `main.py`

Coordena o fluxo principal da aplicação:

- Carrega as composições a serem alteradas através de `get_changes`.
- Inicia o navegador e realiza login na plataforma.
- Acessa e exibe a lista de composições do orçamento selecionado.
- Aplica as mudanças e verifica encargos remanescentes.

## ✔️ Técnicas e tecnologias utilizadas

| [![My Skills](https://skillicons.dev/icons?i=py)]() |  
|                          :---:                      |
| Python                                              |  

<br />

### Bibliotecas

- `OpenPyXL`: Biblioteca para manipulação de planilhas Excel.
- `Selenium` WebDriver**: Automação de navegação web para manipular a plataforma de orçamentos.
- `dotenv`: Gerenciamento de variáveis de ambiente.
- `Chrome WebDriver Manager`: Gerenciamento automático do driver do Chrome para Selenium.


## 🛠️ Como Usar

1. **Pré-requisitos**:
   - Instalar as bibliotecas: 
     ```
     pip install -r requeriments.txt
     ```
   - Criar um arquivo chamado '.env' na raiz do projeto, definindo as variáveis:
      - EMAIL: Usuário para login na plataforma de orçamentos.
      - CODIGO: Código de acesso.
      - FOLDER: Pasta onde estão os arquivos em excel.
      - FILE_COMPOSICOES: Nome do arquivo .xlsx com as composições.
      - HOME: URL da plataforma de orçamentos.
      - URL_ORCAMENTOS: URL da lista de orçamentos.
      - TITLE_ORCAMENTO: Nome do orçamento a ser processado.

      exemplo:
      ```
      echo "EMAIL=usuario@email.com" > .env
      echo "CODIGO=codigo_de_acesso" >> .env
      echo "FOLDER=\(...)\caminho-da-pasta-com-os-arquivos" >> .env
      echo "FILE_COMPOSICOES=planilha_composicoes.xlsx" >> .env
      echo "HOME=https://url_completa_plataforma" >> .env
      echo "URL_ORCAMENTOS=https://url_completa_lista_orcamentos" >> .env
      echo "TITLE_ORCAMENTO=titulo_do_orcamento" >> .env
      ```
   
2. **Execução**:
   - Execute a aplicação
   ```
   python main.py
   ```


## 🚶 Autor

| [<img loading="lazy" src="https://github.com/marcus88santos.png?size=115" width=115><br><sub>marcUs fiLLipe santos</sub>](https://github.com/marcus88santos) |
| :---: |

<div>
<a href="https://www.linkedin.com/in/marcus88santos" target="_blank"><img loading="lazy" src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>   
</div>