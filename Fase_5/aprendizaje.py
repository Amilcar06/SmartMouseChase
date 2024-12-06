import pickle
import random

class Aprendizaje:
    def __init__(self, laberinto, pos_queso, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.99):
        self.laberinto = laberinto
        self.pos_queso = pos_queso
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = {}
        self.acciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Derecha, Abajo, Izquierda, Arriba

        # Cargar la tabla Q si existe
        self.cargar_q_table()

    def guardar_q_table(self):
        with open("q_table.pkl", "wb") as f:
            pickle.dump(self.q_table, f)

    def cargar_q_table(self):
        try:
            with open("q_table.pkl", "rb") as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print("No se encontró la tabla Q, comenzando desde cero.")

    def obtener_estado(self, pos):
        return tuple(pos)

    def seleccionar_accion(self, estado):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.acciones)
        else:
            q_valores = self.q_table.get(estado, [0, 0, 0, 0])
            max_q = max(q_valores)
            mejores_acciones = [self.acciones[i] for i, q in enumerate(q_valores) if q == max_q]
            return random.choice(mejores_acciones)

    def actualizar_q_valor(self, estado, accion, recompensa, siguiente_estado):
        if estado not in self.q_table:
            self.q_table[estado] = [0, 0, 0, 0]
        accion_indice = self.acciones.index(accion)
        q_actual = self.q_table[estado][accion_indice]
        max_q_siguiente = max(self.q_table.get(siguiente_estado, [0, 0, 0, 0]))
        nuevo_q = q_actual + self.alpha * (recompensa + self.gamma * max_q_siguiente - q_actual)
        self.q_table[estado][accion_indice] = nuevo_q

        # Guardamos la ecuación de Bellman en un archivo
        with open("datos/bellman_ecuaciones.txt", "a") as log:
            log.write(f"Ecuación de Bellman:\n")
            log.write(
                f"Q({estado}, {accion}) = {q_actual} + {self.alpha} * ({recompensa} + {self.gamma} * {max_q_siguiente} - {q_actual})\n")
            log.write(f"Nuevo Q({estado}, {accion}) = {nuevo_q}\n\n")

    def registrar_movimientos(self, estado, accion, nueva_pos, recompensa, epsilon):
        with open("datos/registroMovimiento.txt", "a") as log:
            log.write(f"Estado: {estado}, Acción: {accion}, Nueva posición: {nueva_pos}, Recompensa: {recompensa}, Caida Epsilon: {epsilon}\n")

    def entrenar(self, pos_raton, pos_zorro):
        estado = self.obtener_estado(pos_raton)
        accion = self.seleccionar_accion(estado)
        nueva_pos = [pos_raton[0] + accion[0], pos_raton[1] + accion[1]]

        if nueva_pos[0] < 0 or nueva_pos[0] >= len(self.laberinto) or nueva_pos[1] < 0 or nueva_pos[1] >= len(
                self.laberinto[0]) or self.laberinto[nueva_pos[0]][nueva_pos[1]] == 1:
            recompensa = -1  # Penalización por movimiento inválido
            nueva_pos = pos_raton
        elif nueva_pos == self.pos_queso:
            recompensa = 10  # Recompensa al encontrar el queso
        elif self.es_cercano(pos_zorro, nueva_pos):
            recompensa = -10  # Penalización severa por acercarse al zorro
        else:
            recompensa = -0.1  # Penalización leve por cada movimiento

        self.registrar_movimientos(estado, accion, nueva_pos, recompensa, self.epsilon)
        siguiente_estado = self.obtener_estado(nueva_pos)
        self.actualizar_q_valor(estado, accion, recompensa, siguiente_estado)
        self.epsilon *= self.epsilon_decay  # Decaimiento del epsilon (menos exploración con el tiempo)
        self.guardar_q_table()  # Guardar la tabla Q después de cada movimiento
        return nueva_pos

    def es_cercano(self, pos_zorro, nueva_pos):
        return abs(nueva_pos[0]-pos_zorro[0]) <= 1 and abs(nueva_pos[1]-pos_zorro[1]) <= 1

