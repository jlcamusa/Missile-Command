import pygame
import sys
import random
import math

from launcher import Launcher
from missile import Missile
from explosion import Explosion

# Inicializar Pygame
pygame.init()

# Cambiar cursor
pygame.mouse.set_cursor(*pygame.cursors.diamond)

# Obtener dimensiones de la pantalla
INFO = pygame.display.Info()

# Definir el tamaño de la pantalla
SCREEN_WIDTH = int(INFO.current_h * 0.5)
SCREEN_HEIGHT = int(INFO.current_h * 0.5)

# Definir altura de los elementos del juego
GROUND_HEIGHT = int(SCREEN_HEIGHT / 15)
SHELTER_HEIGHT = int(SCREEN_HEIGHT / 10)

# Crear display para el juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Configura la fuente para el texto
font = pygame.font.SysFont("consolas", int(SCREEN_HEIGHT * 0.035))

# Inicializa puntajes
player_score = 0
high_score = 1000  # Puedes establecer un valor inicial o cargarlo desde un archivo

# Configurar el título de la ventana
pygame.display.set_caption("Missile Command")

half = SCREEN_WIDTH/18

shelter_positions = [SCREEN_WIDTH/9 - half, 2*SCREEN_WIDTH/9 - half,
                     3*SCREEN_WIDTH/9 - half, 4*SCREEN_WIDTH/9 - half,
                     5*SCREEN_WIDTH/9 - half, 6*SCREEN_WIDTH/9 - half,
                     7*SCREEN_WIDTH/9 - half, 8*SCREEN_WIDTH/9 - half,
                     9*SCREEN_WIDTH/9 - half]

enemy_missiles = []
enemies = []
level = 0
player_missiles = []
explosion_list = []
shelter = [True, True, True, True, True, True]

player_speed = 10    # 0.2
enemy_speed = 1    # 0.04

launcher_list = [Launcher(0), Launcher(1), Launcher(2)]
launcher_positions = [SCREEN_WIDTH/9 - half, 5*SCREEN_WIDTH/9 - half, 9*SCREEN_WIDTH/9 - half]

# Definir los colores
BLACK = pygame.Color(0,0,0)
GREEN = pygame.Color(0, 255, 0)
RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
CYAN = pygame.Color(0, 255, 255)
PURPLE = pygame.Color(255, 0, 255)
WHITE = pygame.Color(255, 255, 255)
BLUE = pygame.Color(0, 0, 255)

colors_list = [GREEN, RED, YELLOW,
               CYAN, PURPLE, WHITE,
               BLUE]

def draw_scores(screen, player_score, high_score):
    
    # Dibuja el puntaje del jugador en la parte superior izquierda
    player_score_text = font.render(f"Score: {player_score}", True, WHITE)
    screen.blit(player_score_text, (10, 10))
    
    # Dibuja el puntaje más alto en la parte superior derecha
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    text_width = high_score_text.get_width()
    screen.blit(high_score_text, (SCREEN_WIDTH - text_width - 10, 10))

def draw_button(text, pos, font, color, hover_color):
    button_text = font.render(text, True, (255, 255, 255))
    button_rect = button_text.get_rect(center=pos)
    
    # Efecto de hover
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect.inflate(20, 10))
    else:
        pygame.draw.rect(screen, color, button_rect.inflate(20, 10))
    
    screen.blit(button_text, button_rect)
    
    return button_rect

# draw: dibuja todos los elementos del juego
def draw():
    screen.fill(BLACK)    
    hill_height = SCREEN_HEIGHT - SHELTER_HEIGHT

    # Dibuja el suelo
    pygame.draw.rect(screen, colors_list[2], (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    # Dibuja las colinas y los misiles en reserva
    for storage_silo in range(len(launcher_list)):
        pygame.draw.polygon(screen, colors_list[2],
                            [(storage_silo * SCREEN_WIDTH / 2 - SHELTER_HEIGHT/2 + GROUND_HEIGHT - (GROUND_HEIGHT * storage_silo), hill_height),
                             (storage_silo * SCREEN_WIDTH / 2 + SHELTER_HEIGHT/2 + GROUND_HEIGHT - (GROUND_HEIGHT * storage_silo), hill_height),
                             (storage_silo * SCREEN_WIDTH / 2 + SHELTER_HEIGHT + GROUND_HEIGHT - (GROUND_HEIGHT * storage_silo), SCREEN_HEIGHT), 
                             (storage_silo * SCREEN_WIDTH / 2 - SHELTER_HEIGHT + GROUND_HEIGHT - (GROUND_HEIGHT * storage_silo), SCREEN_HEIGHT)])
        
        counter = launcher_list[storage_silo].ammo
        number = 1

        while counter > 0:
            for j in range(number):
                ellipse_x = launcher_positions[storage_silo] - ((number - 2 * j) * SCREEN_WIDTH / 100) + SCREEN_WIDTH / 200
                ellipse_y = SCREEN_HEIGHT - SHELTER_HEIGHT + ((number - 1) * SCREEN_WIDTH / 100)
                ellipse_width = SCREEN_WIDTH / 100
                ellipse_height = SCREEN_WIDTH / 100
                ellipse_rect = (ellipse_x, ellipse_y, ellipse_width, ellipse_height)

                pygame.draw.ellipse(screen, colors_list[6], ellipse_rect)

                counter = counter-1
                if counter == 0:
                    break
            number = number+1

    # Dibuja las ciudades restantes
    launcher_pos = 1
    for i in range(len(shelter)):
        if shelter[i]:
            rect_x = (i + launcher_pos) * SCREEN_WIDTH / 9 + SHELTER_HEIGHT / 4
            rect_y = SCREEN_HEIGHT - GROUND_HEIGHT * 1.2
            rect_width = SHELTER_HEIGHT / 2
            rect_height = SHELTER_HEIGHT / 3
            rect = (rect_x, rect_y, rect_width, rect_height)

            pygame.draw.rect(screen, colors_list[6], rect)
            
        if (i + 1) % 3 == 0:
            launcher_pos = launcher_pos+1
    
    # Dibuja los misiles del jugador
    for p in player_missiles:
        pygame.draw.line(screen, colors_list[0], (p.start_x, p.start_y), (p.current_x, p.current_y), 1)
        pygame.draw.ellipse(screen, random.choice(colors_list),
                            (p.current_x-1.5, p.current_y-1.5, 4, 4), 0)
        col = random.choice(colors_list)
        pygame.draw.line(screen, col, (p.end_x-5, p.end_y-5),
                         (p.end_x+5, p.end_y+5), 1)
        pygame.draw.line(screen, col, (p.end_x+5, p.end_y-5),
                         (p.end_x-5, p.end_y+5), 1)
        p.move()
        
    # Dibuja los misiles enemigos
    for p in enemy_missiles:
        pygame.draw.line(screen, pygame.Color(255, 0, 0), (p.start_x, p.start_y), (p.current_x, p.current_y), 1)
        pygame.draw.ellipse(screen, random.choice(colors_list),
                            (p.current_x-1.5, p.current_y-1.5, 4, 4), 0)

        p.move()
    
    # Dibuja las explosiones
    for w in explosion_list:
        if w.expires:
            w.frame -= 1
            if w.frame == 0:
                explosion_list.remove(w)
                del w
                continue
        elif w.frame == 60:
            w.expires = True
        else:
            w.frame += 1
        pygame.draw.ellipse(screen, random.choice(colors_list),
                            (w.poz_x-w.frame/2, w.poz_y-w.frame/2, w.frame, w.frame), 0)
        
    # Dibuja los puntajes
    draw_scores(screen, player_score, high_score)
    
    pygame.display.update()

# selects launcher closest to where the player clicked that still has ammo
def designate_launcher(x,y):
    minimum_x = 10
    y1 = SCREEN_HEIGHT - 50
    dy = y-y1
    minimum = 100000
    if launcher_list[0].ammo > 0:
        x1 = launcher_positions[0]
        dx = x1-x
        temp = math.sqrt(dx*dx + dy*dy)
        if temp < minimum:
            minimum = temp
            minimum_x = x1
    if launcher_list[1].ammo > 0:
        x1 = launcher_positions[1]
        dx = x1-x
        temp = math.sqrt(dx*dx + dy*dy)
        if temp < minimum:
            minimum = temp
            minimum_x = x1
    if launcher_list[2].ammo > 0:
        x1 = launcher_positions[2]
        dx = x1-x
        temp = math.sqrt(dx*dx + dy*dy)
        if temp < minimum:
            minimum = temp
            minimum_x = x1
    return minimum_x

def launch_rocket(x, y):
    if y > SCREEN_HEIGHT-SHELTER_HEIGHT*1.4:
        return
    
    launcher_position = designate_launcher(x, y)
    if launcher_position == launcher_positions[0]:
        launcher_list[0].ammo -= 1
    elif launcher_position == launcher_positions[1]:
        launcher_list[1].ammo -= 1
    elif launcher_position == launcher_positions[2]:
        launcher_list[2].ammo -= 1
    else:
        return
    player_missiles.append(Missile(launcher_position, SCREEN_HEIGHT - SHELTER_HEIGHT, x, y, player_speed, 0))

def middle_point(x, y, wx, wy, r):
    p = ((math.pow((x - wx), 2) // math.pow(r+1, 2)) + 
         (math.pow((y - wy), 2) // math.pow(r+1, 2))) 
  
    return p

def collision():
    for p in player_missiles:
        if p.current_y-p.end_y < 0.1:
            temp = Explosion(p.current_x, p.current_y)
            explosion_list.append(temp)
            player_missiles.remove(p)
            del p
            continue
        
        for w in explosion_list:
            if middle_point(p.current_x, p.current_y, w.poz_x, w.poz_y, w.frame / 2) < 1:
                temp = Explosion(p.current_x, p.current_y)
                explosion_list.append(temp)
                player_missiles.remove(p)
                del p
                break
    for p in enemy_missiles:
        if p.current_y-p.end_y > -0.1:
            temp = Explosion(p.current_x, p.current_y)
            explosion_list.append(temp)
            if p.end_x == shelter_positions[0]:
                launcher_list[0].ammo = 0
            elif p.end_x == shelter_positions[1]:
                shelter[0] = False
            elif p.end_x == shelter_positions[2]:
                shelter[1] = False
            elif p.end_x == shelter_positions[3]:
                shelter[2] = False
            elif p.end_x == shelter_positions[4]:
                launcher_list[1].ammo = 0
            elif p.end_x == shelter_positions[5]:
                shelter[3] = False
            elif p.end_x == shelter_positions[6]:
                shelter[4] = False
            elif p.end_x == shelter_positions[7]:
                shelter[5] = False
            elif p.end_x == shelter_positions[8]:
                launcher_list[2].ammo = 0
            lose()
            enemy_missiles.remove(p)
            del p
            continue
        
        for w in explosion_list:
            if middle_point(p.current_x, p.current_y, w.poz_x, w.poz_y, w.frame / 2) < 1:
                temp = Explosion(p.current_x, p.current_y)
                explosion_list.append(temp)
                enemy_missiles.remove(p)
                del p
                break

def new_level():
    if not enemy_missiles:
        launcher_list[0].ammo = 10
        launcher_list[1].ammo = 10
        launcher_list[2].ammo = 10
        explosion_list.clear()
        global level
        level += 1
        for _ in range(10):
            temp = Missile(random.randrange(SCREEN_WIDTH), -10,
                           random.choice(shelter_positions), SCREEN_HEIGHT - GROUND_HEIGHT, enemy_speed, random.randrange(120))
            enemy_missiles.append(temp)

def lose():
    for i in shelter:
        if i:
            return
    del explosion_list[:]
    del player_missiles[:]
    del enemy_missiles[:]
    global level
    draw()
    text_surface = font.render("Survived waves : " + str(level) +
                                     " Press space to start again", True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    screen.blit(text_surface, text_rect)
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    launcher_list[0].ammo = 10
                    launcher_list[1].ammo = 10
                    launcher_list[2].ammo = 10
                    shelter[0] = True
                    shelter[1] = True
                    shelter[2] = True
                    shelter[3] = True
                    shelter[4] = True
                    shelter[5] = True
                    level = 0
                    main()

def show_menu():
    # Definir los botones
    button_font = pygame.font.Font(None, 50)
    button_color = (100, 100, 255)
    button_hover_color = (150, 150, 255)
    
    buttons = [
        {"text": "Play", "action": "play"},
        {"text": "HighScore", "action": "highscore"},
        {"text": "Exit", "action": "exit"}
    ]
    
    menu_running = True
    while menu_running:
        screen.fill((0, 0, 0))  # Fondo negro
        
        # Dibujar el título
        title_text = font.render("Mi Juego", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        screen.blit(title_text, title_text_rect)
        
        # Dibujar los botones
        button_rects = []
        y_offset = 0
        for button in buttons:
            button_rect = draw_button(button["text"], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset), button_font, button_color, button_hover_color)
            button_rects.append({"rect": button_rect, "action": button["action"]})
            y_offset += 70  # Espacio entre botones
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in button_rects:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["action"] == "play":
                            menu_running = False  # Cerrar el menú para empezar el juego
                        elif button["action"] == "highscore":
                            pass  # Por ahora, no hace nada
                        elif button["action"] == "exit":
                            pygame.quit()
                            sys.exit(0)
        
        clock.tick(60)  # Limitar a 60 FPS

def main():

    show_menu()  # Mostrar el menú al inicio

    while True:
        collision()
        draw()
        new_level()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                launch_rocket(x, y)
        
        clock.tick(60)

main()