import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import xml.etree.ElementTree as ET

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


import os
from pathlib import Path

def load_minsky_file(model, filepath):
    print(f"Attempting to load: {filepath}")
    print(f"File exists: {os.path.exists(filepath)}")
    print(f"File permissions: {oct(os.stat(filepath).st_mode)}")

    try:
        # Debug file header
        with open(filepath, 'rb') as f:
            print(f"First 100 bytes: {f.read(100)}")  # Check file magic number

        # Parse and process XML
        tree = ET.parse(filepath)
        root = tree.getroot()

        # === Extract variables ===
        stock_values = {}
        flow_equations = {}

        for var in root.findall(".//variable"):
            name = var.attrib["name"]
            var_type = var.attrib["type"]
            if var_type == "stock":
                init_val = float(var.attrib.get("init", 0.0))
                stock_values[name] = init_val
            elif var_type == "flow":
                equation = var.attrib.get("equation", "0.0")
                flow_equations[name] = equation

        # Add stocks
        for name, val in stock_values.items():
            model.add_stock(name, val)

        # Add flows (danger: using eval!)
        for name, expr in flow_equations.items():
            # Safe wrapper for eval using only stock values
            def make_flow_fn(equation_str):
                return lambda t, s: eval(equation_str, {}, s)
            model.add_flow(name, make_flow_fn(expr))

        # === Extract Godley table ===
        for table in root.findall(".//godleyTable"):
            for row in table.findall("row"):
                account = row.attrib.get("account")
                for cell in row.findall("cell"):
                    op = cell.attrib.get("op")
                    flow = (cell.text or "").strip()
                    if flow:
                        sign = +1 if op == "inflow" else -1
                        model.add_godley_entry(account, flow, sign)

        return model

    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise



from pathlib import Path
import re

def sanitize_xml(filepath):
    """Remove invalid XML characters"""
    with open(filepath, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')

    # Remove non-XML-compatible chars
    clean_content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)

    clean_path = Path(filepath).with_suffix('.clean.mky')
    with open(clean_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    return clean_path

# Usage:
# clean_file = sanitize_xml("/workspaces/SFC_economic/minsky/Mice.mky")
# tree = ET.parse(clean_file)

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


