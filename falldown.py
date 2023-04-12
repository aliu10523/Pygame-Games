#Andrew Liu, jjs7vc

import uvage
import random

screen_width = 600
screen_height = 800

global camera, box, walls, score, floors, topIndex, game_over, final_Score

camera = uvage.Camera(screen_width, screen_height)
box = uvage.from_color(100, 100, "green", 40, 40)
box.center = [300, 80]
score = 0
final_Score = 0
score_display = uvage.from_text(100, 600, str(score), 50, "brown")
gapSize = screen_width - 60
topIndex = 0  # represents the position of the current highest floor pair
random_x1 = random.randint(0, gapSize)
# variable to generate random width size of the left and right floor in the same height
game_over = False


walls = [
        uvage.from_color(0, screen_height / 2, "black", 10, screen_height),  # x,y, color, width, height
        uvage.from_color(screen_width, screen_height / 2, "black", 10, screen_height)
    ]

floors = []

for i in range(1, 7):
    random_x1 = random.randint(0, gapSize)
    floors.append(uvage.from_color(random_x1 / 2, 150 * i, "black", random_x1, 40))
    floors.append(uvage.from_color(screen_width - (screen_width - random_x1 - 60) / 2, 150 * i, "black", screen_width - random_x1 - 60, 40))
    # positions it by subtracting the screen width by the width of the right side of the floor
    # creates the length of the right side of the floor by subtracting screen width by
    # the random_x1(width size of the right side of the floor) and gap size which is 60 for width

for floor in floors:  # sets each floor speed to move up
    floor.speedy = -2

def touching():
    """ Contains all the code for border/touching aspects of this game

    :return: None
    """
    global topIndex, score
    for wall in walls:   # prevent box from moving beyond the screen walls
        box.move_to_stop_overlapping(wall)

    if box.center[1] <= 0:  # if box center reaches the top of the screen
        for each_floor in floors:
            each_floor.speedy = 0   # set the floor speed to zero to make them static
        endgame()  # call endgame function

    for floor in floors:  # loops through each floor in the floor list
        floor.move_speed()  # move speed at -2 which was set at the beginning
        box.move_to_stop_overlapping(floor)

    if floors[topIndex].center[1] <= -20:  # once the floor reaches the top of the screen
        random_x = random.randint(0, gapSize)  # create random x number
        floors[topIndex].size = [random_x, floors[topIndex].height]
        # adjusts the size to same height and a random width
        floors[topIndex].center = [random_x / 2, floors[topIndex - 1].center[1] + 150]
        floors[topIndex + 1].center = [screen_width - (screen_width - random_x - 60) / 2, floors[topIndex - 1].center[1] + 150]
        # Moves the y position of the floor pair by using negative index and accessing the bottom floor pair's y
        # position and adding 150 to make it evenly spaced between each floor
        floors[topIndex + 1].size = [screen_width - random_x - 60, floors[topIndex].height]
        topIndex += 2  # adds two to go to next pair
        topIndex = topIndex % len(floors)  # prevent the topIndex from going beyond list size by using mod
        # this block of code essentially displaces the first floor which includes the left side and right side and
        # moves its position below the screen while also changing the gap position in the floor

def endgame():
    global game_over
    if box.center[1] <= 0:  # if the boxes center reaches the top of the screen
        camera.draw(uvage.from_text(300, 400, "Game Over", 70, "red"))  # display text Game Over
        game_over = True   # sets global variable to True

def draw_environment():
    for wall in walls:  # loops through each wall in the list of walls and draws it
        camera.draw(wall)
    for floor in floors:
        camera.draw(floor)  # loops through each floor in the list of floors and draws it

def handle_keys():
    box.speedx = 0  # speed is still if not pressed by button
    if uvage.is_pressing("right arrow"):
        box.speedx = 5
    if uvage.is_pressing("left arrow"):
        box.speedx = -5
    box.speedy = 7 # make speed of y always set to fall down
    if box.center[1] >= 800:   # if the box touches the top of the screen the game ends, and the box speed is set to 0
        box.speedy = 0
    box.move_speed()

def draw_stats():
    """ Updating global variable score and display it

    :return: None
    """
    global score, final_Score
    score += 0.03
    camera.draw("Score: " + str(int(score)), 50, "red", 75, 725)
    final_Score = score

def tick():
    camera.clear('white')
    #if not game_over:  # the game will call handle_keys function if the game is not over
        #handle_keys()
        #draw_stats()
    camera.draw(box)
    draw_environment()
    touching()
    if not game_over:  # the game will call handle_keys function if the game is not over
        handle_keys()
        draw_stats()
    if game_over: # displays the final score once the game ends
        camera.draw("Score: " + str(int(final_Score)), 50, "red", 75, 725)
    camera.display()

uvage.timer_loop(60, tick)

