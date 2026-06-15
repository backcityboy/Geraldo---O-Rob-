# === BIBLIOTECAS QUE VAMOS USAR ===

import pygame      # biblioteca pra fazer jogos, desenhar na tela e ler as teclas do teclado
import sys         # serve pra fechar o script do python de verdade no final
import random      # biblioteca pra gerar numeros aleatórios tipo um dado


# === INICIANDO O JOGO ===

pygame.init() # esse comando inicializa todas as ferramentas do pygame pra não dar erro


# === CONFIGURANDO O TAMANHO DA TELA ===

TAMANHO_MAPA = 5
TAMANHO_CELULA = 100

LARGURA = 500
ALTURA = 580  

# cria a janela do jogo usando as constantes
TELA = pygame.display.set_mode((LARGURA, ALTURA))

# bota o título na barra lá em cima da janela do jogo
pygame.display.set_caption("O Bug do Milênio")


# === CARREGANDO AS IMAGENS ===

# Carrega e redimensiona a imagem do robô Geraldo
imagem_geraldo = pygame.image.load("image_1ee39c.png")
imagem_geraldo = pygame.transform.scale(imagem_geraldo, (70, 70))

# Carrega e redimensiona a imagem do Servidor
imagem_servidor = pygame.image.load("unnamed (2).png")
imagem_servidor = pygame.transform.scale(imagem_servidor, (80, 80))


# === VARIAVEIS DE CORES E TEXTO ===

# escolhe a fonte e o tamanho do texto
FONTE = pygame.font.SysFont(None, 30)

# escolha de cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (50, 100, 255)
VERDE = (0, 180, 0)
VERMELHO = (220, 50, 50)
CINZA = (180, 180, 180)


# === CONFIGURAÇÕES DO JOGADOR E COISAS FIXAS ===

# posição que o jogador começa no mapa
jogador_x = 0
jogador_y = 0

# x e y do servidor que fica no final do mapa
SERVIDOR_X = 4
SERVIDOR_Y = 4


# === STATUS DO JOGO ===

energia = 5
componentes_coletados = 0
mensagem = "" # começa sem mensagem nenhuma

game_over = False
vitoria = False


# === ONDE ESTÃO OS COMPONENTES ===

componentes = [
    (1, 0),
    (2, 2),
    (3, 1)
]


# === SORTEIO DA POSIÇÃO DE UM BUG NOVO ===

def gerar_posicao_bug():
    while True:
        sorteio_x = random.randint(0, 4) # sorteia a posição pro X
        sorteio_y = random.randint(0, 4) # sorteia a posição pro Y
        pos = (sorteio_x, sorteio_y)

        # evita que o bug apareça na casa que já exista algo
        if pos == (jogador_x, jogador_y):
            continue
        if pos == (SERVIDOR_X, SERVIDOR_Y):
            continue
        if pos in componentes:
            continue
        if pos in bugs:
            continue
            
        return pos # se passou em todos os testes, aceita essa posição


# === CRIANDO OS 3 BUGS DO COMEÇO DO JOGO ===

bugs = []

while len(bugs) < 3:
    sorteio_x = random.randint(0, 4)
    sorteio_y = random.randint(0, 4)
    posicao = (sorteio_x, sorteio_y)
   
    # Não pode começar no inicio (0,0), nem no servidor (4,4) e nem nos componentes
    if posicao != (0, 0) and posicao != (4, 4) and posicao not in componentes and posicao not in bugs:
        bugs.append(posicao) # adiciona o bug na lista


# === FUNÇÃO PRA MUDAR O TEXTO DE ALERTA ===

def mostrar_mensagem(texto):
    global mensagem
    mensagem = texto


# === CONFERE O QUE TEM NA CASA QUE O JOGADOR PISOU ===

def verificar_posicao():
    global energia
    global componentes_coletados
    global game_over
    global vitoria

    posicao_atual = (jogador_x, jogador_y)

    # Vê se tem componente pra pegar
    if posicao_atual in componentes:
        componentes.remove(posicao_atual) # tira o componente da lista pra sumir
        componentes_coletados = componentes_coletados + 1
        mostrar_mensagem("Componente coletado!")

    # Vê se pisou no bug
    if posicao_atual in bugs:
        bugs.remove(posicao_atual) # tira o bug dali
        energia = energia - 1 # perde vida
        mostrar_mensagem("Bug Corruptor encontrado! -1 energia")

        # Bota o bug em outro lugar aleatório pro mapa não ficar vazio
        nova_posicao = gerar_posicao_bug()
        bugs.append(nova_posicao)

        # Se a energia acabar, perde o jogo
        if energia <= 0:
            mostrar_mensagem("Game Over! O Bug do Milênio corrompeu o Geraldo.")
            game_over = True
            return

    # Vê se chegou no Servidor Final
    if jogador_x == SERVIDOR_X and jogador_y == SERVIDOR_Y:
        if componentes_coletados >= 3:
            mostrar_mensagem("Vitória! Servidor reparado.")
            vitoria = True
        else:
            mostrar_mensagem("Componentes insuficientes para realizar o reparo.")


# === FUNÇÃO QUE DESENHA AS COISAS NA TELA ===

def desenhar_tela():
    # pinta o fundo de branco
    TELA.fill(BRANCO)

    # Desenha os quadradinhos do mapa
    for linha in range(TAMANHO_MAPA):
        for coluna in range(TAMANHO_MAPA):
            # cria a forma de um retângulo especificando onde ele fica e o tamanho
            quadrado = pygame.Rect(coluna * TAMANHO_CELULA, linha * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
            # desenha o retângulo na tela usando a cor cinza
            pygame.draw.rect(TELA, CINZA, quadrado, 1)

    # Desenha a imagem do Servidor e posiciona ele
    TELA.blit(imagem_servidor, (SERVIDOR_X * TAMANHO_CELULA + 10, SERVIDOR_Y * TAMANHO_CELULA + 10))

    # Desenha a imagem do Jogador (Cyber-Geraldo)
    TELA.blit(imagem_geraldo, (jogador_x * TAMANHO_CELULA + 15, jogador_y * TAMANHO_CELULA + 15))

    # Escreve os textos na parte de baixo da tela
    # transforma a string de texto em uma imagem que pode ser desenhada, passando o texto e a cor
    texto_status = FONTE.render(f"Energia: {energia} | Componentes: {componentes_coletados}", True, PRETO)
    # esse comando blit serve pra colar uma imagem ou texto em cima da tela principal
    TELA.blit(texto_status, (10, ALTURA - 70))

    texto_mensagem = FONTE.render(mensagem, True, VERMELHO)
    TELA.blit(texto_mensagem, (10, ALTURA - 35))

    # mostra tudo que a gente desenhou de uma vez só pro jogador ver na tela
    pygame.display.flip()


# === LOOP PRINCIPAL DO JOGO (FICA RODANDO SEM PARAR) ===


while True:

    # faz a leitura de tudo que aconteceu no computador tipo cliques ou teclas apertadas
    for evento in pygame.event.get():

        # Se o usuário clicou no X da janela pra fechar
        if evento.type == pygame.QUIT:
            pygame.quit() # desliga as coisas internas do pygame
            sys.exit()    # fecha o programa python de vez pra não continuar rodando no fundo

        # Se o usuario apertou uma tecla
        if evento.type == pygame.KEYDOWN and not game_over and not vitoria:

            novo_x = jogador_x
            novo_y = jogador_y

            # Ve qual tecla foi apertada (letras ou setas) e muda a posição do jogador
            if evento.key == pygame.K_w or evento.key == pygame.K_UP:
                novo_y = novo_y - 1
            elif evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                novo_y = novo_y + 1
            elif evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                novo_x = novo_x - 1
            elif evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                novo_x = novo_x + 1

            # Confere se está dentro do limite do mapa
            if 0 <= novo_x < 5 and 0 <= novo_y < 5:
                jogador_x = novo_x
                jogador_y = novo_y
                verificar_posicao() # só checa o tabuleiro se a posição é válida
            else:
                mostrar_mensagem("Ops! Local não permitido.")

    # mostra as atualizações na tela
    desenhar_tela()

    # Se ganhou ou perdeu, o jogo para
    if game_over or vitoria:
        # faz o programa ter um delay pro jogador ler a mensagem
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()