import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 12), padding=6)
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12))

        title = ttk.Label(root, text="Currency Converter", font=("Helvetica", 18, "bold"), background="#f0f0f0")
        title.pack(pady=10)

        frame = ttk.Frame(root)
        frame.pack(pady=10, padx=20, fill='x')

        ttk.Label(frame, text="Amount:").grid(row=0, column=0, sticky='w')
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=0, column=1, pady=5, sticky='ew')

        ttk.Label(frame, text="From:").grid(row=1, column=0, sticky='w')
        self.from_currency = tk.StringVar()
        self.from_combo = ttk.Combobox(frame, textvariable=self.from_currency, state='readonly')
        self.from_combo.grid(row=1, column=1, pady=5, sticky='ew')

        ttk.Label(frame, text="To:").grid(row=2, column=0, sticky='w')
        self.to_currency = tk.StringVar()
        self.to_combo = ttk.Combobox(frame, textvariable=self.to_currency, state='readonly')
        self.to_combo.grid(row=2, column=1, pady=5, sticky='ew')

        self.convert_btn = ttk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_btn.pack(pady=10)

        self.result_label = ttk.Label(root, text="", font=("Helvetica", 14, "bold"), background="#f0f0f0")
        self.result_label.pack(pady=10)

        frame.columnconfigure(1, weight=1)

        # Only these currencies
        self.currencies = ['INR', 'USD', 'EUR', 'JPY']
        self.rates = {}
        self.load_currencies()

    def load_currencies(self):
        try:
            # Fetch rates relative to USD
            url = "https://open.er-api.com/v6/latest/USD"
            response = requests.get(url)
            data = response.json()

            if data['result'] == 'success':
                all_rates = data['rates']
                # Filter only required currencies
                self.rates = {cur: all_rates[cur] for cur in self.currencies}
                self.from_combo['values'] = self.currencies
                self.to_combo['values'] = self.currencies

                self.from_combo.set('USD')
                self.to_combo.set('INR')
            else:
                messagebox.showerror("Error", "Failed to load currency data.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching currency data:\n{e}")

    def convert_currency(self):
        amount = self.amount_var.get()
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid positive number for amount.")
            return

        if from_curr not in self.rates or to_curr not in self.rates:
            messagebox.showerror("Invalid currency", "Please select valid currencies.")
            return

        try:
            # Convert amount to USD first, then to target currency
            amount_in_usd = amount / self.rates[from_curr]
            converted_amount = amount_in_usd * self.rates[to_curr]
            self.result_label.config(text=f"{amount:.2f} {from_curr} = {converted_amount:.2f} {to_curr}")
        except Exception as e:
            messagebox.showerror("Conversion error", f"Error during conversion:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
