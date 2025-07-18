import sys
import time

import ccxt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import json
import os
import re
from CONSTANT import *
import subprocess
import pandas as pd
import re
import calendar

import random


# Aggiungi il percorso della repository esterna a sys.path
repo_esterna_path = os.path.expanduser("~/PRIVATE_SMART_HOME")
sys.path.insert(0, repo_esterna_path)

# Ora puoi importare tutto dallo script desiderato
from confidential_data import *
import registro_crypto as PORTFOLIO



DAY_FOR_PORTFOLIO_PLOT_AND_BTC = 150


def plot_moves_preformance_time_wrt_BTC(data,days_limit = 120):
    x_values = []
    y_values_crypto = []
    y_values_BTC = []
    crypto_symbol = []

    for item in data:
        # Split della stringa per trovare le diverse parti
        parts = item.split()

        # Estrazione della crypto
        crypto = parts[0].replace(":", "")

        # Estrazione del valore y per la crypto
        y_crypto = float(parts[1].replace("%", ""))

        # Estrazione della data
        date_str = parts[2].split(":")[1].replace("[", "").replace("]", "").replace("$", "")
        date = datetime.strptime(date_str, '%d%b%y').date()
        # Estrazione del valore y per BTC

        y_BTC = float(parts[3].replace("%BTC", ""))

        y_BTC_real = y_crypto - (y_BTC)

        x_values.append(date)
        y_values_crypto.append(y_crypto)
        y_values_BTC.append(y_BTC_real)
        crypto_symbol.append(crypto)

        # Creazione del grafico

        # # Calcolo dei valori massimi e minimi per impostare gli assi y
        # max_y = max(max(y_values_crypto), max(y_values_BTC)) + 5
        # min_y = min(min(y_values_crypto), min(y_values_BTC)) - 5

        # Trova la data più recente e la più antica










    filtered_y_crypto = []
    filtered_y_BTC = []
    filtered_date =[]
    crypto_symbol_filtered = []

    # Creazione del grafico
    latest_date = None
    for date, y_crypto_value, y_BTC_value, crypto_label in zip(x_values, y_values_crypto, y_values_BTC,crypto_symbol):
        if latest_date is None or date > latest_date:
            latest_date = date
    print("LETEST DAY PURCHESE:::: ",latest_date)


    today = latest_date

    # 60 giorni fa
    days_ago_60 = today - timedelta(days=days_limit)



    for date, y_crypto_value, y_BTC_value, crypto_label in zip(x_values, y_values_crypto, y_values_BTC,crypto_symbol):
        if date > days_ago_60:
            filtered_y_crypto.append(y_crypto_value)
            filtered_y_BTC.append(y_BTC_value)
            filtered_date.append(date)
            crypto_symbol_filtered.append(crypto_label)


    plt.figure(figsize=(16, 6), dpi=300)

        # Scatter plot per Crypto
    plt.scatter(filtered_date, filtered_y_crypto, label='Crypto', color='blue', marker="_",s = 500)
    # Scatter plot per BTC Diff
    plt.scatter(filtered_date, filtered_y_BTC, label='BTC', color='olive',marker="_",s = 500)
    for i in range(len(filtered_date)):
        if filtered_y_crypto[i] > filtered_y_BTC[i]:
            plt.plot([filtered_date[i], filtered_date[i]], [filtered_y_crypto[i], filtered_y_BTC[i]], color='lightgreen', linestyle='--', linewidth = 4, alpha=0.5)
            plt.text(filtered_date[i], filtered_y_crypto[i], crypto_symbol_filtered[i], fontsize=8, ha='left', va='bottom')
        else:
            plt.plot([filtered_date[i], filtered_date[i]], [filtered_y_crypto[i], filtered_y_BTC[i]], color='red', linestyle='--', linewidth = 4, alpha=0.5)
            plt.text(filtered_date[i], filtered_y_crypto[i], crypto_symbol_filtered[i], fontsize=8, ha='left', va='top')


    max_y = max(max(filtered_y_crypto),max(filtered_y_BTC))
    min_y = min(min(filtered_y_crypto),min(filtered_y_BTC))
    plt.ylim(min_y-5, max_y+5)
    plt.xlim(days_ago_60, today)

    # Aggiunta delle etichette e della legenda
    plt.xlabel('Date',fontsize=12)
    plt.ylabel('Performance (%)',fontsize=12)
    plt.title('Performance Time w.r.t BTC',fontsize=12)
    plt.legend()
    plt.grid(True)

    # Trova la data più recente e la più antica

    # Rotazione delle date sull'asse x per migliorare la leggibilità
    plt.xticks(rotation=45)

    # Visualizzazione del grafico
    plt.tight_layout()


    # Percorso del file di salvataggio
    file_path_fig = FOLDER_GRAPH + '/MOVERS_price_plot.png'

    # Verifica se il file esiste già
    if os.path.exists(file_path_fig):
        # Se il file esiste, eliminilo
        os.remove(file_path_fig)
        print("removed old plot")

    # Salva la figura
    plt.savefig(file_path_fig)


def convet_numbers_to_day_in_past_dates(days_in_past):
    today = datetime.now()
    custom_dates = []
    for days in days_in_past:
        date = today - timedelta(days=days)
        month_name = calendar.month_abbr[date.month]
        custom_date_format = f"{date.day} {month_name}, {date.year}"
        custom_dates.append(custom_date_format)
    return custom_dates

def extract_purchase_dates_and_amounts(crypto_portfolio):
    purchase_dates = []
    purchase_amounts = []

    for (date_str, _), amount in crypto_portfolio.items():
        # Converti la data da stringa a oggetto datetime
        date = datetime.strptime(date_str, "%Y-%m-%d")

        # Calcola il numero di giorni trascorsi dall'acquisto fino ad oggi
        days_since_purchase = (datetime.now() - date).days

        # Aggiungi la data all'elenco dei giorni di acquisto
        purchase_dates.append(days_since_purchase)

        # Aggiungi l'importo dell'acquisto all'elenco dei soldi spesi
        purchase_amounts.append(amount)

    return purchase_dates, purchase_amounts
def calculate_cumulative_percentage_change(prices):
    cumulative_percentage = [0]  # Inizializza con il primo giorno a 0%
    for i in range(1, len(prices)):
        percentage_change = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        cumulative_percentage.append(cumulative_percentage[-1] + percentage_change)
    return cumulative_percentage


def plot_portfolio_variation(portfolio_variation, crypto_portfolio, crypto_data_dict, DAYS_IN_PAST, name):
    PLOT_DAYS = DAYS_IN_PAST
    REDUCTION_BITCOIN_POWER = 50
    # Trova la data del primo acquisto nel portafoglio
    first_purchase_date = min([datetime.strptime(date, "%Y-%m-%d") for date, _ in crypto_portfolio.keys()])

    # Trova la data attuale
    current_date = datetime.now()

    # Calcola tutti i giorni tra la data del primo acquisto e la data attuale
    days_since_first_purchase = [(current_date - first_purchase_date - timedelta(days=i)).days for i in range((current_date - first_purchase_date).days)]

    days_since_purchase, purchase_amounts = extract_purchase_dates_and_amounts(crypto_portfolio)
    #print(days_since_purchase, purchase_amounts)


    # Estrai i prezzi di chiusura di Bitcoin
    bitcoin_prices = crypto_data_dict.get('BTC/USDT', {}).get('close', [])

    # Calcola il rendimento percentuale cumulativo di Bitcoin
    bitcoin_cumulative_percentage = calculate_cumulative_percentage_change(bitcoin_prices)

    # Se ci sono dati disponibili per Bitcoin
    # Calcola la differenza di lunghezza tra i dati del portafoglio e i dati di Bitcoin
    days_since_first_purchase.append(0)
    del bitcoin_cumulative_percentage[:9]

    #print(len(days_since_first_purchase),len(bitcoin_cumulative_percentage),len(portfolio_variation))

    length_difference = len(days_since_first_purchase) - len(bitcoin_cumulative_percentage)

    if length_difference > 0:

        # Se la lunghezza di days_since_first_purchase è maggiore, taglia i primi elementi dei prezzi di Bitcoin
        days_since_first_purchase_mod = days_since_first_purchase[length_difference:]
    else:
        days_since_first_purchase_mod = days_since_first_purchase

    length_difference_2 = len(days_since_first_purchase) - len(portfolio_variation)
    if length_difference_2 > 0:
        # Se la lunghezza di days_since_first_purchase è maggiore, taglia i primi elementi dei prezzi di Bitcoin
        days_since_first_purchase_2 = days_since_first_purchase[length_difference_2:]
    else:
        days_since_first_purchase_2 = days_since_first_purchase

    # portfolio_variation.reverse()
    # bitcoin_cumulative_percentage.reverse()





    # Plot dell'andamento del portafoglio
    plt.figure(figsize=(12, 6))
    plt.plot(convet_numbers_to_day_in_past_dates(days_since_first_purchase_2), portfolio_variation, label='Portafoglio')
    plt.grid(True)

    # Estrai solo l'ultimo dodicesimo elemento dalla lista dei valori del portafoglio e delle date
    bitcoin_cumulative_percentage_mod = [x - REDUCTION_BITCOIN_POWER for x in bitcoin_cumulative_percentage]


    portfolio_variation_last_twelfth = portfolio_variation[-PLOT_DAYS:]
    BTC_variation_last_twelfth = bitcoin_cumulative_percentage_mod[-PLOT_DAYS:]
    date_labels_last_twelfth = days_since_first_purchase_mod[-PLOT_DAYS:]

    converted_last_dates_twelfth = convet_numbers_to_day_in_past_dates(date_labels_last_twelfth)

    max_portfolio_value = max(portfolio_variation_last_twelfth)
    min_portfolio_value = min(portfolio_variation_last_twelfth)

    max_BTC_value = max(BTC_variation_last_twelfth)
    min_BTC_value = min(BTC_variation_last_twelfth)

    max_graph = max([max_BTC_value,max_portfolio_value])
    min_graph = min([min_BTC_value,min_portfolio_value])

    # Plot dell'andamento di Bitcoin


    plt.plot(convet_numbers_to_day_in_past_dates(days_since_first_purchase_mod), bitcoin_cumulative_percentage_mod, label=f'Bitcoin - {REDUCTION_BITCOIN_POWER}%')
    #if len(days_since_purchase) > len(portfolio_variation):




    portfolio_values_acquisition = []
    for day in days_since_purchase:
        portfolio_values_acquisition.append(portfolio_variation[len(portfolio_variation) - (day+1)])

    # Aggiungi punti per i giorni di acquisto sul grafico
    raggi = [elemento / 2 for elemento in purchase_amounts]
    #day_shift = [x -1 for x in days_since_purchase]
    day_shift = [x - 0 for x in days_since_purchase]

    plt.scatter(convet_numbers_to_day_in_past_dates(day_shift), portfolio_values_acquisition, s=raggi, color='red')
    # Aggiungi etichette agli assi e una legenda
    plt.xlabel('Giorni dalla data del primo acquisto')
    plt.ylabel('Valore del Portafoglio')
    plt.legend()
    plt.xlim(converted_last_dates_twelfth[0], converted_last_dates_twelfth[-1])

    if name == "RECENT":
        plt.ylim(min_portfolio_value, max_portfolio_value)
    else:
        plt.ylim(min_graph, max_graph)
    plt.xticks(rotation=45)  # Rotazione delle date per una migliore leggibilità
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=15))  # Imposta il numero massimo di ticks sull'asse x
    plt.tight_layout()  # Ottimizza il layout del grafico



    # Percorso del file di salvataggio
    file_path_fig = FOLDER_GRAPH + '/'+ name +'_ALL_price_plot.png'

    # Verifica se il file esiste già
    if os.path.exists(file_path_fig):
        # Se il file esiste, eliminilo
        os.remove(file_path_fig)
        print("removed old plot")

    # Salva la figura
    plt.savefig(file_path_fig)




def reso_totale_per_portafoglio_tempo(crypto_portfolio, crypto_data_dict, plusvalenze):

    # Somma delle plusvalenze
    total_plusvalenze = sum(plusvalenze)

    string_acquisti = []
    reso_percentuale_cumulativo = []

    # Estrai le date degli acquisti
    purchase_dates = [pd.to_datetime(date) for date, _ in crypto_portfolio.keys()]

    # Trova la data del primo acquisto
    first_purchase_date = min(purchase_dates).date()

    # Ciclo attraverso tutte le date da first_purchase_date fino ad oggi
    current_date = datetime.now().date()
    delta = timedelta(days=1)
    while first_purchase_date <= current_date:
        # Calcola la data in formato stringa
        current_date_str = first_purchase_date.strftime("%Y-%m-%d")

        # Calcola il rendimento percentuale dal primo acquisto a current_date
        total_invested = 0
        total_returns = 0
        for (data_acquisto, nome_crypto), importo in crypto_portfolio.items():
            if pd.to_datetime(data_acquisto).date() <= first_purchase_date:
                # Calcola il rendimento percentuale parziale dal primo acquisto a current_date per ogni crypto
                rendimento = get_crypto_percentage_change(nome_crypto, data_acquisto, crypto_data_dict, current_date_str)
                if rendimento is not None:
                    reso_acquisto = importo * rendimento / 100

                    total_returns += reso_acquisto
                    total_invested += importo
        total_invested -= total_plusvalenze
        reso_totale_percentuale = (total_returns / total_invested) * 100

        # Aggiornamento del totale investito e del rendimento totale





        # Calcola il rendimento percentuale cumulativo
        reso_percentuale_cumulativo.append(reso_totale_percentuale)

        # Passa al giorno successivo
        first_purchase_date += delta


    return reso_percentuale_cumulativo


def get_binance_symbols():
    # Crea un'istanza del modulo di scambio Binance
    exchange = ccxt.binance()

    try:
        # Ottieni tutti i simboli (coppie di trading) disponibili su Binance
        symbols = exchange.fetch_markets()


        # Filtra i simboli per coppie che hanno USDT come valuta quotata
        usdt_symbols = [symbol['symbol'] for symbol in symbols if symbol['quote'] == 'USDT']


        return usdt_symbols
    except Exception as e:
        print(f"Si è verificato un errore durante il recupero dei simboli da Binance: {e}")
        return None


def save_symbols_to_file(symbols, filename):
    if symbols is not None:
        with open(filename, 'w') as file:

            for symbol in symbols:
                file.write(symbol + '\n')


def load_symbols_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            symbols = [line.strip() for line in file.readlines()]
            return symbols
    else:
        return []


def check_for_new_symbols(filename):


    print("Nuove criptovalute quotate su Binance: CERCATELE DA SOLO")


    return None


def image_inspector(filepath):
    # Lista per salvare le prime parti dei nomi dei file
    crypto_names = []

    # Scansiona i file nella cartella
    for filename in os.listdir(filepath):
        # Verifica che il file sia un'immagine
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Divide il nome del file in base all'underscore
            parts = filename.split("_")
            # Prendi la prima parte del nome del file (prima dell'underscore)
            crypto_name = parts[0]
            # Aggiungi la prima parte alla lista crypto_names
            crypto_names.append(crypto_name)
            # Se la tipologia di grafico non è stata ancora impostata, impostala

    return (crypto_names)


def custom_sort_key(element):
    # Utilizza espressione regolare per trovare il primo valore numerico nella stringa
    match = re.search(r'-?\d+', element)
    if match:
        # Restituisci il primo valore numerico trovato
        return -int(match.group())  # Aggiungi il segno negativo per l'ordinamento decrescente
    else:
        # Se non ci sono valori numerici, posiziona la stringa all'inizio
        return float('-inf')  # Utilizza meno infinito come valore minimo


def fetch_cryptocurrency_data(exchange, symbol, limit_days=365, frequency='1d'):
    # Calcola la data di inizio e fine
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=limit_days)

    # Converte le date in timestamp UNIX
    since = int(start_date.timestamp() * 1000)
    until = int(end_date.timestamp() * 1000)

    # Recupera i dati tramite ccxt
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=frequency, since=since, limit=limit_days)

    # Costruisci il DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # Converti il timestamp in formato leggibile
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Imposta il timestamp come indice
    df.set_index('timestamp', inplace=True)

    return df


def create_cryptocurrency_data_dict(exchange, symbols, limit_days=730, frequency='1d'):
    print(f"parto da {limit_days} giorni fa")
    data_dict = {}
    for symbol in symbols:
        try:
            df = fetch_cryptocurrency_data(exchange, symbol, limit_days, frequency)
            data_dict[symbol] = df
            print(f"Data fetched successfully for {symbol}")
        except Exception as e:
            print(f"Failed to fetch data for {symbol}: {e}")
    return data_dict


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




def reso_totale_per_portafoglio(crypto_portfolio, crypto_data_dict, plusvalenze):
    total_invested = 0
    total_returns = 0

    # Somma delle plusvalenze
    total_plusvalenze = sum(plusvalenze)

    string_acquisti = []

    # Ciclo attraverso tutte le coppie chiave-valore nel dizionario
    for (data_acquisto, nome_crypto), importo in crypto_portfolio.items():
        # Calcolo del rendimento parziale per ogni criptovaluta nel portafoglio
        rendimento = get_crypto_percentage_change(nome_crypto, data_acquisto, crypto_data_dict)
        reso_acquisto = importo * rendimento / 100

        # Aggiornamento del totale investito e del rendimento totale
        total_invested += importo
        total_returns += reso_acquisto

        # Costruzione della stringa relativa agli acquisti per ogni criptovaluta
        #string_acquisti.append(f"{nome_crypto}: {importo} USD, Rendimento: {rendimento:.2f}%")

    # Sottrazione delle plusvalenze dal totale investito
    total_invested -= total_plusvalenze

    # Calcolo del rendimento totale percentuale
    reso_totale_percentuale = (total_returns / total_invested) * 100

    # Aggiunta delle informazioni sul rendimento totale alla stringa degli acquisti
    string_acquisti.append(f"PORTAFOGLIO: {reso_totale_percentuale:.1f}%, {total_returns:.0f}/{total_invested:.0f}$ PLUS:{total_plusvalenze}$")

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
            mesi_abbreviati = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May',
                               '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct',
                               '11': 'Nov', '12': 'Dec'}
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


def trend_e_variazione_percentuale(crypto_data_dict, symbol, num_giorni):

    # Ottieni la data e l'ora correnti
    current_datetime = datetime.now()

    # Formatta la data e l'ora correnti con ore e minuti
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

    # Estrai i dati storici della criptovaluta specificata dal dizionario
    if symbol in crypto_data_dict:
        df = crypto_data_dict.get(symbol)
        if df is None:
            print(f"No data found for {symbol}")
            return None

        # Estrai il prezzo di chiusura per ogni giorno
        prices = df['close'].tolist()

        if len(prices) > num_giorni+1:

            # Calcola il trend degli ultimi N giorni
            trend = "++" if prices[-1] > prices[-num_giorni] else "--"

            # Calcola la variazione percentuale degli ultimi N giorni
            variazione_percentuale = ((prices[-1] - prices[-num_giorni]) / prices[-num_giorni]) * 100
        else:
            trend = "++"
            variazione_percentuale = 0

        return trend, variazione_percentuale
    else:
        print(f"Il simbolo '{symbol}' non è presente nel dizionario crypto_data_dict.")
        return None, None



def giorni_passati_da_minimo_locale_con_sconto(symbol, crypto_data_dict, sconto_percentuale=2):
    MINIMUM_HISTORY_ON_BINANCEC = 15
    ultimi_giorni_da_non_contare = 10
    # Ottieni la data e l'ora correnti
    current_datetime = datetime.now()

    # Formatta la data e l'ora correnti con ore e minuti
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

    # Estrai i dati OHLCV dalla criptovaluta specificata
    df = crypto_data_dict.get(symbol)
    if df is None:
        print(f"No data found for {symbol}")
        return None

    # Estrai il prezzo di chiusura per ogni giorno
    prices = df['close'].astype(float).tolist()

    if len(prices) > MINIMUM_HISTORY_ON_BINANCEC:

        # Calcola il valore attuale della criptovaluta
        valore_attuale = prices[-1]

        # Trova l'indice del minimo locale con uno sconto del 5%
        minimo_locale_index = None

        for i in range(len(prices) - ultimi_giorni_da_non_contare, 0, -1):

            if (valore_attuale - prices[i]) / valore_attuale * 100 >= sconto_percentuale:
                minimo_locale_index = i
                break

        if minimo_locale_index is not None:
            # Calcola il numero di giorni passati dal minimo locale con sconto
            giorni_passati = len(prices) - minimo_locale_index - 1

            # Calcola il massimo valore tra oggi e il minimo locale
            # Estrai il massimo valore dei prezzi dalla lista dei prezzi dal minimo locale fino alla fine
            max_price = max(prices[minimo_locale_index:])

            # Prendi il prezzo di chiusura degli ultimi due giorni
            ultimo_prezzo = prices[-1]
            penultimo_prezzo = prices[-2]

            # Calcola l'andamento
            if ultimo_prezzo > penultimo_prezzo:
                andamento = "+"
            elif ultimo_prezzo < penultimo_prezzo:
                andamento = "-"
            else:
                andamento = "="





            # Plot dei dati relativi al periodo dell'ultimo minimo locale
            min_date = df.index[minimo_locale_index]
            max_index = prices.index(max(prices[minimo_locale_index:]))
            data_massimo_locale = df.index[max_index]
            oggi = df.index[-1]

            min_price = prices[minimo_locale_index]

            percentage = abs(max_price - valore_attuale) / valore_attuale * 100

            today = datetime.now()

            plt.figure(figsize=(12, 3))

            if giorni_passati < 30:
                # Se il minimo locale è meno di 30 giorni fa, plotta solo gli ultimi 30 giorni
                plt.plot(df.index[-30:], df['close'][-30:], label='Price')
            else:
                # Altrimenti, plotta dal minimo locale fino alla fine dei dati disponibili
                plt.plot(df.index[minimo_locale_index:], df['close'][minimo_locale_index:], label='Price')

            # Aggiungi un punto sul grafico per indicare il minimo locale
            plt.scatter(min_date, min_price, color='red', label='Local Min')


            if giorni_passati > 3:
                plt.plot([data_massimo_locale, data_massimo_locale], [max_price, valore_attuale], color='green', linestyle='dashed', linewidth=1)

                plt.plot([data_massimo_locale, oggi], [valore_attuale, valore_attuale], color='green', linestyle='dashed', linewidth=1)
                plt.scatter(data_massimo_locale, max_price, color='black')
                plt.scatter(data_massimo_locale, valore_attuale, color='black')
                plt.scatter(oggi, valore_attuale, color='black')



            # Aggiungi il titolo al grafico con informazioni aggiuntive
            plt.title(f'{formatted_datetime}: {rimuovi_USDT(symbol)}. Local minimum: {giorni_passati}g. Max module: {percentage:.2f}%')

            plt.xlabel('Date')
            plt.ylabel('Price (USD)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            # Salva il grafico con il nome della criptovaluta
            plt.savefig(FOLDER_GRAPH + f'/{rimuovi_USDT(symbol)}_price_plot.png')
            plt.close()

            return giorni_passati, andamento, percentage
    else:

        return 1, "=", 0




def aggiungi_plusvalenza(plusvalenze, valore):
    plusvalenze.append(valore)
    return plusvalenze

def valutatore_singoli_investimenti_DEPRECATED(crypto_portfolio, crypto_data_dict, symbol, esprimi_percentuale=True):
    total_invested = 0
    total_returns = 0

    string_acquisti = []

    # Calcola il rendimento della crypto in questione
    for (data_acquisto, nome_crypto), importo in crypto_portfolio.items():
        if nome_crypto == symbol:
            total_invested += importo

            # Ottieni il rendimento dalla funzione get_crypto_percentage_change
            rendimento = get_crypto_percentage_change(nome_crypto, data_acquisto, crypto_data_dict)
            reso_acquisto = importo * rendimento / 100
            total_returns += reso_acquisto

            # Calcola il rendimento come se fosse Bitcoin
            rendim_btc = get_crypto_percentage_change('BTC/USDT', data_acquisto, crypto_data_dict)
            string_acquisti.append(f"{rimuovi_USDT(symbol)}: {rendimento:.0f}% [{importo}$:{converti_formato_data(data_acquisto)}] {rendimento-rendim_btc:.0f}%BTC")

    reso_totale_percentuale = (total_returns / total_invested) * 100

    # Ritorna il rendimento totale e la lista degli investimenti
    return reso_totale_percentuale, string_acquisti

def valutatore_singoli_investimenti(crypto_portfolio, crypto_data_dict, symbol, esprimi_percentuale=True):
    total_invested = 0
    total_returns = 0
    rendimento_BTC_somma = 0
    conteggio = 0
    date_acquisti = []

    string_acquisti = []

    # Calcola il rendimento cumulativo su tutti gli acquisti di questa crypto
    for (data_acquisto, nome_crypto), importo in crypto_portfolio.items():
        if nome_crypto == symbol:
            total_invested += importo
            rendimento = get_crypto_percentage_change(nome_crypto, data_acquisto, crypto_data_dict)
            reso_acquisto = importo * rendimento / 100
            total_returns += reso_acquisto

            rendim_btc = get_crypto_percentage_change('BTC/USDT', data_acquisto, crypto_data_dict)
            if rendim_btc is not None:
                rendimento_BTC_somma += rendim_btc
                conteggio += 1

            date_acquisti.append(data_acquisto)

    # Evita divisione per zero
    if total_invested == 0:
        reso_totale_percentuale = 0
    else:
        reso_totale_percentuale = (total_returns / total_invested) * 100

    if conteggio > 0:
        differenza_BTC = reso_totale_percentuale - (rendimento_BTC_somma / conteggio)
    else:
        differenza_BTC = 0

    # Prendi la data del primo acquisto
    if date_acquisti:
        data_rappresentativa = converti_formato_data(min(date_acquisti))
    else:
        data_rappresentativa = "01Jan70"  # fallback di sicurezza

    # Costruisci la stringa IDENTICA al formato originale
    string_acquisti.append(
        f"{rimuovi_USDT(symbol)}: {reso_totale_percentuale:.0f}% [{total_invested}$:{data_rappresentativa}] {differenza_BTC:.0f}%BTC"
    )

    return reso_totale_percentuale, string_acquisti




def get_crypto_percentage_change(symbol, start_date, crypto_data_dict, end_date=None):
    if symbol in crypto_data_dict:
        # Estrai il DataFrame dei dati della criptovaluta
        df = crypto_data_dict.get(symbol)
        if df is None:
            print(f"No data found for {symbol}")
            return None

        # Converte la data di inizio e fine in oggetti datetime
        start_timestamp = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date is None:
            end_timestamp = df.index[-1]
        else:
            end_timestamp = datetime.strptime(end_date, "%Y-%m-%d")

        # Estrai i prezzi di chiusura per il periodo specificato
        close_prices = df.loc[start_timestamp:end_timestamp, 'close']
        prices = close_prices.tolist()

        if len(prices) == 0:
            print(f"No data available for {symbol} between {start_date} and {end_date}")
            return None

        # Calcola la variazione percentuale tra la data di inizio e quella di fine
        start_price = prices[0]
        end_price = prices[-1]
        percentage_change = ((end_price - start_price) / start_price) * 100

        return percentage_change
    else:
        print(f"Il simbolo '{symbol}' non è presente nel dizionario crypto_data_dict.")
        return None


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


def calcola_rapporto_btc_eth(crypto_data_dict):
    btc_prices = crypto_data_dict.get('BTC/USDT', {}).get('close', [])
    eth_prices = crypto_data_dict.get('ETH/USDT', {}).get('close', [])

    min_length = min(len(btc_prices), len(eth_prices))
    btc_prices = btc_prices[:min_length]
    eth_prices = eth_prices[:min_length]

    rapporto_btc_eth = [btc_price / eth_price for btc_price, eth_price in zip(btc_prices, eth_prices)]

    return btc_prices, eth_prices, rapporto_btc_eth


def plot_rapporto_btc_eth(btc_prices, eth_prices, rapporto_btc_eth):
    DAYS_RATIO = 120

    # Seleziona gli ultimi 150 valori
    btc_prices_last_150 = btc_prices[-DAYS_RATIO:]
    eth_prices_last_150 = eth_prices[-DAYS_RATIO:]
    rapporto_btc_eth_last_150 = rapporto_btc_eth[-DAYS_RATIO:]

    min_btc = min(btc_prices_last_150)
    max_btc = max(btc_prices_last_150)
    min_eth = min(eth_prices_last_150)
    max_eth = max(eth_prices_last_150)
    min_rapporto = min(rapporto_btc_eth_last_150)
    max_rapporto = max(rapporto_btc_eth_last_150)



    fig, axs = plt.subplots(3, 1, figsize=(12, 18))

    # Plot BTC prices
    axs[0].plot(btc_prices_last_150, label='BTC', color='orange')

    axs[0].set_ylabel('BTC $')
    axs[0].grid(True)

    axs[0].set_ylim(min_btc, max_btc)

    # Plot ETH prices
    axs[1].plot(eth_prices_last_150, label='ETH', color='blue')
    axs[1].set_ylabel('ETH $')
    axs[1].grid(True)
    axs[1].set_ylim(min_eth, max_eth)

    # Plot BTC/ETH ratio
    axs[2].plot(rapporto_btc_eth_last_150, label='BTC/ETH', color='green')

    axs[2].set_xlabel('Days')
    axs[2].set_ylabel('BTC/ETH')
    axs[2].grid(True)

    axs[2].set_ylim(min_rapporto, max_rapporto)

    plt.tight_layout()


    file_path_fig = FOLDER_GRAPH + '/RATIO_price_plot.png'

    # Verifica se il file esiste già
    if os.path.exists(file_path_fig):
        # Se il file esiste, eliminilo
        os.remove(file_path_fig)
        print("removed old plot")

    # Salva la figura
    plt.savefig(file_path_fig)


def calcola_giorni_primo_acquisto(crypto_portfolio):
    # Trova la data più vecchia nel portafoglio
    data_acquisto_più_vecchia = min(
        [datetime.strptime(data_acquisto, "%Y-%m-%d") for data_acquisto, _ in crypto_portfolio.keys()])

    # Calcola la differenza di giorni tra la data più vecchia e la data odierna
    oggi = datetime.now()
    giorni_passati = (oggi - data_acquisto_più_vecchia).days
    return giorni_passati

def crypto_request():


    crypto_portfolio = PORTFOLIO.crea_portafoglio()



    giorni_acquisto_piu_vecchio = calcola_giorni_primo_acquisto(crypto_portfolio)

    plusvalenze = []
    PEPE = 15
    FLOKY = 29
    PEPE_DATA = ('PEPE/USDT', '2024-02-23', '2024-03-02', 10) #25
    plusvalenze = aggiungi_plusvalenza(plusvalenze, PEPE)


    # Estrai tutti i nomi unici di criptovalute
    # Estrai tutti i nomi unici di criptovalute
    symbols = list(set([key[1] for key in crypto_portfolio.keys()]))
    symbols.sort()


    exchange = ccxt.binance()

    # Crea il dizionario dei dati delle criptovalute
    crypto_data_dict = create_cryptocurrency_data_dict(exchange, symbols, giorni_acquisto_piu_vecchio + 10 )


    crypto_set = set()
    sconto_percentuale = 2
    string = []
    defi_string = []
    string_all_buyed_asset =[]
    dict_minimi = {}
    dict_andam = {}
    dict_perc = {}
    dict_short_value ={}
    today = datetime.now().strftime("%Y-%m-%d")



    ##print("Criptovalute nel portafoglio:")
    for nome_crypto in symbols:

        #print("1 ",nome_crypto)
        try:
            giorni_passati, andamento_ld, percentage_max = giorni_passati_da_minimo_locale_con_sconto(nome_crypto, crypto_data_dict)
        except Exception as e:
            print("error giorni_passati_da_minimo_locale_con_sconto",e)
            print(nome_crypto)
            print(crypto_data_dict.get(nome_crypto))
        if giorni_passati is not None:
            #string.append(f"MINIMO LOCALE {nome_crypto}:  {giorni_passati} giorni fa.")
            dict_minimi[nome_crypto] = giorni_passati
            dict_andam[nome_crypto] = andamento_ld
            dict_perc[nome_crypto] = percentage_max

            ##print(f"MINIMO LOCALE {nome_crypto}:  {giorni_passati} giorni fa.")
        else:
            ##print(f"Nessun minimo locale con sconto del 5% trovato per {nome_crypto}.")
            #string.appedd(f"Nessun minimo locale con sconto del 5% trovato per {nome_crypto}.")
            dict_minimi[nome_crypto] = 1
            dict_andam[nome_crypto] = 1
            dict_perc[nome_crypto] = 1




        num_giorni_2 = 2
        trend_2, variazione_percentuale_2 = trend_e_variazione_percentuale(crypto_data_dict, nome_crypto, num_giorni_2)
        num_giorni_4 = 4
        trend_4, variazione_percentuale_4 = trend_e_variazione_percentuale(crypto_data_dict,nome_crypto, num_giorni_4)
        num_giorni_8 = 8
        trend_8, variazione_percentuale_8 = trend_e_variazione_percentuale(crypto_data_dict,nome_crypto, num_giorni_8)
        dict_short_value[nome_crypto] = (variazione_percentuale_2, variazione_percentuale_4, variazione_percentuale_8)


        crypto_set.add(nome_crypto)

        a, string_acquisti = valutatore_singoli_investimenti(crypto_portfolio,crypto_data_dict,nome_crypto)

        string_all_buyed_asset.extend(string_acquisti)




    for crypto, value in dict_minimi.items():
        # Stampo la stringa e il valore associato
        values = dict_short_value[crypto]
        defi_string.append(f"{rimuovi_USDT(crypto)}:{value}g [{dict_perc[crypto]:.1f}%]({dict_andam[crypto]})|{values[0]:.1f}%|{values[1]:.1f}%|{values[2]:.1f}%|")

    defi_string = sorted(defi_string, key=custom_sort_key, reverse=True)
    defi_string.insert(0, "LOCAL MIN | MODULE | TRENDS, ")



    filname = "symbol_binance.txt"
    new_symbol_binance = check_for_new_symbols(filname)
    defi_string.append("NEW CRYPTO: "+str(new_symbol_binance))


    # Ottieni la data e l'ora correnti
    current_datetime = datetime.now()

    # Formatta la data e l'ora correnti con ore e minuti

    exact_time = current_datetime.strftime("%Y-%m-%d %H:%M")
    defi_string.insert(0,"CRIPTOVALUTE: " + str(exact_time))

    total = reso_totale_per_portafoglio(crypto_portfolio,crypto_data_dict,plusvalenze)
    portfolio_variation = reso_totale_per_portafoglio_tempo(crypto_portfolio, crypto_data_dict, plusvalenze)
    plot_portfolio_variation(portfolio_variation, crypto_portfolio, crypto_data_dict, 60 , "RECENT")
    plot_portfolio_variation(portfolio_variation, crypto_portfolio, crypto_data_dict, 365, "OLD")

    # Supponiamo che crypto_data_dict sia il tuo dizionario dei dati di criptovaluta
    btc_prices, eth_prices, rapporto_btc_eth = calcola_rapporto_btc_eth(crypto_data_dict)
    plot_rapporto_btc_eth(btc_prices, eth_prices, rapporto_btc_eth)

    defi_string.append(total[0])
    defi_string.append("end_simple")
    defi_string.insert(0,"MOVES: " + str(exact_time))



    plot_moves_preformance_time_wrt_BTC(string_all_buyed_asset)

    string_all_buyed_asset = sorted(string_all_buyed_asset, key=custom_sort_key, reverse=False)
    defi_string.extend(string_all_buyed_asset)








    return defi_string

DEBUG = 0

if DEBUG:

    print("DEBUG")
    delete_file(FILEPATH_DATI)
    # #salva file con dati di oggi, se gia ci sono skippa
    controlla_file()
    #
    # # print(defi_string)
    crypto_string = leggi_stringa_oggi()
    # print(crypto_string)


    # crypto_string = crypto_request()

    for info in crypto_string:
        info_c = converti_formato_data(info)
        if info_c == "end_simple":
            break
        else:
            print(info_c)

    # MOVERS
    pr = 0
    for info in crypto_string:
        info_c = converti_formato_data(info)
        if info_c == "end_simple":
            pr = 1
        if pr == 1:
            print(info_c)

