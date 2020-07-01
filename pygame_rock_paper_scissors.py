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
        self.hitbox = (self.x-4*3, self.y-4*3, 10*3, 18*3)

    def movement_controls(self, left_key, right_key, up_key, down_key):
        if keys[left_key] and self.x > 32 + self.spd:
            self.x -= self.spd
        if keys[right_key] and self.x < win_w - 32 - self.spd:
            self.x += self.spd
        if keys[up_key] and self.y > 32 + self.spd:
            self.y -= self.spd
        if keys[down_key] and self.y < win_h - 64 - self.spd:
            self.y += self.spd

    def draw_hitbox(self, win):
        self.hitbox = (self.x-4*3, self.y-4*3, 10*3, 18*3)
        pygame.draw.rect(win, (0, 0, 200), self.hitbox, 2)

class Projectile():
    def __init__(self, x, y, direction, spd, spr_index, variety):
        self.x = x
        self.y = y
        self.direction = direction
        self.vel = direction * spd
        self.spr_index = spr_index
        self.variety = variety
        self.hitbox = (self.x-8*3, self.y-8*3, 16*3, 16*3)

    def draw_hitbox(self, win):
        self.hitbox = (self.x-8*3, self.y-8*3, 16*3, 16*3)
        pygame.draw.rect(win, (0, 0, 200), self.hitbox, 2)

    # decide player 1 and player 2 projectile collisions for the RPS mechanic
    def bullet_collision(self, targ_bullet, all_bullets):
        for test_bullet in all_bullets:
            if test_bullet == targ_bullet:
                pass
            elif check_collision(targ_bullet, test_bullet):
                if targ_bullet.direction == 1:
                    player_1_proj = targ_bullet
                    player_2_proj = test_bullet
                elif targ_bullet.direction == -1:
                    player_2_proj = targ_bullet
                    player_1_proj = test_bullet
                # running math to determine what bullet wins
                results = (player_1_proj.variety) - (player_2_proj.variety + 10)
                if results == -10:
                    all_bullets.pop(all_bullets.index(player_1_proj))
                    all_bullets.pop(all_bullets.index(player_2_proj))
                elif results == -12 or results == -9:
                    all_bullets.pop(all_bullets.index(player_2_proj))
                elif results == -8 or results == -11:
                    all_bullets.pop(all_bullets.index(player_1_proj))

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

def scale_sprite(sprite, sprite_size, cols, rows, scale_factor):
    """scale a sprite given the arguments"""
    return pygame.transform.scale(sprite, (cols*sprite_size*scale_factor, rows*sprite_size*scale_factor))

def check_collision(obj1, obj2): # requires objects to have defined hitboxes
    # collision check on the y-axis
    if obj1.hitbox[1] < obj2.hitbox[1] + obj2.hitbox[3] and obj1.hitbox[1] + obj1.hitbox[3] > obj2.hitbox[1]:
        if obj1.hitbox[0] < obj2.hitbox[0] + obj2.hitbox[2] and obj1.hitbox[0] + obj1.hitbox[2] > obj2.hitbox[0]:
            return True

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

index_update = 5 # update sprite every 5 frames (out of 60 FPS (12 sprite frams per second))

# shooting cooldown timer used in conjuction with Player.cooldown
player_1_shoot_timer = 0
player_2_shoot_timer = 0

# projectile speed for all players
proj_spd = 8

player_1 = Player(mode='player', color=(50, 50, 250), x=50, y=win_h/2-25, spd=6, cooldown=40)
player_2 = Player(mode='player', color=(50, 175, 50), x=win_w-100, y=win_h/2-25, spd=6, cooldown=40)

player_1_has_control = True
player_2_has_control = True

# load, scale, and set sprites

# player sprites
spr_knight_file = pygame.image.load("spr_rpss_knight.png")
spr_orc_file = pygame.image.load("spr_rpss_orc.png")

spr_knight_scaled = scale_sprite(spr_knight_file, 32, 7, 3, 3)
spr_orc_scaled = scale_sprite(spr_orc_file, 32, 7, 3, 3)

spr_knight = SpriteSheet(spr_knight_scaled, 7, 3)
spr_orc = SpriteSheet(spr_orc_scaled, 7, 3)

# projectile sprites
spr_proj_file = pygame.image.load("spr_rpss_projectiles.png")
spr_proj_scaled = scale_sprite(spr_proj_file, 32, 3, 1, 3)
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

    win.fill((200, 200, 200))

    # draw the character referencing the draw method in the class, SpritSheet()
    spr_knight.draw(win, (index % 4)+7, player_1.x, player_1.y, CENTER_HANDLE)
    spr_orc.draw(win, (index % 4)+7, player_2.x, player_2.y, CENTER_HANDLE)

    # updating hitbox location to the players location
    player_1.draw_hitbox(win)
    player_2.draw_hitbox(win)


    # checking bullet collisions with one another
    for bullet in bullets:
        bullet.bullet_collision(targ_bullet=bullet, all_bullets=bullets)

    for bullet in bullets:
        if bullet.direction == 1:
            if check_collision(bullet, player_2):
                bullets.pop(bullets.index(bullet))
        elif bullet.direction == -1:
            if check_collision(bullet, player_1):
                bullets.pop(bullets.index(bullet))
        if bullet.x > 0 and bullet.x < win_w:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))   

    # draw bullets from the bullets list
    for bullet in bullets:
        if bullet.direction == 1:
            spr_proj.draw(win, bullet.spr_index, bullet.x, bullet.y, handle=CENTER_HANDLE)
            bullet.draw_hitbox(win)
        if bullet.direction == -1:
            spr2_proj.draw(win, bullet.spr_index, bullet.x, bullet.y, handle=CENTER_HANDLE)
            bullet.draw_hitbox(win)

    # sprite (index) frame rate
    index_timer += 1
    if index_timer >= index_update:
        index_timer = 0
        index += 1

    keys = pygame.key.get_pressed()

    # RPS shoot timers counting down; stops at zero
    if player_1_shoot_timer > 0:
        player_1_shoot_timer -= 1

    if player_2_shoot_timer > 0:
        player_2_shoot_timer -= 1

    # player 1 controls (and screen boundaries)
    if player_1_has_control:

        # shooting
        if player_1_shoot_timer <= 0:
            if keys[pygame.K_f]:
                bullets.append(Projectile(player_1.x+8*3, player_1.y+16, 1, proj_spd, spr_index=0, variety=1)) # rock
                player_1_shoot_timer = player_1.cooldown
            elif keys[pygame.K_g]:
                bullets.append(Projectile(player_1.x+8*3, player_1.y+16, 1, proj_spd, spr_index=1, variety=2)) # paper
                player_1_shoot_timer = player_1.cooldown
            elif keys[pygame.K_h]:
                bullets.append(Projectile(player_1.x+8*3, player_1.y+16, 1, proj_spd, spr_index=2, variety=3)) # scissors
                player_1_shoot_timer = player_1.cooldown

        # movement
        player_1.movement_controls(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
 
    # player 2 controls (and screen boundaries)
    if player_2_has_control:

        # shooting
        if player_2_shoot_timer <= 0:
            if keys[pygame.K_RSHIFT]:
                bullets.append(Projectile(player_2.x-8*3, player_2.y+16, -1, proj_spd, spr_index=2, variety=1)) # rock
                player_2_shoot_timer = player_2.cooldown
            elif keys[pygame.K_RETURN]:
                bullets.append(Projectile(player_2.x-8*3, player_2.y+16, -1, proj_spd, spr_index=1, variety=2)) # paper
                player_2_shoot_timer = player_2.cooldown
            elif keys[pygame.K_BACKSLASH]:
                bullets.append(Projectile(player_2.x-8*3, player_2.y+16, -1, proj_spd, spr_index=0, variety=3)) # scissors
                player_2_shoot_timer = player_2.cooldown

        # movement
        player_2.movement_controls(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

    pygame.display.update()

pygame.quit()