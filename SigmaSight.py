## Imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from watchlist import open_watchlist

import yfinance as yf
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import customtkinter as ctk

import os
import tkinter as tk

## Graph Formatting
def format_num(value, tick_number):
    # Format the number based on its size
    if value >= 1e12:
        return f'{value * 1e-12:.0f}T'
    elif value >= 1e9:
        return f'{value * 1e-9:.0f}B'  # Billions
    elif value >= 1e6:
        return f'{value * 1e-6:.0f}M'  # Millions
    elif value >= 1e3:
        return f'{value * 1e-3:.0f}K'  # Thousands
    else:
        return f'{value}'  # Less than thousand
    
def set_colours(ax):
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    
    ax.set_facecolor('black') 
    
    ax.tick_params(axis='x', colors='white')  # Set tick label color
    ax.tick_params(axis='y', colors='white')  # Set y-tick color
    ax.tick_params(bottom=True, left=False)
    
    ax.set_axisbelow(True)
    
    ax.yaxis.grid(True, color='#333333')
    ax.xaxis.grid(False)

## Graphs
def plot_stock_ytd(stock_symbol, ax):
    today = datetime.today().strftime('%Y-%m-%d')
    stock_data = yf.download(stock_symbol, start=f'{datetime.today().year}-01-01', end=today)
    
    # Plot the stock data
    ax.plot(stock_data.index, stock_data['Close'], label='YTD Price', color='blue')
    ax.set_title('Year-to-Date Price', color='white', loc='left')
    
    # Format x-axis to show only the month numbers
    months = stock_data.index.strftime('%m')  # Extract only month numbers
    ax.set_xticks(stock_data.index[::30])  # Set ticks approximately monthly (adjust the step if necessary)
    ax.set_xticklabels(months[::30], fontsize=8)  # Use month numbers for the labels

    # Label the x-axis
    ax.set_xlabel('Month', fontsize=8, color='white')
    
    # Format y-axis
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    
    # Set chart colors and other properties
    set_colours(ax)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.legend()

def plot_revenue(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    financials = stock.financials.T
    revenue = financials['Total Revenue'].dropna()
    revenue = revenue[revenue.index.year >= 2002]

    current_value = revenue.iloc[-1]
    previous_value = revenue.iloc[-2] if len(revenue) > 1 else None
    
    # Calculate percentage change
    percentage_change = ((current_value - previous_value) / previous_value * 100) if previous_value else None
    
    ax.bar(revenue.index.year, revenue.values, color='#3b86ff', width=0.95)
    ax.set_title('Revenue', color='white', loc='left', fontsize=18, x=-0.1258)

    ax.set_xticks(revenue.index.year)
    ax.set_xticklabels(revenue.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))

    set_colours(ax)

def plot_ebitda(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    financials = stock.financials.T
    ebitda = financials['EBITDA'].dropna()
    ebitda = ebitda[ebitda.index.year >= 2002]
    
    ax.bar(ebitda.index.year, ebitda.values, color='#00b5d9', width=0.95)
    ax.set_title('EBITDA', color='white', loc='left', x=-0.1258)
    ax.set_xticks(ebitda.index.year)
    ax.set_xticklabels(ebitda.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)

def plot_free_cash_flow(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    financials = stock.cashflow.T
    free_cash_flow = financials['Free Cash Flow'].dropna()
    free_cash_flow = free_cash_flow[free_cash_flow.index.year >= 2002]
    
    ax.bar(free_cash_flow.index.year, free_cash_flow.values, color='#03045e', width=0.95)
    ax.set_title('Free Cash Flow', color='white',  loc='left', x=-0.1258)
    ax.set_xticks(free_cash_flow.index.year)
    ax.set_xticklabels(free_cash_flow.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)

def plot_net_income(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    financials = stock.financials.T
    net_income = financials['Net Income'].dropna()
    net_income = net_income[net_income.index.year >= 2002]
    
    ax.bar(net_income.index.year, net_income.values, color='#004d00', width=0.95)
    ax.set_title('Net Income', color='white', loc='left', x=-0.1258)
    ax.set_xticks(net_income.index.year)
    ax.set_xticklabels(net_income.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)
    
def plot_eps(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    financials = stock.financials.T
    shares_outstanding = stock.balance_sheet.T['Ordinary Shares Number'].dropna()
    net_income = financials['Net Income'].dropna()
    eps = net_income / shares_outstanding
    eps = eps[eps.index.year >= 2002]
    
    ax.bar(eps.index.year, eps.values, color='#009933', width=0.95)
    ax.set_title('Earnings Per Share (EPS)', color='white',  loc='left', x=-0.1258)
    ax.set_xticks(eps.index.year)
    ax.set_xticklabels(eps.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)

def plot_cash_debt(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    balance_sheet = stock.balance_sheet.T
    cash = balance_sheet['Cash And Cash Equivalents'].dropna()
    debt = balance_sheet['Total Debt'].dropna()
    cash = cash[cash.index.year >= 2002]
    debt = debt[debt.index.year >= 2002]
    
    ax.bar(cash.index.year - 0.2, cash.values, width=0.475, label='Cash', color='#00d346')
    ax.bar(debt.index.year + 0.2, debt.values, width=0.475, label='Debt', color='#e31c1c')
    ax.set_title('Cash & Debt', color='white',  loc='left', x=-0.1258)
    ax.set_xticks(cash.index.year)
    ax.set_xticklabels(cash.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)

def plot_dividend_rate(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    dividends = stock.dividends
    dividend_rate = dividends.resample('YE').sum()  # Sum of dividends per year
    dividend_rate = dividend_rate[dividend_rate.index.year >= 2000]
    
    # Plot the data
    ax.bar(dividend_rate.index.year, dividend_rate.values, color='#66cc99', width=0.95)
    ax.set_title('Dividend Rate ($)', color='white', loc='left', x=-0.1258)
    
    years = dividend_rate.index.year
    ax.set_xticks(years[::5])
    ax.set_xticklabels(years[::5], fontsize=6)
    
    ax.tick_params(axis='y', labelsize=6)
    
    set_colours(ax)

def plot_shares_outstanding(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    shares_outstanding = stock.balance_sheet.T['Ordinary Shares Number'].dropna()
    shares_outstanding = shares_outstanding[shares_outstanding.index.year >= 2002]
    
    ax.bar(shares_outstanding.index.year, shares_outstanding.values, color='#FFD700', width=0.95)
    ax.set_title('Shares Outstanding (Billion)', color='white',  loc='left', x=-0.1258)
    ax.set_xticks(shares_outstanding.index.year)
    ax.set_xticklabels(shares_outstanding.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)

def plot_market_cap(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    stock_data = yf.download(stock_symbol, start='2002-01-01')
    shares_outstanding = stock.balance_sheet.T['Ordinary Shares Number'].dropna()
    
    market_cap = stock_data['Close'] * (shares_outstanding)  # Convert to billions
    market_cap = market_cap.dropna()  # Remove empty values
    
    ax.bar(market_cap.index.year, market_cap.values, color='#FFA500', width=0.95)
    ax.set_title('Market Capitalization', color='white',  loc='left', x=-0.1258)
    ax.set_xticks(market_cap.index.year)
    ax.set_xticklabels(market_cap.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)

def plot_ev(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    stock_data = yf.download(stock_symbol, start='2002-01-01')
    balance_sheet = stock.balance_sheet.T
    cash = balance_sheet['Cash And Cash Equivalents'].dropna()
    total_debt = balance_sheet['Total Debt'].dropna()
    shares_outstanding = balance_sheet['Ordinary Shares Number'].dropna()
    
    market_cap = stock_data['Close'] * (shares_outstanding)  # Convert to billions
    ev = market_cap + total_debt - cash  # Enterprise Value formula
    ev = ev.dropna()  # Remove empty values
    
    ax.bar(ev.index.year, ev.values, color='#bf9b30', width=0.95)
    ax.set_title('Enterprise Value', color='white',  loc='left', x=-0.1258)
    ax.set_xticks(ev.index.year)
    ax.set_xticklabels(ev.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)

def plot_pe_ratio(stock_symbol, ax):
    stock = yf.Ticker(stock_symbol)
    financials = stock.financials.T
    shares_outstanding = stock.balance_sheet.T['Ordinary Shares Number'].dropna()
    net_income = financials['Net Income'].dropna()
    eps = net_income / shares_outstanding
    stock_data = yf.download(stock_symbol, start='2002-01-01')
    
    pe_ratio = stock_data['Close'] / eps  # P/E ratio
    pe_ratio = pe_ratio.dropna()  # Remove empty values
    
    ax.bar(pe_ratio.index.year, pe_ratio.values, color='#ffcf40', width=0.95)
    ax.set_title('Price/Earnings Ratio (P/E)', color='white',  loc='left', x=-0.1258)
    ax.set_xticks(pe_ratio.index.year)
    ax.set_xticklabels(pe_ratio.index.year, fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_num))
    set_colours(ax)


##  GUI Content
def toggle_sidebar(sidebar_frame):
    if sidebar_frame.winfo_ismapped():
        sidebar_frame.grid_remove()
    else:
        sidebar_frame.grid()

def display_charts_with_sidebar(default_symbol='AAPL'):
    root = tk.Tk()
    
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title('SigmaSight000')
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.state('zoomed')
    
    root.configure(background="#23222b")
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    stock_symbol_var = tk.StringVar(value=default_symbol)

    sidebar_frame = ctk.CTkScrollableFrame(root, width=250, fg_color="black")
    sidebar_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

    content_frame = ctk.CTkScrollableFrame(root, fg_color="transparent")
    content_frame.grid(row=0, column=1, sticky="nsew")
    
    # Create a grid of frames for charts
    chart_frames = []
    for i in range(3):  # 3 rows
        row_frames = []
        content_frame.grid_rowconfigure(i, weight=1)  # Make rows expandable
        for j in range(4):  # 4 columns
            frame = ctk.CTkFrame(content_frame, fg_color="black", corner_radius=7.5)
            frame.grid(row=i, column=j, padx=5, pady=2.5, sticky="nsew")
            
            content_frame.grid_columnconfigure(j, weight=1)  # Make columns expandable
            
            canvas = FigureCanvasTkAgg(plt.Figure(figsize=(4.5, 3.5), facecolor='black'), master=frame)  # Adjust size here
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx= 2.5, pady = 2.5)  # Added padding inside frame
            
            row_frames.append((frame, canvas))
        chart_frames.append(row_frames)
        
    def update_charts():
        stock_symbol = stock_symbol_var.get()
        for i, row in enumerate(chart_frames):
            for j, (frame, canvas) in enumerate(row):
                canvas.figure.clear()  # Clear the figure
                ax = canvas.figure.add_subplot(111)  # Create a new subplot for each canvas

                # Fill each frame with the corresponding chart
                if i == 0 and j == 0:
                    plot_stock_ytd(stock_symbol, ax)  # Example for YTD chart
                elif i == 0 and j == 1:
                    plot_revenue(stock_symbol, ax)  # Example for Revenue chart
                elif i == 0 and j == 2:
                    plot_ebitda(stock_symbol, ax)  # Example for EBITDA chart
                elif i == 0 and j == 3:
                    plot_free_cash_flow(stock_symbol, ax)  # Example for Free Cash Flow chart
                elif i == 1 and j == 0:
                    plot_net_income(stock_symbol, ax)  # Example for Net Income chart
                elif i == 1 and j == 1:
                    plot_eps(stock_symbol, ax)  # Example for EPS chart
                elif i == 1 and j == 2:
                    plot_cash_debt(stock_symbol, ax)  # Example for Cash Debt chart
                elif i == 1 and j == 3:
                    plot_dividend_rate(stock_symbol, ax)  # Example for Dividend Rate chart
                elif i == 2 and j == 0:
                    plot_shares_outstanding(stock_symbol, ax)  # Example for Shares Outstanding chart
                elif i == 2 and j == 1:
                    plot_market_cap(stock_symbol, ax)  # Example for Market Cap chart
                elif i == 2 and j == 2:
                    plot_ev(stock_symbol, ax)  # Example for EV chart
                elif i == 2 and j == 3:
                    plot_pe_ratio(stock_symbol, ax)  # Example for PE Ratio chart

                update_dividend_info(stock_symbol)
                update_balance_info(stock_symbol)
                update_margins_growth_info(stock_symbol)
                update_value_info(stock_symbol)
                update_quality_info(stock_symbol)
                
                canvas.draw()  # Draw the updated figure

    def update_dividend_info(stock_symbol):
        stock = yf.Ticker(stock_symbol)
        info = stock.info
        calendar = stock.calendar
        
        dividend_yield.set(f"Dividend Yield: {info.get('dividendYield', 'N/A')}")
        payout_ratio.set(f"Payout Ratio: {round(float(info.get('payoutRatio', 'N/A')) * 100, 2)}%") 
        ex_div_date.set(f"Ex-Div Date: {datetime.fromtimestamp(info.get('exDividendDate', 'N/A')).strftime('%d/%m/%Y')}")
        payout_date.set(f"Payout Date: {calendar.get('Dividend Date', 'N/A').strftime('%d/%m/%Y')}")

    def update_balance_info(stock_symbol):
        stock = yf.Ticker(stock_symbol)
        balance_sheet = stock.balance_sheet.T
        cash = balance_sheet['Cash And Cash Equivalents'].dropna().iloc[-1] if not balance_sheet.empty else 0
        debt = balance_sheet['Total Debt'].dropna().iloc[-1] if not balance_sheet.empty else 0
        net = cash - debt
        
        cash_var.set(f"Cash: ${cash:,.2f}")
        debt_var.set(f"Debt: ${debt:,.2f}")
        net_var.set(f"Net: ${net:,.2f}")

    def update_margins_growth_info(stock_symbol):
        stock = yf.Ticker(stock_symbol)
        info = stock.info
        financials = stock.financials.T
        
        profit_margin_value = info.get('profitMargins', 0)
        operating_margin_value = info.get('operatingMargins', 0)
        
        quarterly_earnings = financials['Gross Profit'].iloc[-1] if not financials.empty else 0
        quarterly_revenue = financials['Total Revenue'].iloc[-1] if not financials.empty else 0
        
        profit_margin.set(f"Profit Margin: {profit_margin_value:.2%}" if profit_margin_value else "Profit Margin: N/A")
        operating_margin.set(f"Operating Margin: {operating_margin_value:.2%}" if operating_margin_value else "Operating Margin: N/A")
        quarterly_earnings_var.set(f"Quart. Earnings: ${quarterly_earnings:,.2f}" if quarterly_earnings else "Quart. Earnings: N/A")
        quarterly_revenue_var.set(f"Quart. Revenue: ${quarterly_revenue:,.2f}" if quarterly_revenue else "Quart. Revenue: N/A")

    def update_value_info(stock_symbol):
        stock = yf.Ticker(stock_symbol)
        info = stock.info
        
        market_cap.set(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")
        pe.set(f"P/E: {info.get('trailingPE', 'N/A')}")
        price_to_sales.set(f"Price to Sales: {info.get('priceToSalesTrailing12Months', 'N/A')}")
        ev_to_ebitda.set(f"EV/EBITDA: {info.get('enterpriseToEbitda', 'N/A')}")
        price_to_book.set(f"Price to Book: {info.get('priceToBook', 'N/A')}")
        free_cash_flow_yield.set(f"Free Cash Flow Yield: {info.get('freeCashflow', 'N/A')}")

    def update_quality_info(stock_symbol):
        stock = yf.Ticker(stock_symbol)
        financials = stock.financials.T
        balance_sheet = stock.balance_sheet.T
        info = stock.info
        
        score = 0
        profitability_criteria = [
            info.get('netIncome', 0) > 0,
            info.get('returnOnAssets', 0) > 0,
            info.get('operatingCashflow', 0) > 0,
            info.get('operatingCashflow', 0) > info.get('netIncome', 0)
        ]
        
        leverage_criteria = [
            balance_sheet['Total Debt'].dropna().iloc[-1] < balance_sheet['Total Debt'].dropna().iloc[-2],
            info.get('currentRatio', 0) > (balance_sheet['Total Assets'].dropna().iloc[-2] / balance_sheet['Total Liabilities Net Minority Interest'].dropna().iloc[-2]),
            info.get('sharesOutstanding', 0) <= info.get('sharesOutstanding', 0)  # Assuming no new shares were issued
        ]
        
        efficiency_criteria = [
            financials['Gross Profit'].iloc[-1] > financials['Gross Profit'].iloc[-2],
            info.get('assetTurnover', 0) > info.get('assetTurnover', 0)  # Placeholder for actual asset turnover values
        ]

        score += sum(1 for criterion in profitability_criteria if criterion)
        score += sum(1 for criterion in leverage_criteria if criterion)
        score += sum(1 for criterion in efficiency_criteria if criterion)

        quality_rating = ''
        if score >= 8:
            quality_rating = 'Superb'
        elif score >= 6:
            quality_rating = 'High'
        elif score >= 4:
            quality_rating = 'Medium'
        elif score >= 2:
            quality_rating = 'Okay'
        else:
            quality_rating = 'Low'

        piotroski.set(f"Piotroski Score: {score}")
        quality.set(f"Quality Rating: {quality_rating}")
    
    def create_styled_frame(parent):
        frame = ctk.CTkFrame(parent, fg_color="#131313")
        return frame    
    
    ## SIDE BAR CONTENT
    toggle_button = ctk.CTkButton(content_frame, text="☰", command=lambda: toggle_sidebar(sidebar_frame), bg_color='black', border_width=2, border_color="white", width=20)
    toggle_button.place(x=10, y=10)
    
    # Ticker Look Up Section
    ticker_lookup_frame = create_styled_frame(sidebar_frame)
    ticker_lookup_frame.pack(pady=2.5, fill='x')
    
    input_label = ctk.CTkLabel(ticker_lookup_frame, text="Enter Ticker Symbol:")
    input_label.pack(padx=5.5, anchor='nw')
    
    stock_input = ctk.CTkEntry(ticker_lookup_frame, textvariable=stock_symbol_var)
    stock_input.pack(padx=5.5, anchor='nw')

    update_button = ctk.CTkButton(ticker_lookup_frame, text="Update Charts", command=update_charts)
    update_button.pack(pady=5, padx=5.5, anchor='nw')

    watchlist_button = ctk.CTkButton(ticker_lookup_frame, text="Go to Watchlist", command=open_watchlist)
    watchlist_button.pack(pady=5, padx=5.5, anchor='nw')

    # Margins & Growth Section
    margins_growth_frame = create_styled_frame(sidebar_frame)
    margins_growth_frame.pack(pady=2.5, fill='x')

    ctk.CTkLabel(margins_growth_frame, text="Margins & Growth", font=('Helvetica', 12, 'bold'),padx=5.5,fg_color="transparent").pack(anchor='nw')
    profit_margin = tk.StringVar()
    operating_margin = tk.StringVar()
    quarterly_earnings_var = tk.StringVar()
    quarterly_revenue_var = tk.StringVar()

    ctk.CTkLabel(margins_growth_frame, textvariable=profit_margin,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(margins_growth_frame, textvariable=operating_margin,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(margins_growth_frame, textvariable=quarterly_earnings_var,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(margins_growth_frame, textvariable=quarterly_revenue_var,padx=5,fg_color="transparent").pack(anchor='nw')

    # Balance Section
    balance_frame = create_styled_frame(sidebar_frame)
    balance_frame.pack(pady=2.5,fill='x')

    ctk.CTkLabel(balance_frame, text="Balance", font=('Helvetica', 12, 'bold'),padx=5,fg_color="transparent").pack(anchor='nw')
    cash_var = tk.StringVar()
    debt_var = tk.StringVar()
    net_var = tk.StringVar()

    ctk.CTkLabel(balance_frame, textvariable=cash_var,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(balance_frame, textvariable=debt_var,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(balance_frame, textvariable=net_var,padx=5,fg_color="transparent").pack(anchor='nw')

    # Dividend Section
    dividend_frame = create_styled_frame(sidebar_frame)
    dividend_frame.pack(pady=2.5, fill='x')

    ctk.CTkLabel(dividend_frame, text="Dividend", font=('Helvetica', 12, 'bold'),padx=5,fg_color="transparent").pack(anchor='nw')
    dividend_yield = tk.StringVar()
    payout_ratio = tk.StringVar()
    ex_div_date = tk.StringVar()
    payout_date = tk.StringVar()

    ctk.CTkLabel(dividend_frame, textvariable=dividend_yield,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(dividend_frame, textvariable=payout_ratio,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(dividend_frame, textvariable=ex_div_date,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(dividend_frame, textvariable=payout_date,padx=5,fg_color="transparent").pack(anchor='nw')

    # Value Section
    value_frame = create_styled_frame(sidebar_frame)
    value_frame.pack(pady=2.5, fill='x')

    ctk.CTkLabel(value_frame, text="Value", font=('Helvetica', 12, 'bold'),padx=5,fg_color="transparent").pack(anchor='nw')
    market_cap = tk.StringVar()
    pe = tk.StringVar()
    price_to_sales = tk.StringVar()
    ev_to_ebitda = tk.StringVar()
    price_to_book = tk.StringVar()
    free_cash_flow_yield = tk.StringVar()

    ctk.CTkLabel(value_frame, textvariable=market_cap,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(value_frame, textvariable=pe,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(value_frame, textvariable=price_to_sales,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(value_frame, textvariable=ev_to_ebitda,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(value_frame, textvariable=price_to_book,padx=5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(value_frame, textvariable=free_cash_flow_yield,padx=5,fg_color="transparent").pack(anchor='nw')

    # Quality Section
    quality_frame = create_styled_frame(sidebar_frame)
    quality_frame.pack(pady=2.5, fill='x')

    ctk.CTkLabel(quality_frame, text="Quality", font=('Helvetica', 12, 'bold'),padx=5,fg_color="transparent").pack(anchor='nw')
    piotroski = tk.StringVar()
    quality = tk.StringVar()

    ctk.CTkLabel(quality_frame, textvariable=piotroski,padx=2.5,fg_color="transparent").pack(anchor='nw')
    ctk.CTkLabel(quality_frame, textvariable=quality,padx=5,fg_color="transparent").pack(anchor='nw')

    # Initial update of all information
    update_dividend_info(default_symbol)
    update_balance_info(default_symbol)
    update_margins_growth_info(default_symbol)
    update_value_info(default_symbol)
    update_quality_info(default_symbol)

    # Initial update of all charts
    update_charts()  # Call this to populate the charts on startup

    root.mainloop()

os.system("cls")
display_charts_with_sidebar()