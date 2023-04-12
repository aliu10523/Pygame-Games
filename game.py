# jgv7kg - Julian Krese
# jjs7vc - Andrew Liu

"""
We created a game based slightly off of the classic arcade game Space Invaders. There are two players who each control
a spaceship and protect an area from invading enemy spaceships. The user spaceships can only move left and right,
and shoot a projectile that c![](8TGboEqGc.png)an explode an enemy invader on impact. The players cannot win and continue to shoot
the enemy spaceships until they reach a red line. However, the longer the players last, the faster the enemies fall
down the screen. The collectible is the coin that increases the players' score. There is a score displayed in the
corner of the screen, which is a created by adding how many ships have been destroyed and how many coins have
been collected.
"""

""" 3 Basic Features
User input - This feature will be incorporated through keyboard input, with movement keys for both players and also
firing keys

Game over - The game ends if any of the incoming invaders reach the bottom of the screen before the player eliminates 
them. The speed of the invaders will progressively get faster as the game goes on. It will be incorporated by having a boolean value 
representing if the game is currently running or not.

Images  - This feature will be incorporated in every visible object in the game. We will also use different image files/sprite 
sheets to represent the players’ spaceship, the enemy invaders, the missiles, explosion effect, and background.

"""
""" 4 Additional Features
Sprite Animation - We created sprite animation by using a sprite-sheet to show an explosion whenever an enemy is 
hit by a player's missile. 

Collectables - We created a collectible coin that falls from the top of the screen and can be collected by the players. 
It moves faster than the base speed of the enemy ships, so it is more difficult to catch but counts for the 
equivalent of shooting 10 enemy ships.

Two Players - We created two different spaceships to be controlled by two players. Each fires and functions 
independently of the other.

Restart - We created a replay-able game, that is to say once the players lose they can hit "space" to restart the 
game and play again.
"""
"""
Changes:
We decided to not implement powerups as collectibles but instead created coins as collectibles that boost the score. 
We also decided to get rid of the asteroids as a hinderance because we didn't need them anymore to fulfill the 
4 special requirements. We also decided to not do sprite animation for the ships but instead only for the explosion. 
There is also no way to win, which we originally were going to have a limited amount of enemies and once they are 
dealt with the players would win. Now, the enemies are infinite and their falling speed increases as the game goes on. 
The score is also composited differently, with it originally being the number of enemy ships destroyed. It now is 
calculated by 10 points per ship and 100 points per coin. The final change was that our 4th requirement of enemies is 
now a restartable game (although we still do technically have enemies).
"""


import uvage
import random

camera = uvage.Camera(800, 600)
background = uvage.from_image(400, 400, "1071647.jpg")
background.scale_by(2.21)

p1_spaceship = uvage.from_image(500, 510, "spaceship-clipart-16.png")
p1_spaceship.scale_by(.2)
p1_spaceship_xvelocity = 5  # variable because easy to change all at once
p2_spaceship = uvage.from_image(300, 560, "spaceship-clipart-16.png")
p2_spaceship.scale_by(.2)
p2_spaceship_xvelocity = 5  # variable because easy to change all at once

enemies = []
coins = []

explosion_images = uvage.load_sprite_sheet("exp2_0.png", 4, 4)
explosion_list = []
explosion_timer = 0  # used to loop through sprite-sheet frames

enemy_speed_increase = 0

score = 0
timer_count_1 = 50  # timer meant for p1_spaceship fire rate
timer_count_2 = 50  # different from timer_count_1 because both spaceships should have a separate cool down
enemy_counter = 0  # timer meant for spawning enemies at a specified rate
coin_counter = 0  # timer meant for spawning coins at a specified rate

rules = [
    uvage.from_text(400, 310, "let them touch the red line", 50, "white"),
    uvage.from_text(400, 260, "Shoot the enemies and don't", 50, "white"),
    uvage.from_text(400, 210, "Press \"Q\" to start", 50, "white"),
    uvage.from_text(400, 160, "P1 \"up arrow\" fires and P2 \"w\" fires", 50, "white"),
    uvage.from_text(400, 80, "SPACE DEFENDERS", 70, "red", italic=True)
]

game_on = False
game_over = False
projectile_list = []
missile_velocity = 8  # variable cause easy to change all at once

boundaries = [
    uvage.from_color(-5, 500, "yellow", 10, 100),  # left wall
    uvage.from_color(805, 500, "yellow", 10, 100),  # right wall
]

finishing_line = uvage.from_color(400, 480, "red", 800, 2)  # game ends if enemy touches this line


def draw():
    global projectile_list
    global game_on
    global enemies
    global finishing_line
    global coins
    global explosion_list
    global explosion_timer
    """
    The function draw() takes no parameters and returns nothing. It clears the camera, 
    draws everything, and displays everything.
    """
    camera.clear("black")
    camera.draw(background)
    camera.draw(finishing_line)
    if not game_on:
        for each in rules:
            camera.draw(each)
    camera.draw(p1_spaceship)
    camera.draw(p2_spaceship)
    for missile in projectile_list:
        camera.draw(missile)
    for wall in boundaries:
        camera.draw(wall)
    for each_enemy in enemies:
        camera.draw(each_enemy)
    for coin in coins:
        camera.draw(coin)
    for explosion in explosion_list:  # deals with the explosion sprite-sheet
        if explosion_timer <= 15:
            explosion.image = explosion_images[explosion_timer]
            explosion_timer += 1
        elif explosion_timer > 15: # controls explosion effect
            explosion_list.remove(explosion)
            explosion_timer = 1
        camera.draw(explosion)
    camera.draw("Score: " + str(int(score)), 40, "white", 100, 20)  # draws score
    camera.display()


def endgame():
    """
    The function endgame() takes in no parameters and returns nothing. It displays the "game-over"
    screen after the players lose, replacing draw() and therefore having to re-display the background.
    No clear is necessary because once the player decides to resume, the draw function is enacted and
    what is drawn by endgame() is cleared. It calls restart() to help reset the objects in the game.
    """
    camera.draw(background)
    camera.draw(uvage.from_text(400, 200, "Game Over", 100, "red"))
    camera.draw(uvage.from_text(400, 300, "Your Score: " + str(int(score)), 60, "white"))
    camera.draw(uvage.from_text(400, 350, "Want to play Again? Press Space", 60, "white"))
    camera.display()
    restart()


def spaceship_actions():
    """
    The function spaceship_actions takes in no parameters and returns nothing. It controls both
    spaceships' left and right movement, fire-rate, firing, missile spawning, and boundary collision.
    """
    global game_on
    global projectile_list
    global timer_count_1
    global timer_count_2
    global enemies

    if uvage.is_pressing("q"):
        game_on = True

    if game_on and not game_over:
        # TIMER COUNTS FOR FIRING
        if timer_count_1 < 41:
            timer_count_1 += 1
        if timer_count_2 < 41:
            timer_count_2 += 1
        # P1 SPACESHIP MOVEMENT + FIRING
        if uvage.is_pressing("left arrow"):
            p1_spaceship.x -= p1_spaceship_xvelocity
        if uvage.is_pressing("right arrow"):
            p1_spaceship.x += p1_spaceship_xvelocity
        if uvage.is_pressing("up arrow") and timer_count_1 >= 40:
            missile = uvage.from_image(p1_spaceship.x, p1_spaceship.y, "8TGboEqGc.png")
            missile.scale_by(0.02)
            projectile_list.append(missile)
            timer_count_1 = 0
        # P2 SPACESHIP MOVEMENT + FIRING
        if uvage.is_pressing("a"):
            p2_spaceship.x -= p2_spaceship_xvelocity
        if uvage.is_pressing("d"):
            p2_spaceship.x += p2_spaceship_xvelocity
        if uvage.is_pressing("w") and timer_count_2 >= 40:
            missile = uvage.from_image(p2_spaceship.x, p2_spaceship.y, "8TGboEqGc.png")
            missile.scale_by(0.02)
            projectile_list.append(missile)
            timer_count_2 = 0
        # PLAYER BOUNDARIES
        for wall in boundaries:  # loops through walls to prevent player from moving off-screen
            p1_spaceship.move_to_stop_overlapping(wall)
            p2_spaceship.move_to_stop_overlapping(wall)


def projectile_actions():
    """
    The function projecticle_actions() takes no parameters and returns nothing. It controls the
    movement of missiles and also removes them from the project_list if they go off of the screen.
    """
    global missile_velocity
    global projectile_list
    if len(projectile_list) != 0:
        for missile in projectile_list:
            missile.y -= missile_velocity
            if missile.y < -10:
                projectile_list.remove(missile)  # gets rid of missile if they pass off-screen


def enemy_actions():
    """
    The function enemy_actions() takes no parameters and returns nothing. It controls the movement speed
    of the enemy spaceships (which slowly increases with time), randomly generates the enemies off of
    the screen to fall down, controls enemy spawn frequency, and deals with missile-enemy collision.
    :return:
    """
    global game_on
    global score
    global enemies
    global enemy_counter
    global projectile_list
    global finishing_line
    global game_over
    global explosion_images
    global explosion_list
    global enemy_speed_increase

    for enemy in enemies:  # loops through enemy list and moves them
        enemy.move_speed()

    random_x = random.randint(40, 760)
    random_y = random.randint(-20, 0)
    if game_on and not game_over:
        enemy_spaceship = uvage.from_image(random_x, random_y, "1654871.png")
        enemy_spaceship.scale_by(0.065)
        # generates enemy above screen to fall down
        if enemy_counter < 41:  # controls the pace of the enemy spawn rate
            enemy_counter += 1
            if enemy_counter >= 40:
                enemies.append(enemy_spaceship)  # spawns enemy
                enemy_counter = 0   # resets enemy counter to zero

    enemy_speed_increase += 0.001
    for enemy in enemies:  # sets speed of enemy to fall down at a constant rate
        enemy.speedy = 2 + enemy_speed_increase
        for projectile in projectile_list:  # if projectile touches enemy removes both enemy and projectile
            if projectile.touches(enemy):  # actions occur if projectile touches enemy
                explosion_point = uvage.from_image(enemy.x, enemy.y, explosion_images[0])  # explosion effect
                explosion_list.append(explosion_point)
                enemies.remove(enemy)  # removes enemy
                projectile_list.remove(projectile)  # removes projectile
                score += 10  # adds 10 to score if enemy is destroyed
        if enemy.touches(finishing_line):
            game_over = True


def coin_actions():
    """
    The function coin_actions() takes no parameters and returns nothing. It controls coin movement
    speeds, randomly generates the enemies off of the screen to fall down, controls coin spawning
    frequency, and coin-player collision.
    """
    global coins
    global coin_counter
    global p1_spaceship
    global p2_spaceship
    global score

    for coin in coins:
        coin.move_speed()

    random_x = random.randint(20, 750)
    random_y = random.randint(-20, 0)
    if game_on and not game_over:
        falling_coins = uvage.from_image(random_x, random_y, "bitcoin-2018-30.png")
        falling_coins.scale_by(0.035)
        if coin_counter < 300:  # helps control the spawn rate of the falling coin
            coin_counter += 1  # adds one to coin_counter
            if coin_counter >= 300:    # after a fixed time
                coins.append(falling_coins)   # spawns falling coin
                coin_counter = 0   # resets the count to zero and repeats the process
        for coin in coins:   # loops through each coin in coin list
            coin.speedy = 3.9  # sets the speed to fall down
            if coin.touches(p1_spaceship) or coin.touches(p2_spaceship):
                # if the coin comes in contact with any of the players' spaceship
                coins.remove(coin)  # coin is removed from the list
                score += 100  # coin is with 100 additional points
            elif coin.y > 605:  # if the coin passes below the screen it is automatically removed
                coins.remove(coin)


def restart():
    """
    The function restart() takes no parameters and returns nothing. All it does is reset any changing
    global variables, any global lists, and the starting position of the spaceships.
    """
    global game_over
    global enemies
    global coins
    global score
    global p1_spaceship
    global p2_spaceship
    global explosion_list
    global enemy_speed_increase

    if uvage.is_pressing("space"):
        # empties objects lists and changes boolean back to False so game can reset from the beginning circumstances
        game_over = False
        enemies = []
        coins = []
        explosion_list = []
        score = 0
        enemy_speed_increase = 0
        p1_spaceship.x = 500
        p2_spaceship.x = 300


def tick():
    """
    The function tick() takes no parameters and returns nothing. It calls each individual function
    (except restart, which is in endgame()) to then be called and used in uvage.timer_loop.
    """
    spaceship_actions()  # calls spaceship_actions to occur
    projectile_actions()  # calls projectile_actions to occur
    enemy_actions()  # calls enemy_actions to occur
    coin_actions()  # calls coin_actions to iccur
    if not game_over:
        draw()  # draws everything
    else:
        endgame()


uvage.timer_loop(60, tick)