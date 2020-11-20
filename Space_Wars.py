import pygame
import random
import sys

pygame.font.init()
level = 1
play_game = True

fps = 30
width = 750
height = 700
alien_cooldown = 500
last_alien_shoot = pygame.time.get_ticks()
rows = level * 2 + 3

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SPACE WARS')
clock = pygame.time.Clock()
background = pygame.image.load('images/background1_7.jpg')
img = pygame.transform.scale(background, (750, 800))
spaceship = pygame.image.load('images/spaceship.png')
img1 = pygame.transform.scale(spaceship, (60, 50))
alien = pygame.image.load('images/alien(3).png')
img2 = pygame.transform.scale(alien, (50, 40))
lazer1 = pygame.image.load('images/lazer1.png')
img3 = pygame.transform.scale(lazer1, (20, 20))
shield = pygame.image.load('images/solar_panels.png')
img4 = pygame.transform.scale(shield, (10, 10))
lazer2 = pygame.image.load('images/lazer2.png')
img5 = pygame.transform.scale(lazer2, (20, 20))
win = pygame.image.load('images/win.png')
img6 = pygame.transform.scale(win, (750, 800))
lose = pygame.image.load('images/lose.png')
img7 = pygame.transform.scale(lose, (750, 800))
img8 = pygame.transform.scale(alien, (200, 100))

'''pygame.mixer.music.load('sounds/background_music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.20)
lazer_sound = pygame.mixer.Sound('sounds/lazer_sound.mp3')
lazer_sound.set_volume(0.25)
explosion1_sound = pygame.mixer.Sound('sounds/explosion1_sound.mp3')
explosion1_sound.set_volume(0.25)
sunpanels_sound = pygame.mixer.Sound('sounds/sun_panel_sound.mp3')
sunpanels_sound.set_volume(0.25)
alienbullet_sound = pygame.mixer.Sound('sounds/aliens_bullet_sound.mp3')
alienbullet_sound.set_volume(0.15)'''


class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img1
        self.rect = self.image.get_rect()
        self.rect.centerx = int(width / 2)
        self.rect.bottom = height - 50
        self.initial_health = 200
        self.remaining_health = 200

    def update(self):
        global play_game
        speed = 20
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.rect.x += speed
        elif key[pygame.K_LEFT]:
            self.rect.x -= speed
        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0

        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, (self.rect.bottom + 5), self.rect.width, 10))
        if self.remaining_health > 0:
            pygame.draw.rect(screen, (0, 255, 0), (
            self.rect.x, (self.rect.bottom + 5), int((self.rect.width) * (self.remaining_health / self.initial_health)),
            10))
        if pygame.sprite.spritecollide(self, alien_bullet_group, True):
            self.remaining_health -= 1
        if self.remaining_health == 0:
            self.kill()
            screen.blit(img7, (0, 0))
            for i in range(1000):
                f1 = pygame.font.SysFont('serif', 54)
                text1 = f1.render('GAME OVER!', True, (0, 0, 0))
                screen.blit(text1, (200, 430))
                pygame.display.update()
                i = i + 1
            play_game = False

    def shoot(self):
        lazer = Lazer(self.rect.centerx, self.rect.top)
        if len(spaceship_group) > 0:
            lazer_group.add(lazer)


class Lazer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img3
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, aliens_group, True):
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.top)
            explosion_group.add(explosion)
            '''explosion1_sound.play()'''
        if pygame.sprite.spritecollide(self, shields_group, True):
            self.kill()


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img2
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 5
        if abs(self.move_counter) > 500:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
            self.rect.y += 5

    def collide(self):
        if pygame.sprite.spritecollide(self, shields_group, True):
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.explosion = []
        for i in range(1, 6):
            img = pygame.image.load(f'images/exp{i}.png')
            img = pygame.transform.scale(img, (i * 5, i * 5))
            self.explosion.append(img)
        self.index = 0
        self.image = self.explosion[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.explosion) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.explosion[self.index]
        if self.index >= len(self.explosion) - 1 and self.counter >= explosion_speed:
            self.kill()


class Alien_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img5
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speedy = 15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False):
            self.kill()
            spaceship.remaining_health -= 1
        if pygame.sprite.spritecollide(self, shields_group, True):
            self.kill()


class Shields(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img4
        self.rect = self.image.get_rect()

    def update(self):
        if pygame.sprite.spritecollide(self, aliens_group, False):
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img8
        self.rect = self.image.get_rect()
        self.rect.centerx = int(width/2)
        self.rect.centery = int(height/2 - 300)
        self.health = 10
        self.remaining_health = 10
        self.move_direction=1
        self.move_counter=0
    def update(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, (self.rect.bottom -90), self.rect.width, 10))
        if self.remaining_health > 0:
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, (self.rect.bottom -90),
                int((self.rect.width) * (self.remaining_health / self.health)),
                10))
        if pygame.sprite.spritecollide(self, lazer_group, True):
            if len(aliens_group) == 0:
                self.remaining_health -= 1
        if self.remaining_health == 0:
            self.kill()
        self.rect.x += 4*self.move_direction
        self.move_counter += 4
        if abs(self.move_counter) > 275:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

class Boss_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img5
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speedy = 20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False):
            self.kill()
            spaceship.remaining_health -= 1

spaceship_group = pygame.sprite.Group()
spaceship = Spaceship()
spaceship_group.add(spaceship)
lazer_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
shields_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
boss = Boss()
boss_group.add(boss)
boss_bullets_group = pygame.sprite.Group()

def create_aliens(a, x, y):
    for row in range(1, a):
        for column in range(1, 11):
            alien = Aliens((x + (50 * column)), (y + (50 * row)))
            aliens_group.add(alien)


def count(s):
    screen.blit(img, (0, 0))
    if spaceship.remaining_health != 0:
        for i in range(500):
            f1 = pygame.font.SysFont('serif', 56)
            text1 = f1.render(s, True, (255, 255, 255))
            screen.blit(text1, (300, 300))
            pygame.display.update()
            i = i + 1
        screen.blit(img, (0, 0))
        for i in range(500):
            f1 = pygame.font.SysFont('serif', 56)
            text1 = f1.render('3', True, (255, 255, 255))
            screen.blit(text1, (350, 300))
            pygame.display.update()
            i = i + 1
        screen.blit(img, (0, 0))
        for i in range(500):
            f1 = pygame.font.SysFont('serif', 56)
            text1 = f1.render('2', True, (255, 255, 255))
            screen.blit(text1, (350, 300))
            pygame.display.update()
            i = i + 1
        screen.blit(img, (0, 0))
        for i in range(500):
            f1 = pygame.font.SysFont('serif', 56)
            text1 = f1.render('1', True, (255, 255, 255))
            screen.blit(text1, (350, 300))
            pygame.display.update()
            i = i + 1


def start(s):
    global play_game, last_alien_shoot
    count(s)
    play_game1 = play_game
    while play_game1:
        clock.tick(fps)
        screen.blit(img, (0, 0))
        time_now = pygame.time.get_ticks()
        if time_now - last_alien_shoot > alien_cooldown:
            if len(aliens_group) > 0:
                attacking_alien = random.choice(aliens_group.sprites())
                alien_bullet = Alien_Bullet(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                alien_bullet_group.add(alien_bullet)
                last_alien_shoot = time_now

        if s == 'Boss':
            if time_now - last_alien_shoot > alien_cooldown:
                if len(aliens_group) == 0:
                    if spaceship.rect.x >= boss.rect.left and spaceship.rect.x <= boss.rect.right:
                        boss_bullet = Boss_Bullets(spaceship.rect.x, boss.rect.bottom)
                        boss_bullets_group.add(boss_bullet)
                        '''alienbullet_sound.play()'''
                    elif spaceship.rect.x <= boss.rect.left:
                        boss_bullet = Boss_Bullets(boss.rect.x, boss.rect.bottom)
                        boss_bullets_group.add(boss_bullet)
                        '''alienbullet_sound.play()'''
                    elif spaceship.rect.x >= boss.rect.right:
                        boss_bullet = Boss_Bullets(boss.rect.right, boss.rect.bottom)
                        boss_bullets_group.add(boss_bullet)
                last_alien_shoot = pygame.time.get_ticks()

            boss_group.add(boss)
            boss_group.draw(screen)
            boss_bullets_group.draw(screen)
            boss_group.update()
            boss_bullets_group.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_game = False
                play_game1 = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spaceship.shoot()
                    '''lazer_sound.play()'''

        if spaceship.remaining_health == 0:
            play_game = False
            play_game1 = False

        spaceship_group.draw(screen)
        lazer_group.draw(screen)
        aliens_group.draw(screen)
        shields_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)

        spaceship_group.update()
        lazer_group.update()
        aliens_group.update()
        shields_group.update()
        alien_bullet_group.update()
        explosion_group.update()
        pygame.display.update()

        if len(aliens_group) == 0 and s != 'Boss':
            play_game1 = False
        elif len(boss_group) == 0 and s == 'Boss':
            play_game1 = False

screen.blit(img, (0, 0))
for i in range(700):
    f1 = pygame.font.SysFont('serif', 48)
    text1 = f1.render('SPACE WARS', True, (255, 255, 255))
    screen.blit(text1, (250, 300))
    pygame.display.update()
    i = i + 1
screen.blit(img, (0, 0))

# count('Level 1')

create_aliens(5, 80, 30)
for shield in range(4):
    for row in range(5):
        for column in range(10):
            shields = Shields()
            shields.rect.x = (50 + (195 * shield)) + (10 * column)
            shields.rect.y = 500 + (10 * row)
            shields_group.add(shields)
start('Level 1')

create_aliens(7, 80, 30)
fps = 45
alien_cooldown = 400
for shield in range(4):
    for row in range(3):
        for column in range(10):
            shields = Shields()
            shields.rect.x = (50 + (195 * shield)) + (10 * column)
            shields.rect.y = 500 + (10 * row)
            shields_group.add(shields)
start('Level 2')

create_aliens(9, 80, 30)
fps = 60
alien_cooldown = 300
for shield in range(4):
    for row in range(3):
        for column in range(5):
            shields = Shields()
            shields.rect.x = (50 + (195 * shield)) + (10 * column)
            shields.rect.y = 500 + (10 * row)
            shields_group.add(shields)
start('Level 3')

create_aliens(9, 80, 30)
fps = 60
alien_cooldown = 200
for shield in range(1):
    for row in range(5):
        for column in range(20):
            shields = Shields()
            shields.rect.x = (290 + (195 * shield)) + (10 * column)
            shields.rect.y = 500 + (10 * row)
            shields_group.add(shields)
start('Level 4')

create_aliens(7, 80, 150)
spaceship.remaining_health = spaceship.initial_health
fps = 60
alien_cooldown = 500
for shield in range(4):
    for row in range(3):
        for column in range(10):
            shields = Shields()
            shields.rect.x = (50 + (195 * shield)) + (10 * column)
            shields.rect.y = 500 + (10 * row)
            shields_group.add(shields)
start('Boss')


if spaceship.remaining_health != 0:
    screen.blit(img6, (0, 0))
    for i in range(1000):
        f1 = pygame.font.SysFont('serif', 54)
        text1 = f1.render('YOU ARE A WINNER!', True, (255, 255, 255))
        screen.blit(text1, (120, 400))
        pygame.display.update()
        i = i + 1

pygame.quit()
