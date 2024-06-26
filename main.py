import pygame
from labirinto import *

def tela_inicial():
    pygame.init()
    tela = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Configurações do Labirinto")
    fonte = pygame.font.Font(None, 21)
    clock = pygame.time.Clock()

    texto_dimensoes = fonte.render("Digite a dimensão do labirinto (ex: 50):", True, (0, 0, 0))
    texto_taxa = fonte.render("Digite a taxa de atualização por nós (1 a 100):", True, (0, 0, 0))
    instrucoes = [
        "Pressione a tecla 'TAB' para alternar entre os campos de digitação.",
        "Pressione a tecla 'ENTER' para gerar o labirinto.",
        "Pressione a tecla 'ENTER' para voltar à tela inicial."
    ]
    entrada_dimensoes = ""
    entrada_taxa = ""
    foco_dimensoes = True

    while True:
        tela.fill(COR_CAMPO)
        tela.blit(texto_dimensoes, (20, 20))
        tela.blit(texto_taxa, (20, 100))

        # Desenhar borda preta fina para a caixa de dimensões
        pygame.draw.rect(tela, COR_PAREDE, (19, 39, 302, 32), 2)

        # Desenhar borda preta fina para a caixa de taxa
        pygame.draw.rect(tela, COR_PAREDE, (19, 119, 302, 32), 2)

        # Desenhar caixas de texto
        if foco_dimensoes:
            pygame.draw.rect(tela, (150, 150, 150), (20, 40, 300, 30))
        else:
            pygame.draw.rect(tela, (150, 150, 150), (20, 120, 300, 30))

        tela.blit(fonte.render(entrada_dimensoes, True, (0, 0, 0)), (25, 45))
        tela.blit(fonte.render(entrada_taxa, True, (0, 0, 0)), (25, 125))

        # Exibir instruções
        for i, instrucao in enumerate(instrucoes):
            tela.blit(fonte.render(instrucao, True, (0, 0, 0)), (20, 200 + i * 30))

        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None, None
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if foco_dimensoes:
                        foco_dimensoes = False
                    else:
                        dimensao = int(entrada_dimensoes) if entrada_dimensoes else DIMENSAO_PADRAO
                        taxa_atualizacao = int(entrada_taxa) if entrada_taxa else TAXA_PADRAO
                        pygame.quit()
                        return dimensao, taxa_atualizacao
                elif evento.key == pygame.K_BACKSPACE:
                    if foco_dimensoes:
                        entrada_dimensoes = entrada_dimensoes[:-1]
                    else:
                        entrada_taxa = entrada_taxa[:-1]
                elif evento.unicode.isdigit():
                    if foco_dimensoes:
                        entrada_dimensoes += evento.unicode
                    else:
                        entrada_taxa += evento.unicode
                elif evento.key == pygame.K_TAB:
                    foco_dimensoes = not foco_dimensoes


def main():
    dimensao, taxa_atualizacao = tela_inicial()
    if dimensao is not None and taxa_atualizacao is not None:
        pygame.init()
        tela = pygame.display.set_mode((TAMANHO_JANELA, TAMANHO_JANELA))
        pygame.display.set_caption("Labirinto")
        labirinto = Labirinto(dimensao)
        
        # Definir tamanho_celula e deslocamento_x, deslocamento_y aqui
        tamanho_celula = min(TAMANHO_JANELA // labirinto.labirinto.shape[1], TAMANHO_JANELA // labirinto.labirinto.shape[0])
        deslocamento_x = (TAMANHO_JANELA - tamanho_celula * labirinto.labirinto.shape[1]) // 2
        deslocamento_y = (TAMANHO_JANELA - tamanho_celula * labirinto.labirinto.shape[0]) // 2
        
        desenhar_labirinto(tela, labirinto.labirinto)
        tela_resolvida, caminho = resolver_labirinto(labirinto, tela, tamanho_celula, deslocamento_x, deslocamento_y, taxa_atualizacao=taxa_atualizacao)
        
        # Animar o caminho encontrado
        animar_caminho_encontrado(tela_resolvida, caminho, tamanho_celula, deslocamento_x, deslocamento_y)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    main()
            pygame.display.flip()

if __name__ == "__main__":
    main()