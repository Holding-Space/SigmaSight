import customtkinter as ctk
import yfinance as yf

import tkinter
import json
import os

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Watchlist config file
WATCHLIST_FILE = 'watchlist_config.json'

# Initialize the watchlist config file if it doesn't exist
if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump([], f)

def load_watchlist():
    with open(WATCHLIST_FILE, 'r') as f:
        return json.load(f)

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(watchlist, f)

def add_ticker_to_watchlist(ticker, watchlist, watchlist_frame):
    stock = yf.Ticker(ticker)
    info = stock.info
    if info and ticker not in watchlist:
        watchlist.append(ticker)
        save_watchlist(watchlist)
        refresh_watchlist(watchlist_frame, watchlist)

def remove_ticker(watchlist, ticker, frame, watchlist_frame):
    watchlist.remove(ticker)
    save_watchlist(watchlist)
    frame.destroy()
    refresh_watchlist(watchlist_frame, watchlist)

def refresh_watchlist(watchlist_frame, watchlist):
    # Clear the previous content
    for widget in watchlist_frame.winfo_children():
        widget.destroy()

    # Retrieve data for all tickers at once
    if watchlist:
        tickers = ' '.join(watchlist)  # Create a space-separated string of tickers
        stocks = yf.Tickers(tickers)  # Retrieve data for all tickers
        info_dict = {ticker: stocks.tickers[ticker].info for ticker in watchlist}

        # Display each ticker's data
        for ticker in watchlist:
            info = info_dict[ticker]
            
            company_name = info.get('shortName', 'N/A')
            current_price = float(info.get('currentPrice', 'N/A'))
            previousClose = float(info.get('previousClose', 'N/A'))
            
            price_change_percent = round(((current_price - previousClose) / previousClose) * 100, 2)

            # Create a frame for each ticker with its data
            frame = ctk.CTkFrame(watchlist_frame, fg_color="#808080", height=50)
            frame.pack(pady=2.5, fill='x')

            # Add a remove button (X) to delete ticker from watchlist
            remove_button = ctk.CTkButton(frame, text="✖", width=35, text_color="#505050", fg_color="transparent", command=lambda t=ticker, f=frame: remove_ticker(watchlist, t, f, watchlist_frame))
            remove_button.place(rely=0.25, relx=0.85)
            
            # Display ticker in bold, with company name directly below it
            ticker_label = tkinter.Label(frame, text=ticker, font=("Arial", 10, "bold"), anchor='w', fg="#ffffff", background="#808080")
            ticker_label.place(x=5, y=2.5)
            
            if len(company_name) > 15:
                company_name = f"{company_name[:15]}... "
                
            company_label = tkinter.Label(frame, text=company_name, font=("Arial", 10), anchor='w', fg="#ffffff",background="#808080")
            company_label.place(x=5, y=22.5)

            # Display price and change directly to the right of the company info
            price_label = tkinter.Label(frame, text=f"${current_price}", font=("Arial", 10, "bold"), anchor='e', fg="#ffffff",background="#808080")
            price_label.place(x=125, y=2.5)

            if price_change_percent > 0:
                label_colour = "green"
            else:
                label_colour = "red"
                
            change_label = ctk.CTkLabel(frame, text=f"{price_change_percent}%", font=("Arial", 12), anchor='e', text_color ="#ffffff", fg_color=f"{label_colour}", corner_radius=4, height=25)
            change_label.place(x=130, y=22.5)

def calculate_dip_data(watchlist):
    dip_data = []
    
    tickers = ' '.join(watchlist)  # Create a space-separated string of tickers
    stocks = yf.Tickers(tickers)  # Retrieve data for all tickers
    info_dict = {ticker: stocks.tickers[ticker].info for ticker in watchlist}

    for ticker in watchlist:
        info = info_dict[ticker]
        
        current_price = info.get('currentPrice', 'N/A')
        ema_200 = info.get('twoHundredDayAverage', 'N/A')
        
        dip_percent = ((current_price - ema_200) / ema_200) * 100    
        dip_data.append((ticker, dip_percent))
            
    dip_data.sort(key=lambda x: x[1])  # Sort by dip percentage (lowest to highest)
    
    return dip_data

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

def display_dip_finder_chart(dip_data, frame):
    chart_frame = ctk.CTkFrame(frame, fg_color="black")
    chart_frame.pack(fill='both', expand=True, padx=(0, 5), pady=5)
    
    canvas = FigureCanvasTkAgg(plt.Figure(figsize=(4.5, 3.5), facecolor='black'), master=chart_frame)
    canvas.get_tk_widget().pack(padx= 2.5, pady = 2.5, fill='both', expand=True)
    
    ax = canvas.figure.add_subplot(111)
    
    # Extract ticker names and dip percentages for plotting
    tickers = [item[0] for item in dip_data]
    dip_percents = [item[1] for item in dip_data]
    
    # Plot the vertical bar chart
    bars = ax.bar(tickers, dip_percents, color=["#FF5733" if dp < 0 else "#33FF57" for dp in dip_percents])
    ax.set_title("Dip Finder (Price vs 200d EMA)", color="white")
    set_colours(ax)
    
    for bar, dip_percent in zip(bars, dip_percents):
        if dip_percent > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # Center text on the bar
                bar.get_height(),  # Position at the top of the bar
                f"{dip_percent:.2f}%",  # Format value with two decimals and percentage sign
                ha='center', va='bottom', color="white"  # Center align and set color
            )
        else:
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # Center text on the bar
                0,
                f"{dip_percent:.2f}%",
                ha='center', va='bottom', color="white"  
            )
        
    canvas.draw()

def open_watchlist():
    root = tkinter.Tk()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.title('Watchlist')
    
    root.configure(background="#23222b")
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    # Sidebar Frame for input and buttons
    sidebar_frame = ctk.CTkFrame(root, width = 500, fg_color="black")
    sidebar_frame.grid_rowconfigure(0, weight=1)
    sidebar_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
    
    main_frame = ctk.CTkFrame(root, fg_color="#23222b")
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid(row=0, column=1, sticky="nsew")

    watchlist = load_watchlist()

    # Section for adding tickers
    control_section = ctk.CTkFrame(sidebar_frame, fg_color="#131313")
    control_section.pack(pady=5, padx=5, fill='x')

    ticker_input_var = tkinter.StringVar()
    ticker_input = ctk.CTkEntry(control_section, textvariable=ticker_input_var)
    ticker_input.pack(padx=5, pady=(5,0))

    add_button = ctk.CTkButton(control_section, text="Add to Watchlist", command=lambda: add_ticker_to_watchlist(ticker_input_var.get(), watchlist, watchlist_section))
    add_button.pack(padx=5, pady=5)

    close_button = ctk.CTkButton(control_section, text="Close Page", command=root.destroy)
    close_button.pack(padx=5, pady=(0, 5))

    watchlist_section = ctk.CTkScrollableFrame(sidebar_frame, fg_color="#131313")
    watchlist_section.pack(padx=5, pady =5, fill='both', expand=True)
    
    # Display watchlist data
    refresh_watchlist(watchlist_section, watchlist)

    # Dip Finder chart
    dip_data = calculate_dip_data(watchlist)
    display_dip_finder_chart(dip_data, main_frame)

    root.mainloop()