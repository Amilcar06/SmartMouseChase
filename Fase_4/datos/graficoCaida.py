import matplotlib.pyplot as plt

# Leer los datos del archivo registro.txt
with open('registroEpsilon.txt', 'r') as archivo:
    datos = archivo.read()

# Procesar la cadena para extraer los números
epsilon = [float(dato.strip().rstrip(',')) for dato in datos.split(',')]

# Crear el gráfico
plt.plot(epsilon)
plt.xlabel('Iteración')
plt.ylabel('Epsilon')
plt.title('Caída de epsilon')
plt.show()