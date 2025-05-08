from ants import *
from food import *
from utils import *
from constantes import *
import pygame
import numpy as np

def main():
    mapa = np.ones((GRID_HEIGHT,GRID_WIDTH),dtype=int)
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if np.sqrt((i - GRID_HEIGHT//2)**2 + (j - GRID_HEIGHT//2)**2) <= 20:
                mapa[i, j] = 0
    mapa_feromonios = np.zeros((GRID_HEIGHT,GRID_WIDTH))
    
    n = 150
    m = 5
    formigas = [Ants() for _ in range(n)]
    comida = Food()
    comidas = [Food() for _ in range(m)]
    running = True
    pygame.init()
    screen = pygame.display.set_mode((HEIGHT,WIDTH))
    clock = pygame.time.Clock()
    pygame.display.set_caption("ANTS COLONY")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        formigas = [ant for ant in formigas if ant.morre_de_fome()]
        
        draw_soil(screen,mapa)
        for ant in formigas:
            if ant.viva:
                ant.draw_ant(screen)
                ant.movimento_por_feromonio(mapa_feromonios,mapa)
                ant.alimento_encontrado(comidas)
                ant.chegou_no_ninho()
                decaimento_feromonios(ant.posicao,mapa_feromonios)

        verificar_colisoes(formigas,mapa)
        for comida in comidas:
            comida.draw_food(screen,mapa)
        
        pygame.display.flip()
        clock.tick(1000)

if __name__ == "__main__":
    main()