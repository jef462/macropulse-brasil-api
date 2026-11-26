import sqlite3
import pandas as pd

# 1. Criar base SQLite e carregar dados reais da API
conn = sqlite3.connect('sql/macropulse_brasil.db')
df = pd.read_csv('data/indicadores_macro_brasil.csv')
df.to_sql('serie_macro_bcb', conn, if_exists='replace', index=False)

# 2. Query com Window Functions: Variação Mensal (LAG) e Média Móvel Trimestral
q_series = """
SELECT 
    ano_mes,
    ipca_mensal_pct,
    ROUND(AVG(ipca_mensal_pct) OVER (ORDER BY ano_mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS media_movel_ipca_3m,
    selic_meta_aa,
    ROUND(selic_meta_aa - LAG(selic_meta_aa) OVER (ORDER BY ano_mes), 2) AS variacao_selic_pp,
    dolar_medio_brl,
    ipca_acum_12m_pct,
    juro_real_pct
FROM serie_macro_bcb
WHERE ano_mes >= '2025-11'
ORDER BY ano_mes;
"""
print("--- EVOLUÇÃO MACRO RECENTE (WINDOW FUNCTIONS: LAG & MÉDIA MÓVEL) ---")
print(pd.read_sql_query(q_series, conn).to_string(index=False))

# 3. Resumo Anual (2021 a 2026)
q_anual = """
SELECT 
    SUBSTR(ano_mes, 1, 4) AS ano,
    COUNT(*) AS meses_registrados,
    ROUND(AVG(selic_meta_aa), 2) AS selic_media_aa,
    ROUND(AVG(dolar_medio_brl), 2) AS dolar_medio_brl,
    ROUND(AVG(juro_real_pct), 2) AS juro_real_medio_pct,
    MAX(ipca_acum_12m_pct) AS pico_inflacao_12m
FROM serie_macro_bcb
GROUP BY SUBSTR(ano_mes, 1, 4)
ORDER BY ano;
"""
print("\n--- RESUMO ANUAL CONSOLIDADO (2021 - 2026) ---")
print(pd.read_sql_query(q_anual, conn).to_string(index=False))

conn.close()