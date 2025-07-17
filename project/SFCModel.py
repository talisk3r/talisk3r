from collections import defaultdict
from tabulate import tabulate

class SFCModel:
    def __init__(self):
        self.stocks = {}         # stock name -> value
        self.stock_types = {}    # name -> ASSET, LIABILITY, EQUITY
        self.flows = {}          # flow name -> expression string
        self.connections = []    # list of (flow_name, stock_name, sign)
        self.parameters = {}     # parameter name -> value
        self.parameters_min = {}
        self.parameters_max = {}

    def add_stock(self, name, initial_value=0, account_type="ASSET"):
        self.stocks[name] = float(initial_value)
        self.stock_types[name] = account_type.upper()

    def add_parameter(self, name, value, min ,max):
        self.parameters[name] = float(value)
        self.parameters_min[name] = min
        self.parameters_max[name] = max

    def connect(self, flow_name, legs, expr):
        """legs: list of (stock_name, sign), expr: string expression"""
        self.flows[flow_name] = expr
        for stock, sign in legs:
            self.connections.append((flow_name, stock, sign))

    def evaluate_flow(self, expr):
        env = {}
        env.update(self.stocks)
        env.update(self.parameters)
        return eval(expr, {}, env)

    def compute_derivatives(self):
        """Return a dictionary of stock derivatives."""
        d_stocks = {name: 0.0 for name in self.stocks}
        for flow_name, stock, sign in self.connections:
            value = self.evaluate_flow(self.flows[flow_name])
            d_stocks[stock] += sign * value
        return d_stocks

    def step(self, dt):
        """Perform a forward Euler integration step."""
        d_stocks = self.compute_derivatives()
        for stock, delta in d_stocks.items():
            self.stocks[stock] += dt * delta

    def simulate(self, days=100, dt=1.0):
        """
        Simulate the model over a given number of days using Euler integration.
        Returns a list of dicts with stock values at each step.
        """
        history = []

        for step in range(days):
            snapshot = {"day": step * dt}
            snapshot.update({k: v for k, v in self.stocks.items()})
            history.append(snapshot)
            self.step(dt)

        return history

    def print_godley_table(self):
        stock_names = list(self.stocks.keys())
        table = []
        row_labels = []

        # Merge all effects by flow_name into a row
        flow_map = defaultdict(lambda: [""] * len(stock_names))
        for flow_name, stock, sign in self.connections:
            idx = stock_names.index(stock)
            prefix = "" if sign == 1 else "-"
            flow_map[flow_name][idx] = f"{prefix}{flow_name}"

        # Add initial conditions
        init_row = [str(int(self.stocks.get(name, 0))) for name in stock_names]
        table.append(init_row)
        row_labels.append("Initial Conditions")

        for flow_name, row in flow_map.items():
            table.append(row)
            row_labels.append(flow_name)

        print(tabulate(table, headers=[""] + stock_names, showindex=row_labels, tablefmt="grid"))
