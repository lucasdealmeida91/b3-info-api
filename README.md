# B3 Info API

Este projeto fornece uma API para dados da B3 (Bolsa de Valores do Brasil) e uma interface web para visualização dos dados.

## Links

- **API**: [https://b3-info-api.onrender.com/api/b3-data](https://b3-info-api.onrender.com/api/b3-data)
- **Interface Web**: [https://lucasdealmeida91.github.io/b3-info-api/](https://lucasdealmeida91.github.io/b3-info-api/)

## Funcionalidades

- Consulta de dados de ações da B3
- Visualização em tabela interativa
- Ordenação e filtro de dados
- Formatação de valores em formato brasileiro
- Atualização automática dos dados

## Tecnologias Utilizadas

- Backend:
  - Python
  - Flask
  - yfinance
  - investpy
  - pandas
  
- Frontend:
  - HTML5
  - Bootstrap 5
  - DataTables
  - jQuery

## Hospedagem

- Backend: Render.com
- Frontend: GitHub Pages

## Como Usar

1. Acesse a [interface web](https://lucasdealmeida91.github.io/b3-info-api/)
2. Os dados serão carregados automaticamente
3. Use a barra de pesquisa para filtrar dados
4. Clique nas colunas para ordenar
5. Use a paginação para navegar entre os resultados

## API Endpoints

- GET `/api/b3-data`: Retorna dados das ações da B3

## Desenvolvimento Local

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute a API: `python gerador_dados_b3_json_csv.py`
4. Abra o arquivo `index.html` no navegador
