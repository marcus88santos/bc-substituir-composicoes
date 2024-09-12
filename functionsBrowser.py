import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

load_dotenv()

USER = os.getenv('EMAIL')
PASS = os.getenv('CODIGO')
HOME = os.getenv('HOME')
URL_ORCAMENTOS = os.getenv('URL_ORCAMENTOS')

def open_browser():
  chrome_install = ChromeDriverManager().install()
  directory = os.path.dirname(chrome_install)
  chromedriver_path = os.path.join(directory, "chromedriver.exe")
  service = Service(chromedriver_path)
  options = webdriver.ChromeOptions()
  options.add_experimental_option("detach", True)
  options.add_argument('--enable-notifications')
  options.add_argument("start-maximized")
  options.add_argument("--headless=new")
  options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
  browser = webdriver.Chrome(service=service,options=options)
  
  return browser

def login(browser):
  browser.get(HOME)
  
  # Verificando se o usuário já está logado
  try:
    write_on(browser, 'id', 'email', USER)
    write_on(browser, 'id', 'senha', PASS)
    
    # Fazendo login
    click_on(browser, 'xpath', '//*[@id="bottom-wizard"]/button')
    # browser.get(HOME)
    print('\n-> Login realizado com sucesso')
  except:
    print('\n-> Usuário já está logado')
    return

def skip_alert(browser):
  try:
    browser.switch_to.alert.acept()
    print('-> Alerta aceito')
    return True
  except:
    print('-> Não há alerta')
    return False

def navegate_to(url, browser):
  # skip_alert(browser)
  browser.get(url)
  # skip_alert(browser)
  print('-> Url acessada: ' + browser.current_url) 

def write_on(el, selector_type, selector_search, text):
  try:
    el = find_el(el, selector_type, selector_search)
    el.send_keys(text)
  except:
    return

def click_on(el, selector_type, selector_search):
  try:
    el = find_el(el, selector_type, selector_search)
    el.click()
  except:
    return

def get_encargos(browser):
  encargos = []
  els = find_els(browser, 'CSS_SELECTOR', 'tr.success')
  for el in els:
    title = find_el(el, 'CSS_SELECTOR', 'td:nth-child(3)>a').text
    if title.lower().find('encargos') != -1:
      encargos.append({'codigo_a_substituir': find_el(el, 'CSS_SELECTOR', 'td:nth-child(1)').text,
                       'base': find_el(el, 'CSS_SELECTOR', 'td:nth-child(2)').text, 'descricao': title})
  
  if len(encargos) > 0:
    print('\n-> Composições restantes com o termo "encargos":\n')
    for encargo in encargos:
      print(encargo['codigo_a_substituir'] + ';' + encargo['base'] + ';' + encargo['descricao'])
    print('')
  else:
    print('\n-> Não existem mais composições com o termo "encargos"\n')
  return

def do_changes(browser, changes):
  composicoes = find_els(browser, 'CSS_SELECTOR', 'tr.success')
  i = 0
  
  # Iterando sobre as composições
  while i < len(composicoes):
    codigo_comp = str(find_el(composicoes[i], 'CSS_SELECTOR', 'td:nth-child(1)').text)
    base_comp = str(find_el(composicoes[i], 'CSS_SELECTOR', 'td:nth-child(2)').text).lower()
    descricao_comp = str(find_el(composicoes[i], 'CSS_SELECTOR', 'td:nth-child(3)').text).lower()
    
    # Excluindo encargos ORSE
    if (base_comp == "orse") and (descricao_comp.find('encargos complementares') != -1):
      delete_comp(browser, composicoes[i])
      composicoes = find_els(browser, 'CSS_SELECTOR', 'tr.success')
      i = 0
      continue
    
    # Alterando composições
    for change in changes:
      codigo_alteracao = str(change['codigo_a_substituir'])
      # print('-> código alteração: ' + str(change['codigo_a_substituir']))
      if codigo_alteracao == codigo_comp:
        if change['novo_tipo'] == 'excluir':
          delete_comp(browser, composicoes[i])

        else:
          update_comp(browser, composicoes[i], change)
        
        composicoes = find_els(browser, 'CSS_SELECTOR', 'tr.success')
        i = -1
        break
    i += 1
  return

def update_comp(browser, composicao, change):
#   # Clicando no ícone de substituição
  codigo_comp = str(find_el(composicao, 'CSS_SELECTOR', 'td:nth-child(1)').text)
  base_comp = str(find_el(composicao, 'CSS_SELECTOR', 'td:nth-child(2)').text).lower()
  descricao_comp = str(find_el(composicao, 'CSS_SELECTOR', 'td:nth-child(3)').text).lower()
  el = find_el(composicao, 'CSS_SELECTOR', 'td:nth-child(8)>a')
  el.click()
  
  # Localizando o container
  id_container = el.get_attribute('href')[el.get_attribute('href').find('#'):]
  container = find_el(browser, 'CSS_SELECTOR', id_container)
  
  # Escolhendo o tipo e a base
  match change['novo_tipo']:
    case 'insumo':
      click_on(container, 'css_selector', 'i.flaticon-bricks9')
      
      match change['nova_base'].lower():
        case 'sinapi':
          click_on(container, 'css_selector', 'a[classe="insumo"][banco="SINAPI"]')
        case 'próprio':
          click_on(container, 'css_selector', 'a[classe="insumo"][banco="Emp"]')
        case 'orse':
          click_on(container, 'css_selector', 'a[classe="insumo"][banco="ORSE"]')
    
    case 'composicao':
      match change['nova_base'].lower():
        case 'sinapi':
          click_on(container, 'css_selector', 'a[classe="composicao"][banco="SINAPI"]')
        case 'próprio':
          click_on(container, 'css_selector', 'a[classe="composicao"][banco="Emp"]')
        case 'orse':
          click_on(container, 'css_selector', 'a[classe="composicao"][banco="ORSE"]')
  
#   # Escolhendo a nova composição ou insumo
  write_on(container, 'css_selector', 'input[name="input_codigo"]', change['novo_codigo'])
  nova_descricao = find_el(container, 'css_selector', 'tr[codigo="' + change['novo_codigo'] + '"]').get_attribute('descricao')
  click_on(container, 'css_selector', 'tr[codigo="' + change['novo_codigo'] + '"]')
  click_on(container, 'css_selector', 'button.btn.btn-primary')
  print('\n-> Alterado:')
  print(codigo_comp + ' ' + base_comp.upper() + ' - ' + descricao_comp)
  print('-> Para:')
  print(str(change['novo_tipo']) + ': ' + str(change['novo_codigo']) + ' ' + str(change['nova_base']).upper() + ' - ' + str(nova_descricao))
  wait_close(browser, 'CSS_SELECTOR', id_container)

def delete_comp(browser, composicao):
  # Clicando no ícone de exclusão
  codigo_comp = str(find_el(composicao, 'CSS_SELECTOR', 'td:nth-child(1)').text)
  base_comp = str(find_el(composicao, 'CSS_SELECTOR', 'td:nth-child(2)').text).lower()
  descricao_comp = str(find_el(composicao, 'CSS_SELECTOR', 'td:nth-child(3)').text).lower()
  el = find_el(composicao, 'CSS_SELECTOR', 'td:nth-child(9)>a')
  el.click()
  
  # Localizando o container
  id_container = el.get_attribute('href')[el.get_attribute('href').find('#'):]
  container = find_el(browser, 'CSS_SELECTOR', id_container)
  
  # Digitando a palavra excluir
  href = id_container[id_container.find('confirmar-exclusao-'):].replace('-', '_', 1)
  id_input = 'texto_de_exclusao_' + str(href[href.find('-') + 1:])
  write_on(container, 'id', id_input, 'excluir')
  
  # Clicando em excluir
  click_on(container, 'css_selector', id_container + ' > div.modal-footer > button')
  print('\n-> Deletado:\n' + codigo_comp + ' ' + base_comp.upper() + ' - ' + descricao_comp)
  wait_close(browser, 'CSS_SELECTOR', id_container)

def find_el(el, selector_type, selector_search):
  try:
    WebDriverWait(el, 2).until(
      EC.element_to_be_clickable((
        eval('By.' + selector_type.upper()), selector_search
      ))
    )
    return el.find_element(eval('By.' + selector_type.upper()), selector_search)
  except:
    print('-> Elemento não encontrado:\nseletor:' + selector_search)
    return None

def find_els(el, selector_type, selector_search):
  try:
    # WebDriverWait(el, 2).until(
    #   EC.element_to_be_clickable((
    #     eval('By.' + selector_type.upper()), selector_search
    #   ))
    # )
    return el.find_elements(eval('By.' + selector_type.upper()), selector_search)
  except:
    print('-> Elementos não encontrados:\nseletor:' + selector_search)
    return None

def wait_close(el, selector_type, selector_search):
  while True:
    try:
      WebDriverWait(el, 2).until(
        EC.element_to_be_clickable((
          eval('By.' + selector_type.upper()), selector_search
        ))
      )
      e = el.find_element(eval('By.' + selector_type.upper()), selector_search)
    except:
      e = None
    if e == None:
      break