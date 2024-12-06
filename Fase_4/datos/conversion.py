import os
import pickle
import pandas as pd

# Define las acciones en el mismo orden que en tu clase
acciones = ["Derecha", "Abajo", "Izquierda", "Arriba"]

try:
    # Verifica si el archivo existe y tiene contenido
    if os.path.exists("../q_table.pkl") and os.path.getsize("../q_table.pkl") > 0:
        with open("../q_table.pkl", "rb") as f:
            q_table = pickle.load(f)

        # Convierte la tabla Q a un formato tabular
        rows = []
        for estado, q_valores in q_table.items():
            for i, q_valor in enumerate(q_valores):
                rows.append({
                    "Estado": estado,
                    "Acción": acciones[i],
                    "Q-valor": q_valor
                })

        # Crea un DataFrame y guárdalo como CSV
        df = pd.DataFrame(rows)
        df.to_csv("datosTablaQ.csv", index=False)
        print("Tabla Q guardada en formato tabular en 'q_table_tabular.csv'.")
    else:
        print("El archivo 'q_table.pkl' no existe o está vacío.")
except (EOFError, pickle.UnpicklingError) as e:
    print(f"Error al cargar los datos: {e}")
