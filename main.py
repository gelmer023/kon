import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# --- Constantes y configuración ---
ANCHO, ALTO = 800, 600
FPS = 60

# Estados del juego
MENU, TUTORIAL, JUGANDO, GAMEOVER = range(4)
estado = MENU

# Colores
BLANCO = (255, 255, 255)
ROJO   = (255,   0,   0)
VERDE  = (  0, 255,   0)
AMARILLO = (255,255, 0)

# Crea el overlay (una vez, al iniciar)
overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
# RGBA: (0,0,0,100) es negro con alpha =100/255
overlay.fill((0, 0, 0, 180))


# Pantalla y reloj
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Shooter Mejorado")
reloj = pygame.time.Clock()

# --- Carga y escalado de imágenes ---
# Ahora usamos convert_alpha() para preservar cualquier transparencia del PNG
fondo_img     = pygame.transform.scale(
    pygame.image.load("fondo.png").convert_alpha(),
    (ANCHO, ALTO)
)
player_img    = pygame.transform.scale(
    pygame.image.load("nave.png").convert_alpha(),
    (50, 50)
)
bullet_img    = pygame.transform.scale(
    pygame.image.load("laser.png").convert_alpha(),
    (90, 120)
)
enemy1_img    = pygame.transform.scale(
    pygame.image.load("enemigo.png").convert_alpha(),
    (40, 40)
)
enemy2_img    = pygame.transform.scale(
    pygame.image.load("enemigo2.png").convert_alpha(),
    (50, 50)
)
explosion_img = pygame.transform.scale(
    pygame.image.load("explosion.png").convert_alpha(),
    (40, 40)
)

# Sonidos
pygame.mixer.music.load("musica_fondo.mp3")
pygame.mixer.music.play(-1)
sonido_disparo   = pygame.mixer.Sound("disparo.wav")
sonido_explosion = pygame.mixer.Sound("explosion.wav")

# Fuente
def dibujar_texto(texto, tamaño, color, x, y):
    fuente = pygame.font.SysFont(None, tamaño)
    surf   = fuente.render(texto, True, color)
    rect   = surf.get_rect(center=(x, y))
    pantalla.blit(surf, rect)

# --- Variables de juego ---
jugador    = pygame.Rect(ANCHO//2 - 25, ALTO - 60, 50, 50)
balas      = []
enemigos   = []
explosiones = []
puntuacion = 0
nivel      = 1

# Temporizador: genera un enemigo cada cierto intervalo
def ajustar_timer_por_nivel(n):
    delay = max(300, 1000 - (n - 1)*200)
    pygame.time.set_timer(pygame.USEREVENT, delay)

ajustar_timer_por_nivel(nivel)

# --- Funciones de menú y estado ---
def menu_principal():
    pantalla.blit(fondo_img, (0, 0))
    pantalla.blit(overlay, (0, 0))
    dibujar_texto("KON", 64, BLANCO, ANCHO//2, 150)
    dibujar_texto("PRESIONE ENTER: Iniciar  |  TECLA T: Tutorial  |  ESC: Salir", 24, AMARILLO, ANCHO//2, 350)
    pygame.display.flip()

def pantalla_tutorial():
    pantalla.blit(fondo_img, (0, 0))
    pantalla.blit(overlay, (0, 0))
    dibujar_texto("TUTORIAL", 64, BLANCO, ANCHO//2, 100)
    dibujar_texto("Teclas <-   -> : Mover nave", 32, BLANCO, ANCHO//2, 220)
    dibujar_texto("Barra Espaciadora : Disparar", 32, BLANCO, ANCHO//2, 270)
    dibujar_texto("100 puntos para subir de nivel", 28, BLANCO, ANCHO//2, 320)
    dibujar_texto("ENTER: Volver al menú", 24, BLANCO, ANCHO//2, 400)
    pygame.display.flip()

def reiniciar_juego():
    global balas, enemigos, explosiones, puntuacion, nivel, estado
    balas = []
    enemigos = []
    explosiones = []
    puntuacion = 0
    nivel = 1
    jugador.x = ANCHO//2 - 25
    ajustar_timer_por_nivel(nivel)
    estado = JUGANDO

def subir_nivel():
    global nivel
    nivel += 1
    enemigos.clear()
    ajustar_timer_por_nivel(nivel)

# --- Lógica de enemigos, balas y colisiones ---
def crear_enemigo():
    tipo = 1 if nivel == 1 else random.choice([1, 2])
    size = (40, 40) if tipo == 1 else (50, 50)
    img  = enemy1_img if tipo == 1 else enemy2_img
    x = random.randint(0, ANCHO - size[0])
    vel_x = random.choice([-3 - nivel, 3 + nivel])
    rect = pygame.Rect(x, 0, *size)
    enemigos.append({"rect": rect, "vel_x": vel_x, "img": img})

def actualizar_enemigos():
    for e in enemigos[:]:
        e["rect"].y += 4 + nivel
        e["rect"].x += e["vel_x"]
        if e["rect"].left <= 0 or e["rect"].right >= ANCHO:
            e["vel_x"] *= -1
        if e["rect"].y > ALTO:
            enemigos.remove(e)

def actualizar_balas():
    for b in balas[:]:
        b.y -= 10
        if b.y < -20:
            balas.remove(b)

def detectar_colisiones():
    global estado, puntuacion
    for e in enemigos[:]:
        if jugador.colliderect(e["rect"]):
            sonido_explosion.play()
            estado = GAMEOVER
            return
        for b in balas[:]:
            if e["rect"].colliderect(b):
                sonido_explosion.play()
                explosiones.append({"rect": e["rect"].copy(), "timer": 15})
                enemigos.remove(e)
                balas.remove(b)
                puntuacion += 10
                if puntuacion >= 200 * nivel:
                    subir_nivel()
                break

def actualizar_explosiones():
    for ex in explosiones[:]:
        ex["timer"] -= 1
        if ex["timer"] <= 0:
            explosiones.remove(ex)

# --- Bucle principal ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == MENU:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    reiniciar_juego()
                elif evento.key == pygame.K_t:
                    estado = TUTORIAL
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        elif estado == TUTORIAL:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                estado = MENU

        elif estado == JUGANDO:
            if evento.type == pygame.USEREVENT:
                crear_enemigo()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                # Dos láseres, uno por cada ala
                offset_y = jugador.top
                left_x  = jugador.left + 5
                right_x = jugador.right - 15  # 10 ancho bala + 5 px margen
                balas.append(pygame.Rect(left_x,  offset_y, 10, 20))
                balas.append(pygame.Rect(right_x, offset_y, 10, 20))
                sonido_disparo.play()

        elif estado == GAMEOVER:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                reiniciar_juego()

    # Lógica de juego según estado
    if estado == MENU:
        menu_principal()

    elif estado == TUTORIAL:
        pantalla_tutorial()

    elif estado == JUGANDO:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.left > 0:
            jugador.x -= 5
        if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
            jugador.x += 5

        actualizar_balas()
        actualizar_enemigos()
        detectar_colisiones()
        actualizar_explosiones()

        # Dibujado: fondo semitransparente si tu PNG tiene alpha
        pantalla.blit(fondo_img, (0, 0))
        pantalla.blit(overlay, (0, 0))
        pantalla.blit(player_img, jugador)
        for b in balas:
            pantalla.blit(bullet_img, b)
        for e in enemigos:
            pantalla.blit(e["img"], e["rect"])
        for ex in explosiones:
            pantalla.blit(explosion_img, ex["rect"])

        dibujar_texto(f"Puntuación: {puntuacion}", 24, BLANCO, 100, 20)
        dibujar_texto(f"Nivel: {nivel}", 24, BLANCO, ANCHO - 100, 20)

        pygame.display.flip()
        reloj.tick(FPS)

    elif estado == GAMEOVER:
        pantalla.blit(fondo_img, (0, 0))
        pantalla.blit(overlay, (0, 0))
        dibujar_texto("GAME OVER", 64, ROJO, ANCHO//2, ALTO//2 - 50)
        dibujar_texto(f"Puntuación final: {puntuacion}", 32, VERDE, ANCHO//2, ALTO//2)
        dibujar_texto("ENTER: Reiniciar  |  ESC: Salir", 24, BLANCO, ANCHO//2, ALTO//2 + 50)
        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
