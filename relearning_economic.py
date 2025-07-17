from project.SFCModel import SFCModel


# model = SFCModel(dt=1.0)
model = SFCModel()

# Assumptions related to flows and connects
# The flow functions are already defined (either via .add_flow() or .connect()).
# All flow values apply linearly over the time step dt.
# Stock updates respect flow directions:
# from_stock: subtracts flow
# to_stock: adds flow
# Flows with None as source or destination are treated as external inflows or outflows.


# # Connect flows
# model.connect(None, "Sucept_pop", "Births", "0.01 * s['Total_pop']")
# model.connect("Total_pop", None, "Deaths", "0.005 * s['Total_pop']")
# model.connect("Sucept_pop", "Expose_pop", "Exposure", "0.2 * s['Sucept_pop']")
# model.connect("Expose_pop", "Infected_pop", "Infection", "0.1 * s['Expose_pop']")
# model.connect("Infected_pop", "Recovered_pop", "Recovery", "0.05 * s['Infected_pop']")


# SIR=Suceptible Infectd Recoverted

# column are stocks VAriable
# rows are for flows


# ___________________| Total_pop | Sucept_pop  | Expose_pop | Infected_pop | Recoverd_pop |
# Initial contitions |  10000    |  999        |            |        1     |        0     |
# Births             |  Births   |  Births     |            |              |              |
# Deaths             |-Deaths    |             |            |    -Deaths   |              |
# Suceptibility      |           |  s          |            |              |        -s    |
# Exposure           |           | -e          |    e       |              |              |
# Infection          |           |             |   -i       |        i     |              |
# Recovery           |           |             |            |       -r     |       r      |

# Total_pop * Birth_Rate = Births
# (Infected_pop * Death_Rate)/Death_Time_constant = Deaths
# Recovered_pop * Immunity_Time_constant = Suceptibility
# (Total_pop * Sucept_pop) / (Infected_pop * Expose_time_constant) = Exposure
# Exposed_pop / Incubation_Time_constant = Infection
# (1 - Death_Rate) * Infected_pop / Recovery_Time_constant = Recovery

model.add_stock("Total_pop", 1000, "ASSET")     # Unit: person
model.add_stock("Sucept_pop", 999, "LIABILITY") # Unit: person
model.add_stock("Exposed_pop", 0, "LIABILITY")   # Unit: person
model.add_stock("Infected_pop", 1, "LIABILITY") # Unit: person
model.add_stock("Recovered_pop", 0, "EQUITY")   # Unit: person

model.add_parameter("Expose_Time_constant", 1, 1, 21)# Unit: Day
model.add_parameter("Incubation_Time_constant", 1, 1 , 14)# Unit: Day
model.add_parameter("Recovery_Time_constant", 1, 1, 7) # Unit: Day
model.add_parameter("Birth_Rate", 0.001, 0, 1) #  Day^-1
model.add_parameter("Death_Time_constant", 1, 1, 100) # Unit: Day
model.add_parameter("Death_Rate", 0.001, 0, 1) # Unit: NA
model.add_parameter("Immunity_Time_constant", 180, 1, 365) # Unit: Day

model.connect("Births", [("Total_pop", 1), ("Sucept_pop", 1)], "Total_pop * Birth_Rate")
model.connect("Deaths", [("Total_pop", -1), ("Infected_pop", -1)], "(Infected_pop * Death_Rate) / Death_Time_constant")
model.connect("Suceptibility", [("Recovered_pop", -1), ("Sucept_pop", 1)], "Recovered_pop / Immunity_Time_constant")
model.connect("Exposure", [("Sucept_pop", -1), ("Exposed_pop", 1)], "(Total_pop * Sucept_pop) / (Infected_pop * Expose_Time_constant + 1e-6)")
model.connect("Infection", [("Exposed_pop", -1), ("Infected_pop", 1)], "Exposed_pop / Incubation_Time_constant")
model.connect("Recovery", [("Infected_pop", -1), ("Recovered_pop", 1)], "(1 - Death_Rate) * Infected_pop / Recovery_Time_constant")

# Note: I added + 1e-6 to the denominator of "Exposure" to prevent divide-by-zero when Infected_pop is zero.

model.print_godley_table()

# Simulate
history = model.simulate(days=100, dt=1.0)

# # Plot and save
# import matplotlib.pyplot as plt

# filename = "my_plot.png"

# stock_names = [k for k in history[0] if k != "day"]
# time = [row["day"] for row in history]

# plt.figure(figsize=(10, 6))
# for stock in stock_names:
#     values = [row[stock] for row in history]
#     plt.plot(time, values, label=stock)

# plt.xlabel("Day")
# plt.ylabel("Stock Value")
# plt.title("SFC Model Stocks Over Time")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.savefig(filename)
# print(f"Saved plot to {filename}")

################################################################################
#TODO Units, Enable slider (min,max)
#TODO check ALE is 0.

# Simulation parameter
# Time_unit
# Min_step_size
# Max_step_size
# No.steps_per_iteration
# Start_time
# Run_until
# Absolute_err
# Relative_err
# Solver_order (1,2 4)
# Enable_implicit_solver