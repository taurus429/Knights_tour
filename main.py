import pygame

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CHOCO = (137, 104, 89)
V_CHOCO = (237, 104, 89)
v=2
C_CHOCO = (123, 180, 80)
BAMBOO = (216, 199, 169)
V_BAMBOO = (255, 155, 133)
C_BAMBOO = (137, 204, 89)
PRIO_1 = (56, 93, 250)
PRIO_2 = (99, 191, 247)
PRIO_3 = (32, 176, 80)
PRIO_4 = (146, 208, 80)
PRIO_5 = (255, 192, 0)
PRIO_6 = (247, 124, 49)
PRIO_7 = (255, 71, 71)


BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
box_length = 100
board_start = [50, 50]
chessboard = []
chessboard_lenght = 8

#체스보드 생성
for _ in range(chessboard_lenght):
    chessboard.append([False]*chessboard_lenght)
#기사말 이미지
knight = pygame.image.load("realknight.png")
knight = pygame.transform.scale(knight, (box_length, box_length))
#소리
laugh = pygame.mixer.Sound("teemo_laugh.mp3")
tick = pygame.mixer.Sound("tick.mp3")
put = pygame.mixer.Sound("put.mp3")
success_sound = pygame.mixer.Sound("wow.mp3")
laugh2 = pygame.mixer.Sound("laugh2.mp3")
size = [board_start[0]*2+ box_length*chessboard_lenght, board_start[0]*2+ box_length*chessboard_lenght]
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("kopubworld바탕체", box_length//3, bold=1)
guidefont = pygame.font.SysFont("kopubworld바탕체", box_length//3, bold=1)
#print(pygame.font.get_fonts())
pygame.display.set_caption("Knight's Tour")

# Loop until the user clicks the close button.
done = False
flag = None
fail = False
clock = pygame.time.Clock()


# print text function
def printText(msg, color='BLACK', pos=(50, 50)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)

def printGuide(msg, color='BLACK', pos=(50, 50)):
    textSurface = guidefont.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)

def colorbox(x, y, color):
    pygame.draw.rect(screen, color, [board_start[0]+box_length*x, board_start[1]+box_length*y, box_length, box_length])

def candibox(x, y, prio):
    if prio == 7:
        color = PRIO_7
    elif prio == 6:
        color = PRIO_6
    elif prio == 5:
        color = PRIO_5
    elif prio == 4:
        color = PRIO_4
    elif prio == 3:
        color = PRIO_3
    elif prio == 2:
        color = PRIO_2
    else:
        color = PRIO_1
    pygame.draw.rect(screen, color, [board_start[0]+box_length*x, board_start[1]+box_length*y, box_length, box_length])

def linebox(x, y, color):
    bound = box_length//20
    pygame.draw.rect(screen, color, [board_start[0]+box_length*x+bound, board_start[1]+box_length*y+bound, box_length-2*bound, box_length-2*bound], bound)

def candi(x, y):
    possible = [[x+1, y+2], [x+1, y-2], [x-1, y+2], [x-1, y-2], [x+2, y+1], [x+2, y-1], [x-2, y+1], [x-2, y-1]]
    dellist = []
    for pos in possible:
        if 0 <= pos[0] < chessboard_lenght and 0 <= pos[1] < chessboard_lenght and not chessboard[pos[0]][pos[1]]:
            pass
        else:
            dellist.append(pos)
    for p in dellist:
        possible.remove(p)
    return possible
move = 0
past_x = -1
past_y = -1
mouse_x_pos = -1
mouse_y_pos = -1

while not done:

    clock.tick(100)
    if move == 0:
        candidate = []
        for i in range(chessboard_lenght):
            for j in range(chessboard_lenght):
                candidate.append([i, j])
    for event in pygame.event.get():  # User did something
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if move != 0: # 첫 클릭 체스판 벗어나도 되는 버그
                past_x = x_pos
                past_y = y_pos
            x_pos = (pos[0]-board_start[0])//box_length
            y_pos = (pos[1]-board_start[1])//box_length
            if [x_pos, y_pos] not in candidate:
                x_pos = past_x
                y_pos = past_y
            else:
                chessboard[x_pos][y_pos] = True
                move += 1
                put.play()
            candidate = candi(x_pos, y_pos)
            flag = True
            if len(candidate) == 0:
                if move != chessboard_lenght*chessboard_lenght:
                    fail = True
                    #laugh.play()
                    laugh2.play()
                else:
                    success_sound.play()
        elif event.type == pygame.MOUSEBUTTONUP:  # If user press any key.
            flag = False
        elif event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
            temp_x_pos = (mouse[0]-board_start[0])//box_length
            temp_y_pos = (mouse[1]-board_start[1])//box_length
            if 0 <= temp_x_pos < chessboard_lenght and 0 <= temp_y_pos < chessboard_lenght:
                if mouse_x_pos != temp_x_pos or mouse_y_pos != temp_y_pos:
                    pass
                    #tick.play()
                mouse_x_pos = (mouse[0]-board_start[0])//box_length
                mouse_y_pos = (mouse[1]-board_start[1])//box_length
        elif event.type == pygame.QUIT:  # If user clicked close.
            done = True

    screen.fill(WHITE)

    for i in range(chessboard_lenght):
        for j in range(chessboard_lenght):
            if (i + j) % 2 == 0:
                if chessboard[i][j]:
                    colorbox(i, j, V_CHOCO)
                elif [i, j] in candidate:
                    if move != 0:
                        candibox(i, j, len(candi(i, j)))
                    else:
                        colorbox(i, j, CHOCO)
                else:
                    colorbox(i, j, CHOCO)
            else:
                if chessboard[i][j]:
                    colorbox(i, j, V_BAMBOO)
                elif [i, j] in candidate:
                    if move != 0:
                        candibox(i, j, len(candi(i, j)))
                    else:
                        colorbox(i, j, BAMBOO)
                else:
                    colorbox(i, j, BAMBOO)

    if 0 <= mouse_x_pos < chessboard_lenght and 0<= mouse_y_pos < chessboard_lenght:
        linebox(mouse_x_pos, mouse_y_pos, RED)
    try:
        screen.blit(knight, (x_pos*box_length+board_start[0], y_pos*box_length+board_start[1]))
    except:
        pass
    if not fail:
        # Print red text if user pressed any key.
        if flag == True:
            printText('이동 횟수 :{}, 남은 이동:{}'.format(move, chessboard_lenght*chessboard_lenght-move), pos=(board_start[0] + chessboard_lenght/2*box_length, 0))
            pass

        # Print blue text if user released any key.
        elif flag == False:
            printText('이동 횟수 :{}, 남은 이동:{}'.format(move, chessboard_lenght*chessboard_lenght-move), pos=(board_start[0] + chessboard_lenght/2*box_length, 0))
            pass
        # Print default text if user do nothing.
        else:
            printText('Knight\' Tour', pos=(board_start[0] + chessboard_lenght/2*box_length- 70, board_start[1] + chessboard_lenght/2*box_length-30))
            printText('Chose start point of knight', pos=(board_start[0] + chessboard_lenght/2*box_length- 150, board_start[1] + chessboard_lenght/2*box_length))
    else:
        printText('YOU FAILED', pos=(board_start[0] + chessboard_lenght / 2 * box_length - 70,
                                        board_start[1] + chessboard_lenght / 2 * box_length - 30), color= RED)
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
