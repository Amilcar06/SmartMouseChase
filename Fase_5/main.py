import pygame
import sys
import time
from aprendizaje import Aprendizaje
import random

# Función para encontrar una posición aleatoria válida
def generar_posicion_aleatoria(laberinto, excepciones=[]):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    while True:
        fila = random.randint(0, filas - 4)
        columna = random.randint(0, columnas - 3)
        if laberinto[fila][columna] == 0 and [fila, columna] not in excepciones:
            return [fila, columna]

# Función para mostrar valores Q de un estado en la consola
def mostrar_valores_q(q_table, estado):
    if estado in q_table:
        print(f"Estado: {estado}")
        print(f"Valores Q: {q_table[estado]}")
    else:
        print(f"Estado: {estado} aún no visitado.")

# Función para registrar el tiempo transcurrido al encontrar el queso.
def registrar_tiempo(tiempo):
    with open("datos/registroTiempo.txt", "a") as log:
        log.write(f"Tiempo en encontrar el queso: {tiempo:.2f}\n")

# Inicialización de Pygame y configuración básica
pygame.init()
ANCHO_PANTALLA, ALTO_PANTALLA = 320, 320
TAMANO_CELDA = 40
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego del Ratón, el Queso y el Zorro")

# Definición de colores RGB
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Variables para el control del tiempo
inicio_tiempo = None  # Para guardar el tiempo de inicio
tiempo_transcurrido = 0  # Para guardar el tiempo transcurrido

# Carga de imágenes y ajuste de tamaño
imagen_raton = pygame.image.load("../imagenes/mouse.png")
imagen_queso = pygame.image.load("../imagenes/cheese.png")
imagen_zorro = pygame.image.load("../imagenes/zorroSolo.png")
imagen_raton = pygame.transform.scale(imagen_raton, (TAMANO_CELDA, TAMANO_CELDA))
imagen_queso = pygame.transform.scale(imagen_queso, (TAMANO_CELDA, TAMANO_CELDA))
imagen_zorro = pygame.transform.scale(imagen_zorro, (TAMANO_CELDA, TAMANO_CELDA))

# Laberinto y posiciones iniciales
laberinto = [
    [0, 0, 1, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0, 1, 0]
]

pos_queso = [7, 7]
pos_zorro = [4, 3]
pos_inicial_raton = generar_posicion_aleatoria(laberinto, excepciones=[pos_queso, pos_zorro])
pos_raton = pos_inicial_raton[:]

movimientos_maximos = 100  # Número máximo de movimientos permitidos
movimientos_restantes = movimientos_maximos

# Inicialización del agente de aprendizaje por refuerzo (Q-Learning)
qlearning = Aprendizaje(laberinto, pos_queso)

# Variables para el control de la velocidad del ratón
intervalo_movimiento_raton = 60  # Fotogramas raton
contador_movimiento = 0  # Contador de fotogramas

# Estados del juego
MENU_PRINCIPAL = 0
JUGANDO = 1
VICTORIA_RATON = 2
VICTORIA_ZORRO = 3
estado_juego = MENU_PRINCIPAL

# Función para dibujar texto
def dibujar_texto(texto, tamano, color, x, y):
    fuente = pygame.font.Font(None, tamano)
    superficie_texto = fuente.render(texto, True, color)
    pantalla.blit(superficie_texto, (x, y))

# Menú principal
def menu_principal():
    pantalla.fill(BLANCO)
    dibujar_texto("Juego del Ratón y el Queso", 25, AZUL, 40, 50)
    dibujar_texto("1. Iniciar Juego", 25, VERDE, 120, 150)
    dibujar_texto("2. Salir", 25, ROJO, 120, 200)
    pygame.display.flip()

# Menú de victoria del zorro
def menu_victoria_zorro():
    pantalla.fill(BLANCO)
    dibujar_texto("¡Ganaste, atrapaste al ratón!", 25, AZUL, 50, 50)
    dibujar_texto(f"Tiempo: {tiempo_transcurrido:.2f} segundos", 25, VERDE, 50, 100)  # Mostrar el tiempo
    dibujar_texto("1. Reiniciar", 25, VERDE, 120, 150)
    dibujar_texto("2. Salir", 25, ROJO, 120, 200)
    pygame.display.flip()

# Menú de victoria del ratón
def menu_victoria_raton():
    pantalla.fill(BLANCO)
    dibujar_texto("¡Ganaste, te comiste el queso!", 25, AZUL, 50, 50)
    dibujar_texto(f"Tiempo: {tiempo_transcurrido:.2f} segundos", 25, VERDE, 50, 100)
    dibujar_texto("1. Reiniciar", 25, VERDE, 120, 150)
    dibujar_texto("2. Salir", 25, ROJO, 120, 200)
    pygame.display.flip()

# Dibujar laberinto
def dibujar_laberinto():
    for fila in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            rect_celda = pygame.Rect(col * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            color = NEGRO if laberinto[fila][col] == 1 else BLANCO
            pygame.draw.rect(pantalla, color, rect_celda)
            pygame.draw.rect(pantalla, NEGRO, rect_celda, 1)

# Movimiento del zorro con las teclas de flecha
def mover_zorro(tecla, pos_zorro):
    movimientos = {
        pygame.K_UP: (-1, 0),
        pygame.K_DOWN: (1, 0),
        pygame.K_LEFT: (0, -1),
        pygame.K_RIGHT: (0, 1)
    }
    if tecla in movimientos:
        nuevo_x = pos_zorro[0] + movimientos[tecla][0]
        nuevo_y = pos_zorro[1] + movimientos[tecla][1]
        if 0 <= nuevo_x < len(laberinto) and 0 <= nuevo_y < len(laberinto[0]) and laberinto[nuevo_x][nuevo_y] == 0:
            pos_zorro[0], pos_zorro[1] = nuevo_x, nuevo_y
    return pos_zorro

# Reiniciar posiciones de los personajes
def reiniciar_juego():
    global pos_raton, pos_zorro, estado_juego, inicio_tiempo, tiempo_transcurrido, movimientos_restantes

    # Reiniciar posiciones de los personajes
    pos_raton = generar_posicion_aleatoria(laberinto, excepciones=[pos_queso, pos_zorro])
    pos_zorro = [4, 3]
  # Reinicia al zorro en su posición fija

    # Reiniciar estado del juego y control de tiempo
    estado_juego = JUGANDO
    inicio_tiempo = time.time()
    tiempo_transcurrido = 0

    # Reiniciar movimientos permitidos
    movimientos_restantes = movimientos_maximos

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if estado_juego == MENU_PRINCIPAL:
                if evento.key == pygame.K_1:
                    reiniciar_juego()
                elif evento.key == pygame.K_2:
                    ejecutando = False
            elif (estado_juego == VICTORIA_RATON
                  or estado_juego == VICTORIA_ZORRO):
                if evento.key == pygame.K_1:
                    reiniciar_juego()
                elif evento.key == pygame.K_2:
                    ejecutando = False
            elif estado_juego == JUGANDO:
                pos_zorro = mover_zorro(evento.key, pos_zorro)

    if estado_juego == MENU_PRINCIPAL:
        menu_principal()
    elif estado_juego == JUGANDO:
        pantalla.fill(BLANCO)
        dibujar_laberinto()
        # Actualizar el tiempo transcurrido solo si el juego está en curso
        tiempo_transcurrido = time.time() - inicio_tiempo

        # Control de la velocidad del ratón
        contador_movimiento += 1
        # En el bucle principal, donde llamas a entrenar:
        if contador_movimiento >= intervalo_movimiento_raton:
            pos_raton = qlearning.entrenar(pos_raton, pos_zorro)  # Pasar la posición del zorro
            mostrar_valores_q(qlearning.q_table, tuple(pos_raton))
            contador_movimiento = 0  # Reiniciar el contador
            movimientos_restantes -= 1  # Reducir los movimientos restantes

            # Verificar si los movimientos restantes llegaron a 0
            if movimientos_restantes <= 0:
                estado_juego = VICTORIA_ZORRO  # Puedes definir un menú personalizado para "Fin de movimientos"

        # Dibujar personajes
        pantalla.blit(imagen_raton, (pos_raton[1] * TAMANO_CELDA, pos_raton[0] * TAMANO_CELDA))
        pantalla.blit(imagen_queso, (pos_queso[1] * TAMANO_CELDA, pos_queso[0] * TAMANO_CELDA))
        pantalla.blit(imagen_zorro, (pos_zorro[1] * TAMANO_CELDA, pos_zorro[0] * TAMANO_CELDA))

        # Verificar victorias
        if pos_raton == pos_queso:
            estado_juego = VICTORIA_RATON
            registrar_tiempo(tiempo_transcurrido)
        elif pos_raton == pos_zorro:
            estado_juego = VICTORIA_ZORRO

        pygame.display.flip()
    elif estado_juego == VICTORIA_RATON:
        menu_victoria_raton()
    elif estado_juego == VICTORIA_ZORRO:
        menu_victoria_zorro()

