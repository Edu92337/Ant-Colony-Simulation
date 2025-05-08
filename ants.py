import pygame
import random
import numpy as np
from utils import *
from constantes import *

class Ants():

    def __init__(self):
        self.posicao = [GRID_HEIGHT//2,GRID_WIDTH//2]
        self.energias = 100
        self.ultimas_pos = [self.posicao[:]]
        self.encontrou_alimento = False
        self.cor = 'black'
        self.viva = True

    def procurando_comida(self,mapa_feromonios,mapa):
        movimentos =  [[1,0], [-1,0], [0,1], [0,-1]]
        proxima_pos = self.posicao
        random.shuffle(movimentos)
        for move in movimentos:
            nova_pos = [self.posicao[0] + move[0], self.posicao[1] + move[1]]
            if dentro_dos_limites(nova_pos[0],nova_pos[1],mapa_feromonios):
                chance_seguir_feromonio = 0.9
                if len(self.ultimas_pos) > 5 and len(set(tuple(pos) for pos in self.ultimas_pos[-3:])) == 1:
                    chance_seguir_feromonio = 0.8
                    
                if mapa[nova_pos[0]][nova_pos[1]] == 0 and  random.random() < chance_seguir_feromonio:
                    if mapa_feromonios[nova_pos[0]][nova_pos[1]] > 0:
                        mapa_feromonios[self.posicao[0]][self.posicao[1]] = 1
                        proxima_pos = nova_pos
                        break
                elif mapa[nova_pos[0]][nova_pos[1]] == 0 and random.random() >= chance_seguir_feromonio:
                    proxima_pos = nova_pos
                    break
                else:
                    if mapa[nova_pos[0]][nova_pos[1]] == 1:
                        self.energias -= 1
                        mapa[nova_pos[0]][nova_pos[1]] = 0
                        break
                
        self.posicao = proxima_pos
        if len(self.ultimas_pos) >= 10:
            self.ultimas_pos.pop(0)
        self.ultimas_pos.append(self.posicao)

    def caminho_para_ninho(self,mapa_feromonios,mapa):
        moves = [[1,0], [-1,0], [0,1], [0,-1]]
        random.shuffle(moves)
        menor_dist = float('inf')
        melhor_mov = None

        for move in moves:
            nova_pos = [self.posicao[0] + move[0], self.posicao[1] + move[1]]
            if dentro_dos_limites(nova_pos[0], nova_pos[1], mapa):
                if mapa[nova_pos[0]][nova_pos[1]] == 0 :
                    dist = abs(nova_pos[0] - GRID_WIDTH//2) + abs(nova_pos[1] - GRID_HEIGHT//2)
                    if dist < menor_dist:
                        menor_dist = dist
                        melhor_mov = move

        if melhor_mov is not None:
            nova_pos = [self.posicao[0] + melhor_mov[0], self.posicao[1] + melhor_mov[1]]
            self.posicao = nova_pos
            mapa_feromonios[self.posicao[0]][self.posicao[1]] = 1
            self.ultimas_pos.append(nova_pos)
        if len(self.ultimas_pos) >= 10:
            self.ultimas_pos.pop(0)

    def movimento_por_feromonio(self,mapa_feromonios,mapa):
        if self.encontrou_alimento == True:
            self.caminho_para_ninho(mapa_feromonios,mapa)
        else:
            self.procurando_comida(mapa_feromonios,mapa)
    
    def morre_de_fome(self):
        if self.energias <= 0:
            self.viva = False
        return self.viva

    def alimento_encontrado(self,comidas):
        for comida in comidas:
            if (abs(self.posicao[0] - comida.posicao[0]) <= 2 and abs(self.posicao[1] - comida.posicao[1]) <= 2):
                self.energias += 1
                self.encontrou_alimento = True 
                self.cor = 'red'  

    def chegou_no_ninho(self):
        if self.posicao[0] == GRID_HEIGHT//2 and self.posicao[1] == GRID_WIDTH//2:
            self.cor = 'black'
            self.encontrou_alimento = False
                
    def draw_ant(self, screen):
        x = self.posicao[1] * CELL_SIZE + CELL_SIZE // 2
        y = self.posicao[0] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, self.cor, (x, y), CELL_SIZE // 2)

