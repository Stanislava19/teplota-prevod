"""Zadanie: vlastná aplikácia v Pythone (pole hodnôt, výpočet, graf, GUI).

Vzorec: prevod teploty zo stupňov Celzia na stupne Fahrenheita
        F = C * 9 / 5 + 32
(ak máte v zadaní z Mendixu iný vzorec, zmeňte iba funkciu calculate()).
"""
import random
import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ---------- 1. Pole vstupných hodnôt ----------
def generate_values(count=50, low=-10.0, high=40.0):
    """Vygeneruje pole náhodných teplôt (min. 50 hodnôt)."""
    return [round(random.uniform(low, high), 1) for _ in range(count)]


# ---------- 2. Práca s poľom (min. 2 operácie) ----------
def sort_values(values):
    """Zoradí hodnoty od najmenšej po najväčšiu."""
    return sorted(values)


def get_min(values):
    return min(values)


def get_max(values):
    return max(values)


def get_average(values):
    return sum(values) / len(values)


# ---------- 3. Výpočet podľa vzorca ----------
def calculate(x):
    """°C -> °F"""
    return x * 9 / 5 + 32


# ---------- 4. GUI + graf ----------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Teploty: °C a °F")
        self.values = generate_values()

        # ovládacie prvky
        top = tk.Frame(root)
        top.pack(pady=8, padx=8, fill="x")

        tk.Label(top, text="Zadajte teplotu v °C:").pack(side="left")
        self.entry = tk.Entry(top, width=10)
        self.entry.pack(side="left", padx=5)
        tk.Button(top, text="Vypočítať", command=self.on_calculate).pack(side="left")

        self.result_label = tk.Label(top, text="Výsledok: -", font=("Arial", 11, "bold"))
        self.result_label.pack(side="left", padx=15)

        buttons = tk.Frame(root)
        buttons.pack(pady=4)
        tk.Button(buttons, text="Nové hodnoty", command=self.on_new).pack(side="left", padx=4)
        tk.Button(buttons, text="Zoradiť", command=self.on_sort).pack(side="left", padx=4)

        self.stats_label = tk.Label(root, text="")
        self.stats_label.pack()

        # graf
        self.figure = Figure(figsize=(8, 4.5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        """Prekreslí graf (pôvodné aj vypočítané hodnoty) a štatistiky."""
        computed = [calculate(v) for v in self.values]
        idx = range(1, len(self.values) + 1)

        self.ax.clear()
        self.ax.plot(idx, self.values, marker="o", markersize=3, label="Pôvodné (°C)")
        self.ax.plot(idx, computed, marker="s", markersize=3, label="Vypočítané (°F)")
        self.ax.set_xlabel("Poradie merania")
        self.ax.set_ylabel("Teplota")
        self.ax.set_title("Porovnanie pôvodných a vypočítaných hodnôt")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

        self.stats_label.config(
            text=f"Min: {get_min(self.values)} °C   "
                 f"Max: {get_max(self.values)} °C   "
                 f"Priemer: {get_average(self.values):.2f} °C"
        )

    def on_new(self):
        self.values = generate_values()
        self.refresh()

    def on_sort(self):
        self.values = sort_values(self.values)
        self.refresh()

    def on_calculate(self):
        text = self.entry.get().replace(",", ".").strip()
        try:
            x = float(text)
        except ValueError:
            messagebox.showerror("Chyba", "Zadajte platné číslo.")
            return
        self.result_label.config(text=f"Výsledok: {calculate(x):.2f} °F")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
