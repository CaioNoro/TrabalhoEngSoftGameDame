from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

servico = Service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service=servico)

navegador.get("http://127.0.0.1:8000/")

navegador.find_element('xpath', '//*[@id="search"]').send_keys('of')
navegador.find_element('xpath', '//*[@id="search-form"]/button').click()

if navegador.current_url.startswith("http://127.0.0.1:8000/search/"):
    print("Teste 1 - Concluído")

flag = 1
while (flag):
    flag = input()


navegador.get("http://127.0.0.1:8000/accounts/login/")
navegador.find_element('xpath', '//*[@id="id_username"]').send_keys('teste')
navegador.find_element(
    'xpath', '//*[@id="id_password"]').send_keys('Senhadeteste2023')
navegador.find_element(
    'xpath', '/html/body/div/div/div/div/div/form/button').click()
navegador.get("http://127.0.0.1:8000/accounts/login/")
navegador.get("http://127.0.0.1:8000/game/7")
navegador.find_element('xpath', '//*[@id="cart-button"]').click()

if (navegador.current_url == "http://127.0.0.1:8000/cart/"):
    print("Teste 2 - Concluído")

flag = 1
while (flag):
    flag = input()

navegador.find_element('xpath', '//*[@id="shopping-cart"]/div/div[1]/div/div/a[2]').click()
navegador.get('http://127.0.0.1:8000/accounts/logout/')
navegador.get('http://127.0.0.1:8000/accounts/register/')
navegador.find_element('xpath', '//*[@id="id_username"]').send_keys('Albert')
navegador.find_element(
    'xpath', '//*[@id="id_email"]').send_keys('albert@email.com')
navegador.find_element('xpath', '//*[@id="id_first_name"]').send_keys('Albert')
navegador.find_element(
    'xpath', '//*[@id="id_last_name"]').send_keys('Einstein')
navegador.find_element(
    'xpath', '//*[@id="id_password1"]').send_keys('Senhadeteste2023')
navegador.find_element(
    'xpath', '//*[@id="id_password2"]').send_keys('fdfdsfdsfsd')
navegador.find_element(
    'xpath', '/html/body/div/div/div/div/div/form/button').click()

if (navegador.find_element('xpath', '//*[@id="error_1_id_password2"]')):
    print("Teste 3 - Concluído")

flag = 1
while (flag):
    flag = input()
