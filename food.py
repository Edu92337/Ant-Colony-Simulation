import pygame,random
import numpy as np
from constantes import *

class Food():
    def __init__(self):
        self.posicao = np.array([np.random.randint(0, GRID_WIDTH),np.random.randint(0, GRID_HEIGHT)])
        self.qnt = 20
        
    def draw_food(self,screen,mapa):
        vazios = []
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if mapa[i][j] == 0:
                    vazios.append((i,j))
        if self.qnt > 0:
            x = self.posicao[1] * CELL_SIZE + CELL_SIZE // 2
            y = self.posicao[0] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.rect(screen, 'green', (x, y, CELL_SIZE, CELL_SIZE))
        else: 
            if vazios:
                self.posicao = np.array(random.choice(vazios))
                self.qnt = 20


