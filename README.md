# **SmartMouseChase**

Un juego de inteligencia artificial en Pygame donde un ratón aprende a encontrar la ruta más rápida hacia el queso, mientras el jugador controla un personaje que intenta atraparlo antes de que logre su objetivo.

## **Descripción**

SmartMouseChase es un juego que combina técnicas de inteligencia artificial con jugabilidad dinámica. El ratón, controlado por un algoritmo de aprendizaje automático, se adapta y aprende las rutas más rápidas para llegar al queso. Mientras tanto, el jugador asume el rol de un cazador, tratando de atrapar al ratón antes de que este logre su objetivo.

El juego es una simulación de "aprendizaje por refuerzo", donde el ratón mejora sus decisiones a medida que avanza el juego, haciendo cada vez más difícil atraparlo.

## **Características**

- **Inteligencia Artificial:** El ratón aprende las mejores rutas hacia el queso utilizando técnicas de IA.
- **Movimiento del jugador:** El jugador puede controlar un personaje para intentar atrapar al ratón antes de que llegue al queso.
- **Entorno dinámico:** El laberinto se genera de manera que el ratón tenga que adaptarse a nuevas rutas cada vez que juega.
- **Teclas de control personalizadas:** Se usan las teclas `W, A, S, D` para mover al cazador.
- **Modo de juego desafiante:** El ratón mejora sus habilidades con el tiempo, aumentando la dificultad del juego.

## **Tecnologías utilizadas**

- **Python 3.x**
- **Pygame:** Para la creación de gráficos y la gestión de eventos en el juego.
- **Inteligencia Artificial:** Algoritmos de búsqueda y aprendizaje para que el ratón optimice sus rutas.

## **Instrucciones de Instalación**

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/tu_usuario/SmartMouseChase.git
   ```

2. Navega al directorio del proyecto:
   ```bash
   cd SmartMouseChase
   ```

3. Instala las dependencias necesarias:
   ```bash
   pip install pygame
   ```

4. Ejecuta el juego:
   ```bash
   python main.py
   ```

## **Cómo jugar**

1. Usa las teclas `W, A, S, D` para el personaje a través del laberinto.
2. El ratón aprenderá las rutas hacia el queso de manera autónoma, y tú tendrás que atraparlo antes de que logre su objetivo.
3. El juego incluye niveles de dificultad, donde el ratón mejora su rendimiento a medida que juega.
