import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np


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


# Folder path
folder_path = 'crypto_data/'

# Reading Bitcoin data
bitcoin_data = pd.read_csv(folder_path + 'Download Data - CRYPTOCURRENCY_US_COINDESK_BTCUSD.csv')
bitcoin_data['Close'] = pd.to_numeric(bitcoin_data['Close'].str.replace(',', ''), errors='coerce')
print(bitcoin_data['Close'])
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