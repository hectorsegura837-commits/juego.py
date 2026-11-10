import pygame
import random
import pyttsx3
import threading

# Inicializar pygame
pygame.init()

# Configuración de pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Caza Monedas con Voz")

# Colores
BLANCO = (255, 255, 255)
AZUL = (50, 100, 255)
DORADO = (255, 215, 0)
ROJO = (255, 50, 50)

# Reloj
clock = pygame.time.Clock()

# Jugador
jugador = pygame.Rect(100, 300, 50, 50)
velocidad = 6

# Moneda
moneda = pygame.Rect(
    random.randint(50, 750),
    random.randint(50, 550),
    30,
    30
)

# Enemigo
enemigo = pygame.Rect(
    random.randint(50, 750),
    random.randint(50, 550),
    40,
    40
)

# Fuente
fuente = pygame.font.SysFont("Arial", 30)

# Puntuación
puntos = 0

# Voz
engine = pyttsx3.init()

def hablar(texto):
    def voz():
        engine.say(texto)
        engine.runAndWait()
    threading.Thread(target=voz, daemon=True).start()

hablar("Bienvenido al juego. Recoge las monedas.")

# Sonido simple generado por sistema
try:
    sonido_moneda = pygame.mixer.Sound("coin.wav")
except:
    sonido_moneda = None

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        jugador.x -= velocidad

    if teclas[pygame.K_RIGHT]:
        jugador.x += velocidad

    if teclas[pygame.K_UP]:
        jugador.y -= velocidad

    if teclas[pygame.K_DOWN]:
        jugador.y += velocidad

    # Colisión con moneda
    if jugador.colliderect(moneda):
        puntos += 1

        if sonido_moneda:
            sonido_moneda.play()

        if puntos % 5 == 0:
            hablar(f"Excelente. Llevas {puntos} puntos")

        moneda.x = random.randint(50, 750)
        moneda.y = random.randint(50, 550)

    # Movimiento enemigo
    if enemigo.x < jugador.x:
        enemigo.x += 2
    elif enemigo.x > jugador.x:
        enemigo.x -= 2

    if enemigo.y < jugador.y:
        enemigo.y += 2
    elif enemigo.y > jugador.y:
        enemigo.y -= 2

    # Colisión enemigo
    if jugador.colliderect(enemigo):
        hablar("Juego terminado")
        ejecutando = False

    # Dibujar
    pantalla.fill(BLANCO)

    pygame.draw.rect(pantalla, AZUL, jugador)
    pygame.draw.circle(
        pantalla,
        DORADO,
        (moneda.x + 15, moneda.y + 15),
        15
    )
    pygame.draw.rect(pantalla, ROJO, enemigo)

    texto = fuente.render(
        f"Puntos: {puntos}",
        True,
        (0, 0, 0)
    )

    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()