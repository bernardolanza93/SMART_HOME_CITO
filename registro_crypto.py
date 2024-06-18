def aggiungi_crypto(portfolio, nome_crypto, data_acquisto, importo):
    key = (data_acquisto, nome_crypto)
    portfolio[key] = importo



def crea_portafoglio():

    crypto_portfolio = {}

    # Esempio di utilizzo
    aggiungi_crypto(crypto_portfolio, 'BNB/USDT', '2024-02-27', 55)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2022-05-30', 100)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2023-01-27', 50)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2023-12-11', 18)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2024-03-05', 100)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2024-04-03', 20)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2024-06-12', 100)

    aggiungi_crypto(crypto_portfolio, 'W/USDT', '2024-04-04', 30)

    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2022-06-09', 50)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2022-11-10', 10)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2023-12-15', 20)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-01-11', 160)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-01-24', 20)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-02-28', 204)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-03-02', 25)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-03-05', 100)
    aggiungi_crypto(crypto_portfolio, 'ETH/USDT', '2024-03-21', 287)

    aggiungi_crypto(crypto_portfolio, 'BOME/USDT', '2024-03-16', 5)
    aggiungi_crypto(crypto_portfolio, 'BOME/USDT', '2024-03-19', 8)

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
    aggiungi_crypto(crypto_portfolio, 'SUPER/USDT', '2024-02-24', 11)
    aggiungi_crypto(crypto_portfolio, 'ADA/USDT', '2023-12-20', 11)
    aggiungi_crypto(crypto_portfolio, 'ADA/USDT', '2024-03-12', 25)
    aggiungi_crypto(crypto_portfolio, 'DOT/USDT', '2024-03-12', 70)
    aggiungi_crypto(crypto_portfolio, 'UNI/USDT', '2024-03-12', 50)
    aggiungi_crypto(crypto_portfolio, 'DOGE/USDT', '2022-05-30', 8)
    aggiungi_crypto(crypto_portfolio, 'DOGE/USDT', '2022-11-01', 20)
    aggiungi_crypto(crypto_portfolio, 'SHIB/USDT', '2023-04-19', 8)
    aggiungi_crypto(crypto_portfolio, 'SHIB/USDT', '2024-03-05', 50)
    aggiungi_crypto(crypto_portfolio, 'WLD/USDT', '2023-12-16', 12)
    aggiungi_crypto(crypto_portfolio, 'JTO/USDT', '2023-12-16', 11)
    aggiungi_crypto(crypto_portfolio, 'XAI/USDT', '2024-01-10', 2)
    aggiungi_crypto(crypto_portfolio, 'XAI/USDT', '2024-03-04', 25)
    aggiungi_crypto(crypto_portfolio, 'XAI/USDT', '2024-03-05', 24)


    aggiungi_crypto(crypto_portfolio, 'CTXC/USDT', '2024-02-20', 8)
    aggiungi_crypto(crypto_portfolio, 'CTXC/USDT', '2024-03-14', 46)
    aggiungi_crypto(crypto_portfolio, 'CTXC/USDT', '2024-03-19', 15)
    aggiungi_crypto(crypto_portfolio, 'AGIX/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'OCEAN/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'OCEAN/USDT', '2024-02-27', 18)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-02-29', 53)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-03-04', 25)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-03-04', 100)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-03-08', 51)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-03-21', 23)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-04-03', 46)

    aggiungi_crypto(crypto_portfolio, 'SOL/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'SOL/USDT', '2024-02-23', 10)
    aggiungi_crypto(crypto_portfolio, 'SOL/USDT', '2024-03-12', 25)
    aggiungi_crypto(crypto_portfolio, 'PROM/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'PROM/USDT', '2024-02-28', 23)
    aggiungi_crypto(crypto_portfolio, 'NMR/USDT', '2024-02-21', 10)
    aggiungi_crypto(crypto_portfolio, 'NMR/USDT', '2024-02-27', 28)
    aggiungi_crypto(crypto_portfolio, 'HBAR/USDT', '2024-02-20', 10)
    aggiungi_crypto(crypto_portfolio, 'HBAR/USDT', '2024-02-23', 10)
    aggiungi_crypto(crypto_portfolio, 'FET/USDT', '2024-02-20', 18)
    aggiungi_crypto(crypto_portfolio, 'GALA/USDT', '2024-02-23', 20)

    aggiungi_crypto(crypto_portfolio, 'JASMY/USDT', '2024-02-23', 35)
    aggiungi_crypto(crypto_portfolio, 'JASMY/USDT', '2024-02-24', 50)
    aggiungi_crypto(crypto_portfolio, 'JASMY/USDT', '2024-03-04', 31)
    aggiungi_crypto(crypto_portfolio, 'JASMY/USDT', '2024-03-08', 45)

    aggiungi_crypto(crypto_portfolio, 'AI/USDT', '2024-02-23', 25)
    aggiungi_crypto(crypto_portfolio, 'RNDR/USDT', '2024-02-23', 30)
    aggiungi_crypto(crypto_portfolio, 'LUNC/USDT', '2024-02-23', 5)
    aggiungi_crypto(crypto_portfolio, 'AVAX/USDT', '2024-02-23', 15)
    aggiungi_crypto(crypto_portfolio, 'NTRN/USDT', '2024-02-23', 10)
    aggiungi_crypto(crypto_portfolio, 'NTRN/USDT', '2024-02-24', 20)
    aggiungi_crypto(crypto_portfolio, 'NTRN/USDT', '2024-03-05', 24)


    aggiungi_crypto(crypto_portfolio, 'ARB/USDT', '2024-02-23', 20)
    aggiungi_crypto(crypto_portfolio, 'ARB/USDT', '2024-03-18', 50)
    aggiungi_crypto(crypto_portfolio, 'ICP/USDT', '2024-02-26', 25)
    aggiungi_crypto(crypto_portfolio, 'PIXEL/USDT', '2024-02-26', 30)
    aggiungi_crypto(crypto_portfolio, 'PEPE/USDT', '2024-03-03', 15)
    aggiungi_crypto(crypto_portfolio, 'ROSE/USDT', '2024-03-04', 75)
    aggiungi_crypto(crypto_portfolio, 'GRT/USDT', '2024-03-06', 48)

    aggiungi_crypto(crypto_portfolio, 'ALCX/USDT', '2024-04-08', 2)
    aggiungi_crypto(crypto_portfolio, 'FARM/USDT', '2024-04-08', 1)
    aggiungi_crypto(crypto_portfolio, 'TNSR/USDT', '2024-04-08', 1)
    aggiungi_crypto(crypto_portfolio, 'STRAX/USDT', '2024-04-08', 1)
    aggiungi_crypto(crypto_portfolio, 'CREAM/USDT', '2024-04-08', 1)

    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-04-13', 20)
    aggiungi_crypto(crypto_portfolio, 'TAO/USDT', '2024-04-12', 15)
    aggiungi_crypto(crypto_portfolio, 'MATIC/USDT', '2024-04-13', 20)
    aggiungi_crypto(crypto_portfolio, 'BOME/USDT', '2024-04-13', 10)
    aggiungi_crypto(crypto_portfolio, 'PEPE/USDT', '2024-04-13', 10)
    aggiungi_crypto(crypto_portfolio, 'XAI/USDT', '2024-04-13', 10)

    aggiungi_crypto(crypto_portfolio, 'ADA/USDT', '2024-04-16', 40)
    aggiungi_crypto(crypto_portfolio, 'JUV/USDT', '2024-04-16', 2)
    aggiungi_crypto(crypto_portfolio, 'PYR/USDT', '2024-04-16', 25)
    aggiungi_crypto(crypto_portfolio, 'MATIC/USDT', '2024-04-16', 30)
    aggiungi_crypto(crypto_portfolio, 'OMNI/USDT', '2024-04-17', 5)
    aggiungi_crypto(crypto_portfolio, 'AR/USDT', '2024-04-18', 36)
    aggiungi_crypto(crypto_portfolio, 'WLD/USDT', '2024-04-18', 50)

    aggiungi_crypto(crypto_portfolio, 'OP/USDT', '2024-04-22', 48)
    aggiungi_crypto(crypto_portfolio, 'LINK/USDT', '2024-04-22', 48)


    aggiungi_crypto(crypto_portfolio, 'ILV/USDT', '2024-04-29', 10)
    aggiungi_crypto(crypto_portfolio, 'AXS/USDT', '2024-04-29', 10)
    aggiungi_crypto(crypto_portfolio, 'GMX/USDT', '2024-04-29', 10)
    aggiungi_crypto(crypto_portfolio, 'RONIN/USDT', '2024-04-29', 10)
    aggiungi_crypto(crypto_portfolio, 'IMX/USDT', '2024-04-29', 10)
    aggiungi_crypto(crypto_portfolio, 'TAO/USDT', '2024-04-29', 10)
    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2024-04-29', 16)
    aggiungi_crypto(crypto_portfolio, 'OP/USDT', '2024-04-29', 20)

    aggiungi_crypto(crypto_portfolio, 'BTC/USDT', '2024-05-06', 197)
    aggiungi_crypto(crypto_portfolio, 'LINK/USDT', '2024-05-20', 20)

    aggiungi_crypto(crypto_portfolio, 'OP/USDT', '2024-06-18', 25)
    aggiungi_crypto(crypto_portfolio, 'XAI/USDT', '2024-06-18', 25)
    aggiungi_crypto(crypto_portfolio, 'WLD/USDT', '2024-06-18', 25)
    aggiungi_crypto(crypto_portfolio, 'ALGO/USDT', '2024-06-18', 20)







#gestire swap :  da cosa a cosa :  swap(10 eth  / BTC  , giorno)
    #calcolo valore come modifica percentuale di investimento
    #implementazione nuova allora si guardano solo le coins totali e il totale speso:
    #calcolo delle coins totali per ogni cripto
    #calcolo crescita di ogni singolo acquisto
    #calcolo crescita di ogni scambio comparato al rimanere in quella (vale anche per le liquyidazioni) obv da giorno acquisto
    #aggiornamento coins totali (prendi giorno di scambio togli il numero di coins vecchie e aggiungiu le nuove dai rispettivi sub totali)
    #gran total: soldi investiti /  valore tutti i coins aggiornati ad oggi










    return crypto_portfolio