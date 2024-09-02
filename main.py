import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Configurar el título de la ventana
pygame.display.set_caption("Missile Command")

# Definir los colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Bucle principal del juego
while True:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Rellenar la pantalla con color negro (fondo)
    screen.fill(BLACK)
    
    # Actualizar la pantalla
    pygame.display.flip()
