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

pb = PushBullet(CHAVE_DA_API_AQUI)

def criar_tabela():
    conn = sqlite3.connect('precos.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS produtos
                        (url TEXT PRIMARY KEY, nome VARCHAR, preco REAL, menor_preco REAL, maior_preco REAL, categoria TEXT)''')
    conn.commit()
    conn.close()

def atualizar_preco(url, nome, preco, categoria):
    conn = sqlite3.connect('precos.db')
    cursor = conn.cursor()

    cursor.execute(''' SELECT * FROM produtos WHERE url = ? ''', (url,))
    produto = cursor.fetchone()

    if produto is None:
        cursor.execute(''' INSERT INTO produtos VALUES (?, ?, ?, ?, ?, ?) ''', (url, nome, preco, preco, preco, categoria))
        print(f'Produto {nome} foi adicionado ao banco de dados.')
        pb.push_note('Novo Produto!', f'Produto {nome} foi adicionado ao banco de dados.')
    else:
        _, _, last_price, min_price, max_price, _ = produto
        if preco != last_price:
            if preco < min_price:
                min_price = preco
                pb.push_note('O produto ficou mais barato!', f'Produto {nome} atingiu o preço {min_price:.2f}.')
            elif preco > max_price:
                max_price = preco
                pb.push_note('O produto ficou mais caro!', f'Produto {nome} atingiu o preço {max_price:.2f}.')
            cursor.execute(''' UPDATE produtos SET preco = ?, menor_preco = ?, maior_preco = ? WHERE url = ? ''', (preco, min_price, max_price, url))
            print(f'Preço do produto {nome} foi atualizado! Acesse o banco de dados para mais detalhes.')
    conn.commit()
    conn.close()


# class tit-prod 
# class val-prod valVista
def verifica_preco(url, categoria):
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)
    time.sleep(5)
    driver.get(url)
    time.sleep(15)

    try:
        nome_element = driver.find_element(By.CSS_SELECTOR, '.tit-prod')
        preco_element = driver.find_element(By.CSS_SELECTOR, '.valVista')
        tbt_avise_elements = driver.find_elements(By.CSS_SELECTOR, '.tbt_avise')

        if not tbt_avise_elements:
            nome = nome_element.text.strip()
            preco = float(preco_element.text.strip().replace('R$', '').replace('.', '').replace(',', '.'))
            print(f'Produto: {nome}')
            print(f'Preço à vista: {preco:.2f}')
            atualizar_preco(url, nome, preco, categoria)
        else:
            print('Fora de estoque')
    except NoSuchElementException:
        print('Elemento não encontrado')



def agendando_notificacao(categorias):
    for categoria, urls in categorias.items():
        for url in urls:
            schedule.every(1).minutes.do(verifica_preco, url, categoria)
    while True:
        schedule.run_pending()
        time.sleep(3)
criar_tabela()
categorias = {
    'CPU': [
        'padrao_para_link_do_produto',
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
    ],
    'GPU': [
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
    ],
    'RAM': [
        'padrao_para_link_do_produto',
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
    ],
    'MOBO': [
        'padrao_para_link_do_produto',
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
    ],
    'ARMAZENAMENTO': [
        'padrao_para_link_do_produto',
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
    ],
    'REFRIGERACAO': [
        'padrao_para_link_do_produto',
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
        
    ],
    'GABINETE': [
        'padrao_para_link_do_produto',
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
        'padrao_para_link_do_produto', 
    ],
    'TECLADO': [],
}

agendando_notificacao(categorias)
