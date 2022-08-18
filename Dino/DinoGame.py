import pygame
import time
import os
import random

pygame.init()


SCREEN_HIGTH = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGTH))

SMALLROCK =[pygame.image.load(os.path.join("Assets/Other", "Small_rock1.png")),
    pygame.image.load(os.path.join("Assets/Other", "Small_rock2.png")),
    pygame.image.load(os.path.join("Assets/Other", "Small_rock3.png"))]
BIGROCK = [pygame.image.load(os.path.join("Assets/Other", "Big_rock1.png")),
    pygame.image.load(os.path.join("Assets/Other", "Big_rock2.png"))]

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "Mario_run1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "Mario_run2.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Placefolder_Bird.png")),
    pygame.image.load(os.path.join("Assets/Bird", "Placefolder_Bird2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "Mario_jump.png"))
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "Placefolder_duck.png")),
    pygame.image.load(os.path.join("Assets/Dino", "Placefolder_duck2.png"))]
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
ACTUAL_BG = pygame.image.load(os.path.join("Assets/Other", "Backround.png"))
RETRY = [pygame.image.load(os.path.join("Assets/Other", "Retry.png")),
    pygame.image.load(os.path.join("Assets/Other", "Retry2.png"))]

class Dinosaur:
    X_POS = 80
    Y_POS = 250
    Y_POS_DUCK = 280
    JUMP_VEL = 2.5

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.duck_img = DUCKING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.stepindex = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
    
    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.stepindex >= 10:
            self.stepindex = 0
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False  
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False 
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.stepindex // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.stepindex += 1

    def run(self):
        self.image = self.run_img[self.stepindex // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.stepindex += 1
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -=  0.1
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
        if self.dino_rect.y <= 100:
            quit()
        


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallRock(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 275

class BigRock(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 250

class Bird(Obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Cloud:
     def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

     def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)
     def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

os.system("toturial.txt")

def Main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, Actual_x_pos, Actual_y_pos

    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    points = 0
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 325
    death_count = 0

    Actual_x_pos = 0
    Actual_y_pos = -600

    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []

    

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def backround():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def ActualBackround():
        global Actual_x_pos, Actual_y_pos
        image_width = BG.get_width()
        SCREEN.blit(ACTUAL_BG, (Actual_x_pos, Actual_y_pos))
        SCREEN.blit(ACTUAL_BG, (image_width + Actual_x_pos - 487, Actual_y_pos))
        if Actual_x_pos <= -image_width + 487:
            SCREEN.blit(BG, (image_width + Actual_x_pos, Actual_y_pos))
            Actual_x_pos = 0
        Actual_x_pos -= game_speed -13


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                death_count += 1
        SCREEN.fill((255,255,255))  
        ActualBackround()

        userinput = pygame.key.get_pressed()

        cloud.draw(SCREEN)
        cloud.update()

        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(SmallRock(SMALLROCK))
            elif random.randint(0,2) == 1:
                obstacles.append(BigRock(BIGROCK))
            elif random.randint(0,2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        player.draw(SCREEN)
        player.update(userinput)

        score()

        backround()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    spin = 0
    while run:

        SCREEN.fill((255,255,255))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any key to Start", True, (0,0,0))
        elif death_count > 0:
            text = font.render("Press any key to Start", True ,(0,0,0))
            if points >= 1350:
                score = font.render("You beat the creator with this score : " + str(points), True ,(0,0,0))
            elif points >= 1000:
                score = font.render("that is preaty hard, Your Score: " + str(points), True ,(0,0,0))
            elif points == 69:
                score = font.render(" Your Score: 69, haha funny", True ,(0,0,0))
            else:
                score = font.render(" Your Score: " + str(points), True ,(0,0,0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HIGTH // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HIGTH // 2)
        SCREEN.blit(text, textRect)
        
        if spin <= 5:
            SCREEN.blit(RETRY[0], (SCREEN_WIDTH // 2 - 50, SCREEN_HIGTH // 2 - 200))
        else:
            SCREEN.blit(RETRY[1], (SCREEN_WIDTH // 2 - 50, SCREEN_HIGTH // 2 - 200))

        pygame.display.update()
        spin += 1
        if spin >= 10:
            spin = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            elif event.type  == pygame.KEYDOWN:

                Main()
        time.sleep(0.1)
        


menu(death_count=0)