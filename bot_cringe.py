import ccxt
import time
from datetime import datetime

import matplotlib.pyplot as plt
from datetime import datetime

def plot_prices(price_file, last_trade_date):
    # Inizializza le liste per i dati
    dates = []
    btc_changes = []
    eth_changes = []

    # Leggi i dati dal file
    with open(price_file, 'r') as file:
        for line in file:
            data = line.strip().split(', ')
            date = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')

            # Salta i dati precedenti all'ultimo trade
            if date < last_trade_date:
                continue

            btc_price = float(data[1].split(': ')[1])
            eth_price = float(data[2].split(': ')[1])

            dates.append(date)
            btc_changes.append(btc_price)
            eth_changes.append(eth_price)

    # Calcola le variazioni percentuali
    btc_percent_changes = [(btc_changes[i] - btc_changes[i-1]) / btc_changes[i-1] * 100 for i in range(1, len(btc_changes))]
    eth_percent_changes = [(eth_changes[i] - eth_changes[i-1]) / eth_changes[i-1] * 100 for i in range(1, len(eth_changes))]

    # Plot dei dati
    plt.figure(figsize=(10, 6))
    plt.plot(dates[1:], btc_percent_changes, label='BTC/USDT', color='blue')
    plt.plot(dates[1:], eth_percent_changes, label='ETH/USDT', color='red')

    # Aggiungi titolo e legenda
    plt.title('Variazioni percentuali ogni 4 ore')
    plt.xlabel('Data')
    plt.ylabel('Variazione percentuale')
    plt.legend()

    # Salva il grafico come immagine
    plt.savefig('price_changes_plot.png')

# Funzione per ottenere il cambio percentuale tra due valori
def percent_change(old_value, new_value):
    return ((new_value - old_value) / old_value) * 100

# Funzione per effettuare lo scambio tra le criptovalute
def exchange_crypto(balance, crypto1, crypto2, amount):
    # Calcolo della quantità da scambiare (metà del bilancio in dollari)
    amount_to_exchange = balance / 2

    # Calcolo della quantità di crypto2 ottenuta in cambio
    amount_obtained = amount_to_exchange * (1 / amount)

    # Aggiornamento dei bilanci delle criptovalute
    balance -= amount_to_exchange
    return amount_to_exchange, amount_obtained

# Inizializzazione delle criptovalute e del bilancio iniziale in dollari
crypto1 = 'BTC/USDT'
crypto2 = 'ETH/USDT'
initial_balance = 1000  # Iniziamo con $1000

# Nome del file in cui salvare i prezzi delle criptovalute
price_file = 'prices.txt'

# Inizializzazione dei prezzi precedenti
last_prices = {crypto1: None, crypto2: None}

# Inizializzazione dello stato degli avvisi
alert_sent = {crypto1: False, crypto2: False}


last_trade_crypto = None
last_trade_amount = initial_balance / 2
last_trade_date = None

while True:
    try:
        # Inizializzazione dell'exchange
        exchange = ccxt.binance()

        # Ottenere i dati di mercato per le due criptovalute
        ticker1 = exchange.fetch_ticker(crypto1)
        ticker2 = exchange.fetch_ticker(crypto2)

        # Ottenere i prezzi attuali delle criptovalute
        price1 = ticker1['last']
        price2 = ticker2['last']

        # Data e ora attuali
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Calcolo delle variazioni percentuali rispetto all'ultimo prezzo acquistato
        percent_change1 = percent_change(last_prices[crypto1], price1) if last_prices[crypto1] is not None else 0
        percent_change2 = percent_change(last_prices[crypto2], price2) if last_prices[crypto2] is not None else 0

        # Stampa delle variazioni percentuali
        print(f'{crypto1}: {percent_change1:.2f}%')
        print(f'{crypto2}: {percent_change2:.2f}%')

        # Salva i prezzi delle criptovalute su file insieme alla data e ora attuali
        with open(price_file, 'a') as file:
            file.write(f'{current_time}, {crypto1}: {price1}, {crypto2}: {price2}\n')

        # Verifica delle condizioni di trading
        if percent_change1 < -5 and not alert_sent[crypto1]:
            print(f'{crypto1} è in calo di più del 5% ({percent_change1:.2f}%), momento di acquistare {crypto2}!')
            alert_sent[crypto1] = True
            # Aggiungi qui la logica per effettuare lo swap
            if last_trade_crypto == crypto1:
                # Esegui uno swap
                print(f'Eseguo uno swap da {crypto1} a {crypto2}')
                # Calcola il nuovo saldo dopo lo swap
                new_balance = last_trade_amount * price2
                # Aggiorna le variabili dell'ultimo acquisto
                last_trade_crypto = crypto2
                last_trade_amount = new_balance / 2
                last_trade_date = current_time
            # ...
        elif percent_change2 > 5 and not alert_sent[crypto2]:
            print(f'{crypto2} è in crescita di più del 5% ({percent_change2:.2f}%), momento di comprare {crypto1}!')
            alert_sent[crypto2] = True
            # Aggiungi qui la logica per effettuare lo swap
            if last_trade_crypto == crypto2:
                # Esegui uno swap
                print(f'Eseguo uno swap da {crypto2} a {crypto1}')
                # Calcola il nuovo saldo dopo lo swap
                new_balance = last_trade_amount * price1
                # Aggiorna le variabili dell'ultimo acquisto
                last_trade_crypto = crypto1
                last_trade_amount = new_balance / 2
                last_trade_date = current_time
            # ...
        elif percent_change1 >= 0 and percent_change2 <= 0:
            print(f'{crypto1} è in crescita e {crypto2} è in calo!')
            # Resetta lo stato degli avvisi
            alert_sent[crypto1] = False
            alert_sent[crypto2] = False
            # Aggiungi qui la logica per decidere se replicare lo swap o attendere
            # ...
        # ...

    except Exception as e:
        print(f'An error occurred: {e}')
        # Attendi 1 minuto prima di riprovare dopo un errore
        time.sleep(60)