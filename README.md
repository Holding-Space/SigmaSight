# SigmaSight 📈
![SigmaSight Logo](https://i.imgur.com/E3gFCqC.png)

**SigmaSight** is a Python-based tool that transforms stock market data into actionable insights through interactive visuals. Ideal for both beginners and seasoned investors, SigmaSight offers customizable watchlists, trend analysis, and up-to-date data to help users understand market dynamics and make informed decisions.
## Features

- **Customizable Watchlist**: Track and manage stocks with price updates and performance summaries.
- **Interactive Charts**: Explore stock trends, historical performance, and key indicators like the 200-day EMA to spot investment opportunities.
- **Reliable Data**: Powered by `yfinance` for up-to-date stock market information.
- **User-Friendly Interface**: A clean, responsive design built with `customtkinter` for easy navigation.
## Installation 🔨

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Holding-Space/SigmaSight.git
    cd SigmaSight
    ```

2. **Install Dependencies** - Ensure Python is installed, then use:
    ```bash
    pip install -r requirements.txt
    ```
    ## Usage

To start SigmaSight, run:
```bash
python SigmaSight.py
```

**Main Menu**

There will be various graphs which will display data on the company. Scroll down to view more charts.

**Sidebar**

Enter your ticker and press update, data will update after a sec. Scroll in the sidebar to see various data like: Piotroski Score, Margins & Growth, Balance and Company Value data.

**Watchlist**

Input a ticker and press add to watchlist to do that. To update the dip finder just close and reopen the watchlist. 
## Screenshots 📸
![Main view](https://i.imgur.com/7QevEh9.png)

![Screenshot of watchlist view](https://i.imgur.com/QccEiKk.png)

## Updates ⌚
Exciting updates coming soon, including:
- **News**: See related news to a stock in the watchlist.
- **Projections**: View estimated performance for the company
- **Dividend Advisor**: Based on various factors, recommend companies that would be worth investing in.


## License

[MIT](https://choosealicense.com/licenses/mit/) License

Copyright (c) 2024 Holding-Space

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
