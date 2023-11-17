import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk


class CurrencyConverter:
    def __init__(self, base_currency='USD'):
        self.base_currency = base_currency
        self.exchange_rates = self._get_exchange_rates()

    def _get_exchange_rates(self):
        url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
        data = requests.get(url).json()
        return {entry['cc']: entry['rate'] for entry in data} if data else {}

    def convert_to_usd(self, amount, currency):
        if currency == 'UAH':
            return amount / self.exchange_rates.get('USD', 1)
        return amount / self.exchange_rates.get(currency, 1)


class CurrencyConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Currency:").grid(row=1, column=0, padx=10, pady=10)
        self.currency_combobox = ttk.Combobox(root, values=['USD', 'UAH', 'EUR', 'GBP'])
        self.currency_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.currency_combobox.set('USD')

        tk.Button(root, text="Convert", command=self.convert_currency).grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def convert_currency(self):
        try:
            amount, currency = float(self.amount_entry.get()), self.currency_combobox.get().upper()
            converter = CurrencyConverter()
            converted_amount = converter.convert_to_usd(amount, currency)
            self.result_label.config(text=f"{amount} {currency} is approximately {converted_amount:.2f} USD")
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterGUI(root)
    root.mainloop()
