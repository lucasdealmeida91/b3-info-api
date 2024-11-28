import yfinance as yf
import pandas as pd
import datetime
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import investpy as inv

app = Flask(__name__)
CORS(app)

# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def get_b3_data():
    # Definição da data de referência
    hoje = datetime.datetime.today()
    data_referencia = hoje.strftime('%Y-%m-%d')
    data_referencia_start = hoje.strftime('%Y-%m-%d')
    data_referencia_end = (hoje + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    try:
        br = inv.stocks.get_stocks(country='brazil')
    except Exception as e:
        print(f"Erro ao obter dados das ações brasileiras: {e}")
        br = pd.DataFrame()  # Garantir que br seja inicializado mesmo em caso de erro

    dados_por_empresa = []
    
    if not br.empty:
        # Criar lista de ações com símbolos válidos (<= 5 caracteres)
        carteira = [f"{a}.SA" for a in br['symbol'] if len(a) <= 5]

        # Selecionar todos os ativos para consulta
        carteira_pequena = carteira[:100]
        
        for ticker in carteira_pequena:
            try:
                dados = yf.download(ticker, start=data_referencia_start, end=data_referencia_end)
                if not dados.empty:
                    print(dados, f'aqui estão os dados de {ticker}')

                    # Resolver problema de MultiIndex nas colunas
                    if isinstance(dados.columns, pd.MultiIndex):
                        # Achatar o MultiIndex concatenando os níveis
                        dados.columns = [' '.join(col).strip() for col in dados.columns]

                    # Adicionar os dados ao JSON, um objeto por empresa
                    for date, row in dados.iterrows():
                        objeto = {
                            "Ticker": ticker,  # Adiciona o ticker correspondente
                            "Date": date.strftime("%Y-%m-%d"),
                            "Close": row.get(f"Close {ticker}", None),
                            "High": row.get(f"High {ticker}", None),
                            "Low": row.get(f"Low {ticker}", None),
                            "Open": row.get(f"Open {ticker}", None),
                            "Volume": row.get(f"Volume {ticker}", None),
                        }
                        # Adicionar 'Adj Close' apenas se existir
                        if f"Adj Close {ticker}" in row:
                            objeto["Adj Close"] = row.get(f"Adj Close {ticker}", None)

                        dados_por_empresa.append(objeto)
                else:
                    print(f"Nenhum dado encontrado para {ticker}.")
            except Exception as e:
                print(f"Erro ao coletar dados para {ticker}: {e}")
        
        print(f"\nTotal de registros processados: {len(dados_por_empresa)}")
    
    return dados_por_empresa

@app.route('/', methods=['GET'])
def index():
    return send_file('index.html')

@app.route('/api/b3-data', methods=['GET'])
@limiter.limit("10 per minute")
def get_b3_data_endpoint():
    dados = get_b3_data()
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
