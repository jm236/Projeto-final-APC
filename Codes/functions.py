import pygame
from random import randint

def escrever(string, tela, fonte, cor, x, y, tamanho):
    """
    Função que escreve uma mensagem na tela do jogo
    """
    font = pygame.font.SysFont(fonte, tamanho, True, True)
    texto = font.render(string, True, cor)
    tela.blit(texto, (x, y))
    pygame.display.flip()

def menu(tela, tam, largura, altura):
    """"
    Função que apresenta o menu inicial na tela
    """
    nome_do_jogo = 'GTA VII'
    vermelho = (255, 0, 0)
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    tela.fill(preto)
    
    escrever(nome_do_jogo, tela, "Monospace", vermelho, 225, 40, tam * 10)

    string = "1- Jogar"
    escrever(string, tela, "Monospace", branco, ((altura // 2) - 60), ((largura // 2) - 40), tam * 3)   

    string = "2- Configurações" 
    escrever(string, tela, "Monospace", branco, ((altura // 2) - 60), ((largura // 2) - 20), tam * 3)  

    string = "3- Ranking" 
    escrever(string, tela, "Monospace", branco, ((altura // 2) - 60), ((largura // 2)), tam * 3) 

    string = "4- Instruções" 
    escrever(string, tela, "Monospace", branco, ((altura // 2) - 60), ((largura // 2) + 20), tam * 3)

    string = "5- Sair" 
    escrever(string, tela, "Monospace", branco, ((altura // 2) - 60), ((largura // 2) + 40), tam * 3)  
    
    pygame.display.flip()

def escolhe_cor(element):
    """
    Função que escolhe a cor de acordo com o elemento do jogo (inimigo, jogador, bala ou combustível)
    """
    if  element == ' ':
        cor = (255, 255, 255)
    elif element == '+':
        cor = (0, 255, 0)
    elif element == 'X':
        cor = (255, 0, 0)
    elif element == '>':
        cor = (0, 100, 0)
    elif element == 'F':
        cor = (0, 0, 100)

    return cor

def desenhar(screen, cor, x, y, size):
    """"
    Função que desenha um elemento específico na tela do jogo
    """
    pygame.draw.rect(screen, cor, (x * size,
    y * size, size, size))

def mostrar_matriz(matriz, altura, largura, tela, tamanho, pont, energ, fonte):
    """
    Função que desenha todo o jogo na tela
    """
    tela.fill((255, 255, 255))

    for i in range(0, altura):
        for j in range(0, largura):
                    desenhar(tela, escolhe_cor(matriz[i][j]), j, i, tamanho) # desenho

    escrever(f'Energia: {energ}', tela, fonte, (0,0,0), 3, 0, tamanho)
    escrever(f'Pontuação: {pont}', tela, fonte, (0,0,0), 600, 0, tamanho)
    pygame.display.flip()

def mover_objetos(matriz, altura, largura, pont, energ):
    """
    função que move os objetos presentes no jogo(inimigos, balas e combustível)
    """

    # movimentação dos tiros
    i = 0
    j = 0
    while i < altura:
        while j < largura:
            if matriz[i][j] == '>':
                    if j < (largura - 1):
                        if matriz[i][j + 1] == ' ':
                            matriz[i][j + 1] = '>'
                            matriz[i][j] = ' '
                            j += 1

                        elif matriz[i][j + 1] == 'X' or matriz[i][j + 1] == 'F':
                            if matriz[i][j + 1] == 'X':
                                 pont += 50
                            matriz[i][j + 1] = ' '
                            matriz[i][j] = ' '

                    elif j == (largura - 1):
                        matriz[i][j] = ' '
            j += 1
        j = 0
        i += 1

    # movimentação dos inimigos e do combustível
    i = 0
    j = 0
    while i < altura:
        while j < largura:
            if matriz[i][j] == 'X':
                    if j > 0:
                        if matriz[i][j - 1] == ' ':
                            matriz[i][j - 1] = 'X'
                            matriz[i][j] = ' '
                            j += 1

                        elif matriz[i][j - 1] == '+': # morte do player
                            matriz[i][j - 1] = ' '
                            matriz[i][j] = ' '

                    elif j == 0:
                        matriz[i][j] = ' '
            elif matriz[i][j] == 'F':
                    if j > 0:
                        if matriz[i][j - 1] == ' ':
                            matriz[i][j - 1] = 'F'
                            matriz[i][j] = ' '
                            j += 1
                        elif matriz[i][j - 1] == '+': # aumento do combustivel
                            energ += 40
                            matriz[i][j] = ' '
                            j += 1
                    elif j == 0:
                        matriz[i][j] = ' '
            j += 1
        j = 0
        i += 1

    # retorno da matriz e dos valores da energia e pontuação após a movimentação    
    return matriz, pont, energ

def spawn(matriz, objeto, prob, limpar, qtde_max):
    """
    Função que spawna aleatoriamente inimigos ou combustível no mapa
    OBS: chance em porcentagem
    """
    b = randint(0, 100) 
    if b <= prob:
        qtde = randint(0, qtde_max) # qtde de inimigos que vão aparecer
        
        if qtde > 0:
                usadas = []
                for i in range(0, qtde):
                    while True:
                        y = randint(0, 9)

                        if y not in usadas:
                            matriz[y][134] = objeto 
                            usadas.append(y)
                            break
                if limpar:
                    del usadas

def morreu(matriz, altura, largura, comb):
    """
    Retorna se o jogador está morto ou vivo e o motivo da morte, respectivamente
    """
    for i in range(0, altura):
        for j in range(0, largura):
            if matriz[i][j] == '+':
                if comb <= 0:
                    return 'Sim gasosa'
                else:
                    return 'Não'
            
    return 'Sim atingido'
    
                        
def tela_morte(l, h, fonte, t, pont, motivo):
    screen = pygame.display.set_mode((h, l))
    screen.fill((0, 0, 0))

    escrever('GAME OVER', screen, fonte, (255, 0, 0), 175, 50, t * 10)
    escrever(f'Pontuação: {pont} pontos.', screen, fonte, (255, 255, 255), 235, 120, t * 3)
    escrever(motivo, screen, fonte, (255, 255, 255), 230, 140, t * 3)
    escrever('Aperte Enter para retornar ao menu.', screen, fonte, (255, 255, 255), 140, 250, t * 4)


    pygame.display.flip()