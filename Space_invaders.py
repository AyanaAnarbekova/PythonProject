import pygame
import random

level = 1

play_game = True
pygame.mixer.init()

fps = 30
width = 750
height = 700
alien_cooldown = 500
last_alien_shoot = pygame.time.get_ticks()
rows = level*2+3

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('GALAXIAN')
clock = pygame.time.Clock()
background=pygame.image.load('images/background1_7.jpg')
img = pygame.transform.scale(background,(750,800))
spaceship=pygame.image.load('images/spaceship.png')
img1=pygame.transform.scale(spaceship,(60,50))
alien=pygame.image.load('images/alien(3).png')
img2=pygame.transform.scale(alien,(50,40))
lazer1=pygame.image.load('images/lazer1.png')
img3=pygame.transform.scale(lazer1,(20,20))
shield=pygame.image.load('images/solar_panels.png')
img4=pygame.transform.scale(shield,(10,10))
lazer2=pygame.image.load('images/lazer2.png')
img5=pygame.transform.scale(lazer2,(20,20))

'''lazer_sound=pygame.mixer.Sound('sounds/lazer_sound.wav')
lazer_sound.set_volume(0.25)'''

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img1
        self.rect = self.image.get_rect()
        self.rect.centerx = int(width / 2)
        self.rect.bottom = height - 50
        self.initial_health = 10
        self.remaining_health = 10

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

        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, (self.rect.bottom+5), self.rect.width, 10))
        if self.remaining_health > 0:
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, (self.rect.bottom+5), int((self.rect.width) * (self.remaining_health / self.initial_health)), 10))
        if pygame.sprite.spritecollide(self, alien_bullet_group, True):
            self.remaining_health -= 1
        if self.remaining_health == 0:
            self.kill()
            play_game = False


    def shoot(self):
        lazer = Lazer(self.rect.centerx, self.rect.top)
        if len(spaceship_group)>0:
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
            explosion=Explosion(self.rect.x,self.rect.top)
            explosion_group.add(explosion)

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
        for i in range(1,6):
            img = pygame.image.load(f'images/exp{i}.png')
            img = pygame.transform.scale(img, (i*5,i*5))
            self.explosion.append(img)
        self.index = 0
        self.image = self.explosion[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
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
         self.rect.center = [x,y]
         self.speedy = 15

     def update(self):
         self.rect.y += self.speedy
         if self.rect.top > height:
             self.kill()
         if pygame.sprite.spritecollide(self, spaceship_group, False):
             self.kill()
             explosion = Explosion(self.rect.x, self.rect.top)
             explosion_group.add(explosion)
             spaceship.remaining_health-=1
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


spaceship_group=pygame.sprite.Group()
spaceship = Spaceship()
spaceship_group.add(spaceship)
lazer_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
shields_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
def create_aliens():
    for row in range(1, rows):
        for column in range(1, 11):
            alien = Aliens((80 + (50 * column)),(30 + (50 * row)))
            aliens_group.add(alien)

create_aliens()

for shield in range(4):
    for row in range(5):
        for column in range(10):
            shields = Shields()
            shields.rect.x = (50 + (195 * shield)) + (10 * column)
            shields.rect.y = 500 + (10 * row)
            shields_group.add(shields)

while play_game:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    screen.blit(img,(0,0))


    time_now = pygame.time.get_ticks()
    if time_now - last_alien_shoot > alien_cooldown:
        attacking_alien = random.choice(aliens_group.sprites())
        alien_bullet = Alien_Bullet(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shoot = time_now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spaceship.shoot()
                '''lazer_sound.play()'''

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
pygame.quit()

