from project.godley_model import SFCModel, plot_history


model = SFCModel(dt=1.0)

# Stocks
model.add_stock("Household_Deposits", 1000)
model.add_stock("Firm_Deposits", 0)

# Flows
model.add_flow("Wages", lambda t, s: 100)
model.add_flow("Consumption", lambda t, s: 0.8 * s["Household_Deposits"])

# Godley Table entries
model.add_godley_entry("Household_Deposits", "Wages", +1)
model.add_godley_entry("Firm_Deposits",     "Wages", -1)

model.add_godley_entry("Household_Deposits", "Consumption", -1)
model.add_godley_entry("Firm_Deposits",     "Consumption", +1)

# Simulate 10 time steps
history = model.run(T=10, return_history=True)

# Print result
for t, h in enumerate(history):
    print(f"t={t}: {h}")


    # plot_history(file) # TODO


