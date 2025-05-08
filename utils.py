import pygame,random
import numpy as np
from constantes import *
def dentro_dos_limites(i, j, matriz):
    return 0 <= i < matriz.shape[0] and 0 <= j < matriz.shape[1] 
 
def draw_soil(screen,mapa):
    screen.fill('gray')
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if mapa[i][j] == 1:
                pygame.draw.rect(screen,'orange',(j*CELL_SIZE,i*CELL_SIZE,CELL_SIZE,CELL_SIZE))
            
def resolver_colisao(formigas_colidindo,mapa):
    for formiga in formigas_colidindo:
        if formiga.ultimas_pos:  
            for pos_anterior in reversed(formiga.ultimas_pos):
                if pos_anterior != formiga.posicao:
                    formiga.posicao = pos_anterior.copy()
                    break
            else:  
                movimentos = [[1,0], [-1,0], [0,1], [0,-1]]
                random.shuffle(movimentos)
                for move in movimentos:
                    nova_pos = [formiga.posicao[0] + move[0], formiga.posicao[1] + move[1]]
                    if dentro_dos_limites(nova_pos[0], nova_pos[1], mapa):
                        formiga.posicao = nova_pos
                        break

def verificar_colisoes(formigas,mapa):
    posicoes = {}
    for i, formiga in enumerate(formigas):
        pos = tuple(formiga.posicao) 
        if pos in posicoes:
            posicoes[pos].append(i)
        else:
            posicoes[pos] = [i]
    
    for pos, indices in posicoes.items():
        if len(indices) > 1:
            resolver_colisao([formigas[i] for i in indices],mapa)

def decaimento_feromonios(pos, mapa_feromonios):
    mapa_feromonios[pos[0]][pos[1]] *= 0.6
    if mapa_feromonios[pos[0]][pos[1]] < 0.01:
        mapa_feromonios[pos[0]][pos[1]] = 0



