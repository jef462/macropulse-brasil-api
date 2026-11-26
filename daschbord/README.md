# 📈 MacroPulse Brasil — Monitoramento de Inflação (IPCA), Selic e Câmbio via API do Banco Central

## 1. Contexto do Problema de Negócio
Decisões de crédito, precificação, estoque e investimentos dependem diretamente do comportamento da taxa básica de juros (**Selic**), da inflação oficial (**IPCA**) e da taxa de câmbio (**Dólar PTAX**). O objetivo deste projeto é construir um pipeline automatizado que consome dados oficiais diretamente da API do **Banco Central do Brasil (SGS)**, estrutura uma base histórica relacional e calcula indicadores macroeconómicos reais (inflação acumulada em 12 meses, médias móveis e juro real *ex-post*).

## 2. Arquitetura de Dados e Técnicas Aplicadas
* **Consumo de API REST & ETL (Python / Requests & Pandas):** Extração automatizada em formato JSON das séries temporais oficiais do BCB (Séries 433, 432 e 3698) desde 2021, padronização de frequência mensal e cálculo composto de inflação acumulada em 12 meses.
* **Análise Temporal em SQL (SQLite):** Armazenamento relacional (`macropulse_brasil.db`) e consultas analíticas avançadas utilizando **Window Functions** temporais (`LAG()` para variação mensal da Selic e `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` para médias móveis trimestrais).
* **Data Visualization (Matplotlib):** Painel executivo com quatro visões integradas de política monetária, juro real, câmbio e deflação/inflação mensal.

## 3. Painel Executivo e Principais Descobertas
![Painel MacroPulse Brasil](daschbord/painel_macropulse_brasil.png)

1. **Juro Real Elevado na Média Histórica:** Ao longo do período analisado, o juro real *ex-post* (Selic descontada a inflação acumulada de 12 meses) apresentou média de **7,05% a.a.**, superando os 10% a.a. em momentos de aperto monetário (2023 e início de 2026).
2. **Ciclo de Política Monetária (2021–2026):** Após o choque inflacionário de 2021–2022 (pico de ~12% em 12 meses) e uma nova pressão cambial no final de 2024 (dólar superando R$ 6,10), a manutenção da Selic em patamar contracionista (15,00% no início de 2026) ancorou o IPCA na faixa de 4,2% a 4,6%, abrindo espaço para cortes graduais até 13,75%.
3. **Episódios de Deflação Pontual:** A série mensal destaca meses específicos de deflação (variação negativa do IPCA, como em 2022 e agosto de 2026 com -0,32%), evidenciando o impacto de choques de oferta e desonerações pontuais.

## 4. Estrutura do Repositório
* `data/`: Base histórica consolidada extraída da API (`indicadores_macro_brasil.csv`).
* `notbook/`: Scripts Python de extração da API (`01_extracao_api_bcb.py`) e geração do painel visual (`02_painel_macro.py`).
* `sql/`: Banco de dados SQLite (`macropulse_brasil.db`) e queries com *Window Functions* (`01_analise_macro.py`).
* `daschbord/`: Painel macroeconómico exportado (`painel_macropulse_brasil.png`).