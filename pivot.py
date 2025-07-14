import pandas as pd
df = pd.DataFrame(history)
summary = pd.pivot_table(df, values="Firm_Deposits", aggfunc="mean")