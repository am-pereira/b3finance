import re
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from flask import Flask, render_template, request

app = Flask(__name__)

# Lista exibida no frontend (código limpo + nome da empresa)
DISPLAY_ITEMS = [
    ('IBOV', 'IBOVESPA'),
    ('PETR4', 'Petrobras'),
    ('VALE3', 'Vale'),
    ('ITUB4', 'Itaú Unibanco'),
    ('BBDC4', 'Bradesco'),
    ('ABEV3', 'Ambev'),
    ('WEGE3', 'WEG'),
    ('RENT3', 'Localiza'),
    ('B3SA3', 'B3'),
    ('SUZB3', 'Suzano'),
    ('RAIL3', 'Rumo'),
    ('GGBR4', 'Gerdau'),
    ('CSNA3', 'CSN'),
    ('KLBN11', 'Klabin'),
    ('LREN3', 'Lojas Renner'),
    ('EMBR3', 'Embraer'),
    ('VIVT3', 'Telefônica Brasil'),
    ('SANB11', 'Santander Brasil'),
    ('BBAS3', 'Banco do Brasil'),
    ('CMIG4', 'Cemig'),
    ('UGPA3', 'Ultrapar'),
    ('CCRO3', 'CCR'),
    ('EQTL3', 'Equatorial'),
    ('ELET3', 'Eletrobras'),
    ('CPFE3', 'CPFL Energia'),
    ('TRPL4', 'Transmissão Paulista'),
    ('TAEE11', 'TAESA'),
    ('EGIE3', 'Engie Brasil'),
    ('NTCO3', 'Natura &Co'),
    ('RADL3', 'Raia Drogasil'),
    ('HAPV3', 'Hapvida'),
    ('MRVE3', 'MRV'),
    ('CYRE3', 'Cyrela'),
    ('BRFS3', 'BRF'),
    ('SMTO3', 'São Martinho'),
    ('VVAR3', 'Via'),
    ('COGN3', 'Cogna'),
    ('AZUL4', 'Azul'),
    ('PCAR3', 'Pão de Açúcar'),
    ('CRFB3', 'Carrefour Brasil'),
    ('LWSA3', 'Locaweb'),
    ('BTOW3', 'B2W'),
    ('JBSS3', 'JBS'),
    ('TOTS3', 'Totvs'),
    ('PRIO3', 'PetroRio'),
    ('CASH3', 'Méliuz'),
    ('BIDI4', 'Banco Inter'),
    ('AURE3', 'Auren'),
    ('SLCE3', 'SLC Agrícola'),
    ('MGLU3', 'Magazine Luiza'),
    ('JHSF3', 'JHSF'),
]


def normalize_display(raw):
    """Remove sufixos/símbolos e retorna o código limpo para exibição no frontend."""
    clean = raw.strip().upper().replace('.SA', '').lstrip('^')
    return 'IBOV' if clean in ('BVSP', 'IBOV', 'IBOVESPA') else clean


def is_brazilian_equity(code):
    """Detecta padrão de ações brasileiras (ex: PETR4, ITUB3, KLBN11)"""
    return bool(re.match(r'^[A-Z]{3,4}[0-9]{1,2}$', code))


def resolve_api_ticker(clean_code, original_raw):
    """Converte o código limpo para o formato exigido pela API yfinance."""
    if clean_code == 'IBOV':
        return '^BVSP'
    if is_brazilian_equity(clean_code):
        return f'{clean_code}.SA'
    # Preserva ^ para índices/cripto se o usuário digitou originalmente
    if original_raw.strip().upper().startswith('^'):
        return f'^{clean_code}'
    return clean_code  # Ativos estrangeiros, ETFs, etc.


def get_candlestick_chart(api_ticker, display_ticker):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)

        df = yf.download(
            api_ticker, start=start_date, end=end_date, progress=False
        )

        if df.empty:
            return None, f'Nenhum dado encontrado para {display_ticker}.'

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red',
                    increasing_fillcolor='rgba(0, 128, 0, 0.3)',
                    decreasing_fillcolor='rgba(255, 0, 0, 0.3)',
                )
            ]
        )

        fig.update_layout(
            title=f'Gráfico Candlestick - {display_ticker}',
            xaxis_title='Data',
            yaxis_title='Preço',
            template='plotly_white',
            height=600,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis_rangeslider_visible=False,
        )

        return fig.to_html(full_html=False, include_plotlyjs='cdn'), None
    except Exception as e:
        return None, f'Erro ao buscar dados: {str(e)}'


@app.route('/', methods=['GET', 'POST'])
def index():
    chart_html = None
    error = None
    display_ticker = 'IBOV'  # O que o usuário vê
    api_ticker = '^BVSP'  # O que o yfinance usa

    if request.method == 'POST':
        raw_input = request.form.get('ticker', '').strip()
        display_ticker = normalize_display(raw_input)
        api_ticker = resolve_api_ticker(display_ticker, raw_input)
    else:
        api_ticker = '^BVSP'

    chart_html, error = get_candlestick_chart(api_ticker, display_ticker)

    return render_template(
        'index.html',
        chart_html=chart_html,
        active_ticker=display_ticker,
        error=error,
        sidebar_items=DISPLAY_ITEMS,
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
