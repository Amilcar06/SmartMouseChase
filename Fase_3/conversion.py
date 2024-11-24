import os
import pickle
import pandas as pd

try:
    if os.path.getsize("q_table.pkl") > 0:
        with open("q_table.pkl", "rb") as f:
            data = pickle.load(f)
            df = pd.DataFrame(data)
            df.to_csv('datos.csv', index=False)
    else:
        print("Pickle file is empty. No data to load.")
except (EOFError, pickle.UnpicklingError) as e:
    print(f"Error loading data: {e}")