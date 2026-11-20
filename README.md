# FinauxP

O FinauxP é uma aplicação em Python (>=3.14, gerenciada com `uv`) criada para automatizar o controle de finanças pessoais. O usuário faz o download manual de faturas e extratos para uma pasta do Google Drive; a aplicação monitora essa pasta, baixa os arquivos novos e aplica uma transformação padronizada para consolidá-los em uma planilha. Ao final do fluxo, um site de dashboard é gerado para análise dos gastos. O projeto utiliza Google Drive API com OAuth2 (por meio de `google-api-python-client` e `google-auth-oauthlib`), `pandas` para a transformação dos dados e `requests` para as chamadas HTTP. O contexto de criação é eliminar o trabalho manual e repetitivo de baixar arquivos e copiar números para planilhas, tornando o acompanhamento financeiro mais confiável e menos suscetível a erros.

## Estrutura do projeto:


```
├── data/

├── processed/

├── config/

├── processed_raw/

├── raw/

└── src/
```

### Raw
Aonde os dados brutos chegarão e serão padronizados antes de serem tratados.

### processed_raw
Os dados aqui são padronizados em 3 colunas somente

### data
Os dados são organizados em planilhas únicas. A partir daqui, serão criadas novas colunas buscando padrões para insights posteriores

Por enquanto é só.
