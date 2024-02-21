import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

def convert_portfolio(crypto_orig_portfolio, crypto_orig_value, current_crypto_dest_value):
    """
    Funzione per la conversione di un portafoglio di una criptovaluta nell'altra criptovaluta.

    Args:
    crypto_orig_portfolio (float): Quantità della criptovaluta nel portafoglio di origine.
    crypto_orig_value (float): Valore della criptovaluta nel portafoglio di origine.
    current_crypto_dest_value (float): Valore corrente della criptovaluta nel portafoglio di destinazione.

    Returns:
    float: Nuova quantità della criptovaluta nel portafoglio di origine dopo la conversione.
    float: Nuova quantità della criptovaluta nel portafoglio di destinazione dopo la conversione.
    """

    # Calcola la quantità di crypto da trasferire
    crypto_to_transfer = crypto_orig_portfolio * (crypto_orig_value / current_crypto_dest_value)

    # Aggiorna i portafogli dopo la conversione
    new_crypto_orig_portfolio = 0.0
    new_crypto_dest_portfolio = crypto_to_transfer

    return new_crypto_orig_portfolio, new_crypto_dest_portfolio

def buy_crypto(funds, crypto_portfolio, crypto_price, percentage):
    """
    Funzione per acquistare una percentuale di una criptovaluta con i fondi disponibili.

    Args:
    funds (float): Fondi disponibili per l'acquisto.
    crypto_portfolio (float): Quantità della criptovaluta già presente nel portafoglio.
    crypto_price (float): Prezzo corrente della criptovaluta.
    percentage (float): Percentuale dei fondi da spendere per acquistare la criptovaluta.

    Returns:
    float: Nuova quantità della criptovaluta nel portafoglio dopo l'acquisto.
    float: Nuovi fondi disponibili dopo l'acquisto.
    """

    # Calcola l'importo dei fondi da spendere
    amount_to_spend = funds * (percentage / 100)

    # Calcola la quantità di crypto da acquistare
    crypto_to_buy = amount_to_spend / crypto_price

    # Aggiorna il portafoglio cripto
    new_crypto_portfolio = crypto_portfolio + crypto_to_buy

    # Aggiorna i fondi disponibili
    new_funds = funds - amount_to_spend

    return new_crypto_portfolio, new_funds

def correlation_matrix(normalized_data,name):
    print(name)

    #print(normalized_data)
    # Calcola la correlazione tra tutte le coppie di criptovalute
    correlation_matrix = pd.DataFrame(index=normalized_data.keys(), columns=normalized_data.keys())
    for crypto1 in normalized_data.keys():
        for crypto2 in normalized_data.keys():
            if crypto1 != crypto2:
                correlation_matrix.loc[crypto1, crypto2] = normalized_data[crypto1][name].corr(
                    normalized_data[crypto2][name])

    # Trasforma i valori NaN in un valore arbitrariamente grande negativo
    correlation_matrix.fillna(1, inplace=True)
    print(correlation_matrix)
    #print(correlation_matrix)

    # Trova l'indice della riga e della colonna corrispondente al valore minimo della matrice di correlazione
    min_corr_index = correlation_matrix.stack().idxmin()

    # Ottieni il nome delle criptovalute corrispondenti all'indice
    crypto1, crypto2 = min_corr_index

    print("La coppia di criptovalute con il valore di correlazione minimo è:", crypto1, "e", crypto2)
    print("Il valore di correlazione minimo è:", correlation_matrix.loc[crypto1, crypto2])


# Function to calculate cross-correlation
def cross_correlation(x, y):
    n =  366
    result = np.fft.ifft(np.fft.fft(x, n) * np.fft.fft(y, n).conj()).real
    result /= np.sqrt(np.dot(x, x) * np.dot(y, y))
    return result


# Function to calculate cross-correlation with Bitcoin
def calculate_cross_correlation(crypto_data, bitcoin_data):
    # Extracting date and close prices for both cryptocurrencies and Bitcoin
    crypto_close = crypto_data['Close']
    bitcoin_close = bitcoin_data['Close']

    # Calculate cross-correlation
    cross_corr = cross_correlation(crypto_close, bitcoin_close)

    return cross_corr


def plot_correlation():

    # Folder path
    folder_path = 'crypto_data/'

    # Reading Bitcoin data
    bitcoin_data = pd.read_csv(folder_path + 'Download Data - CRYPTOCURRENCY_US_COINDESK_BTCUSD.csv')
    bitcoin_data['Close'] = pd.to_numeric(bitcoin_data['Close'].str.replace(',', ''), errors='coerce')

    # Reading other crypto data
    crypto_files = [file for file in os.listdir(folder_path) if file != 'Download Data - CRYPTOCURRENCY_US_COINDESK_BTCUSD.csv']
    correlation_values = []

    for file in crypto_files:
        crypto_name = file.split('_')[-1].split('.')[0]  # Extracting the cryptocurrency name
        crypto_data = pd.read_csv(folder_path + file)
        crypto_data['Close'] = pd.to_numeric(crypto_data['Close'].astype(str).str.replace(',', ''), errors='coerce')

        # Merge datasets on 'Date' column
        merged_data = pd.merge(crypto_data[['Date', 'Close']], bitcoin_data[['Date', 'Close']], on='Date',
                               suffixes=('_crypto', '_bitcoin'))

        # Calculate monthly correlation
        merged_data['Date'] = pd.to_datetime(merged_data['Date'])
        merged_data.set_index('Date', inplace=True)
        monthly_correlation = merged_data.resample('M').apply(lambda x: x['Close_crypto'].corr(x['Close_bitcoin']))
        correlation_values.append(monthly_correlation)

        # Calculating cross-correlation with Bitcoin
        cross_correlation_result = calculate_cross_correlation(crypto_data, bitcoin_data)
        print(f"{crypto_name} Cross-Correlation with Bitcoin:\n{cross_correlation_result}")

        # Plotting cross-correlation
        plt.figure(figsize=(10, 6))
        plt.plot(np.arange(len(cross_correlation_result)), cross_correlation_result)
        plt.title(f"{crypto_name} Cross-Correlation with Bitcoin")
        plt.xlabel('Time Lag')
        plt.ylabel('Cross-Correlation')
        plt.grid(True)
        plt.show()

    # Plotting staircase graph
    fig, ax = plt.subplots()
    for i, correlation in enumerate(correlation_values):
        correlation.plot(drawstyle='steps-post', ax=ax, label=crypto_files[i].split('_')[-1].split('.')[0])

    plt.xlabel('Date')
    plt.ylabel('Correlation')
    plt.title('Monthly Correlation with Bitcoin')
    plt.legend()
    plt.show()

#____


def plot_percentage(name = 'percenatage'):
    # Folder path
    folder_path = 'crypto_data/'

    # Lista dei file delle criptovalute
    crypto_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Dizionario per memorizzare i dati normalizzati delle criptovalute
    normalized_data = {}

    # Leggi e normalizza i dati di ogni criptovaluta
    for file in crypto_files:
        print(file)
        # Leggi i dati dalla criptovaluta
        crypto_data = pd.read_csv(os.path.join(folder_path, file))
        crypto_data['Close'] = pd.to_numeric(crypto_data['Close'].astype(str).str.replace(',', ''), errors='coerce')


        # Calcola la variazione percentuale tra il prezzo di oggi e il prezzo di ieri
        crypto_data[name] = (crypto_data['Close'] - crypto_data['Close'].shift(1)) / crypto_data[
            'Close'].shift(1) * 100

        # Salva i dati nel dizionario
        crypto_name = file.split('_')[-1].split('.')[0]
        normalized_data[crypto_name] = crypto_data

    print("CORR PERCENTAGE")
    correlation_matrix(normalized_data,name)

    # Plot dell'andamento della variazione percentuale di tutte le criptovalute
    plt.figure(figsize=(10, 6))
    for crypto_name, data in normalized_data.items():
        plt.plot(data[name], label=crypto_name)

    plt.title('Variazione percentuale giornaliera delle criptovalute')
    plt.xlabel('Giorni')
    plt.ylabel('Variazione percentuale (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()




def plot_value_normalized(name = 'normalized'):
    # Folder path
    folder_path = 'crypto_data/'

    # Lista dei file delle criptovalute
    crypto_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Dizionario per memorizzare i dati normalizzati delle criptovalute
    normalized_data = {}


    # Leggi e normalizza i dati di ogni criptovaluta
    for file in crypto_files:

        # Leggi i dati dalla criptovaluta
        crypto_data = pd.read_csv(os.path.join(folder_path, file))
        crypto_data['Close'] = pd.to_numeric(crypto_data['Close'].astype(str).str.replace(',', ''), errors='coerce')


        # Normalizza i dati tra 0 e 1
        crypto_data[name] = (crypto_data['Close'] - crypto_data['Close'].min()) / (
                    crypto_data['Close'].max() - crypto_data['Close'].min())

        # Salva i dati normalizzati nel dizionario
        crypto_name = file.split('_')[-1].split('.')[0]
        normalized_data[crypto_name] = crypto_data

    print("CORR NORMALIZED")
    correlation_matrix(normalized_data,name)

    # Plot dell'andamento normalizzato di tutte le criptovalute
    plt.figure(figsize=(10, 6))
    for crypto_name, data in normalized_data.items():
        plt.plot(data[name], label=crypto_name)

    plt.title('Andamento normalizzato delle criptovalute')
    plt.xlabel('Giorni')
    plt.ylabel('Prezzo normalizzato')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def percantege_cumulative(name = 'cumulative'):
    # Folder path
    folder_path = 'crypto_data/'

    # Lista dei file delle criptovalute
    crypto_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Dizionario per memorizzare i dati normalizzati delle criptovalute
    normalized_data = {}

    # Leggi e normalizza i dati di ogni criptovaluta
    for file in crypto_files:
        # Leggi i dati dalla criptovaluta
        crypto_data = pd.read_csv(os.path.join(folder_path, file))
        crypto_data['Close'] = pd.to_numeric(crypto_data['Close'].astype(str).str.replace(',', ''), errors='coerce')

        # Calcola la variazione percentuale tra il prezzo di oggi e il prezzo di ieri
        crypto_data['Percent_Change'] = (crypto_data['Close'] - crypto_data['Close'].shift(1)) / crypto_data[
            'Close'].shift(1) * 100

        # Calcola la variazione percentuale cumulativa
        crypto_data[name] = crypto_data['Percent_Change'].cumsum()

        # Salva i dati nel dizionario
        crypto_name = file.split('_')[-1].split('.')[0]
        normalized_data[crypto_name] = crypto_data
    print("CORR PERCENTAGE CUMULATIVE")
    correlation_matrix(normalized_data,name)

    # Plot dell'andamento della variazione percentuale cumulativa di tutte le criptovalute
    plt.figure(figsize=(10, 6))
    for crypto_name, data in normalized_data.items():
        plt.plot(data[name], label=crypto_name)

    plt.title('Variazione percentuale cumulativa delle criptovalute')
    plt.xlabel('Giorni')
    plt.ylabel('Variazione percentuale cumulativa (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()




def bot_simulator_alpha(crypto_name_1 = "BTCUSD",crypto_name2 = 'ETHUSD'):
    # Folder path
    credito_crypto_1 = 1000
    credito_crypto_2 = 1000

    primal_crypto = crypto_name_1
    secondary_crypto = crypto_name2


    folder_path = 'crypto_data/'

    # Lista dei file delle criptovalute
    crypto_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Dizionario per memorizzare i dati normalizzati delle criptovalute
    normalized_data = {}

    # Leggi e normalizza i dati di ogni criptovaluta
    for file in crypto_files:
        # Leggi i dati dalla criptovaluta
        crypto_data = pd.read_csv(os.path.join(folder_path, file))
        crypto_data['Close'] = pd.to_numeric(crypto_data['Close'].astype(str).str.replace(',', ''), errors='coerce')
        # Salva i dati nel dizionario
        crypto_name = file.split('_')[-1].split('.')[0]
        normalized_data[crypto_name] = crypto_data



    # Estrai i dati relativi alla criptovaluta di interesse
    crypto_data = normalized_data[primal_crypto]

    # Inverti l'ordine delle righe nel DataFrame
    # Inverti l'ordine delle righe nel DataFrame e l'indice
    crypto_data = crypto_data.reindex(index=crypto_data.index[::-1])
    crypto_data.reset_index(drop=True, inplace=True)


    # Itera su ogni riga del DataFrame
    for i in range(len(crypto_data)):

        if i == 0:
            print(crypto_data.at[i,'Close'])
            crypto_data.at[i, 'Trend'] = "BUY 20 BTCUSD"
        else:

            # Inizializza l'indice per cercare all'indietro
            j = i

            # Cerca all'indietro fino a trovare l'ultimo valore non NaN nella colonna "Trend"
            while j >= 0 and pd.isnull(crypto_data.at[j, 'Trend']):
                j -= 1

                # Se è stato trovato un valore non NaN, calcola la variazione percentuale
            if j >= 0:
                last_valid_close = crypto_data.at[j, 'Close']
                current_close = crypto_data.at[i, 'Close']
                percent_change = (current_close - last_valid_close) / last_valid_close * 100


            else:
                print(f"Per la riga {i}: Nessun valore non NaN trovato nella colonna 'Trend'")

            if percent_change <= -5:

                crypto_data.at[i, 'Trend'] = "BUY 1/2 BTCUSD"
                print(
                    f"oggi {i+1}^ giorno: Variazione dall ultimo swap[{i - j} giorni fa]: {percent_change:.2f}%, Swap = {crypto_data.at[j, 'Trend']}, {crypto_data.at[j, 'Date']}")
                print("NEGATIVO PER " + primal_crypto + "CONTINUA! BUY 1/2 BTCUSD")


                #COMPRA QUI

            elif percent_change >= 5:

                crypto_data.at[i, 'Trend'] = "SWAP 20 " + primal_crypto + " to " + secondary_crypto

                print(
                    f"oggi {i+1}^ giorno: Variazione dall ultimo swap[{i - j} giorni fa]: {percent_change:.2f}%, Swap = {crypto_data.at[j, 'Trend']}, {crypto_data.at[j, 'Date']}")
                print("farò! SELL 20 BTCUSD")

                #SWAPPA QUI

                primal_crypto, secondary_crypto = secondary_crypto, primal_crypto
                print("PRIMARIA: " + primal_crypto)
                crypto_data = normalized_data[primal_crypto]




            else:
                crypto_data.at[i, 'Trend'] = None

    print(crypto_data)





    # Visualizza il DataFrame con la nuova colonna


bot_simulator_alpha()
# percantege_cumulative()
# plot_value_normalized()
# plot_percentage()