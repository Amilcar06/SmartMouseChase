import matplotlib.pyplot as plt

# Datos
iteraciones = [1, 2, 3, 4, 5]
prueba1 = [21.95, 15.36, 11.75, 7.14, 4.94]
prueba2 = [24.16, 6.5, 6.31, 0, 0]
prueba3 = [11.94, 10.18, 4.57, 1.34, 0]
prueba4 = [4.89, 2.21, 1.60, 1.48, 1.52]

# Crear la gráfica
plt.figure(figsize=(8, 6))
plt.plot(iteraciones, prueba1, label='Prueba 1', marker='o')
plt.plot(iteraciones, prueba2, label='Prueba 2', marker='o')
plt.plot(iteraciones, prueba3, label='Prueba 3', marker='o')
plt.plot(iteraciones, prueba4, label='Prueba 4', marker='o')

# Etiquetas y título
plt.xlabel('Iteraciones')
plt.ylabel('Valores')
plt.title('Resultados de las Pruebas')
plt.legend()
plt.grid(True)

# Mostrar la gráfica
plt.show()
