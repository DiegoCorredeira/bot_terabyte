import time
import os 
import dotenv
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
    chrome_options = Options()
    chrome_options.add_argument("--window-position=-2000,0")
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
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
        'https://www.terabyteshop.com.br/produto/21631/placa-de-video-inno3d-geforce-rtx-3060-twin-x2-12gb-gddr6-dlss-ray-tracing-n30602-12d6-119032ah',
        'https://www.terabyteshop.com.br/produto/24906/placa-de-video-zotac-gaming-geforce-rtx-3060-twin-edge-oc-white-12gb-gddr6-dlss-ray-tracing-zt-a30600h-10m', 
        'https://www.terabyteshop.com.br/produto/24158/placa-de-video-leadtek-winfast-nvidia-geforce-rtx-3060-ti-hurricane-white-edition-8gb-gddr6-dlss-ray-tracing',
        'https://www.terabyteshop.com.br/produto/23276/placa-de-video-colorful-igamer-nvidia-geforce-rtx-3060-ultra-w-oc-8gb-gddr6-dlss-ray-tracing', 
        'https://www.terabyteshop.com.br/produto/24508/placa-de-video-superframe-nvidia-geforce-rtx-3060-12gb-gddr6-dlss-ray-tracing-rtx306012gd6p2ip3'
        'https://www.terabyteshop.com.br/produto/24384/placa-de-video-galax-nvidia-geforce-rtx-3060-ti-1-click-oc-plus-8gb-gddr6x-dlss-ray-tracing-36ism6md2kcv', 
        'https://www.terabyteshop.com.br/produto/21409/placa-de-video-gigabyte-nvidia-geforce-rtx-2060-windforce-oc-12gb-gddr6-dlss-ray-tracing-gv-n2060wf2oc-12gd',
        'https://www.terabyteshop.com.br/produto/20438/placa-de-video-msi-geforce-rtx-3060-ventus-2x-oc-lhr-12gb-gddr6-dlss-ray-tracing-912-v397-050',
        'https://www.terabyteshop.com.br/produto/25063/placa-de-video-msi-nvidia-geforce-rtx-4060-ti-ventus-3x-oc-8gb-gddr6x-dlss-ray-tracing-912-v515-023'
        'https://www.terabyteshop.com.br/produto/25064/placa-de-video-msi-nvidia-geforce-rtx-4060-ti-gaming-x-8gb-gddr6-dlss-ray-tracing-912-v515-022'
    ],
    'RAM': [
        'https://www.terabyteshop.com.br/produto/19314/memoria-kingston-fury-beast-8gb-3200mhz-ddr4-black-kf432c16bb8',
        'https://www.terabyteshop.com.br/produto/25032/memoria-ddr4-kingston-fury-superframe-rgb-8gb-3200mhz-black-kf432c16bba8cl', 
        'https://www.terabyteshop.com.br/produto/16829/memoria-ddr4-geil-orion-rgb-edicao-amd-8gb-3000mhz-gray-gaosg48gb3000c16asc', 
        'https://www.terabyteshop.com.br/produto/18885/memoria-ddr4-xpg-spectrix-d50-8gb-3200mhz-rgb-gray-ax4u320088g16a-st50', 
        'https://www.terabyteshop.com.br/produto/23879/memoria-ddr4-zadak-spark-rgb-16gb-3600mhz-black-zd4-spr36c25-16gyb1?p=714486', 
        'https://www.terabyteshop.com.br/produto/16835/memoria-ddr4-geil-evo-x-ii-rgb-sync-8gb-3000mhz-gaexsy48gb3000c16asc?p=714486',
        'https://www.terabyteshop.com.br/produto/19156/memoria-kingston-fury-beast-16gb-3600mhz-ddr4-cl17-preto-kf436c17bbk216',
        'https://www.terabyteshop.com.br/produto/25000/memoria-ddr4-netac-shadow-ii-8gb-3200mhz-white-ntswd4p32sp-08w',
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