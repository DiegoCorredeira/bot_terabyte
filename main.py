import time
import os 
import dotenv
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from pushbullet import PushBullet
import sqlite3



API_KEY = os.getenv("API_KEY")
pb = PushBullet(API_KEY)

def criar_tabela():
    conn = sqlite3.connect('precos.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS produtos
                        (url TEXT PRIMARY KEY, nome VARCHAR, preco REAL, menor_preco REAL, maior_preco REAL, categoria TEXT)''')
    conn.commit()
    conn.close()

# class tit-prod 
# class val-prod valVista
def verifica_preco(url, categoria):
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)

    driver.get(url)

    try:
        nome_element = driver.find_element(By.CSS_SELECTOR, '.tit-prod')
        preco_element = driver.find_element(By.CSS_SELECTOR, '.valVista')

        nome = nome_element.text.strip()
        preco = float(preco_element.text.strip().replace('R$', '').replace(',', '.'))

        print(f'Produto: {nome}')
        print(f'Preço à vista: {preco:2f}')
    except NoSuchElementException:
        print('Elemento não encontrado')
    
    driver.quit()

 
