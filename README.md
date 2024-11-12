# Smart Home System Multi-Utility



The **Smart Home System Multi-Utility** is an advanced DIY IoT solution designed to manage home automation, security, and personal financial analysis, all controlled remotely via a Telegram bot hosted on a Raspberry Pi.



## Features



### 1. Home Automation and Security

This system enables remote control of essential home functions, ensuring convenience and security:



- **Automatic Gate Control**: The system remotely controls an automatic gate using electrical relays managed by a Raspberry Pi.

- **Environmental Monitoring**: Continuously monitors temperature and humidity, providing real-time data for a comfortable and secure living environment.

- **Password-Protected Access**: Access to the bot and all its commands is secured, ensuring high protection.



### 2. Financial Bot for Cryptocurrency Portfolio Analysis

This project also includes a sophisticated financial bot with real-time cryptocurrency tracking and analysis tools:



#### Portfolio Tracking and Analysis

- **Performance Comparison with Bitcoin (BTC)**: Tracks individual crypto assets against BTC, illustrating how each asset performs relative to BTC over time.

- **Daily Price Change Monitoring**: Analyzes daily changes in portfolio value and offers statistical comparisons across assets.

- **Trend Analysis**: Detects short-term (2, 4, 8-day) and long-term trends for each cryptocurrency asset.

- **Local Minimum Identification**: Highlights recent minimum prices for each asset to help users make informed investment decisions.



#### Data Analysis Techniques

The financial bot incorporates multiple data analysis techniques to aid in portfolio evaluation:



- **Cumulative Percentage Change**: Calculates cumulative returns for each asset from the purchase date, making it easier to assess long-term investment performance.

- **Scatter and Line Plots**: Uses scatter plots to illustrate performance against BTC and line plots for cumulative trends, facilitating easy interpretation of portfolio growth or decline.

- **BTC/ETH Ratio Tracking**: Provides a comparative view of Bitcoin and Ethereum by visualizing their price ratio over time, enabling users to monitor the relative strength of these two major assets.



#### Data Management and Storage

The bot saves portfolio data locally in JSON files, making it easy to retrieve and update data. This local storage ensures that data is retained between sessions and provides users with persistent access to their portfolio information.



### 3. Automated Updates and Remote Reboot

The system can be remotely rebooted via the Telegram bot. After rebooting, it automatically updates by pulling the latest changes from GitHub and relaunches, ensuring it runs with the most recent version. This remote update mechanism keeps the system up-to-date and reliable without requiring physical access.



## Usage



The **Smart Home System Multi-Utility** is accessible through a Telegram bot, allowing users to manage home automation and financial tracking tasks via their mobile devices:



- **Home Automation**: Control the gate and monitor environmental data with simple commands.

- **Portfolio Management**: Receive daily updates on portfolio performance, track new cryptocurrencies, and view visual reports on asset behavior.

- **System Management**: Remotely reboot and update the system to ensure it’s running the latest version.



## Project Setup



To set up the **Smart Home System Multi-Utility**:



1. Clone the repository to your Raspberry Pi.

2. Configure your Telegram bot token and other personal settings in the constants file.

3. Run the bot to activate the home automation and financial tracking features.



## Technical Requirements



- **Hardware**: Raspberry Pi, temperature and humidity sensors, and electrical relays.

- **Software**: Python, libraries including `ccxt` for cryptocurrency data, `Adafruit_DHT` for sensors, and `telepot` for the Telegram bot interface.

- **Data Visualization**: Uses `matplotlib` to generate portfolio graphs, trend charts, and BTC/ETH ratio plots.



## Future Enhancements

The following features may be added in future updates:



- Advanced financial analysis tools for in-depth market insights.

- Expanded home automation to control additional devices.

- Multi-user access with separate permissions for enhanced security.



## License

This project is licensed under the MIT License.

"""


