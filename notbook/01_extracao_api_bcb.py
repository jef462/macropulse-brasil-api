import requests
import pandas as pd

def buscar_serie_bcb(codigo_serie, nome_coluna, data_inicio='01/01/2021'):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={data_inicio}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resposta = requests.get(url, headers=headers, timeout=15)
    resposta.raise_for_status()
    
    df = pd.DataFrame(resposta.json())
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df[nome_coluna] = pd.to_numeric(df['valor'])
    return df[['data', nome_coluna]]

print("Conectando à API oficial do Banco Central do Brasil...")

# 1. Extrair séries reais (2021 a 2026)
df_ipca = buscar_serie_bcb(433, 'ipca_mensal_pct')
df_selic = buscar_serie_bcb(432, 'selic_meta_aa')
df_dolar = buscar_serie_bcb(3698, 'dolar_medio_brl')

# 2. Padronizar frequência mensal (Ano-Mês) para cruzar as 3 bases
for df_temp in [df_ipca, df_selic, df_dolar]:
    df_temp['ano_mes'] = df_temp['data'].dt.to_period('M').astype(str)

# Agrupar Selic e Dólar pela média/último valor do mês
selic_mensal = df_selic.groupby('ano_mes')['selic_meta_aa'].last().reset_index()
dolar_mensal = df_dolar.groupby('ano_mes')['dolar_medio_brl'].mean().round(2).reset_index()
ipca_mensal = df_ipca[['ano_mes', 'ipca_mensal_pct']]

# 3. Unificar em uma base analítica consolidada (Merge)
df_macro = ipca_mensal.merge(selic_mensal, on='ano_mes', how='inner')
df_macro = df_macro.merge(dolar_mensal, on='ano_mes', how='inner')

# 4. Calcular IPCA Acumulado em 12 meses (Juros Compostos) e Juro Real Ex-Post aproximado
df_macro['fator_ipca'] = 1 + (df_macro['ipca_mensal_pct'] / 100.0)
df_macro['ipca_acum_12m_pct'] = (
    df_macro['fator_ipca'].rolling(window=12).apply(lambda x: x.prod(), raw=True) - 1
) * 100
df_macro['ipca_acum_12m_pct'] = df_macro['ipca_acum_12m_pct'].round(2)

# Juro Real = ((1 + Selic) / (1 + IPCA 12m)) - 1
df_macro['juro_real_pct'] = (
    (((1 + df_macro['selic_meta_aa']/100) / (1 + df_macro['ipca_acum_12m_pct']/100)) - 1) * 100
).round(2)

df_macro = df_macro.drop(columns=['fator_ipca'])
df_macro.to_csv('data/indicadores_macro_brasil.csv', index=False)

print(f"\nExtração concluída com sucesso! {len(df_macro)} meses consolidados (2021-2026).")
print(df_macro.tail(10).to_string(index=False))
