import tkinter as tk
from tkinter import ttk, messagebox

# Constants
BASE_FEE_RATE = 0.0001  # 0.01%
HIGHER_FEE_RATE = 0.0001  # 0.01%
MIN_FEE = 5  # Minimum transaction fee
FEE_THRESHOLD = 5  # Fee threshold

def calculate_fee(amount):
    base_fee = amount * BASE_FEE_RATE
    if base_fee > FEE_THRESHOLD:
        return amount * HIGHER_FEE_RATE
    else:
        return MIN_FEE

def calculate_profit(buy_price, sell_price, shares):
    buy_amount = buy_price * shares
    sell_amount = sell_price * shares
    buy_fee = calculate_fee(buy_amount)
    sell_fee = calculate_fee(sell_amount)
    total_fee = buy_fee + sell_fee
    profit = sell_amount - buy_amount - total_fee
    return profit

def calculate_final_cost(current_shares, current_cost, new_shares, new_cost, sell_shares, sell_price):
    total_cost = current_shares * current_cost + new_shares * new_cost
    sell_amount = sell_shares * sell_price
    sell_fee = calculate_fee(sell_amount)
    total_cost -= sell_amount - sell_fee  # Subtracting sell amount and adding sell fee
    total_shares = current_shares + new_shares - sell_shares
    return total_cost / total_shares if total_shares > 0 else 0

def calculate_initial_cost(current_shares, current_cost, new_shares, new_cost):
    current_total = current_shares * current_cost
    new_total = new_shares * new_cost
    new_fee = calculate_fee(new_total)
    total_cost = current_total + new_total + new_fee
    total_shares = current_shares + new_shares
    return total_cost / total_shares

class StockTradingAnalysis:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Trading Analysis")
        self.master.geometry("1200x1200")

        self.create_widgets()
        self.current_shares_entry.focus_set()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Fee Rate Information Frame
        fee_frame = ttk.LabelFrame(main_frame, text="Fee Rate Information", padding="10")
        fee_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        ttk.Label(fee_frame, text=f"Base Fee Rate: {BASE_FEE_RATE:.6f}").grid(column=0, row=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(fee_frame, text=f"Higher Fee Rate: {HIGHER_FEE_RATE:.6f}").grid(column=1, row=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(fee_frame, text=f"Minimum Fee: {MIN_FEE}").grid(column=2, row=0, sticky=tk.W, padx=5, pady=2)

        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.current_shares = tk.StringVar()
        self.current_cost = tk.StringVar()
        self.new_shares = tk.StringVar()
        self.buy_price = tk.StringVar()

        ttk.Label(input_frame, text="Current number of shares:").grid(column=0, row=0, sticky=tk.W)
        self.current_shares_entry = ttk.Entry(input_frame, width=20, textvariable=self.current_shares)
        self.current_shares_entry.grid(column=1, row=0)
        self.current_shares_entry.bind("<Return>", lambda e: self.current_cost_entry.focus_set())

        ttk.Label(input_frame, text="Current cost per share:").grid(column=0, row=1, sticky=tk.W)
        self.current_cost_entry = ttk.Entry(input_frame, width=20, textvariable=self.current_cost)
        self.current_cost_entry.grid(column=1, row=1)
        self.current_cost_entry.bind("<Return>", lambda e: self.new_shares_entry.focus_set())

        ttk.Label(input_frame, text="Number of shares to buy:").grid(column=0, row=2, sticky=tk.W)
        self.new_shares_entry = ttk.Entry(input_frame, width=20, textvariable=self.new_shares)
        self.new_shares_entry.grid(column=1, row=2)
        self.new_shares_entry.bind("<Return>", lambda e: self.buy_price_entry.focus_set())

        ttk.Label(input_frame, text="Buying price:").grid(column=0, row=3, sticky=tk.W)
        self.buy_price_entry = ttk.Entry(input_frame, width=20, textvariable=self.buy_price)
        self.buy_price_entry.grid(column=1, row=3)
        self.buy_price_entry.bind("<Return>", lambda e: self.calculate())

        ttk.Button(input_frame, text="Calculate", command=self.calculate).grid(column=1, row=4, pady=10)

        for child in input_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Results Frame
        self.results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        self.results_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.initial_cost_label = ttk.Label(self.results_frame, text="")
        self.initial_cost_label.grid(column=0, row=0, sticky=tk.W)

        self.tree = ttk.Treeview(self.results_frame, columns=('Increase (%)', 'Sell Price', 'Profit', 'Final Cost'), show='headings', height=20)
        self.tree.grid(column=0, row=1, sticky="nsew")

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')

        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(column=1, row=1, sticky='ns')
        self.tree.configure(yscroll=scrollbar.set)

        # Configure grid weights
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

    def calculate(self):
        try:
            current_shares = int(self.current_shares.get())
            current_cost = float(self.current_cost.get())
            new_shares = int(self.new_shares.get())
            buy_price = float(self.buy_price.get())

            if current_shares < 0 or current_cost < 0 or new_shares < 0 or buy_price < 0:
                raise ValueError("Input cannot be negative")

            self.show_results(current_shares, current_cost, new_shares, buy_price)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def show_results(self, current_shares, current_cost, new_shares, buy_price):
        initial_cost = calculate_initial_cost(current_shares, current_cost, new_shares, buy_price)
        self.initial_cost_label.config(text=f"Initial cost after this purchase: {initial_cost:.4f} per share")

        results = []
        zero_percent_iid = None
        for i in range(-20, 26):  # 0.2% to 5% increase
            sell_price = buy_price * (1 + i * 0.002)
            profit = calculate_profit(buy_price, sell_price, new_shares)
            final_cost = calculate_final_cost(current_shares, current_cost, new_shares, buy_price, new_shares,
                                              sell_price)
            results.append({
                'Increase (%)': round(i * 0.2, 1),
                'Sell Price': f"{sell_price:.4f}",
                'Profit': round(profit, 2),
                'Final Cost': f"{final_cost:.4f}"
            })

        self.tree.delete(*self.tree.get_children())
        for row in results:
            values = list(row.values())
            if float(row['Final Cost']) < initial_cost:
                iid = self.tree.insert('', 'end', values=values, tags=('red',))
            else:
                iid = self.tree.insert('', 'end', values=values, tags=('green',))

            if row['Increase (%)'] == 0.0:
                zero_percent_iid = iid

        self.tree.tag_configure('red', background='#ffcccb')
        self.tree.tag_configure('green', background='#90ee90')

        if zero_percent_iid:
            self.tree.focus(zero_percent_iid)
            self.tree.selection_set(zero_percent_iid)
            self.tree.see(zero_percent_iid)
def main():
    root = tk.Tk()
    app = StockTradingAnalysis(root)
    root.mainloop()

if __name__ == "__main__":
    main()