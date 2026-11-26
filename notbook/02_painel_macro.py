import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('sql/macropulse_brasil.db')
df = pd.read_sql_query("SELECT * FROM serie_macro_bcb WHERE ipca_acum_12m_pct IS NOT NULL ORDER BY ano_mes", conn)

plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('MacroPulse Brasil (2022–2026) — Inflação, Política Monetária (Selic) e Câmbio (API BCB)', fontsize=15, fontweight='bold', y=0.98)

# Ajustar rótulos do eixo X para não sobrepor
ticks = range(0, len(df), 6)
labels = [df['ano_mes'].iloc[i] for i in ticks]

# --- GRÁFICO 1: Selic Meta vs IPCA Acumulado 12m ---
axes[0, 0].plot(df['ano_mes'], df['selic_meta_aa'], label='Selic Meta (% a.a.)', color='#2980b9', linewidth=2.5)
axes[0, 0].plot(df['ano_mes'], df['ipca_acum_12m_pct'], label='IPCA Acumulado 12m (%)', color='#c0392b', linewidth=2.5)
axes[0, 0].set_title('1. Política Monetária: Taxa Selic vs. Inflação (IPCA 12m)', fontweight='bold')
axes[0, 0].set_ylabel('Taxa (% a.a.)')
axes[0, 0].legend(loc='upper right')
axes[0, 0].set_xticks(ticks)
axes[0, 0].set_xticklabels(labels, rotation=30)

# --- GRÁFICO 2: Juro Real Ex-Post (%) ---
cores_juro = ['#27ae60' if x >= 6 else '#f39c12' for x in df['juro_real_pct']]
axes[0, 1].bar(df['ano_mes'], df['juro_real_pct'], color=cores_juro)
axes[0, 1].axhline(df['juro_real_pct'].mean(), color='#2c3e50', linestyle='--', linewidth=1.5, label=f"Média: {df['juro_real_pct'].mean():.2f}%")
axes[0, 1].set_title('2. Juro Real Ex-Post (Selic descontada a Inflação)', fontweight='bold')
axes[0, 1].set_ylabel('Juro Real (% a.a.)')
axes[0, 1].legend()
axes[0, 1].set_xticks(ticks)
axes[0, 1].set_xticklabels(labels, rotation=30)

# --- GRÁFICO 3: Evolução do Dólar Médio (R$) ---
axes[1, 0].plot(df['ano_mes'], df['dolar_medio_brl'], color='#16a085', linewidth=2.5)
axes[1, 0].fill_between(df['ano_mes'], df['dolar_medio_brl'], df['dolar_medio_brl'].min()*0.95, color='#16a085', alpha=0.15)
axes[1, 0].set_title('3. Câmbio: Evolução do Dólar Comercial Médio (R$)', fontweight='bold')
axes[1, 0].set_ylabel('Cotação (R$)')
axes[1, 0].set_xticks(ticks)
axes[1, 0].set_xticklabels(labels, rotation=30)

# --- GRÁFICO 4: IPCA Mensal (%) ---
cores_ipca = ['#e74c3c' if x > 0.5 else '#3498db' if x >= 0 else '#2ecc71' for x in df['ipca_mensal_pct']]
axes[1, 1].bar(df['ano_mes'], df['ipca_mensal_pct'], color=cores_ipca)
axes[1, 1].axhline(0, color='black', linewidth=0.8)
axes[1, 1].set_title('4. Variação Mensal do IPCA (%) — Destaque para Deflação (<0%)', fontweight='bold')
axes[1, 1].set_ylabel('IPCA Mensal (%)')
axes[1, 1].set_xticks(ticks)
axes[1, 1].set_xticklabels(labels, rotation=30)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('daschbord/painel_macropulse_brasil.png', dpi=300)
print("Painel macroeconómico guardado com sucesso em 'daschbord/painel_macropulse_brasil.png'!")
conn.close()