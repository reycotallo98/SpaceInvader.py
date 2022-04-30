import math
from pygame import mixer
import pygame

# Iniciamos pygame
pygame.init()

# creamos la pantalla
pantalla = pygame.display.set_mode((800, 600))
# Titulo e icono
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("icon.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("img-espacio.jpg")
# Programamos que la pantalla se muestre hasta que se cierre
se_ejecuta = True
# creamos el jugador
img_jugador = pygame.image.load("cohete-espacial.png")
jugador_x = 368  # la mitad-su tamaño
jugador_y = 500
jugador_x_cambio = 0

# creacion del enemigo
img_enemigo = []
enemigo_x = []  # la mitad-su tamaño
enemigo_y = []
enemigo_x_cambio = []
cantidad_enemigos = 8
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("nave-alien.png"))
    enemigo_x.append(100*e)  # la mitad-su tamaño
    enemigo_y.append(64)
    enemigo_x_cambio.append(0.1)

# creamos las balas
bala = pygame.image.load("laser (1).png")
bala = pygame.transform.rotate(bala, +90)
bala_x = 0
bala_y = 500
balavisible = False
colision = False

puntuaje = 0
fuente = pygame.font.Font('pricedown bl.otf',32)
texto_x = 600
texto_y = 20

#agregar musica
mixer.music.load("MusicaFondo.mp3")
mixer.music.play(-1)

#comprobar si hemos perdido
perdido = False
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntuaje}",True,(255,255,255))
    pantalla.blit(texto,(x,y))
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def enemigo(x, y,i):
    if img_enemigo[i] is not None:
        pantalla.blit(img_enemigo[i], (x, y))
    else:
        pass


def disparo(x, y):
    global balavisible
    balavisible = True
    pantalla.blit(bala, (x+10, y+10))

def comprueba_colision(xb,yb,xn,yn):
    distancia = math.sqrt(math.pow((xb-xn),2)+math.pow((yb-yn),2))
    global colision
    if distancia<27:
        colision = True
        global bala_y
        global puntuaje
        bala_y=-11
        puntuaje += 1
        sonido_colision = mixer.Sound('GunShotGun 1012_46_4_preview (mp3cut.net) (1).mp3')
        sonido_colision.play()

    else:
        colision = False
    return colision
def perdido_():
    fo = pygame.font.Font("pricedown bl.otf", 100)
    texto = fo.render(f"GAME OVER", True, (255, 255, 255))
    pantalla.blit(texto, (120, 200))

def ganado():
    fo = pygame.font.Font("pricedown bl.otf", 100)
    texto = fo.render(f"Has ganado", True, (255, 255, 255))
    pantalla.blit(texto, (120, 200))
while se_ejecuta:
    # metemos el fondo si ponemos esto despues de llamar la funcion de jugador, este desapareceria ya que lo coloreamos
    pantalla.blit(fondo, (0, 0))
    mostrar_puntaje(texto_x,texto_y)
    if puntuaje < cantidad_enemigos and not perdido:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Comprueba si el evento es pulsar la X
                se_ejecuta = False
            # Ponemos en escucha el presionado de las flechas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    img_jugador = pygame.transform.rotate(img_jugador, -90)
                    jugador_x_cambio = 0.1
                if evento.key == pygame.K_LEFT:
                    img_jugador = pygame.transform.rotate(img_jugador, +90)
                    jugador_x_cambio = -0.1
                if evento.key == pygame.K_SPACE:
                    if not balavisible:
                        bala_x = jugador_x
                        disparo(bala_x, bala_y)
                        sonido_bala = mixer.Sound('disparo.mp3')
                        sonido_bala.play()
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = 0
                    img_jugador = pygame.transform.rotate(img_jugador, -90)
                if evento.key == pygame.K_RIGHT:
                    img_jugador = pygame.transform.rotate(img_jugador, +90)
                    jugador_x_cambio = 0
                    fondo = None

        # modificar ubicacion jugador
        jugador_x += jugador_x_cambio


        if 0 > jugador_x:
            jugador_x = 0

        if jugador_x >= 800 - 64:
            jugador_x = 800 - 64
        # movimiento de la bala
        if balavisible:
            bala_y -= 0.1
            disparo(bala_x, bala_y)
        # modificar ubicacion enemigo
        for a in range(cantidad_enemigos):
            if img_enemigo[a] is not None:
                enemigo_x[a] += (0.5 * enemigo_x_cambio[a])
                if enemigo_x[a] >= 800 - 64:
                    enemigo_x_cambio[a] *= -1
                    enemigo_y[a] += 75
                if enemigo_x[a] <= 0:
                    enemigo_x_cambio[a] *= -1
                    enemigo_y[a] += 75

                #comprobamos la distancia relativa de los objetos
                if comprueba_colision(bala_x,bala_y,enemigo_x[a],enemigo_y[a]):
                    img_enemigo[a] = None
                enemigo(enemigo_x[a], enemigo_y[a],a)
                if enemigo_y[a] >= 500:
                    perdido = True


        if bala_y <= -10:
            balavisible = False
            bala_y = 500
        jugador(jugador_x, jugador_y)  # cargamos el juego
    else:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:

                se_ejecuta == False
        if not perdido:
            ganado()
        else:
            perdido_()
    pygame.display.update()
