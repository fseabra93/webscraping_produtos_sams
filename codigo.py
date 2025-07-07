import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

#processar Dental Capixaba
#pegar a planilah com os produtos


print("Iniciou dental Capixaba")

df_capixaba = pd.read_csv('teste_webscraping\produtos.csv')
df_capixaba = df_capixaba[['produto', 'Dental_Capixaba']]
df_capixaba = df_capixaba.dropna(subset=['Dental_Capixaba'])
df_capixaba['preco_capixaba'] = 0

lista_precos_capixaba = []

for _, produto in df_capixaba.iterrows():
    url = produto['Dental_Capixaba']
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            price_span = soup.find('span', id='variacaoPreco')
            if price_span:
                price = price_span.get_text(strip=True)
                # print(f"Preço: {produto}: {price}")
            else:
                price = 'Preço não encontrado'
                # print("Elemento de preço não encontrado.")
        else:
            price = f"Erro {response.status_code}"
            print(f"Erro ao acessar o site: {response.status_code}")
    except Exception as e:
        price = 'Erro na requisição'
        print(f"Exceção ao acessar {url}: {e}")

    lista_precos_capixaba.append(price)

df_capixaba['preco_capixaba'] = lista_precos_capixaba
df_capixaba = df_capixaba[['produto', 'preco_capixaba']]
df_capixaba['preco_capixaba'] = df_capixaba['preco_capixaba'].replace('Preço não encontrado', 0)
df_capixaba['preco_capixaba'] = df_capixaba['preco_capixaba'] .str.replace(',', '.', regex=False)
df_capixaba['preco_capixaba'] = pd.to_numeric(df_capixaba['preco_capixaba'], errors='coerce')

# df.to_csv('teste_webscraping\output_capixaba.csv', index=False)

#processar Dental Speed

print("Iniciou Dental Speed")

df_speed = pd.read_csv('teste_webscraping\produtos.csv')
df_speed = df_speed[['produto', 'Dental_Speed']]
df_speed = df_speed.dropna(subset=['Dental_Speed'])
df_speed['preco_speed'] = 0

lista_precos_speed = []

for _, produto in df_speed.iterrows():
    url = produto['Dental_Speed']
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Localiza o input com id 'yv-productPrice'
            input_tag = soup.find('input', id='yv-productPrice')

            if input_tag and input_tag.has_attr('value'):
                price = input_tag['value']
                # print(f"Preço encontrado: {price}")
            else:
                # print("Input com id 'yv-productPrice' não encontrado ou sem valor.")
                price = 0
        else:
            print(f"Erro ao acessar a página: {response.status_code}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    lista_precos_speed.append(price)

df_speed['preco_speed'] = lista_precos_speed
df_speed = df_speed[['produto', 'preco_speed']]
df_speed['preco_speed'] = df_speed['preco_speed'].replace('Preço não encontrado', 0)
df_speed['preco_speed'] = df_speed['preco_speed'] .str.replace(',', '.', regex=False)
df_speed['preco_speed'] = df_speed['preco_speed'] .str.replace('R$', '', regex=False)
df_speed['preco_speed'] = pd.to_numeric(df_speed['preco_speed'], errors='coerce')

# df.to_csv('teste_webscraping\output_speed.csv', index=False)


#processar Dental Cremer

print("Iniciou Dental Cremer")

df_cremer = pd.read_csv('teste_webscraping\produtos.csv')
df_cremer = df_cremer[['produto', 'Dental_Cremer']]
df_cremer = df_cremer.dropna(subset=['Dental_Cremer'])
df_cremer['preco_cremer'] = 0

lista_precos_cremer = []

for _, produto in df_cremer.iterrows():
    url = produto['Dental_Cremer']
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Localiza o input com id 'yv-productPrice'
            input_tag = soup.find('input', id='yv-productPrice')

            if input_tag and input_tag.has_attr('value'):
                price = input_tag['value']
                # print(f"Preço encontrado: {price}")
            else:
                # print("Input com id 'yv-productPrice' não encontrado ou sem valor.")
                price = 0
        else:
            print(f"Erro ao acessar a página: {response.status_code}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    lista_precos_cremer.append(price)

df_cremer['preco_cremer'] = lista_precos_cremer
df_cremer = df_cremer[['produto', 'preco_cremer']]
df_cremer['preco_cremer'] = df_cremer['preco_cremer'].replace('Preço não encontrado', 0)
df_cremer['preco_cremer'] = df_cremer['preco_cremer'] .str.replace(',', '.', regex=False)
df_cremer['preco_cremer'] = df_cremer['preco_cremer'] .str.replace('R$', '', regex=False)
df_cremer['preco_cremer'] = pd.to_numeric(df_cremer['preco_cremer'], errors='coerce')

# df.to_csv('teste_webscraping\output_cremer.csv', index=False)


#processar Dental Web

print("Iniciou Dental Web")

# pegar a planilah com os produtos
df_web = pd.read_csv('teste_webscraping\produtos.csv')
df_web = df_web[['produto', 'Dental_Web']]
df_web = df_web.dropna(subset=['Dental_Web'])
df_web['preco_web'] = 0

lista_precos_web = []

for _, produto in df_web.iterrows():
    url = produto['Dental_Web']
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # levanta erro se status != 200

        soup = BeautifulSoup(response.text, 'html.parser')

        # Busca pelo span com id variacaoPreco
        price_span = soup.find('span', id='variacaoPreco')

        if price_span:
            price = price_span.get_text(strip=True)
            # print("💰 Preço encontrado:", price)
        else:
            # print("❌ Nenhum <span> com id 'variacaoPreco' foi encontrado.")
            price = 0

    except requests.RequestException as e:
        print("⚠️ Erro na requisição:", e)
    except Exception as e:
        print("⚠️ Erro inesperado:", e)

    lista_precos_web.append(price)

df_web['preco_web'] = lista_precos_web
df_web = df_web[['produto', 'preco_web']]
df_web['preco_web'] = df_web['preco_web'].replace('Preço não encontrado', 0)
df_web['preco_web'] = df_web['preco_web'] .str.replace(',', '.', regex=False)
df_web['preco_web'] = df_web['preco_web'] .str.replace('R$', '', regex=False)
df_web['preco_web'] = pd.to_numeric(df_web['preco_web'], errors='coerce')

# # df.to_csv('teste_webscraping\output_web.csv', index=False)


# site utilidadesclinicas.com.br

print("Iniciou utilidadesclinicas")

df_util = pd.read_csv('teste_webscraping\produtos.csv')
df_util = df_util[['produto', 'Dental_Util']]
df_util = df_util.dropna(subset=['Dental_Util'])
df_util['preco_util'] = 0

lista_precos_util = []

for _, produto in df_util.iterrows():
    url = produto['Dental_Util']
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Localiza o input com id 'yv-productPrice'
            input_tag = soup.find('input', id='yv-productPrice')

            if input_tag and input_tag.has_attr('value'):
                price = input_tag['value']
                # print(f"Preço encontrado Dental Util: {price}")
            else:
                # print("Input com id 'yv-productPrice' não encontrado ou sem valor.")
                price = 0
        else:
            print(f"Erro ao acessar a página: {response.status_code}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    lista_precos_util.append(price)

df_util['preco_util'] = lista_precos_util

df_util = df_util[['produto', 'preco_util']]
df_util['preco_util'] = df_util['preco_util'].replace('Preço não encontrado', 0)
df_util['preco_util'] = df_util['preco_util'] .str.replace(',', '.', regex=False)
df_util['preco_util'] = df_util['preco_util'] .str.replace('R$', '', regex=False)
df_util['preco_util'] = pd.to_numeric(df_util['preco_util'], errors='coerce')

# site utilidadesclinicas.com.br

print("Iniciou Dental_Cia")


df_cia = pd.read_csv('teste_webscraping\produtos.csv')
df_cia = df_cia[['produto', 'Dental_Cia']]
df_cia = df_cia.dropna(subset=['Dental_Cia'])
df_cia['preco_cia'] = 0

lista_precos_cia = []

for _, produto in df_cia.iterrows():
    url = produto['Dental_Cia']

    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    try:
        # Requisição à página
        response = requests.get(url, headers=headers)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Procura pela tag <strong> com a classe 'skuBestPrice'
            preco_tag = soup.find("strong", class_="skuBestPrice")

            if preco_tag:
                preco = preco_tag.text.strip()
                # print("Preço encontrado:", preco)
            else:
                # print("Preço não encontrado.")
                preco = 0
        else:
            print(f"Erro ao acessar a página: {response.status_code}")

    except Exception as e:
        print("Erro:", e)

    lista_precos_cia.append(preco)

df_cia['preco_cia'] = lista_precos_cia

df_cia = df_cia[['produto', 'preco_cia']]
df_cia['preco_cia'] = df_cia['preco_cia'].replace('Preço não encontrado', 0)
df_cia['preco_cia'] = df_cia['preco_cia'] .str.replace(',', '.', regex=False)
df_cia['preco_cia'] = df_cia['preco_cia'] .str.replace('R$', '', regex=False)
df_cia['preco_cia'] = pd.to_numeric(df_cia['preco_cia'], errors='coerce')


df_final = pd.merge(df_capixaba, df_speed, on='produto', how='outer')
df_final = pd.merge(df_final, df_cremer, on='produto', how='outer')
df_final = pd.merge(df_final, df_web, on='produto', how='outer')
df_final = pd.merge(df_final, df_util, on='produto', how='outer')
df_final = pd.merge(df_final, df_cia, on='produto', how='outer')
df_final = df_final.fillna(0)
df_final['data_busca'] = date.today().strftime("%d/%m/%Y")

df_final.to_csv('teste_webscraping\planilha_final.csv', index=False)

print("Pesquisa concluída")