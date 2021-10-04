import pygame
import time
import sys
import random



WIDTH = 500
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0 ,0, 0)
GREEN = (102,205,0)
RED = (255, 0, 0)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('professional cubing timer')

def timer():

    
    def scramble(size):
        result = ""
        if size == 3:
            scramble_list = [[" R ", " R2 ", " R' "], [" L ", " L2 ", " L' "], [" B ", " B2 ", " B' "], [" D ", " D2 ", " D' "], [" F ", " F2 ", " F' "], [" U ", " U2 ", " U' "]]
            scramble_list = random.sample(scramble_list, len(scramble_list))
            sub = ''
            for _ in range(3):
                for i in range(len(scramble_list)):
                    j = scramble_list[i]
                    sub = random.sample(j, len(j))[random.randint(0,2)]
                    result += sub
                scramble_list.remove(j)
            return result[:-3]

        elif size == 2:
            scramble_list = [[" R ", " R2 ", " R' "], [" L ", " L2 ", " L' "], [" B ", " B2 ", " B' "], [" F ", " F2 ", " F' "],[" D ", " D2 ", " D' "], [" U ", " U2 ", " U' "]]
            indexs = [[0,1],[2,3],[4,5]]
            result = ""
            j = []

            num = random.randint(0,2)
            if num == 0:
                j = [0,1,2]*3
            elif num == 1:
                j = [1,2,0]*3
            else:
                j = [2,0,1]*3

            for i in range(9):
                index = indexs[j[i]][random.randint(0,1)]
                result += scramble_list[index][random.randint(0,2)]
                
            return result
                

    font_name = pygame.font.match_font("roman")

    def draw_text(surf, text, size, x, y, color, digit=False):
        font = pygame.font.Font(font_name, size)
        if digit:
            font = pygame.font.Font("digital-7.ttf", 75)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

    def draw_time(input, min, hr):
        if hr > 0:
            return f'{hr}:{min}:{input}'  
        elif min > 0:
            return f'{min}:{input}'   
        else:
            return input

    def sec_to_time(sec):
        s, hr, m = float(sec), 0, 0
        if s >= 3600:
            hr = s // 3600
            s %= 3600
        elif s >= 60:
            m = s//60
            s %= 60
        elif s < 60:
            return str(s)

        s, m, hr = int(s),int(m), int(hr)   

        if hr:
            return f'{hr}:{m}:{s}'
        elif m:
            return f'{m}:{s}'
        return f'{s}'
        
    def draw_info(input):
        sec_list = []
        for i in input:
            sec = 0
            for j in range(len(i)):
                if i[j] and j == 0:
                    sec += 3600*i[j]
                elif i[j] and j == 1:
                    sec += 60*i[j]
                elif i[j] and j == 2:
                    sec += i[j]
            sec_list.append(sec)
                
        mean = round(sum(sec_list)/len(sec_list),2)
        mean_time = sec_to_time(mean)
        best = min(sec_list)
        best_time = sec_to_time(best)
        ao5 = '-'
        ao12 = '-'
        if len(input) > 4:
            ao5 = sec_to_time(round(sum(sec_list[-5:])/5, 2))
        if len(input) > 11:
            ao12 = sec_to_time(round(sum(sec_list[-12:])/12, 2))

        draw_text(screen, "Mean: " + mean_time, 25, 155, 400, BLACK)
        draw_text(screen, "Best: " + best_time, 25, 350, 400, GREEN)
        draw_text(screen, "ao5: "+ ao5, 30, 250, 480, BLACK)
        draw_text(screen, "ao12: "+ ao12, 30, 250, 520, BLACK)


    cube_size = int(input("Which cube?(ex: 3 => 3x3): "))

    screen.fill(WHITE)
    draw_text(screen, 'Press space to start timing', 25, 250, 100, RED)
    scramble_info = scramble(cube_size)
    draw_text(screen, f"{cube_size}x{cube_size}", 20, 250, 10, BLACK)
    draw_text(screen, "scramble:" + scramble_info, 20, 250, 40, BLACK)
    pygame.display.update()
    screen.fill(WHITE)
    init = True
    while init:
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.display.update()
                    draw_text(screen, 'Ready...', 40, 250, 100, RED)
                    draw_text(screen, '0.0', 70, 250, 200, RED, True)
                    pygame.display.update()
                    init = False
    
    times = []
    solves = 0
    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYUP:
                
                if event.key == pygame.K_SPACE:
                    timing = True 
                    before = time.time()
                    minutes = 0
                    hours = 0
                    while timing:

                        for event in pygame.event.get():

                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            elif event.type == pygame.KEYUP:

                                if event.key == pygame.K_SPACE:
                                    timing = False
                                    

                        seconds = str(round(time.time() - before, 1))
                        
                        if seconds == '60.0':
                            minutes += 1
                            before = time.time()

                        elif minutes == 60:
                            hours += 1
                            minutes = 0
                        

                        screen.fill(WHITE)
                        draw_text(screen, draw_time(seconds, minutes, hours), 50, 250, 200, BLACK, True)
                        pygame.display.update()
                    
                    if not timing:
                        solves += 1
                        times.append([int(hours),int(minutes),float(seconds)])
                        draw_text(screen, 'Press space again to start', 25, 250, 100, RED)
                        scramble_info = scramble(cube_size)
                        draw_text(screen, f"{cube_size}x{cube_size}", 20, 250, 10, BLACK)
                        draw_text(screen, "scramble:" + scramble_info, 20, 250, 40, BLACK)
                        draw_text(screen, draw_time(seconds, minutes, hours), 50, 250, 200, GREEN, True)
                        draw_info(times)
                        draw_text(screen, f"solve #{solves}", 25, 250, 570, BLACK)
                        pygame.display.update()

                    while not timing:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    screen.fill(WHITE)
                                    draw_text(screen, 'Ready...', 40, 250, 100, RED)
                                    draw_text(screen, '0.0', 70, 250, 200, RED, True)
                                    draw_text(screen, "Previous time: "+draw_time(seconds, minutes, hours), 35, 250, 300, BLACK)
                                    pygame.display.update()
                                    timing = True
                            
timer()