import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

ARQUIVO_CSV = '/content/produtos.csv'

def obter_html(url, headers=None):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def extrair_preco_via_span(soup, span_id='variacaoPreco'):
    if not soup:
        return 0
    span = soup.find('span', id=span_id)
    return span.get_text(strip=True) if span else 0

def extrair_preco_via_input(soup, input_id='yv-productPrice'):
    if not soup:
        return 0
    input_tag = soup.find('input', id=input_id)
    return input_tag['value'] if input_tag and input_tag.has_attr('value') else 0

def extrair_preco_via_strong(soup, class_name='skuBestPrice'):
    if not soup:
        return 0
    tag = soup.find('strong', class_=class_name)
    return tag.text.strip() if tag else 0

def processar_loja(nome_loja, coluna_url, func_extracao, headers=None):
    print(f"Iniciou {nome_loja}")
    df = pd.read_csv(ARQUIVO_CSV)
    df = df[['produto', coluna_url]].dropna()
    precos = []

    for _, linha in df.iterrows():
        url = linha[coluna_url]
        soup = obter_html(url, headers=headers)
        preco = func_extracao(soup)
        precos.append(preco)

    nome_col_preco = f'preco_{nome_loja.lower()}'
    df[nome_col_preco] = precos
    df = df[['produto', nome_col_preco]]
    df[nome_col_preco] = (
        df[nome_col_preco]
        .astype(str)
        .str.replace(',', '.', regex=False)
        .str.replace('R$', '', regex=False)
    )
    df[nome_col_preco] = pd.to_numeric(df[nome_col_preco], errors='coerce').fillna(0)
    return df

# Configurações específicas
headers_padrao = {"User-Agent": "Mozilla/5.0"}

# Processar todas as lojas
df_capixaba = processar_loja('capixaba', 'Dental_Capixaba', extrair_preco_via_span)
df_speed = processar_loja('speed', 'Dental_Speed', extrair_preco_via_input)
df_cremer = processar_loja('cremer', 'Dental_Cremer', extrair_preco_via_input)
df_web = processar_loja('web', 'Dental_Web', extrair_preco_via_span)
df_util = processar_loja('util', 'Dental_Util', extrair_preco_via_input)
df_cia = processar_loja('cia', 'Dental_Cia', extrair_preco_via_strong, headers=headers_padrao)

# Combinar todos os dataframes
dfs = [df_capixaba, df_speed, df_cremer, df_web, df_util, df_cia]
df_final = dfs[0]
for df in dfs[1:]:
    df_final = pd.merge(df_final, df, on='produto', how='outer')

df_final = df_final.fillna(0)
df_final['data_busca'] = date.today().strftime("%d/%m/%Y")

# Ordena por ordem alfabética da coluna 'produto'
df_final = df_final.sort_values(by='produto')

df_final.to_csv('planilha_final.csv', index=False)
print("✅ Pesquisa concluída")
