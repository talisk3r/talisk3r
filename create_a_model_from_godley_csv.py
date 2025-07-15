from project.godley_model import SFCModel, load_godley_table_from_csv, plot_history
import pandas as pd

# Step 1: Create Godley table CSV
godley_data = {
    "Wages":       [ 1, -1],
    "Consumption": [-1,  1],
}
accounts = ["Household_Deposits", "Firm_Deposits"]
df = pd.DataFrame(godley_data, index=accounts)
csv_path = "godley_table.csv"
df.to_csv(csv_path)

# Step 2: Initialize model
model = SFCModel(dt=1.0)
model.add_stock("Household_Deposits", 1000)
model.add_stock("Firm_Deposits", 0)

model.add_flow("Wages", lambda t, s: 100)
model.add_flow("Consumption", lambda t, s: 0.8 * s["Household_Deposits"])

load_godley_table_from_csv(model, csv_path)

# Step 3: Run simulation
history = model.run(T=20, return_history=True)

# Print result
for t, h in enumerate(history):
    print(f"t={t}: {h}")


# Step 4: Convert history to DataFrame for plotting
df_history = pd.DataFrame(history)
df_history.index.name = "Time"

# plot_history(file) # TODO
# Step 5: Plot
# import matplotlib.pyplot as plt
# df_history.plot(title="Stock Levels Over Time", marker='o')
# plt.xlabel("Time")
# plt.ylabel("Stock Value")
# plt.grid(True)
# plt.tight_layout()
# plt.show() # FIXME