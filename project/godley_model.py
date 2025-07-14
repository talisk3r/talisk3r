import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# --- System Dynamics Model Class ---

class SFCModel:
    def __init__(self, dt=1.0):
        self.dt = dt  # time step (e.g. 1 month, 1 year)
        self.stocks = {}  # e.g. {'Money': 1000}
        self.flows = {}   # e.g. {'Income': lambda t, s: 0.1 * s['Capital']}
        self.godley_table = defaultdict(lambda: defaultdict(float))  # accounts x flows

    def add_stock(self, name, initial_value):
        self.stocks[name] = initial_value

    def add_flow(self, name, equation):
        self.flows[name] = equation  # equation is a function of (t, stocks)

    def add_godley_entry(self, account, flow, amount):
        self.godley_table[account][flow] += amount

    def step(self, t):
        # Evaluate all flows
        flow_values = {name: eq(t, self.stocks) for name, eq in self.flows.items()}

        # Check double-entry balance (optional)
        for flow in self.flows:
            balance = sum(self.godley_table[acc][flow] for acc in self.godley_table)
            if not np.isclose(balance, 0.0):
                raise ValueError(f"Flow '{flow}' is unbalanced in Godley table: {balance}")

        # Update stocks using flows and Godley table
        new_stocks = self.stocks.copy()
        for account in self.stocks:
            delta = 0.0
            for flow, amount in self.godley_table[account].items():
                delta += amount * flow_values[flow]
            new_stocks[account] += self.dt * delta
        self.stocks = new_stocks

    def run(self, T, return_history=False):
        history = []
        for t in np.arange(0, T, self.dt):
            if return_history:
                history.append(self.stocks.copy())
            self.step(t)
        return history if return_history else None

# --- Helper Functions ---

def validate_godley_balance(df):
    for flow in df.columns:
        total = df[flow].sum()
        if not np.isclose(total, 0.0):
            raise ValueError(f"Flow '{flow}' is unbalanced: sum = {total}")

def load_godley_table_from_csv(model, path):
    df = pd.read_csv(path, index_col=0)
    validate_godley_balance(df)
    for account in df.index:
        for flow in df.columns:
            value = df.loc[account, flow]
            if pd.notna(value) and value != 0:
                model.add_godley_entry(account, flow, float(value))


def plot_history(self, history, show=True, filename=None):
    """Plot model history.

    Args:
        history (list of dict): Output from run(..., return_history=True)
        show (bool): Whether to show the plot (calls plt.show()).
        filename (str): If given, saves the plot to this file.
    """
    df = pd.DataFrame(history)
    df.plot()
    plt.xlabel("Time")
    plt.ylabel("Stock Values")
    plt.title("SFC Model Simulation")

    if filename:
        plt.savefig(filename, dpi=150)
        print(f"Saved plot to {filename}")
    if show:
        plt.show()
    else:
        plt.close()


