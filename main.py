from tracemalloc import Statistic
from turtle import Screen
import pygame
import os
import random
import time
import math
import neat
from numpy import interp
import gzip

import pickle  # pylint: disable=import-error

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome RIP")

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 20)

DINO_RUN_WIDTH, DINO_RUN_HEIGHT = 87, 94
DINO_DUCK_WIDTH, DINO_DUCK_HEIGHT = 118, 60
DINO_WIDTH, DINO_HEIGHT = 87, 94
BIRD_WIDTH, BIRD_HEIGHT = 97, 68
CACTUS_LARGE1_WIDTH, CACTUS_LARGE1_HEIGHT = 48, 95
CACTUS_LARGE2_WIDTH, CACTUS_LARGE2_HEIGHT = 99, 95
CACTUS_LARGE3_WIDTH, CACTUS_LARGE3_HEIGHT = 102, 95
CACTUS_SMALL1_WIDTH, CACTUS_SMALL1_HEIGHT = 40, 71
CACTUS_SMALL2_WIDTH, CACTUS_SMALL2_HEIGHT = 68, 71
CACTUS_SMALL3_WIDTH, CACTUS_SMALL3_HEIGHT = 105, 71
CLOUD_WIDTH, CLOUD_HEIGHT = 84, 101
TRACK_WIDTH, TRACK_HEIGHT = 2404, 28


FPS = 60
death_count = 0

#------------------------------------Import Sprites DINO---------------------------------------------------------------
DINO_DEAD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Dino', 'DinoDead.png')),(DINO_WIDTH, DINO_HEIGHT)) 
DINO_DUCK1 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Dino', 'DinoDuck1.png')),(DINO_DUCK_WIDTH, DINO_DUCK_HEIGHT)) 
DINO_DUCK2 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Dino', 'DinoDuck2.png')),(DINO_DUCK_WIDTH, DINO_DUCK_HEIGHT)) 

DINO_DUCK = [DINO_DUCK1, DINO_DUCK2]

DINO_JUMP = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Dino', 'DinoJump.png')),(DINO_WIDTH, DINO_HEIGHT)) 
DINO_RUN1 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Dino', 'DinoRun1.png')),(DINO_RUN_WIDTH, DINO_RUN_HEIGHT)) 
DINO_RUN2 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Dino', 'DinoRun2.png')),(DINO_RUN_WIDTH, DINO_RUN_HEIGHT)) 

DINO_RUN = [DINO_RUN1, DINO_RUN2]

DINO_START = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Dino', 'DinoStart.png')),(DINO_WIDTH, DINO_HEIGHT)) 

#------------------------------------Import Sprites BIRD---------------------------------------------------------------
BIRD1 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Bird', 'Bird1.png')),(BIRD_WIDTH, BIRD_HEIGHT)) 
BIRD2 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Bird', 'Bird2.png')),(BIRD_WIDTH, BIRD_HEIGHT)) 

BIRD = [BIRD1, BIRD2]

#------------------------------------Import Sprites Cactus---------------------------------------------------------------
CATCUS_LARGE1 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Cactus', 'LargeCactus1.png')),(CACTUS_LARGE1_WIDTH, CACTUS_LARGE1_HEIGHT)) 
CATCUS_LARGE2 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Cactus', 'LargeCactus2.png')),(CACTUS_LARGE2_WIDTH, CACTUS_LARGE2_HEIGHT)) 
CATCUS_LARGE3 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Cactus', 'LargeCactus3.png')),(CACTUS_LARGE3_WIDTH, CACTUS_LARGE3_HEIGHT))

LARGE_CACTUS = [CATCUS_LARGE1, CATCUS_LARGE2, CATCUS_LARGE3]

CACTUS_SMALL1 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Cactus', 'SmallCactus1.png')),(CACTUS_SMALL1_WIDTH, CACTUS_SMALL1_HEIGHT))
CACTUS_SMALL2 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Cactus', 'SmallCactus2.png')),(CACTUS_SMALL2_WIDTH, CACTUS_SMALL2_HEIGHT))
CACTUS_SMALL3 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Cactus', 'SmallCactus3.png')),(CACTUS_SMALL3_WIDTH, CACTUS_SMALL3_HEIGHT))

SMALL_CACTUS = [CACTUS_SMALL1, CACTUS_SMALL2,CACTUS_SMALL3]


#------------------------------------Import Sprites Background---------------------------------------------------------------
TRACK = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Other', 'Track.png')),(TRACK_WIDTH, TRACK_HEIGHT)) 
CLOUD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Other', 'Cloud.png')),(CLOUD_WIDTH, CLOUD_HEIGHT)) 


class Dino():

    X_POS = 100
    Y_POS = 330
    Y_POS_DUCK = Y_POS + (DINO_RUN_HEIGHT - DINO_DUCK_HEIGHT)

    def __init__(self):
        self.duck_img = DINO_DUCK
        self.run_img = DINO_RUN
        self.jump_img = DINO_JUMP

        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.step_index = 0
        self.step_length = 20
        self.jump_vel = 20
        self.heigth = 0
        self.image = self.run_img
        self.dino_rect = self.image[0].get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS


    def update(self, keys_pressed):

        if self.dino_run and self.heigth == 0:
            self.run()
        if self.dino_jump or self.heigth > 0:
            self.jump()
        if self.dino_duck and self.heigth == 0:
            self.duck()



    def jump(self):
        self.image = self.jump_img
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS

        self.heigth += self.jump_vel
        self.jump_vel -= 1
        self.dino_rect.y = self.Y_POS - self.heigth

        if self.heigth <= 0:
            self.heigth = 0
            self.dino_rect.y = self.Y_POS
            self.jump_vel = 22
            self.dino_jump = False
            self.dino_run = True


    def duck(self):
        self.image = self.duck_img[self.step_index // int(self.step_length/2)]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index +=1
        if self.step_index >= self.step_length:
            self.step_index = 0

    def run(self):
        self.image = self.run_img[self.step_index // int(self.step_length/2)]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index +=1
        if self.step_index >= self.step_length:
            self.step_index = 0
    
    
    def draw(self, WIN):
        WIN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Track():

    X_POS = 0
    Y_POS = 400

    def __init__(self, x_pos_init):
        self.image = TRACK
        self.track_rect = self.image.get_rect()

        self.track_rect.x = x_pos_init
        self.track_rect.y = self.Y_POS

    def move(self, vel):     
        if (self.track_rect.x - vel) >= 0:
            self.track_rect.x = math.floor(self.track_rect.x - vel)
        else:
            self.track_rect.x = math.floor(self.track_rect.x - vel)

        if self.track_rect.x <= -self.track_rect.width:
            tracks.pop(0)
    def draw(self, WIN):
        WIN.blit(self.image, (self.track_rect.x, self.track_rect.y))


class Cloud():
    X_POS_RANGE = [WIDTH, 4*WIDTH]
    Y_POS_RANGE = [50, 200]

    def __init__(self):
        self.image = CLOUD
        self.cloud_rect = self.image.get_rect()

        self.cloud_rect.x = random.uniform(self.X_POS_RANGE[0], self.X_POS_RANGE[1])
        self.cloud_rect.y = random.uniform(self.Y_POS_RANGE[0], self.Y_POS_RANGE[1])

    def move(self, speed):
        self.cloud_rect.x -= speed
        if self.cloud_rect.x < -self.cloud_rect.width:
            self.cloud_rect.x = random.uniform(self.X_POS_RANGE[0], self.X_POS_RANGE[1])
            self.cloud_rect.y = random.uniform(self.Y_POS_RANGE[0], self.Y_POS_RANGE[1])

    def draw(self):
        WIN.blit(self.image, (self.cloud_rect.x, self.cloud_rect.y))


class Obstacles():

    def __init__(self, image, type):
        
        self.image = image
        self.type = type
        self.obstacle_rect = self.image[self.type].get_rect()
        self.obstacle_rect.x = WIDTH

    def move(self, vel):
        self.obstacle_rect.x -= vel
        if self.obstacle_rect.x < -self.obstacle_rect.width:
            obstacles.pop()

    def draw(self, WIN):
        WIN.blit(self.image[self.type], (self.obstacle_rect.x, self.obstacle_rect.y))

class SmallCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.obstacle_rect.y = 350

class LargeCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.obstacle_rect.y = 320


class Bird(Obstacles):
    def __init__(self, image):
        self.type = 0
        self.step_length = 20
        self.step_index = 0
        self.heigth = [160, 270, 320]
        super().__init__(image, self.type)
        self.obstacle_rect.y = self.heigth[random.randint(0,2)]

    def draw(self, WIN):
        self.step_index +=1
        if self.step_index >= self.step_length:
            self.step_index = 0
        WIN.blit(self.image[self.step_index // int(self.step_length/2)], self.obstacle_rect)


def main(genomes, config):

    def Score(WIN):
        global score
        score += 0.2
        for i, dino in enumerate(dinos):
            ge[i].fitness += 0.2
        text_surface = my_font.render('Points: ' + str(int(score)), False, (0, 0, 0))
        WIN.blit(text_surface, (1100,20))

    def statistics():
        global dinos, vel, ge
        text_1 = my_font.render(f'Dinosaurs Alive:  {str(len(dinos))}', True, (0, 0, 0))
        text_2 = my_font.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = my_font.render(f'Game Speed:  {str(int(vel))}', True, (0, 0, 0))
        input_1 = my_font.render(f'Player Heigth:  {str(round(dino.dino_rect.y,0))}', True, (0, 0, 0))
        input_2 = my_font.render(f'Distance do Obstacle:  {str(round(dino.dino_rect.x - obstacles[next_obstacle].obstacle_rect.x,0))}', True, (0, 0, 0))
        input_3 = my_font.render(f'Obstacle Heigth:  {str(round(obstacles[next_obstacle].obstacle_rect.y + obstacles[next_obstacle].obstacle_rect.height,0))}', True, (0, 0, 0))
        input_4 = my_font.render(f'Game Speed:  {str(round(vel,0))}', True, (0, 0, 0))

        WIN.blit(text_1, (50, 450))
        WIN.blit(text_2, (50, 480))
        WIN.blit(text_3, (50, 510))

        WIN.blit(input_1, (300, 450))
        WIN.blit(input_2, (300, 480))
        WIN.blit(input_3, (300, 510))
        WIN.blit(input_4, (300, 540))

        

    def remove(index):
        dinos.pop(index)
        ge.pop(index)
        nets.pop(index)

    global vel, score, obstacles, tracks, death_count, ge , nets, dinos
    vel = 9

    #----------------------------create Objects--------------------------
    
    tracks = []
    clouds = [Cloud(), Cloud(), Cloud()]
    dinos = []
    obstacles = []
    ge = []
    nets = []
    score = 1

    for genome_id, genome in genomes:
        dinos.append(Dino())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        WIN.fill((255, 255, 255))
        keys_pressed = pygame.key.get_pressed()

        if len(dinos) == 0:
            break

        if len(tracks) == 0:
            tracks.append(Track(0))
        elif len(tracks) == 1:
            tracks.append(Track(TRACK_WIDTH))

        for track in tracks:
            track.move(vel)
            track.draw(WIN)

        for cloud in clouds:
            cloud.move(vel/2)
            cloud.draw()

        for dino in dinos:
            dino.update(keys_pressed)
            dino.draw(WIN)


        for obstacle in obstacles:
            obstacle.move(vel)
            obstacle.draw(WIN)
            for i, dino in enumerate(dinos):
                if dino.dino_rect.colliderect(obstacle.obstacle_rect):
                    ge[i].fitness -= 1
                    remove(i)

        if len(obstacles) == 0:
            rand = random.randint(0, 2)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif rand == 2:
                obstacles.append(Bird(BIRD))

        for i, dino in enumerate(dinos): 
            next_obstacle = len(obstacles)-1
            output = nets[i].activate((dino.dino_rect.y,                                                                     
            dino.dino_rect.x - obstacles[next_obstacle].obstacle_rect.x,                                                      
            obstacles[next_obstacle].obstacle_rect.y + obstacles[next_obstacle].obstacle_rect.height,                                                                     
            vel,
            ))

            if output[0] > 0.5:
                dino.dino_run = False
                dino.dino_jump = True
                dino.dino_duck = False

            if output[1] > 0.5:
                dino.dino_run = False
                dino.dino_jump = False
                dino.dino_duck = True

            if output[0] < 0.5 and output[1] < 0.5:
                dino.dino_run = True
                dino.dino_jump = False
                dino.dino_duck = False


        Score(WIN)
        statistics()
        if int(score) % 100 == 0:
            vel += 0.1

        pygame.display.update()
        


def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop = neat.Checkpointer.restore_checkpoint('Checkpoints\\neat-checkpoint-317')
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    #pop.add_reporter(neat.Checkpointer(20, filename_prefix='Checkpoints\\neat-checkpoint-'))
    
    winner = pop.run(main, 1)
    #replay_genome(config_path)
    save_winner(winner)



def save_winner(winner):
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()


def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    global pop
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    main(genomes, config)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)

