import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla y colores
ANCHO_PANTALLA, ALTO_PANTALLA = 400, 400
TAMANO_CELDA = 40
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego del Ratón y el Queso")
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Carga de imágenes
imagen_raton = pygame.image.load("../imagenes/mouse.png")
imagen_queso = pygame.image.load("../imagenes/cheese.jpg")
imagen_zorro = pygame.image.load("../imagenes/zorroSolo.png")
imagen_raton = pygame.transform.scale(imagen_raton, (TAMANO_CELDA, TAMANO_CELDA))
imagen_queso = pygame.transform.scale(imagen_queso, (TAMANO_CELDA, TAMANO_CELDA))
imagen_zorro = pygame.transform.scale(imagen_zorro, (TAMANO_CELDA, TAMANO_CELDA))

# Laberinto y posiciones iniciales
laberinto = [
    [0, 0, 1, 0, 0, 0 , 1, 0 , 0],
    [1, 0, 1, 0, 1, 0 , 0, 0 , 1],
    [0, 0, 0, 0, 0, 0 , 1, 0 , 1],
    [1, 0, 1, 0, 1, 0 , 1, 0 , 0],
    [0, 0, 0, 0, 0, 0 , 1, 1 , 1],
    [1, 0, 1, 0, 1, 0 , 0, 0 , 0],
    [0, 0, 0, 0, 1, 0 , 1, 1 , 0],
    [0, 1, 1, 0, 1, 0 , 1, 0 , 0]
]
pos_inicial_raton = [0, 0]
pos_queso = [7, 7]
pos_zorro = [4, 0]  # Posición inicial del personaje en la esquina inferior izquierda
pos_raton = pos_inicial_raton[:]

# Estados del juego
juego_activo = False
juego_ganado_raton = False
juego_ganado_zorro = False

# Función para dibujar el laberinto
def dibujar_laberinto():
    for fila in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            rect_celda = pygame.Rect(col * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            if laberinto[fila][col] == 1:
                pygame.draw.rect(pantalla, NEGRO, rect_celda)
            else:
                pygame.draw.rect(pantalla, BLANCO, rect_celda)
            pygame.draw.rect(pantalla, NEGRO, rect_celda, 1)

# Función para mostrar texto en pantalla
def dibujar_texto(texto, tamano_fuente, color, x, y):
    fuente = pygame.font.Font(None, tamano_fuente)
    superficie_texto = fuente.render(texto, True, color)
    pantalla.blit(superficie_texto, (x, y))

# Función para reiniciar el juego
def reiniciar_juego():
    global pos_raton, pos_zorro, juego_activo, juego_ganado_raton, juego_ganado_zorro
    pos_raton = pos_inicial_raton[:]
    pos_zorro = [4, 0]  # Restablece el personaje a la esquina inferior izquierda
    juego_activo = True
    juego_ganado_raton = False
    juego_ganado_zorro = False

# Menú principal
def menu_principal():
    pantalla.fill(BLANCO)
    dibujar_texto("Juego del Ratón y el Queso", 25, AZUL, 100, 50)
    dibujar_texto("1. Iniciar Juego", 25, VERDE, 120, 150)
    dibujar_texto("2. Salir", 25, ROJO, 120, 200)
    pygame.display.flip()

# Menú de victoria zorro
def menu_victoria_zorro():
    pantalla.fill(BLANCO)
    dibujar_texto("¡Ganaste, Atrapaste al Raton!", 25, AZUL, 100, 50)
    dibujar_texto("1. Reiniciar", 25, VERDE, 120, 150)
    dibujar_texto("2. Salir", 25, ROJO, 120, 200)
    pygame.display.flip()

# Menú de victoria raton
def menu_victoria_raton():
    pantalla.fill(BLANCO)
    dibujar_texto("¡Ganaste, Te comiste el queso!", 25, AZUL, 100, 50)
    dibujar_texto("1. Reiniciar", 25, VERDE, 120, 150)
    dibujar_texto("2. Salir", 25, ROJO, 120, 200)
    pygame.display.flip()
# Bucle principal
ejecutando = True
menu_principal()

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.KEYDOWN:
            if not juego_activo and not juego_ganado_raton and not juego_ganado_zorro:
                if evento.key == pygame.K_1:
                    reiniciar_juego()
                elif evento.key == pygame.K_2:
                    ejecutando = False
                    pygame.quit()
                    sys.exit()
            elif juego_ganado_raton or juego_ganado_zorro:
                if evento.key == pygame.K_1:
                    reiniciar_juego()
                elif evento.key == pygame.K_2:
                    ejecutando = False
                    pygame.quit()
                    sys.exit()
            elif juego_activo:
                # Movimiento del personaje zorro
                if evento.key == pygame.K_UP and pos_zorro[0] > 0 and laberinto[pos_zorro[0] - 1][pos_zorro[1]] == 0:
                    pos_zorro[0] -= 1
                elif evento.key == pygame.K_DOWN and pos_zorro[0] < len(laberinto) - 1 and laberinto[pos_zorro[0] + 1][pos_zorro[1]] == 0:
                    pos_zorro[0] += 1
                elif evento.key == pygame.K_LEFT and pos_zorro[1] > 0 and laberinto[pos_zorro[0]][pos_zorro[1] - 1] == 0:
                    pos_zorro[1] -= 1
                elif evento.key == pygame.K_RIGHT and pos_zorro[1] < len(laberinto[0]) - 1 and laberinto[pos_zorro[0]][pos_zorro[1] + 1] == 0:
                    pos_zorro[1] += 1
                # Movimiento del personaje raton
                elif evento.key == pygame.K_w and pos_raton[0] > 0 and laberinto[pos_raton[0] - 1][pos_raton[1]] == 0:
                    pos_raton[0] -= 1
                elif evento.key == pygame.K_s and pos_raton[0] < len(laberinto) - 1 and laberinto[pos_raton[0] + 1][pos_raton[1]] == 0:
                    pos_raton[0] += 1
                elif evento.key == pygame.K_a and pos_raton[1] > 0 and laberinto[pos_raton[0]][pos_raton[1] - 1] == 0:
                    pos_raton[1] -= 1
                elif evento.key == pygame.K_d and pos_raton[1] < len(laberinto[0]) - 1 and laberinto[pos_raton[0]][pos_raton[1] + 1] == 0:
                    pos_raton[1] += 1

    if juego_activo:
        # Dibuja el laberinto, ratón, queso y zorro
        dibujar_laberinto()
        pantalla.blit(imagen_raton, (pos_raton[1] * TAMANO_CELDA, pos_raton[0] * TAMANO_CELDA))
        pantalla.blit(imagen_queso, (pos_queso[1] * TAMANO_CELDA, pos_queso[0] * TAMANO_CELDA))
        pantalla.blit(imagen_zorro, (pos_zorro[1] * TAMANO_CELDA, pos_zorro[0] * TAMANO_CELDA))

        # Verifica si el personaje alcanzó el queso
        if pos_zorro == pos_raton:
            juego_activo = False
            juego_ganado_zorro = True
        if pos_raton == pos_queso:
            juego_activo = False
            juego_ganado_raton = True
        pygame.display.flip()

    elif juego_ganado_raton:
        menu_victoria_raton()
    elif juego_ganado_zorro:
        menu_victoria_zorro()
    else:
        menu_principal()