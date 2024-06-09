import pygame
import numpy as np
import random
import heapq

class Labirinto:
    def __init__(self, dimensao):
        self.dimensao = dimensao
        self.labirinto = np.ones((dimensao*2+1, dimensao*2+1))
        self.criar_labirinto()

    def criar_labirinto(self):
        x, y = 0, 0
        self.labirinto[1, 1] = 0
        pilha = [(x, y)]
        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while pilha:
            x, y = pilha[-1]
            random.shuffle(direcoes)
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.dimensao) and (0 <= ny < self.dimensao) and self.labirinto[2*nx+1, 2*ny+1] == 1:
                    self.labirinto[2*nx+1, 2*ny+1] = 0
                    self.labirinto[2*x+1+dx, 2*y+1+dy] = 0
                    pilha.append((nx, ny))
                    break
            else:
                pilha.pop()
        self.labirinto[1, 0] = 0  # entrada
        self.labirinto[-2, -1] = 0  # saída

def resolver_labirinto(labirinto, tela, tamanho_janela=910, taxa_atualizacao=1):
    entrada = (0, 1)
    saida = (labirinto.labirinto.shape[0]-2, labirinto.labirinto.shape[1]-2)
    fila = []
    heapq.heappush(fila, (0, entrada, [entrada]))
    visitados = set([entrada])
    distancias = {entrada: 0}
    
    pygame.init()
    fonte = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()

    # Renderizar o labirinto apenas uma vez
    tamanho_celula = min(tamanho_janela // labirinto.labirinto.shape[1], tamanho_janela // labirinto.labirinto.shape[0])
    deslocamento_x = (tamanho_janela - tamanho_celula * labirinto.labirinto.shape[1]) // 2
    deslocamento_y = (tamanho_janela - tamanho_celula * labirinto.labirinto.shape[0]) // 2

    for x in range(labirinto.labirinto.shape[0]):
        for y in range(labirinto.labirinto.shape[1]):
            if labirinto.labirinto[x, y] == 0:
                pygame.draw.rect(tela, (255, 255, 255), (deslocamento_x + y*tamanho_celula, deslocamento_y + x*tamanho_celula, tamanho_celula, tamanho_celula))
            else:
                pygame.draw.rect(tela, (0, 0, 0), (deslocamento_x + y*tamanho_celula, deslocamento_y + x*tamanho_celula, tamanho_celula, tamanho_celula))
    pygame.display.flip()

    caminho = None
    while fila:
        prioridade, (x, y), caminho_encontrado = heapq.heappop(fila)
        if (x, y) == saida:
            caminho = caminho_encontrado
            break
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < labirinto.labirinto.shape[0]) and (0 <= ny < labirinto.labirinto.shape[1]) and labirinto.labirinto[nx, ny] == 0 and (nx, ny) not in visitados:
                nova_distancia = distancias[(x, y)] + 1
                if (nx, ny) not in distancias or nova_distancia < distancias[(nx, ny)]:
                    distancias[(nx, ny)] = nova_distancia
                    heapq.heappush(fila, (nova_distancia, (nx, ny), caminho_encontrado + [(nx, ny)]))
                    visitados.add((nx, ny))

        # Atualizar a exibição a cada "taxa_atualizacao" nós
        pygame.event.get()
        if len(visitados) % taxa_atualizacao == 0:
            tela.lock()
            for p in visitados:
                pygame.draw.rect(tela, (0, 255, 0), (deslocamento_x + p[1]*tamanho_celula, deslocamento_y + p[0]*tamanho_celula, tamanho_celula, tamanho_celula))
            pygame.draw.rect(tela, (255, 0, 0), (deslocamento_x + caminho_encontrado[-1][1]*tamanho_celula, deslocamento_y + caminho_encontrado[-1][0]*tamanho_celula, tamanho_celula, tamanho_celula))
            tela.unlock()
            pygame.display.flip()

    return tela, caminho

def animar_caminho_encontrado(tela, caminho, tamanho_celula, deslocamento_x, deslocamento_y):
    pygame.draw.rect(tela, (255, 0, 0), (deslocamento_x + caminho[0][1]*tamanho_celula, deslocamento_y + caminho[0][0]*tamanho_celula, tamanho_celula, tamanho_celula))
    pygame.display.flip()
    pygame.time.wait(0)

    for p in caminho[1:]:
        pygame.draw.rect(tela, (255, 0, 0), (deslocamento_x + p[1]*tamanho_celula, deslocamento_y + p[0]*tamanho_celula, tamanho_celula, tamanho_celula))
        pygame.display.flip()
        pygame.time.wait(0)

