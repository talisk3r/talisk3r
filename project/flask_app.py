from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from godley_model import SFCModel, load_godley_table_from_csv

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["godley_csv"]
        if file:
            df = pd.read_csv(file, index_col=0)

            # Setup model
            model = SFCModel(dt=1.0)
            model.add_stock("Household_Deposits", 1000)
            model.add_stock("Firm_Deposits", 0)
            model.add_flow("Wages", lambda t, s: 100)
            model.add_flow("Consumption", lambda t, s: 0.8 * s["Household_Deposits"])

            df.to_csv("uploaded.csv")  # optional: save uploaded file
            load_godley_table_from_csv(model, "uploaded.csv")
            history = model.run(T=20, return_history=True)
            df_hist = pd.DataFrame(history)

            # Create plot
            fig, ax = plt.subplots()
            df_hist.plot(ax=ax)
            ax.set_title("Stock Over Time")
            ax.set_xlabel("Time")
            ax.grid(True)

            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            return send_file(buf, mimetype="image/png")

    return render_template("index.html")