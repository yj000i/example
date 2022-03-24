import os
import pygame
import sys
import random
from time import sleep

dir = os.path.realpath(__file__)
path = os.path.abspath(os.path.join(dir, os.pardir))
os.chdir(path)

padWidth = 480
padHeight = 640
meteos = ['meteo01.png', 'meteo02.png', 'meteo03.png', 'meteo04.png',
          'meteo05.png', 'meteo06.png', 'meteo07.png', 'meteo08.png']
explosion = ['explosion.png']
ex_sound = ['ex01.wav', 'ex02.wav', 'ex03.wav', 'ex04.wav']


def Score(count):
    global game_map
    font = pygame.font.Font('HGRKK.ttc', 15)
    board = font.render("破壊した隕石の数：" + str(count), True, (255, 255, 255))
    game_map.blit(board, (10, 0))


def Passed(count):
    global game_map
    font = pygame.font.Font('HGRKK.ttc', 15)
    board = font.render("逃した隕石の数：" + str(count), True, (255, 0, 0))
    game_map.blit(board, (300, 0))


# Game Over
def Message(text):
    global game_map, game_over_sound
    text_font = pygame.font.Font('HGRKK.ttc', 50)
    notice = text_font.render(text, True, (255, 0, 0))
    notice_pos = notice.get_rect()
    notice_pos.center = (padWidth/2, padHeight/2)

    game_map.blit(notice, notice_pos)
    pygame.display.update()

    pygame.mixer.music.stop()
    game_over_sound.play()

    sleep(2)

    pygame.mixer.music.play(-1)
    runGame()


def drawObject(obj, x, y):
    global game_map
    game_map.blit(obj, (x, y))

# 被弾


def crash():
    global game_map
    Message("被弾しました！")


def game_over():
    global game_map
    Message("Game Over")


def initGame():
    global game_map, clock, background, aircraft, projectile, explosion, projectile_sound, game_over_sound
    pygame.init()
    game_map = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('ShootingStar')
    background = pygame.image.load('background.png')
    clock = pygame.time.Clock()

    aircraft = pygame.image.load('aircraft.png')
    projectile = pygame.image.load('projectile.png')
    explosion = pygame.image.load('explosion.png')

    # audio
    pygame.mixer.music.load('bgm.wav')
    pygame.mixer.music.play(-1)  # bgm play
    projectile_sound = pygame.mixer.Sound('projectile.wav')
    game_over_sound = pygame.mixer.Sound('gameover.wav')


def runGame():
    global game_map, clcok, background, aircraft, projectile, explosion, projectile_sound

    # 戦闘機size
    aircraft_size = aircraft.get_rect().size
    aircraft_width = aircraft_size[0]
    aircraft_height = aircraft_size[1]

    # 戦闘機デフォルト
    x = padWidth * 0.45
    y = padHeight * 0.8
    aircraft_X = 0

    # projectile デフォルト
    projectile_XY = []

    # meteo ランダム生成（最初）
    meteo = pygame.image.load(random.choice(meteos))
    meteo_size = meteo.get_rect().size
    meteo_width = meteo_size[0]
    meteo_height = meteo_size[1]

    meteo_X = random.randrange(0, padWidth - meteo_width)
    meteo_Y = 0
    meteo_sound = pygame.mixer.Sound(random.choice(ex_sound))

    meteo_speed = 3

    # はずれ
    shot = False
    count = 0
    meteo_passed = 0

    inGame = False
    while not inGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    aircraft_X -= 3

                elif event.key == pygame.K_RIGHT:
                    aircraft_X += 3

                elif event.key == pygame.K_LCTRL:
                    projectile_sound.play()
                    projectile_X = 0.95*x
                    projectile_Y = y - aircraft_height
                    projectile_XY.append([projectile_X, projectile_Y])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # キーを押さないと動かないように
                    aircraft_X = 0

        drawObject(background, 0, 0)

        x += aircraft_X
        if x < 0:
            x = 0
        elif x > padWidth - aircraft_width:
            x = padWidth - aircraft_width

        drawObject(aircraft, x, y)

        # projectile
        if len(projectile_XY) != 0:
            for i, pxy in enumerate(projectile_XY):
                pxy[1] -= 5
                projectile_XY[i][1] = pxy[1]

                if pxy[1] < meteo_Y:  # 当たった時(projectile)
                    if pxy[0] > meteo_X and pxy[0] < meteo_X + meteo_width:
                        projectile_XY.remove(pxy)
                        shot = True
                        count += 1

                if pxy[1] <= 0:
                    try:
                        projectile_XY.remove(pxy)  # Mapから離れたprojectile除去
                    except:
                        pass

        if len(projectile_XY) != 0:
            for px, py in projectile_XY:
                drawObject(projectile, px, py)

        # meteo
        Score(count)

        meteo_Y += meteo_speed

        # 新しいmeteo
        if meteo_Y > padHeight:
            meteo = pygame.image.load(random.choice(meteos))
            meteo_size = meteo.get_rect().size
            meteo_width = meteo_size[0]
            meteo_height = meteo_size[1]
            meteo_sound = pygame.mixer.Sound(random.choice(ex_sound))

            meteo_X = random.randrange(0, padWidth - meteo_width)
            meteo_Y = 0
            meteo_passed += 1

        if meteo_passed == 3:
            game_over()

        Passed(meteo_passed)

        # 被弾判定
        if y < meteo_Y + meteo_height:
            if(meteo_X > x and meteo_X < x + aircraft_width) or \
                    (meteo_X + meteo_width > x and meteo_X + meteo_width < x + aircraft_width):
                crash()

        if shot:  # 当たった時(meteo)
            drawObject(explosion, meteo_X, meteo_Y)
            meteo_sound.play()

            meteo = pygame.image.load(random.choice(meteos))
            meteo_size = meteo.get_rect().size
            meteo_width = meteo_size[0]
            meteo_height = meteo_size[1]

            meteo_X = random.randrange(0, padWidth - meteo_width)
            meteo_Y = 0
            shot = False

            # speed up!
            meteo_speed += 0.05
            if meteo_speed >= 10:
                meteo_speed = 10

        drawObject(meteo, meteo_X, meteo_Y)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


initGame()
runGame()
