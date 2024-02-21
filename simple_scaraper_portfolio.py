import sys

import ccxt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import json
import os
import re
from CONSTANT import *
import subprocess


def get_last_git_pull():
    try:
        # Execute git log command to get the last pull
        result = subprocess.run(['git', 'log', '--grep=Merge pull request'], capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            # Split the output by newline character to get individual commits
            commits = result.stdout.split('\n')

            # Check if any pull request merges are found
            if len(commits) > 0:
                last_pull = commits[0]
                return last_pull
            else:
                return "No pull requests found"
        else:
            return "Git command failed"
    except Exception as e:
        return f"Error: {str(e)}"
def delete_file(file_path):
    """
    Cancella il file specificato dal percorso.

    Args:
        file_path (str): Percorso del file da cancellare.

    Returns:
        bool: True se il file è stato cancellato con successo, False altrimenti.
    """
    try:
        os.remove(file_path)
        print(f"Il file '{file_path}' è stato cancellato con successo.")
        return True
    except FileNotFoundError:
        print(f"Il file '{file_path}' non è stato trovato.")
        return False
    except Exception as e:
        print(f"Si è verificato un errore durante la cancellazione del file '{file_path}': {e}")
        return False





def reso_totale_per_portafoglio(crypto_portfolio):
    total_invested = 0
    total_returns = 0

    string_acquisti = []

    # Ciclo attraverso tutte le coppie chiave-valore nel dizionario
    for (data_acquisto, nome_crypto), importo in crypto_portfolio.items():
        # Calcolo del rendimento parziale per ogni criptovaluta nel portafoglio
        rendimento = get_crypto_percentage_change(nome_crypto, data_acquisto)
        reso_acquisto = importo * rendimento / 100

        # Aggiornamento del totale investito e del rendimento totale
        total_invested += importo
        total_returns += reso_acquisto

        # Costruzione della stringa relativa agli acquisti per ogni criptovaluta
        #string_acquisti.append(f"{nome_crypto}: {importo} USD, Rendimento: {rendimento:.2f}%")

    # Calcolo del rendimento totale percentuale
    reso_totale_percentuale = (total_returns / total_invested) * 100

    # Aggiunta delle informazioni sul rendimento totale alla stringa degli acquisti
    string_acquisti.append(f"PORTAFOGLIO: {reso_totale_percentuale:.2f}%, {total_returns:.2f}/{total_invested:.2f} USD")

    # Ritorno del rendimento totale percentuale e della lista delle informazioni sugli acquisti
    return string_acquisti

def rimuovi_USDT(nome_criptovaluta):
    # Dividi il nome della criptovaluta utilizzando '/'
    parti_nome = nome_criptovaluta.split('/')

    # Ritorna la prima parte del nome (prima di '/')
    return parti_nome[0]

def converti_formato_data(testo):
    # Definiamo un'espressione regolare per cercare date nel formato YYYY-MM-DD
    regex_data = r'\b(\d{4})-(\d{2})-(\d{2})\b'

    # Cerchiamo tutte le date nel testo
    match_date = re.findall(regex_data, testo)

    # Se troviamo delle date, le convertiamo nel formato DDmonYY
    if match_date:
        for match in match_date:
            # Estraiamo i componenti della data
            anno, mese, giorno = match

            # Convertiamo il mese nel formato abbreviato
            mesi_abbreviati = {'01': 'gen', '02': 'feb', '03': 'mar', '04': 'apr', '05': 'mag',
                               '06': 'giu', '07': 'lug', '08': 'ago', '09': 'set', '10': 'ott',
                               '11': 'nov', '12': 'dic'}
            mese_abbreviato = mesi_abbreviati[mese]

            # Costruiamo la nuova data nel formato DDmonYY
            nuova_data = f"{giorno}{mese_abbreviato}{anno[2:]}"

            # Sostituiamo la data nel testo originale
            testo = testo.replace(f"{anno}-{mese}-{giorno}", nuova_data)

    # Ritorniamo il testo con le date convertite
    return testo
def controlla_file():
    # Ottieni la data di oggi
    oggi = datetime.now().strftime('%Y-%m-%d')

    # Controlla se il file esiste
    if os.path.exists(FILEPATH_DATI):
        # Leggi il contenuto del file
        with open("dati.json", "r") as file:
            dati = json.load(file)
        # Controlla se la data di oggi è presente nel dizionario
        if oggi in dati:
            print("dati di oggi gia presenti")
        else:

            print("oggi mancante, adding data to file...")
            crypto_string = crypto_request()
            salva_stringa(crypto_string)
    else:
        print("Il file non esiste.")
        # Crea un nuovo file con un dizionario vuoto
        with open("dati.json", "w") as file:
            dati = {}
            json.dump(dati, file)
        print("File creato.")

def leggi_stringa_oggi():
    # Ottieni la data di oggi
    oggi = datetime.now().strftime('%Y-%m-%d')

    # Controlla se il file esiste
    if os.path.exists(FILEPATH_DATI):
        # Leggi il contenuto del file
        with open(FILEPATH_DATI, "r") as file:
            dati = json.load(file)
        # Controlla se la data di oggi è presente nel dizionario
        if oggi in dati:
            print("Stringa/e trovata/e per oggi:")
            return dati[oggi]
        else:
            print("Nessuna stringa trovata per oggi. faccio la cripto request")
            crypto_string = crypto_request()
            salva_stringa(crypto_string)
            print("nuova stringa dati salvata, lettura del file...")
            with open(FILEPATH_DATI, "r") as file:
                dati = json.load(file)
            # Controlla se la data di oggi è presente nel dizionario
            if oggi in dati:
                print("file letto, stringa trovata :")
                return dati[oggi]
            else:
                print("error 2 tentativo di lettura errato")
                return ["try one more", "time"]
    else:
        print("Il file non esiste. Creazione del file...")
        # Crea un nuovo file con un dizionario vuoto
        with open("dati.json", "w") as file:
            dati = {}
            json.dump(dati, file)
        print("File creato.")


def salva_stringa(lista_stringhe):
    # Ottieni la data di oggi
    oggi = datetime.now().strftime('%Y-%m-%d')

    # Crea il dizionario con la lista di stringhe salvata come valore e la data come chiave
    data_dict = {oggi: lista_stringhe}

    # Controlla se il file esiste già
    if os.path.exists("dati.json"):
        # Leggi il contenuto del file
        with open("dati.json", "r") as file:
            dati = json.load(file)
        # Aggiungi il nuovo dizionario ai dati esistenti
        dati.update(data_dict)
    else:
        dati = data_dict

    # Scrivi i dati aggiornati nel file
    with open("dati.json", "w") as file:
        json.dump(dati, file)

    print("Stringa/i salvata/e correttamente.")
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
    string_acquisti.append(f"{rimuovi_USDT(symbol)}:")

    #print(f"Dettagli degli acquisti per {symbol}:")
    for data_acquisto, nome_crypto in crypto_portfolio.keys():
        if nome_crypto == symbol:

            importo = crypto_portfolio[(data_acquisto, nome_crypto)]
            total_invested += importo

            rendimento = get_crypto_percentage_change(nome_crypto, data_acquisto)
            reso_acquisto = importo * rendimento / 100
            total_returns += reso_acquisto
            string_acquisti.append(f"{importo} USD: {rendimento:.2f}% [{data_acquisto}]")

            ##print(f" {symbol} ASSET: {importo} USD del {data_acquisto}, RENDIMENTO: {rendimento:.2f}%")


    reso_totale_percentuale = (total_returns / total_invested) * 100
    string_acquisti.append(f"Total: {reso_totale_percentuale:.2f}% ({total_returns:.2f}/{total_invested}USD)")
    ##print(f"RENDIMENTO TOTALE {symbol}: {reso_totale_percentuale:.2f}% ({total_returns:.2f}USD). Deposito: {total_invested} USD")
    return reso_totale_percentuale ,string_acquisti

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

def leggi_portfolio(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            print("portfolio letto")
            return json.load(f)
    else:
        return {}

def salva_portfolio(portfolio, file_path):
    if os.path.exists(file_path):
        print("porfolio esistente")
        existing_portfolio = leggi_portfolio(file_path)
        existing_portfolio.update(portfolio)
        with open(file_path, 'w') as f:
            json.dump(existing_portfolio, f)
    else:
        print("creo nuovo portfolio")
        with open(file_path, 'w') as f:
            json.dump(portfolio, f)

def crypto_request():



    crypto_portfolio = {}

    # Esempio di utilizzo
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2022-05-30', 200)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2023-01-27', 50)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2023-12-11', 18)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-01-11', 160)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2022-06-09', 50)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-01-24', 20)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2023-12-15', 20)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2022-11-10', 10)
    aggiungi_crypto(crypto_portfolio, 'MATIC/USDT', '2024-01-10', 40)
    aggiungi_crypto(crypto_portfolio, 'MATIC/USDT', '2024-01-24', 20)
    aggiungi_crypto(crypto_portfolio, 'MATIC/USDT', '2023-12-20', 10)
    aggiungi_crypto(crypto_portfolio, 'BTTC/USDT', '2023-12-16', 30)
    aggiungi_crypto(crypto_portfolio, 'BTTC/USDT', '2023-12-16', 10)
    aggiungi_crypto(crypto_portfolio, 'BTTC/USDT', '2024-01-31', 15)
    aggiungi_crypto(crypto_portfolio, 'FLUX/USDT', '2024-01-10', 22)
    aggiungi_crypto(crypto_portfolio, 'AR/USDT', '2023-12-20', 25)
    aggiungi_crypto(crypto_portfolio, 'AR/USDT', '2024-01-31', 10)
    aggiungi_crypto(crypto_portfolio, 'PYR/USDT', '2023-12-20', 20)
    aggiungi_crypto(crypto_portfolio, 'PYR/USDT', '2024-02-07', 20)
    aggiungi_crypto(crypto_portfolio, 'SUPER/USDT', '2023-12-15', 20)
    aggiungi_crypto(crypto_portfolio, 'ADA/USDT', '2023-12-20', 11)
    aggiungi_crypto(crypto_portfolio, 'DOGE/USDT', '2022-05-30', 8)
    aggiungi_crypto(crypto_portfolio, 'DOGE/USDT', '2022-11-01', 20)
    aggiungi_crypto(crypto_portfolio, 'SHIB/USDT', '2023-04-19', 8)
    aggiungi_crypto(crypto_portfolio, 'WLD/USDT', '2023-12-16', 12)
    aggiungi_crypto(crypto_portfolio, 'JTO/USDT', '2023-12-16', 11)
    aggiungi_crypto(crypto_portfolio, 'XAI/USDT', '2024-01-10', 2)
    aggiungi_crypto(crypto_portfolio, 'MDX/USDT', '2023-12-12', 2)
    aggiungi_crypto(crypto_portfolio, 'CTXC/USDT', '2024-02-20', 8)
    aggiungi_crypto(crypto_portfolio, 'AGIX/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'OCEAN/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'SOL/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'PROM/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'NMR/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'HBAR/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'FET/USDT', '2024-02-20', 18)





    crypto_set = set()
    sconto_percentuale = 2
    string = []
    defi_string = []
    string_all_buyed_asset =[]
    dict_minimi = {}
    dict_short_value ={}
    today = datetime.now().strftime("%Y-%m-%d")
    defi_string.append("CRIPTOVALUTE: " + str(today))
    ##print("Criptovalute nel portafoglio:")
    for data_acquisto, nome_crypto in crypto_portfolio.keys():
        print(nome_crypto)
        if nome_crypto not in crypto_set:
            #print("1 ",nome_crypto)
            giorni_passati = giorni_passati_da_minimo_locale_con_sconto(nome_crypto, sconto_percentuale)
            if giorni_passati is not None:
                #string.append(f"MINIMO LOCALE {nome_crypto}:  {giorni_passati} giorni fa.")
                dict_minimi[nome_crypto] = giorni_passati

                ##print(f"MINIMO LOCALE {nome_crypto}:  {giorni_passati} giorni fa.")
            else:
                ##print(f"Nessun minimo locale con sconto del 5% trovato per {nome_crypto}.")
                #string.appedd(f"Nessun minimo locale con sconto del 5% trovato per {nome_crypto}.")
                dict_minimi[nome_crypto] = 99999



            ##print(f"{num_giorni} giorni: {nome_crypto} in {trend} del {variazione_percentuale:.2f}%.")
            #string.append(f"{num_giorni_5} giorni: {nome_crypto} {trend_5} {variazione_percentuale_5:.2f}%.")
            num_giorni_2 = 2
            trend_2, variazione_percentuale_2 = trend_e_variazione_percentuale(nome_crypto, num_giorni_2)
            num_giorni_4 = 4
            trend_4, variazione_percentuale_4 = trend_e_variazione_percentuale(nome_crypto, num_giorni_4)
            num_giorni_8 = 8
            trend_8, variazione_percentuale_8 = trend_e_variazione_percentuale(nome_crypto, num_giorni_8)
            dict_short_value[nome_crypto] = (variazione_percentuale_2, variazione_percentuale_4, variazione_percentuale_8)

            ##print(f"{num_giorni} giorni: {nome_crypto} in {trend} del {variazione_percentuale:.2f}%.")
            #string.append(f"{num_giorni_2} giorni: {nome_crypto} in {trend_2} del {variazione_percentuale_2:.2f}%.")
            crypto_set.add(nome_crypto)

            a, string_acquisti = reso_totale_per_criptovaluta(crypto_portfolio,nome_crypto)
            string_all_buyed_asset.extend(string_acquisti)



    defi_string.append("ULTIMO MINIMO LOCALE:")
    for crypto, value in dict_minimi.items():
        # Stampo la stringa e il valore associato
        defi_string.append(f"{rimuovi_USDT(crypto)}: {value} g")

    # Ciclo attraverso ogni elemento del dizionario
    defi_string.append("| TREND | 2 gg | 4 gg | 8 gg |")
    for key, values in dict_short_value.items():
        # Stampa la stringa della chiave
        defi_string.append(f"|{rimuovi_USDT(key)}|: |{values[0]:.1f}%|{values[1]:.1f}%|{values[2]:.1f}%|")

    total = reso_totale_per_portafoglio(crypto_portfolio)
    defi_string.append(total[0])
    defi_string.append("end_simple")
    defi_string.extend(string_all_buyed_asset)








    return defi_string


# delete_file(FILEPATH_DATI)
# #salva file con dati di oggi, se gia ci sono skippa
# controlla_file()
#
# # print(defi_string)
# crypto_string = leggi_stringa_oggi()
# print(crypto_string)
#
# for info in crypto_string:
#     info_c = converti_formato_data(info)
#     if info_c == "end_simple":
#         break
#     else:
#         print(info_c)
#
#







# Call the function to get the last git pull







