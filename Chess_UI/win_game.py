# coding:utf-8
import sys
import pygame
import random
import os.path
from MyChess.Chess_Core import Chessboard
# from MyChess.Chess_Core.Chessboard import lnotdark
# from MyChess.Chess_Core import Point
from MyChess.Chess_Core import Chessman
from pygame.locals import *


main_dir = os.path.split(os.path.abspath(__file__))[0]
# (left, top, width, height)
# SCREENRECT = Rect(0, 0, 720, 800)
SCREENRECT = Rect(0, 0, 720, 960)


red_dead = []
black_dead = []


def draw_dead_chessman(chessman, screen):
    red_new = True
    black_new = True
    name = chessman.name.split('_')[1]
    if chessman.is_red:
        if chessman.is_dark:
            for i in range(len(red_dead)):
                if 'dark' in red_dead[i]:
                    red_dead[i] = add_one(red_dead[i])
                    red_new = False
                    break
            if red_new:
                red_dead.append('dark')
        else:
            for i in range(len(red_dead)):
                if name in red_dead[i]:
                    red_dead[i] = add_one(red_dead[i])
                    red_new = False
                    break
            if red_new:
                red_dead.append('red_' + name)
    else:
        if chessman.is_dark:
            for i in range(len(black_dead)):
                if 'dark' in black_dead[i]:
                    black_dead[i] = add_one(black_dead[i])
                    black_new = False
                    break
            if black_new:
                black_dead.append('dark')
        else:
            for i in range(len(black_dead)):
                if name in black_dead[i]:
                    black_dead[i] = add_one(black_dead[i])
                    black_new = False
                    break
            if black_new:
                black_dead.append('black_' + name)

    draw_dead_image(red_dead, black_dead, screen)

def add_one(image_name):
    if 'dark' in image_name:
        if image_name.count('_') == 0:
            name = image_name + '_2'
        else:
            current_num = image_name.split('_')[-1]
            num = int(current_num)
            num += 1
            name = image_name.replace(current_num, str(num))
    else:
        if image_name.count('_') == 1:
            name = image_name + '_2'
        else:
            current_num = image_name.split('_')[-1]
            num = int(current_num)
            num += 1
            name = image_name.replace(current_num, str(num))
    return name



def draw_dead_image(red_dead, black_dead, screen):
    for i in range(len(red_dead)):
        screen.blit(load_image(red_dead[i] + ".jpg"), ((8-i) * 80, 0))
    for j in range(len(black_dead)):
        screen.blit(load_image(black_dead[j] + ".jpg"), (j * 80, 11 * 80))

    # ball = load_image("red_pawn_2.png")  # 加载图片
    # screen.blit(load_image("red_pawn_2.png"), (0, 11 * 80))

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'Img', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    return surface.convert()


def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


class Chessman_Sprite(pygame.sprite.Sprite):
    is_selected = False
    images = []
    is_transparent = False

    def __init__(self, images, chessman):
        pygame.sprite.Sprite.__init__(self)
        self.chessman = chessman
        self.images = images
        self.image = self.images[0]
        self.rect = Rect(chessman.col_num * 80,
                         (10 - chessman.row_num) * 80,  80,  80)

    def move(self, col_num, row_num): #c,r为要去的位置
        old_col_num = self.chessman.col_num
        old_row_num = self.chessman.row_num
        is_correct_position = self.chessman.move(col_num, row_num)
        if is_correct_position:
            self.rect.move_ip((col_num - old_col_num)
                              * 80, (old_row_num - row_num) * 80)
            self.rect = self.rect.clamp(SCREENRECT)
            self.chessman.chessboard.clear_chessmans_moving_list()
            self.chessman.chessboard.calc_chessmans_moving_list()
            return True
        return False

    def update(self):
        if self.is_selected:
            if self.is_transparent:
                self.image = self.images[1]
            else:
                self.image = self.images[0]
            self.is_transparent = not self.is_transparent
        else:
            self.image = self.images[0]

# 生成chessman_sprite并加到chessmans中
def creat_sprite_group(sprite_group, chessmans_hash):
    for chessman in chessmans_hash.values():
        if isinstance(chessman, Chessman.King):
            if chessman.is_red:
                images = load_images("red_king.gif", "transparent.gif")
            else:
                images = load_images("black_king.gif", "transparent.gif")
        else:
            images = load_images("dark.gif", "transparent.gif")

        chessman_sprite = Chessman_Sprite(images, chessman)
        sprite_group.add(chessman_sprite)

def replace_sprite_group(sprite_group, chessman):
    if chessman.is_red:
        if isinstance(chessman, Chessman.Rook):
            images = load_images("red_rook.gif", "transparent.gif")
        elif isinstance(chessman, Chessman.Cannon):
            images = load_images("red_cannon.gif", "transparent.gif")
        elif isinstance(chessman, Chessman.Knight):
            images = load_images("red_knight.gif", "transparent.gif")
        elif isinstance(chessman, Chessman.Elephant):
            images = load_images("red_elephant.gif", "transparent.gif")
        elif isinstance(chessman, Chessman.Mandarin):
            images = load_images("red_mandarin.gif", "transparent.gif")
        else:
            images = load_images("red_pawn.gif", "transparent.gif")
    else:
        if isinstance(chessman, Chessman.Rook):
            images = load_images("black_rook.gif", "transparent.gif")
        elif isinstance(chessman, Chessman.Cannon):
            images = load_images("black_cannon.gif", "transparent.gif")
        elif isinstance(chessman, Chessman.Knight):
            images = load_images("black_knight.gif", "transparent.gif")
        elif isinstance(chessman, Chessman.Elephant):
            images = load_images("black_elephant.gif", "transparent.gif")
        elif isinstance(chessman, Chessman.Mandarin):
            images = load_images("black_mandarin.gif", "transparent.gif")
        else:
            images = load_images("black_pawn.gif", "transparent.gif")
    chessman_sprite = Chessman_Sprite(images, chessman)
    sprite_group.add(chessman_sprite)

def select_sprite_from_group(sprite_group, col_num, row_num):
    for sprite in sprite_group:
        if sprite.chessman.col_num == col_num and sprite.chessman.row_num == row_num:
            return sprite


def add_col_row(chessman, col_num, row_num):
    chessman.col_num = col_num
    chessman.row_num = row_num

def translate_hit_area(screen_x, screen_y):
    return screen_x // 80, 10 - screen_y // 80


def main(winstyle=0):

    pygame.init()
    # Pick the best color depth for a display mode
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    # Initialize a window or screen for display
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pygame.display.set_caption("揭棋")
    # create the background, tile the bgd image
    # bgdtile = load_image('boardchess.gif')
    bgdtile = load_image('qp.png')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0)) # blit(): draw many images onto another
    pygame.display.flip() # flip(): Update the full display Surface to the screen
    cbd = Chessboard.Chessboard('000')
    cbd.init_board()
    cbd.get_bright_chessman()

    chessmans = pygame.sprite.Group()
    framerate = pygame.time.Clock()

    # 生成chessman_sprite并且加到chessmans中
    creat_sprite_group(chessmans, cbd.chessmans_hash)
    current_chessman = None # 要移动的棋子

    cbd.calc_chessmans_moving_list() # 计算棋子行动路径
    count = 0 # 无吃子回合数
    while not cbd.is_end(count):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # 返回按键按下情况，返回的是一元组，分别为(左键, 中键, 右键)，如按下则为True
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if index == 0 and pressed_array[index]:
                        # 返回当前鼠标位置(x, y)
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        col_num, row_num = translate_hit_area(mouse_x, mouse_y)
                        # chessman_sprite：点击位置的棋子
                        chessman_sprite = select_sprite_from_group(
                            chessmans, col_num, row_num)
                        if current_chessman is None and chessman_sprite != None:
                            if chessman_sprite.chessman.is_red == cbd.is_red_turn:
                                current_chessman = chessman_sprite
                                chessman_sprite.is_selected = True
                        elif current_chessman != None and chessman_sprite != None:
                            # 如果在已点击棋子基础上再点击同方棋子
                            if chessman_sprite.chessman.is_red == cbd.is_red_turn:
                                current_chessman.is_selected = False
                                current_chessman = chessman_sprite
                                chessman_sprite.is_selected = True
                            else:
                                success = current_chessman.move(
                                    col_num, row_num)

                                if success: # 成功移动棋子（吃子）
                                    count = 0
                                    chessmans.remove(chessman_sprite)
                                    draw_dead_chessman(chessman_sprite.chessman, screen)
                                    if current_chessman.chessman.is_dark:
                                        cbd.d_to_b[current_chessman.chessman].add_to_board(col_num, row_num)
                                        # add_col_row(cbd.lnotdark[0], col_num, row_num)
                                        replace_sprite_group(chessmans, cbd.d_to_b[current_chessman.chessman])
                                        chessmans.remove(current_chessman)
                                        current_chessman.kill()
                                    else:
                                        chessman_sprite.kill()
                                        current_chessman.is_selected = False
                                        current_chessman = None
                        elif current_chessman != None and chessman_sprite is None:
                            success = current_chessman.move(col_num, row_num)
                            # 成功移动棋子（没吃子）
                            if success:
                                count += 0.5
                                if current_chessman.chessman.is_dark:
                                    cbd.d_to_b[current_chessman.chessman].add_to_board(col_num, row_num)
                                    replace_sprite_group(chessmans, cbd.d_to_b[current_chessman.chessman])
                                    chessmans.remove(current_chessman)
                                    current_chessman.kill()
                                else:
                                    current_chessman.is_selected = False
                                    current_chessman = None

        framerate.tick(20)
        # clear/erase the last drawn sprites
        chessmans.clear(screen, background)

        # update all the sprites
        # call the update method on contained Sprites
        chessmans.update()
        # blit the Sprite images
        chessmans.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
