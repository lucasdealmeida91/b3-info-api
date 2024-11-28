import yfinance as yf
import pandas as pd
import json
from datetime import date, timedelta
import investpy as inv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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
    data_referencia = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    data_referencia_start = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    data_referencia_end = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    dados_por_empresa = []

    try:
        br = inv.stocks.get_stocks(country='brazil')
        
        if not br.empty:
            # Criar lista de ações com símbolos válidos (<= 5 caracteres)
            carteira = [f"{a}.SA" for a in br['symbol'] if len(a) <= 5]
            carteira_pequena = carteira[:10]

            # Coletar dados das ações usando yfinance
            for ticker in carteira_pequena:
                try:
                    dados = yf.download(ticker, start=data_referencia_start, end=data_referencia_end)
                    if not dados.empty:
                        # Resolver problema de MultiIndex nas colunas
                        if isinstance(dados.columns, pd.MultiIndex):
                            dados.columns = [' '.join(col).strip() for col in dados.columns]

                        for date_idx, row in dados.iterrows():
                            objeto = {
                                "Ticker": ticker,
                                "Date": date_idx.strftime("%Y-%m-%d"),
                                "Close": row.get(f"Close {ticker}", None),
                                "High": row.get(f"High {ticker}", None),
                                "Low": row.get(f"Low {ticker}", None),
                                "Open": row.get(f"Open {ticker}", None),
                                "Volume": row.get(f"Volume {ticker}", None),
                            }
                            if f"Adj Close {ticker}" in row:
                                objeto["Adj Close"] = row.get(f"Adj Close {ticker}", None)

                            dados_por_empresa.append(objeto)
                except Exception as e:
                    print(f"Erro ao coletar dados para {ticker}: {e}")
    
    except Exception as e:
        print(f"Erro ao obter dados das ações brasileiras: {e}")
    
    return dados_por_empresa

@app.route('/api/b3-data', methods=['GET'])
@limiter.limit("10 per minute")
def get_b3_data_endpoint():
    dados = get_b3_data()
    return jsonify(dados)

if __name__ == '__main__':
    # Development server
    app.run(debug=True, port=8080, host='0.0.0.0')
else:
    # Production server (e.g., PythonAnywhere)
    # Configure logging
    import logging
    logging.basicConfig(level=logging.INFO)
    # The production server will handle the app object directly
