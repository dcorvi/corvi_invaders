__author__ = 'Dennis Corvi'

#   Dennis Corvi

#   Tried to make an explosion occur after BG hit
#   Tried to decrease amount of time between bad guy shots as more bad guys disappeared
#   Tried to have Return key required to exit after winning or losing
#   V.2 to have next level of enemies and incorporate shots per enemy into scoring

#   Commented out available changes for good guy and bad guy characters and sounds
#   Did not see any trademarks for sounds used

#   Use Left and Right arrows or a and d keys to move the hero and space, Up or w key to fire a shot
#   Mouse click to exit out of window at any time
#   Hitting a Bad Guy = 5 points

# Import all modules
import graphics
import time
import rectangle
import random
import pyglet

# Create good guy at bottom of screen
def load_Good_Guy(window):
    hero = graphics.Image(graphics.Point(280, 455), './/images//ship.gif')
    # hero = graphics.Image(graphics.Point(280, 455), 'champion-attack.gif')
    hero.draw(window)
    return hero

# Create cycling bad guys for movement across screen
def load_Bad_Guys(window, numberOfBadGuys):
    bgList = []
    for i in range(numberOfBadGuys):
        bg = graphics.Image(graphics.Point(i*90+50, 70), './/images//bgship.gif')
        # bg = graphics.Image(graphics.Point(i*90+50, 70), 'ogre-attack.gif')
        bgList.append(bg)
        bg.draw(window)
    return bgList

# Create, draw and add good guy shots to a list
def create_GG_Shots(window, goodGuy, ggShotList):
    shot = graphics.Image(graphics.Point((goodGuy.getAnchor()).x, goodGuy.getAnchor().y),".//images//ggshot.gif")
    ggShotList.append(shot)
    shot.draw(window)
    return ggShotList

# Create, draw and add bad guy shots to a list
def create_BG_Shots(window, badGuy, BGShotList):
    shot = graphics.Image(graphics.Point((badGuy.getAnchor()).x, badGuy.getAnchor().y),".//images//bgshot.gif")
    BGShotList.append(shot)
    shot.draw(window)
    return BGShotList

# Create random star pattern
def load_Stars(window, windowWidth, windowHeight):
    # Set number of stars to draw
    NUMBER_OF_STARS = 40
    for i in range(NUMBER_OF_STARS):
        star = graphics.Point((random.randint(1, windowWidth)),(random.randint(1, windowHeight)))
        star.setFill("white")
        star.draw(window)

# Create intro text
def intro_Text(window, windowWidth, windowHeight):
    # Create horizon
    horizon = graphics.Line(graphics.Point(0, 465),graphics.Point(600, 465))
    horizon.setFill("white")
    horizon.setWidth(2)
    horizon.draw(window)
    window.setBackground("black")
    # Add intro text
    welcomeText = graphics.Text((graphics.Point(300,190)),"Welcome to Corvi Invaders \n\n\n\n Eliminate all enemy "
                                                          "ships! \n\n\n Use <-- and --> OR A and D keys to move \n\n"
                                                          " Use Space, Up OR W to fire \n\n\n You have unlimited shots!\n\n\n Game starts in 4 seconds")
    welcomeText.setTextColor("white")
    welcomeText.setFace("courier")
    welcomeText.setStyle("bold")
    welcomeText.draw(window)
    # Draw star pattern
    load_Stars(window, windowWidth, windowHeight)
    # Pause for reading
    time.sleep(3)
    # Play sound for intro to disguise pyglet start up sound play lag
    startSound = pyglet.media.StaticSource(pyglet.media.load(".//sounds//clear.wav"))
    # Used to force sound to prevent error
    window.focus_force()
    startSound.play()
    # Continue reading
    time.sleep(4.3)
    welcomeText.undraw()
    # Add text for comedic value
    baseText = graphics.Text((graphics.Point(300,190)),"Get Ready..")
    baseText.setTextColor("white")
    baseText.setFace("courier")
    baseText.setStyle("bold")
    baseText.draw(window)
    time.sleep(2)
    baseText.undraw()

# Used to detect if picture rectangles are overlapping
# Used rectangle.py to define how rectangles around pictures are created
def overlap(r1,r2):
    hoverlaps = True
    voverlaps = True
    if (r1.left() > r2.right()) or (r1.right() < r2.left()):
        hoverlaps = False
    if (r1.top() > r2.bottom()) or (r1.bottom() < r2.top()):
        voverlaps = False
    return hoverlaps and voverlaps

# Function containing while loop where all window action is contained
def event_Loop(window, badGuys, goodGuy, ggShotList, BGShotList, windowWidth, numberOfBadGuys):
    # Set constants - movement speeds of characters and shots
    BG_SPEED = 5
    GG_X_SPEED = 0
    GG_Y_SPEED = 0
    GG_SHOT_SPEED = -8
    BG_SHOT_SPEED = 8

    # Set starting accumulator values
    loopAccumulator = 250
    enemyNumberAccumulator = 6
    shotNumberAccumulator = 0
    shotsPerEnemyNumberAccumulator = 0
    badGuysShot = 0

    # Define all sounds
    shotSound = pyglet.media.StaticSource(pyglet.media.load(".//sounds//ggShot.wav"))
    # shotSound = pyglet.media.StaticSource(pyglet.media.load("ggShot2.wav"))
    gameOverSound = pyglet.media.StaticSource(pyglet.media.load(".//sounds//gameover.wav"))
    bgSound = pyglet.media.StaticSource(pyglet.media.load(".//sounds//BGExplosion.wav"))
    # bgSound = pyglet.media.StaticSource(pyglet.media.load("bghit.wav"))
    bgshotSound = pyglet.media.StaticSource(pyglet.media.load(".//sounds//fire.wav"))
    winSound = pyglet.media.StaticSource(pyglet.media.load(".//sounds//win.wav"))
    # Update window as backup for exception handling when loop accumulator text redraws itself over
    window.update()
    # Draw score and loop, amount of enemies and shot accumulator information
    loopAccumulatorText = graphics.Text((graphics.Point(500,350)),loopAccumulator)
    loopAccumulatorText.setTextColor("white")
    loopAccumulatorText.draw(window)
    enemyNumberAccumulatorText = graphics.Text((graphics.Point(490,370)),enemyNumberAccumulator)
    enemyNumberAccumulatorText.setTextColor("white")
    enemyNumberAccumulatorText.draw(window)
    shotNumberAccumulatorText = graphics.Text((graphics.Point(500,390)),shotNumberAccumulator)
    shotNumberAccumulatorText.setTextColor("white")
    shotNumberAccumulatorText.draw(window)
    shotsPerEnemyNumberAccumulatorText = graphics.Text((graphics.Point(490,330)),shotsPerEnemyNumberAccumulator)
    shotsPerEnemyNumberAccumulatorText.setTextColor("white")
    shotsPerEnemyNumberAccumulatorText.draw(window)
    # Create initial score text
    scoreText = graphics.Text((graphics.Point(500,410)),"Score: 0")
    scoreText.setTextColor("white")
    scoreText.draw(window)
    # Set starting score
    score = 0

    while True:
        # Look for keys pressed to control good guy
        keyPressed = window.checkKey()
        # Keep good guy moving while keys are pressed
        goodGuy.move(GG_X_SPEED,GG_Y_SPEED)
        # Create a rectangle for the good guy to be used to detect for if its hit by a bad guy shot
        goodGuysRectangle = rectangle.rect(goodGuy)
        # Create a bad guy clone list to be able to remove bad guys from the window
        bgCloneArmy = []
        # Set text to redraw with changing game information
        loopAccumulatorText.setText("Time Until Enemy Shot: %s" % loopAccumulator)
        enemyNumberAccumulatorText.setText("Enemies Left: %s" % enemyNumberAccumulator)
        shotNumberAccumulatorText.setText("Number of Shots: %s" % shotNumberAccumulator)
        shotsPerEnemyNumberAccumulatorText.setText("Shots Per Enemy: %s" % shotsPerEnemyNumberAccumulator)

        # To prevent division by 1 error
        if shotNumberAccumulator >= 1:
            shotsPerEnemyNumberAccumulatorText.setText("Shots Per Enemy: {0:0.2f}"
                                                       .format((badGuysShot/shotNumberAccumulator)))
        # Keep everything in window moving at 0.05 speed
        time.sleep(0.05)

        # Control good guy with left and right keys without letting hero go off screen
        if keyPressed == "Left" or keyPressed == "a" and goodGuy.getAnchor().getX() >= 25:
            GG_X_SPEED = -7
        elif keyPressed == "Right"or keyPressed == "d" and goodGuy.getAnchor().getX() <= 580:
            GG_X_SPEED = 7

        # Fire a shot from the hero and returns accumulated shots in ggshotlist list
        elif keyPressed == "space" or keyPressed == "Up" or keyPressed == "w":
            # Draw shot and accumulate
            create_GG_Shots(window, goodGuy, ggShotList)
            # Add shot number to accumulator
            shotNumberAccumulator = shotNumberAccumulator + 1
            # Play shooting sound
            shotSound.play()
        # To prevent the hero from "skating"
        else:
            GG_X_SPEED = 0

        # Remove hit BGs from original BG list and create clone copies for another list
        if len(ggShotList) > 0:
            for shotRec in ggShotList:
                # Move shots up window
                shotRec.move(0,GG_SHOT_SPEED)
                shotRectangle = rectangle.rect(shotRec)
                # Undraw and remove from list if shot gets past bad guys without a hit
                if shotRec.getAnchor().y < 30:
                    shotRec.undraw()
                    ggShotList.remove(shotRec)
                for bgRec in badGuys:
                    bg = bgRec
                    badGuysRectangle = rectangle.rect(bg)
                    # Detect if shot hits bad guy
                    if (overlap(badGuysRectangle,shotRectangle)):
                        # Create a clone copy for each bad guy hit and add to clone copy list to be compared
                        bgClone = bgRec.clone()
                        bgCloneArmy.append(bgClone)
                        # Undraw shot and remove from shot list
                        shotRec.undraw()
                        ggShotList.remove(shotRec)
                        score = score + 5
                        # Adjust score info for score text each time enemie is defeated
                        scoreText.setText("Score: %s" % score)
                        bgSound.play()

        # Cloned copy of original BG list to be matched up and narrowed down
        # Remove bad guys from screen using list of cloned bad guys
        if len(bgCloneArmy) > 0 and numberOfBadGuys != 0:
            for obg in badGuys:
                obgRectangle = rectangle.rect(obg)
                # Match BGs in original badGuys list with bgClones
                for bgHit in bgCloneArmy:
                    bgHitRectangle = rectangle.rect(bgHit)
                    if (overlap(obgRectangle,bgHitRectangle)) and numberOfBadGuys != 0:
                        # Remove a bad guy from bad guy list, clone bad guy list and undraw 1 bad guy from window
                        obg.undraw()
                        badGuys.remove(obg)
                        bgCloneArmy.remove(bgHit)
                        enemyNumberAccumulator = enemyNumberAccumulator - 1
                        # Remove 1 from current amount of bad guys to minimize errors and check for redundancy
                        numberOfBadGuys = numberOfBadGuys - 1
                        badGuysShot = badGuysShot + 1
                    # Just in case of an error
                    else:
                        pass

        # Create win message if all bad guys eliminated - must position if statement BEFORE bad guys movement
        if numberOfBadGuys == 0:
            winText = graphics.Text((graphics.Point(300,225)),"All Enemies Eliminated! \n\n"
                                                              " You Win! \n \n (Click to exit) ")
            winText.setTextColor("white")
            winText.setSize(14)
            winText.setStyle("bold")
            winText.draw(window)
            # Play win sound and wait for mouse click to exit window
            winSound.play()
            window.getMouse()

        # Move bad guys across the screen without going off
        if badGuys[0].getAnchor().getX()-(badGuys[0].getWidth()/2)<=0 or \
        badGuys[numberOfBadGuys-1].getAnchor().getX()+(badGuys[numberOfBadGuys-1].getWidth()/2) >= windowWidth:
            # Move bad guys in opposite direction if going off screen
            BG_SPEED = -BG_SPEED
        for bg in badGuys:
            loopAccumulator = loopAccumulator - 1
            # loopAccumulator = loopAccumulator + (len(badGuys))+1
            bg.move(BG_SPEED,0)

        # Have bad guys create shot and shoot down
        if len(badGuys) > 0 and numberOfBadGuys != 0:
            if loopAccumulator <= 1:
                create_BG_Shots(window, random.choice(badGuys), BGShotList)
                # Reset the loop accumulator to fire next shot so that shots are not continually streaming down
                loopAccumulator = loopAccumulator + 250
                # loopAccumulator = loopAccumulator - 300//(len(badGuys))
                bgshotSound.play()
            else:
                pass

        # Remove hit BGs from original BG list
        if len(ggShotList) > 0:
            # Turn shots in shot lists into shot rectangles to test for collisions with list of bad guys individually
            for shotRec in ggShotList:
                # Create rectangle for each shot fired
                shotRectangle = rectangle.rect(shotRec)
                for bgRec in badGuys:
                    # Create rectangle for each bad guy
                    badGuysRectangle = rectangle.rect(bgRec)
                    # Check for bad guy and shot rectangle collisions
                    if (overlap(badGuysRectangle,shotRectangle)):
                        bgClone = bgRec.clone()
                        bgCloneArmy.append(bgClone)
                        shotRec.undraw()
                        ggShotList.remove(shotRec)

        # End game if good guy is hit by bad guy shot
        if len(BGShotList) > 0:
            # Go through list of bad guy shots
            for BGshotRec in BGShotList:
                BGshotRec.move(0,BG_SHOT_SPEED)
                BGshotRectangle = rectangle.rect(BGshotRec)
                # Undraw and remove from list if shot gets past bad guys without a hit
                if BGshotRec.getAnchor().y > 455:
                    BGshotRec.undraw()
                    BGShotList.remove(BGshotRec)
                #   Check the bad guy shot against the good guy rectangle for collision -> if a collision, end the game
                elif (overlap(BGshotRectangle,goodGuysRectangle)):
                    winText = graphics.Text((graphics.Point(300,225)),"You Lost! \n \n (Click to exit) ")
                    # Explosion on good guy if hit
                    kaboom = graphics.Image(graphics.Point((goodGuy.getAnchor()).x, goodGuy.getAnchor().y),
                                            ".//images//smallExplosion.gif")
                    kaboom.draw(window)
                    winText.setTextColor("white")
                    winText.setSize(14)
                    winText.draw(window)
                    gameOverSound.play()
                    # Wait for mouse click to exit -> tried to checkKey for return to exit unsuccessfully *???*
                    window.getMouse()
                    window.close()
                else:
                    pass

        # Exit program if mouse clicked
        if window.checkMouse():
            # Break needed to prevent any action from continuing after losing or winning
            break
            window.close()

# Creates the window, sets up the good guy and badguys to be inserted into the event loop - gets the second mouse click
# If game is won or ended
# -> Event loop has the set number of bad guys per game
def main():
    # Gg and bg shot lists for shots fired to be accumulated - placed in main for exception handling purposes
    GG_SHOT_LIST = []
    BG_SHOT_LIST = []
    # Determine window width and height
    WIN_WIDTH = 600
    WIN_HEIGHT = 500
    # Determine number of bad guys
    NUM_OF_BAD_GUYS = 6
    # Create the window
    win = graphics.GraphWin("Corvi Invaders", WIN_WIDTH, WIN_HEIGHT)
    intro_Text(win, WIN_WIDTH, WIN_HEIGHT)
    # Exception handling to fix shot hitting 2 bad guys at once error
    try:
        hero = load_Good_Guy(win)
        bgList = load_Bad_Guys(win, NUM_OF_BAD_GUYS)
        # Start game in motion
        event_Loop(win, bgList, hero, GG_SHOT_LIST, BG_SHOT_LIST, WIN_WIDTH, NUM_OF_BAD_GUYS)
    # Draw message and restart event loop in the case of an error
    except ValueError or IndexError:
        errorText = graphics.Text((graphics.Point(280,255)),"You hit 2 enemies with 1 shot! \n\n "
                                                            "But I fixed this error with exception handling so you can "
                                                            "finish the game!\n Resetting shot"" \n\n (Click to exit) ")
        errorText.setTextColor("white")
        errorText.draw(win)
        win.getMouse()
        errorText.undraw()
        # Restart the event loop -> game information text will flicker but allow the player to finish the game
        event_Loop(win, bgList, hero, GG_SHOT_LIST, BG_SHOT_LIST, WIN_WIDTH, NUM_OF_BAD_GUYS)
main()
