#Import das bibliotecas
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

# Criação do dicionário que receberá os registros
dic_produtos = {'marca':[], 'preco':[], 'desconto':[], 'link':[]}

#FutFanatics - Parte 1
url = 'https://www.futfanatics.com.br/loja/catalogo.php?loja=311840&categoria=1161&variacao=tamanho_41&range=&order=2&pg=1'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
site = requests.get(url, headers=headers)
encoding = site.encoding if 'charset' in site.headers.get('content-type', '').lower() else None
parser = 'html5lib'
soup = BeautifulSoup(site.content, parser, from_encoding=encoding)
totais = soup.find_all('div', class_="search-counter")
total_texto = totais[0].get_text().strip()
index = total_texto.find(' ')
qtd  = total_texto[:index]
ultima_pagina = math.ceil(int(qtd)/40)
print("Quantidade de produtos (FutFanatics):",qtd)
print("Quantidade de páginas (FutFanatics):",ultima_pagina)

#FutFanatics - Parte 2
for i in range(1, ultima_pagina+1):
    print('FutFanatics - página', i, 'de', ultima_pagina)
    url_pag = f'https://www.futfanatics.com.br/loja/catalogo.php?loja=311840&categoria=1161&variacao=tamanho_41&range=&order=2&pg={i}'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, parser, from_encoding=encoding)
    produtos = soup.find_all('div', class_=re.compile('product-item'))
    for produto in produtos:
        marca = produto.find('div', class_=re.compile('product-name')).get_text().strip()
        preco = produto.find('div', class_='price').get_text().strip()
        desconto = 0
        descontos = produto.find_all('span', class_=re.compile('discount'))
        if len(descontos) > 0:
            desconto = descontos[0].get_text().strip()
        link = produto.find_all('a', href=True)[0]['href']
        dic_produtos['marca'].append(marca)
        dic_produtos['preco'].append(preco)
        dic_produtos['desconto'].append(desconto)
        dic_produtos['link'].append(link)

# Cria o DataFrame Pandas com os produtos capturados
df = pd.DataFrame(dic_produtos)

# Faz algumas transformações nas colunas capturadas
tabela = df.copy()
tabela['preco'] = tabela['preco'].apply(lambda x: str(x).replace(".",'').replace("R$",''))
tabela['preco'] = pd.to_numeric(tabela['preco'].apply(lambda x: str(x).replace(",",'.')))
tabela['desconto'] = pd.to_numeric(tabela['desconto'].apply(lambda x: str(x).replace("%",'')))
tabela = tabela.sort_values(by=['desconto'],ascending=False)

# Exporta o resultado para CSV
tabela.to_csv('precoChuteiras.csv', encoding='utf-8', sep=',', index=False)