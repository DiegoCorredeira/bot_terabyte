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
dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
pb = PushBullet(API_KEY)
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
        'https://www.terabyteshop.com.br/produto/21014/ryzen-3-4100-cooler-wraith-stealth',
        'https://www.terabyteshop.com.br/produto/21317/processador-amd-ryzen-5-4600g-37ghz-42ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4-100-100000147box', 
        'https://www.terabyteshop.com.br/produto/20782/processador-amd-ryzen-5-5500-36ghz-42ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4-100-100000457box', 
        'https://www.terabyteshop.com.br/produto/20788/processador-amd-ryzen-5-5600-35ghz-44ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4-100-100000927box'
        'https://www.terabyteshop.com.br/produto/18971/processador-amd-ryzen-5-5600g-39ghz-44ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4-com-video-integrado-100-100000252box', 
        'https://www.terabyteshop.com.br/produto/21277/processador-amd-ryzen-5-4500-36ghz-41ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4-100-100000644box', 
        'https://www.terabyteshop.com.br/produto/15692/processador-amd-ryzen-5-5600x-37ghz-46ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4', 
        'https://www.terabyteshop.com.br/produto/11543/processador-amd-ryzen-3-3200g-36ghz-40ghz-turbo-4-core-4-thread-cooler-wraith-stealth-am4', 
        'https://www.terabyteshop.com.br/produto/20813/processador-amd-ryzen-7-5700x-34ghz-46ghz-turbo-8-cores-16-threads-am4-sem-cooler-100-100000926wof', 
        'https://www.terabyteshop.com.br/produto/18973/processador-amd-ryzen-7-5700g-38ghz-46ghz-turbo-8-cores-16-threads-cooler-wraith-stealth-am4-com-video-integrado-100-100000263box', 
    ],
    'GPU': [
    ],
    'ARMAZENAMENTO': [
        'https://www.terabyteshop.com.br/produto/16596/ssd-wd-green-480gb-m2-nvme-leitura-2400mbs-e-gravacao-1650mbs-wds480g2g0c', 
        'https://www.terabyteshop.com.br/produto/23002/ssd-kingston-nv2-500gb-m2-nvme-2280-leitura-3500mbs-e-gravacao-2100mbs-snv2s500g', 
        'https://www.terabyteshop.com.br/produto/23000/ssd-kingston-nv2-1tb-m2-nvme-2280-leitura-3500mbs-e-gravacao-2100mbs-snv2s1000g',
        'https://www.terabyteshop.com.br/produto/23580/ssd-redragon-blaze-gd-703-512gb-m2-2280-leitura-7050mbs-gravacao-4200mbs', 
        'https://www.terabyteshop.com.br/produto/23808/ssd-kingston-nv2-250gb-m2-nvme-2280-leitura-3000mbs-e-gravacao-1300mbs-snv2s250g' 
    ],
    'REFRIGERACAO': [
        'https://www.terabyteshop.com.br/produto/21866/water-cooler-superframe-isengard-argb-360mm-intel-amd-controladora-black-sf-w360', 
        'https://www.terabyteshop.com.br/produto/25119/water-cooler-cougar-poseidon-lt-360-argb-360mm-intel-amd-black-cgr-psdltrgb-360',
        'https://www.terabyteshop.com.br/produto/15888/water-cooler-xpg-levante-360mm-rgb-intel-amd-15260035' 
        
    ],
    'GABINETE': [
        'https://www.terabyteshop.com.br/produto/24982/gabinete-gamer-liketec-cube-kirra-rgb-mid-tower-vidro-temperado-black-sem-fonte-com-4-fans', 
        'https://www.terabyteshop.com.br/produto/23305/gabinete-gamer-lian-li-o11-dynamic-mini-redragon-edition-mid-tower-vidro-temperado-atx-black-sem-fonte-sem-fan-o11dmini-rd-x', 
        'https://www.terabyteshop.com.br/produto/19584/gabinete-gamer-cooler-master-masterbox-nr200-vidro-temperado-white-mini-itx-sem-fonte-com-2-fans-mcb-nr200-wnnn-s00', 
    ],
    'TECLADO': [
        'https://www.terabyteshop.com.br/produto/24651/teclado-gamer-mecanico-redragon-lakshmi-led-white-switch-brown-abnt2-60-orangeblackgrey-k606-ogbkgy-pt-brown', 
        'https://www.terabyteshop.com.br/produto/22779/teclado-gamer-mecanico-akko-3068b-plus-black-e-gold-rgb-ansi-akko-jelly-purple',
        'https://www.terabyteshop.com.br/produto/23038/teclado-gamer-mecanico-redragon-lakshmi-lunar-white-rainbow-switch-brown-abnt2-k606w-r', 
        'https://www.terabyteshop.com.br/produto/23773/teclado-mecanico-gamer-redragon-dragonborn-rgb-switch-brown-abnt2-pinkwhite-k630pw-rgb-pt-brown', 
        'https://www.terabyteshop.com.br/produto/23628/teclado-mecanico-havit-kb879l-switch-outemu-red-ansi-rgb-blak', 
        'https://www.terabyteshop.com.br/produto/18388/teclado-gamer-optico-redragon-lakshmi-abnt2-61-teclas-switch-blue-k606r', 
        'https://www.terabyteshop.com.br/produto/22781/teclado-gamer-mecanico-akko-3068b-plus-black-e-pink-rgb-ansi-akko-jelly-pink'
    ],
    'CADEIRA': [
        'https://www.terabyteshop.com.br/produto/23097/cadeira-gamer-terabyte-vision-reclinavel-2d-preto-e-branco', 
        'https://www.terabyteshop.com.br/produto/23671/cadeira-gamer-terabyte-style-reclinavel-4d-preto',
        'https://www.terabyteshop.com.br/produto/22744/cadeira-gamer-superframe-knight-reclinavel-suporta-ate-140kg-preto-e-branco', 
        'https://www.terabyteshop.com.br/produto/23646/cadeira-gamer-superframe-godzilla-reclinavel-preto-e-cinza', 
        'https://www.terabyteshop.com.br/produto/19880/cadeira-gamer-superframe-hunter-reclinavel-suporta-ate-140kg-preto-e-branco'
    ]
}

agendando_notificacao(categorias)