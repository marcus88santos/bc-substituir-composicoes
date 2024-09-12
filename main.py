from functions import get_changes, get_orcamento
from functionsBrowser import find_el, find_els, login, open_browser, navegate_to, write_on, click_on, get_encargos, do_changes
import os
from dotenv import load_dotenv
load_dotenv()

FOLDER=os.getenv('FOLDER')
FILE_COMPOSICOES=os.getenv('FILE_COMPOSICOES')
URL_ORCAMENTOS=os.getenv('URL_ORCAMENTOS')
TITLE_ORCAMENTO=os.getenv('TITLE_ORCAMENTO')

# Vericando composições a serem substituídas ou excluídas
changes = get_changes(FOLDER, FILE_COMPOSICOES)

# Abrindo o navegador
browser = open_browser()

# Fazendo login no orçafascio
login(browser)

# Acessando lista de orçamentos
navegate_to(URL_ORCAMENTOS, browser)

# Acessando orçamento
orcamento = get_orcamento(FOLDER, TITLE_ORCAMENTO)

write_on(browser, 'id', 'filtro_descricao', orcamento)
click_on(browser, 'link_text', orcamento)
print('-> Url acessada: ' + browser.current_url) 

# Acessando composições
click_on(browser, 'link_text', 'Exibir')
click_on(browser, 'link_text', 'Lista de Composições')
print('-> Url acessada: ' + browser.current_url) 

# Substituindo composições
do_changes(browser, changes)

# Verifcando se ainda existem encargos
get_encargos(browser)

# Fechando o navegador
browser.quit()
print('-> Processo finalizado com sucesso\n')