import ccxt
from datetime import datetime

def trend_e_variazione_percentuale(symbol, num_giorni):
    # Crea l'istanza del modulo di scambio CCXT
    exchange = ccxt.binance()  # Puoi scegliere un altro scambio se preferisci

    # Ottieni dati storici della criptovaluta
    ohlcv = exchange.fetch_ohlcv(symbol, '1d')

    # Estrai il prezzo di chiusura per ogni giorno
    prices = [candle[4] for candle in ohlcv]

    # Calcola il trend degli ultimi N giorni
    trend = "guadagno" if prices[-1] > prices[-num_giorni] else "perdita"

    # Calcola la variazione percentuale degli ultimi N giorni
    variazione_percentuale = ((prices[-1] - prices[-num_giorni]) / prices[-num_giorni]) * 100

    return trend, variazione_percentuale


def giorni_passati_da_minimo_locale_con_sconto(symbol, sconto_percentuale=2):
    # Crea l'istanza del modulo di scambio CCXT
    exchange = ccxt.binance()  # Puoi scegliere un altro scambio se preferisci

    # Ottieni dati storici della criptovaluta
    ohlcv = exchange.fetch_ohlcv(symbol, '1d')

    # Estrai il prezzo di chiusura per ogni giorno
    prices = [candle[4] for candle in ohlcv]

    # Calcola il valore attuale della criptovaluta
    valore_attuale = prices[-1]

    # Trova l'indice del minimo locale con uno sconto del 5%
    minimo_locale_index = None
    for i in range(len(prices) - 1, 0, -1):
        if (valore_attuale - prices[i]) / valore_attuale * 100 >= sconto_percentuale:
            minimo_locale_index = i
            break

    if minimo_locale_index is not None:
        # Calcola il numero di giorni passati dal minimo locale con sconto
        giorni_passati = len(prices) - minimo_locale_index - 1
        return giorni_passati
    else:
        return None  # Nessun minimo locale con sconto trovato

def aggiungi_crypto(portfolio, nome_crypto, data_acquisto, importo):
    key = (data_acquisto, nome_crypto)
    portfolio[key] = importo

def get_crypto_percentage_change(symbol, start_date, end_date=None):
    # Crea l'istanza del modulo di scambio CCXT
    exchange = ccxt.binance()  # Puoi scegliere un altro scambio se preferisci

    # Converte la data di inizio in timestamp UNIX
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp()) * 1000

    # Usa la data odierna se end_date non è fornita
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    # Converte la data di fine in timestamp UNIX
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp()) * 1000

    # Ottieni dati storici della criptovaluta
    ohlcv = exchange.fetch_ohlcv(symbol, '1d', start_timestamp, end_timestamp)

    # Estrai il prezzo di apertura e chiusura per ogni giorno
    prices = [candle[4] for candle in ohlcv]

    # Calcola la variazione percentuale tra la data di inizio e quella di fine
    start_price = prices[0]
    end_price = prices[-1]
    percentage_change = ((end_price - start_price) / start_price) * 100

    return percentage_change


crypto_portfolio = {}
# Esempio di utilizzo
aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2022-05-30', 200)
aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2023-01-27', 50)
aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-01-11', 150)
aggiungi_crypto(crypto_portfolio, 'MATIC/USDT', '2024-01-10', 40)
aggiungi_crypto(crypto_portfolio, 'BTTC/USDT', '2023-12-16', 30)

print("Crypto Portfolio:")
for key, value in crypto_portfolio.items():
    data_acquisto, nome_crypto = key
    percentage_change = get_crypto_percentage_change(nome_crypto, data_acquisto)
    print(f"L'acquisto di {value} USD di {nome_crypto} effettuato il {data_acquisto} è variato del: {percentage_change:.2f}%")
    sconto_percentuale = 2
    giorni_passati = giorni_passati_da_minimo_locale_con_sconto(nome_crypto,sconto_percentuale)

    if giorni_passati is not None:
        print(f"il minimo locale per {nome_crypto} è stato {giorni_passati} giorni fa. (scontato del {sconto_percentuale}%).")
    else:
        print(f"Nessun minimo locale con sconto del 5% trovato per {nome_crypto}.")

    num_giorni = 5

    trend, variazione_percentuale = trend_e_variazione_percentuale(nome_crypto, num_giorni)

    print(f"{nome_crypto} è in {trend} da {num_giorni} giorni del {variazione_percentuale:.2f}%.")