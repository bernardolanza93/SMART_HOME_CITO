import sys

import ccxt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
def plot_andamento_cripto(crypto_name, crypto_portfolio):
    # Dividi la stringa del nome della criptovaluta per ottenere i simboli separati
    base_symbol, quote_symbol = crypto_name.split('/')

    # Verifica se ci sono acquisti per la criptovaluta specificata
    acquisti_cripto = [(data, importo) for (data, cripto), importo in crypto_portfolio.items() if cripto == crypto_name]
    if not acquisti_cripto:
        print("Nessun acquisto trovato per la criptovaluta specificata.")
        return

    # Trova la data del primo acquisto
    prima_data_acquisto = min([datetime.strptime(data, '%Y-%m-%d') for (data, _) in acquisti_cripto])

    # Crea l'istanza del modulo di scambio CCXT
    exchange = ccxt.binance()  # Puoi scegliere un altro scambio se preferisci

    # Ottieni dati storici della criptovaluta fino alla data odierna
    dati_storici = exchange.fetch_ohlcv(f"{base_symbol}/{quote_symbol}", '1d', int(prima_data_acquisto.timestamp() * 1000))

    # Estrai le date e i prezzi di chiusura
    date = [datetime.utcfromtimestamp(candle[0] / 1000) for candle in dati_storici]
    prices = [candle[4] for candle in dati_storici]

    # Crea il grafico
    plt.plot(date, prices, label=crypto_name)

    # Segna gli acquisti successivi con dei pallini rossi sul grafico
    for data_acquisto, importo in acquisti_cripto:
        if datetime.strptime(data_acquisto, '%Y-%m-%d') >= prima_data_acquisto:
            plt.scatter(datetime.strptime(data_acquisto, '%Y-%m-%d'), prices[(datetime.strptime(data_acquisto, '%Y-%m-%d') - prima_data_acquisto).days], color='red')
            plt.text(datetime.strptime(data_acquisto, '%Y-%m-%d'), prices[(datetime.strptime(data_acquisto, '%Y-%m-%d') - prima_data_acquisto).days], f"${importo}", verticalalignment='bottom')

    # Imposta i limiti del grafico per iniziare dalla data del primo acquisto
    plt.xlim(prima_data_acquisto, datetime.now())

    # Aggiunta di etichette e titoli al grafico
    plt.xlabel('Data')
    plt.ylabel('Prezzo di Chiusura (USD)')
    plt.title(f'Andamento di {crypto_name} dal {prima_data_acquisto.strftime("%Y-%m-%d")} a oggi')
    plt.xticks(rotation=45)
    plt.legend()

    # Mostra il grafico
    plt.show()


def grafico_andamento_e_acquisto(symbol, periodo_passato, data_acquisto):
    # Crea l'istanza del modulo di scambio CCXT
    exchange = ccxt.binance()  # Puoi scegliere un altro scambio se preferisci

    # Calcola la data di inizio del periodo specificato nel passato
    data_inizio = datetime.now() - timedelta(days=periodo_passato)

    # Ottieni dati storici della criptovaluta
    ohlcv = exchange.fetch_ohlcv(symbol, '1d', int(data_inizio.timestamp()) * 1000)

    # Estrai le date e i prezzi di chiusura
    date = [datetime.utcfromtimestamp(candle[0] / 1000).strftime('%Y-%m-%d') for candle in ohlcv]
    prices = [candle[4] for candle in ohlcv]

    # Trova l'indice corrispondente al giorno di acquisto
    try:
        indice_acquisto = date.index(data_acquisto)
    except ValueError:
        raise ValueError(f"La data di acquisto ({data_acquisto}) non è presente nei dati storici.")

    # Calcola la variazione percentuale rispetto ad oggi
    variazione_percentuale = ((prices[-1] - prices[indice_acquisto]) / prices[indice_acquisto]) * 100

    # Creazione del grafico
    plt.plot(date, prices, label=f"{symbol} - Variazione: {variazione_percentuale:.2f}%")

    # Segnalino per il giorno di acquisto
    plt.scatter(date[indice_acquisto], prices[indice_acquisto], color='red', label='Acquisto')

    # Aggiunta di etichette e titoli al grafico
    plt.xlabel('Data')
    plt.ylabel('Prezzo di Chiusura (USD)')
    plt.title(f'Andamento di {symbol} dal {data_inizio.strftime("%Y-%m-%d")} a oggi')
    plt.xticks(rotation=45)
    plt.legend()

    # Mostra il grafico
    plt.show()
def trend_e_variazione_percentuale(symbol, num_giorni):
    # Crea l'istanza del modulo di scambio CCXT
    exchange = ccxt.binance()  # Puoi scegliere un altro scambio se preferisci

    # Ottieni dati storici della criptovaluta
    ohlcv = exchange.fetch_ohlcv(symbol, '1d')

    # Estrai il prezzo di chiusura per ogni giorno
    prices = [candle[4] for candle in ohlcv]

    # Calcola il trend degli ultimi N giorni
    trend = "++" if prices[-1] > prices[-num_giorni] else "--"

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

def reso_totale_per_criptovaluta(crypto_portfolio, symbol, esprimi_percentuale=True):
    total_invested = 0
    total_returns = 0

    string_acquisti = []

    #print(f"Dettagli degli acquisti per {symbol}:")
    for data_acquisto, nome_crypto in crypto_portfolio.keys():
        if nome_crypto == symbol:
            importo = crypto_portfolio[(data_acquisto, nome_crypto)]
            total_invested += importo

            rendimento = get_crypto_percentage_change(nome_crypto, data_acquisto)
            reso_acquisto = importo * rendimento / 100
            total_returns += reso_acquisto
            string_acquisti.append(f" {symbol} ASSET: {importo} USD del {data_acquisto}, RENDIMENTO: {rendimento:.2f}%")

            ##print(f" {symbol} ASSET: {importo} USD del {data_acquisto}, RENDIMENTO: {rendimento:.2f}%")

    if esprimi_percentuale:
        reso_totale_percentuale = (total_returns / total_invested) * 100
        string_acquisti.append(f"RENDIMENTO TOTALE {symbol}: {reso_totale_percentuale:.2f}% ({total_returns:.2f}USD). Deposito: {total_invested} USD")
        ##print(f"RENDIMENTO TOTALE {symbol}: {reso_totale_percentuale:.2f}% ({total_returns:.2f}USD). Deposito: {total_invested} USD")
        return reso_totale_percentuale ,string_acquisti
    else:
        string_acquisti.append(f"Reso totale per {symbol}: {total_returns:.2f} USD su un investimento totale di {total_invested} USD")
        ##print(f"Reso totale per {symbol}: {total_returns:.2f} USD su un investimento totale di {total_invested} USD")
        return total_returns, string_acquisti

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

def crypto_request():

    crypto_portfolio = {}
    # Esempio di utilizzo
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2022-05-30', 200)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2023-01-27', 50)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-01-11', 150)
    aggiungi_crypto(crypto_portfolio, 'MATIC/USDT', '2024-01-10', 40)
    aggiungi_crypto(crypto_portfolio, 'BTTC/USDT', '2023-12-16', 30)
    aggiungi_crypto(crypto_portfolio, 'FLUX/USDT', '2024-01-10', 22)
    aggiungi_crypto(crypto_portfolio, 'AR/USDT', '2023-12-20', 25)
    aggiungi_crypto(crypto_portfolio, 'PYR/USDT', '2023-12-20', 20)

    crypto_set = set()
    sconto_percentuale = 2
    string = []
    string.append("START: Criptovalute nel portafoglio:")
    ##print("Criptovalute nel portafoglio:")
    for data_acquisto, nome_crypto in crypto_portfolio.keys():
        if nome_crypto not in crypto_set:
            print("1 ",nome_crypto)
            giorni_passati = giorni_passati_da_minimo_locale_con_sconto(nome_crypto, sconto_percentuale)
            if giorni_passati is not None:
                string.append(f"MINIMO LOCALE {nome_crypto}:  {giorni_passati} giorni fa.")
                ##print(f"MINIMO LOCALE {nome_crypto}:  {giorni_passati} giorni fa.")
            else:
                ##print(f"Nessun minimo locale con sconto del 5% trovato per {nome_crypto}.")
                string.appedd(f"Nessun minimo locale con sconto del 5% trovato per {nome_crypto}.")

            num_giorni = 5

            trend, variazione_percentuale = trend_e_variazione_percentuale(nome_crypto, num_giorni)

            ##print(f"{num_giorni} giorni: {nome_crypto} in {trend} del {variazione_percentuale:.2f}%.")
            string.append(f"{num_giorni} giorni: {nome_crypto} {trend} {variazione_percentuale:.2f}%.")
            num_giorni = 2

            trend, variazione_percentuale = trend_e_variazione_percentuale(nome_crypto, num_giorni)

            ##print(f"{num_giorni} giorni: {nome_crypto} in {trend} del {variazione_percentuale:.2f}%.")
            string.append(f"{num_giorni} giorni: {nome_crypto} in {trend} del {variazione_percentuale:.2f}%.")
            crypto_set.add(nome_crypto)

            a, string_acquisti = reso_totale_per_criptovaluta(crypto_portfolio,nome_crypto)
            string.append(string_acquisti)

    return string











