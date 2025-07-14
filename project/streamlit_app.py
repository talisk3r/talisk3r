import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from godley_model import SFCModel, load_godley_table_from_csv

st.title("📊 RAVEL-style System Dynamics Model")

# Sidebar for settings
st.sidebar.header("Simulation Settings")
T = st.sidebar.slider("Simulation duration (steps)", 5, 100, 20)
initial_household = st.sidebar.number_input("Initial Household Deposits", value=1000.0)
initial_firm = st.sidebar.number_input("Initial Firm Deposits", value=0.0)


# File upload
uploaded_file = st.file_uploader("Upload a Godley Table CSV", type="csv")

if uploaded_file is not None:
    try:
        st.subheader("Godley Table")
        df_godley = pd.read_csv(uploaded_file, index_col=0)
        st.dataframe(df_godley)

        # Reset file pointer
        uploaded_file.seek(0)

        # Build model
        model = SFCModel(dt=1.0)
        model.add_stock("Household_Deposits", initial_household)
        model.add_stock("Firm_Deposits", initial_firm)
        model.add_flow("Wages", lambda t, s: 100)
        model.add_flow("Consumption", lambda t, s: 0.8 * s["Household_Deposits"])
        load_godley_table_from_csv(model, uploaded_file)

        # Run model
        history = model.run(T=T, return_history=True)
        df_hist = pd.DataFrame(history)

        st.subheader("Simulation Results")
        st.line_chart(df_hist)

        # Download option
        csv_download = df_hist.to_csv(index=True).encode("utf-8")
        st.download_button("Download CSV", csv_download, file_name="simulation_output.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a valid Godley table CSV.")