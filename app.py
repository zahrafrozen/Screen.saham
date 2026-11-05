import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import yfinance as yf

# Wajib: Inisialisasi 'app' di level utama agar terbaca oleh Vercel
app = Flask(__name__, static_folder='.')
CORS(app)

STOCKS_MAP = [
    {"ticker": "ASII", "yf": "ASII.JK", "name": "Astra International Tbk", "market": "BEI", "sector": "Otomotif"},
    {"ticker": "BBRI", "yf": "BBRI.JK", "name": "Bank Rakyat Indonesia Tbk", "market": "BEI", "sector": "Perbankan"},
    {"ticker": "BMRI", "yf": "BMRI.JK", "name": "Bank Mandiri Tbk", "market": "BEI", "sector": "Perbankan"},
    {"ticker": "TLKM", "yf": "TLKM.JK", "name": "Telkom Indonesia Tbk", "market": "BEI", "sector": "Teknologi"},
    {"ticker": "BSSR", "yf": "BSSR.JK", "name": "Baramulti Suksessarana Tbk", "market": "BEI", "sector": "Energi"},
    {"ticker": "SMSM", "yf": "SMSM.JK", "name": "Selamat Sempurna Tbk", "market": "BEI", "sector": "Otomotif"},
    {"ticker": "ICBP", "yf": "ICBP.JK", "name": "Indofood CBP Sukses Makmur", "market": "BEI", "sector": "Konsumsi"},
    {"ticker": "UNVR", "yf": "UNVR.JK", "name": "Unilever Indonesia Tbk", "market": "BEI", "sector": "Konsumsi"},
    {"ticker": "AAPL", "yf": "AAPL", "name": "Apple Inc.", "market": "US", "sector": "Teknologi"},
    {"ticker": "NVDA", "yf": "NVDA", "name": "NVIDIA Corporation", "market": "US", "sector": "Teknologi"},
    {"ticker": "MSFT", "yf": "MSFT", "name": "Microsoft Corp", "market": "US", "sector": "Teknologi"},
    {"ticker": "KO",   "yf": "KO",   "name": "The Coca-Cola Company", "market": "US", "sector": "Konsumsi"},
    {"ticker": "JNJ",  "yf": "JNJ",  "name": "Johnson & Johnson", "market": "US", "sector": "Kesehatan"}
]

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    results = []
    for item in STOCKS_MAP:
        try:
            stock = yf.Ticker(item["yf"])
            fast = stock.fast_info
            info = stock.info

            price = fast.last_price or info.get("currentPrice") or info.get("previousClose", 0)
            per = info.get("trailingPE") or info.get("forwardPE") or 0.0
            pbv = info.get("priceToBook") or 0.0
            roe = (info.get("returnOnEquity") or 0.0) * 100
            div_yield = (info.get("dividendYield") or 0.0) * 100
            der = (info.get("debtToEquity") or 0.0) / 100

            results.append({
                "ticker": item["ticker"],
                "name": item["name"],
                "market": item["market"],
                "sector": item["sector"],
                "price": round(price, 2),
                "per": round(per, 2),
                "pbv": round(pbv, 2),
                "roe": round(roe, 2),
                "divYield": round(div_yield, 2),
                "der": round(der, 2)
            })
        except Exception as e:
            print(f"Error: {e}")

    return jsonify(results)

# PENTING: Untuk Vercel Serverless, app diekspor sebagai handler
app_handler = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

