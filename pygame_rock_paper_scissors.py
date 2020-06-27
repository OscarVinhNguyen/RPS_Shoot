"""
Rock, Paper, Scissor, Shoot (w/ PYGAME)
Made by Oscar-Vinh Nguyen
07/20/2020
"""



import pygame
import time

class Player():
    def __init__(self, mode, color, x, y, spd, cooldown):
        self.mode = mode # "player" or "computer"
        self.color = color
        self.x = x
        self.y = y
        self. spd = spd
        self.cooldown = cooldown

class Projectile():
    def __init__(self, x, y, direction, spd, variety):
        self.x = x
        self.y = y
        self.direction = direction
        self.vel = direction * spd
        self.variety = variety

class SpriteSheet():
    def __init__(self, sheet, cols, rows):
        self.sheet = sheet
        self.cols = cols
        self.rows = rows
        self.total_cell_count = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cell_w = self.rect.width/cols
        h = self.cell_h = self.rect.height/rows
        hw, hh = self.cell_center = (w/2, h/2)

        self.cells = list([(index % cols * w, index//cols * h, w, h) for index in range(self.total_cell_count)])
        # origin posistion, which can be transformed to different positions
        self.handle = list([
            (0,0), (-hw,0), (-w,0), 
            (0,-hh), (-hw,-hh), (-w,-hh), 
            (0,-h), (-hw,-h), (-w,-h)])

    def draw(self, surface, cell_index, x, y, handle=0):
        surface.blit(self.sheet, (x+self.handle[handle][0], y+self.handle[handle][1]), self.cells[cell_index])

def sprite_scale(sprite, sprite_size, cols, rows, scale_factor):
    """scale a sprite given the arguments"""
    scaled_sprite = pygame.transform.scale(sprite, (cols*sprite_size*scale_factor, rows*sprite_size*scale_factor))
    return scaled_sprite

# def redraw_game_window (needed?)

# variables
win_w = 1280
win_h = 756
win = pygame.display.set_mode((win_w, win_h))

pygame.display.set_caption("Rock, Paper, Scissors, Shoot")

FPS = 60 # 60 frames per second that will be set later in the run loop: clock.tick(FPS)
clock = pygame.time.Clock()

CENTER_HANDLE = 4 # center origin position

index = 0 # when drawing sprites
index_timer = 0 # timer when incrimenting sprites

index_update = 5 # update== sprite every 6 frames (out of 60 FPS (10 sprite frams per second))

# shooting cooldown timer used in conjuction with Player.cooldown
player_1_shoot_timer = 0
player_2_shoot_timer = 0

# projectile speed for all players
proj_spd = 10

player_1 = Player(mode='player', color=(50, 50, 250), x=50, y=win_h/2-25, spd=5, cooldown=60)
player_2 = Player(mode='player', color=(50, 175, 50), x=win_w-100, y=win_h/2-25, spd=5, cooldown=60)

player_1_has_control = True
player_2_has_control = True

# load, scale, and set sprites

# player sprites
spr_knight_file = pygame.image.load("spr_rpss_knight.png")
spr_orc_file = pygame.image.load("spr_rpss_orc.png")

spr_knight_scaled = sprite_scale(spr_knight_file, 32, 7, 3, 4)
spr_orc_scaled = sprite_scale(spr_orc_file, 32, 7, 3, 4)

spr_knight = SpriteSheet(spr_knight_scaled, 7, 3)
spr_orc = SpriteSheet(spr_orc_scaled, 7, 3)

# projectile sprites
spr_proj_file = pygame.image.load("spr_rpss_projectiles.png")
spr_proj_scaled = sprite_scale(spr_proj_file, 32, 3, 1, 3)
spr_proj = SpriteSheet(spr_proj_scaled, 3, 1)

spr2_proj_flipped = pygame.transform.flip(spr_proj_scaled, True, False)
spr2_proj = SpriteSheet(spr2_proj_flipped, 3, 1)

# bullet object list
bullets = []

# main run loop thingy
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

    for bullet in bullets:
        if bullet.x > 0 and bullet.x < win_w:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    win.fill((255, 255, 255))   

    for bullet in bullets:
        if bullet.direction == 1:
            spr_proj.draw(win, bullet.variety, bullet.x, bullet.y, handle=3)
        if bullet.direction == -1:
            spr2_proj.draw(win, bullet.variety, bullet.x, bullet.y, handle=5)

    # draw the character referencing the draw method in the class, SpritSheet()
    spr_knight.draw(win, (index % 4)+7, player_1.x, player_1.y, CENTER_HANDLE)
    spr_orc.draw(win, (index % 4)+7, player_2.x, player_2.y, CENTER_HANDLE)

    # sprite (index) frame rate
    index_timer += 1
    if index_timer >= index_update:
        index_timer = 0
        index += 1

    keys = pygame.key.get_pressed()

    if player_1_shoot_timer > 0:
        player_1_shoot_timer -= 1

    if player_2_shoot_timer > 0:
        player_2_shoot_timer -= 1

    # player 1 controls (and screen boundaries)
    if player_1_has_control:

        # shooting
        if player_1_shoot_timer <= 0:
            if keys[pygame.K_f]:
                bullets.append(Projectile(player_1.x+16, player_1.y+16, 1, proj_spd, variety=0)) # rock
                player_1_shoot_timer = player_1.cooldown
            elif keys[pygame.K_g]:
                bullets.append(Projectile(player_1.x+16, player_1.y+16, 1, proj_spd, variety=1)) # paper
                player_1_shoot_timer = player_1.cooldown
            elif keys[pygame.K_h]:
                bullets.append(Projectile(player_1.x+16, player_1.y+16, 1, proj_spd, variety=2)) # scissors
                player_1_shoot_timer = player_1.cooldown

        # movement
        if keys[pygame.K_a] and player_1.x > 32 + player_1.spd:
            player_1.x -= player_1.spd
        if keys[pygame.K_d] and player_1.x < win_w - 32 - player_1.spd:
            player_1.x += player_1.spd
        if keys[pygame.K_w] and player_1.y > 32 + player_1.spd:
            player_1.y -= player_1.spd
        if keys[pygame.K_s] and player_1.y < win_h - 64 - player_1.spd:
            player_1.y += player_1.spd
 
    # player 2 controls (and screen boundaries)
    if player_2_has_control:

        # shooting
        if player_2_shoot_timer <= 0:
            if keys[pygame.K_RSHIFT]:
                bullets.append(Projectile(player_2.x-16, player_2.y+16, -1, proj_spd, variety=2)) # rock
                player_2_shoot_timer = player_2.cooldown
            elif keys[pygame.K_RETURN]:
                bullets.append(Projectile(player_2.x-16, player_2.y+16, -1, proj_spd, variety=1)) # paper
                player_2_shoot_timer = player_2.cooldown
            elif keys[pygame.K_BACKSLASH]:
                bullets.append(Projectile(player_2.x-16, player_2.y+16, -1, proj_spd, variety=0)) # scissors
                player_2_shoot_timer = player_2.cooldown

        # movement
        if keys[pygame.K_LEFT] and player_2.x > 32 + player_2.spd:
            player_2.x -= player_2.spd
        if keys[pygame.K_RIGHT] and player_2.x < win_w - 32 - player_2.spd:
            player_2.x += player_2.spd
        if keys[pygame.K_UP] and player_2.y > 32 + player_2.spd:
            player_2.y -= player_2.spd
        if keys[pygame.K_DOWN] and player_2.y < win_h - 64 - player_2.spd:
            player_2.y += player_2.spd

    pygame.display.update()

pygame.quit()