# I - Import and Initialize
import pygame, centipedeSprites, random
pygame.init()

# Import for background music
pygame.mixer.init()

# Create the screen
screen = pygame.display.set_mode((640, 480))   

def DrawBackground(background, xpos, ypos):
    '''This function draws the background picture on the screen.
       it accepts the background object and the x, y position as
       parameters and uses the x and y positions to know where to
       blit.'''
    screen.blit(background, [xpos, ypos])
    
def main():
    '''This function defines the 'mainline logic' for our game.'''
      
    # D - DISPLAY
    pygame.display.set_caption("pyCentipede")
    
    # Background image of the garden
    background = pygame.image.load('main_menu.jpg')
    background = background.convert()
    
    # x, y pos for blitting the background picture
    xpos = 0
    ypos = 0
     
    # E - ENTITIES
    screen.blit(background, (0, 0))
    
    # GAME OVER sign
    game_over = pygame.image.load("game_over.jpg")
    
    # Convert for efficiancy
    game_over = game_over.convert()
    
    # Main Menu Sprites
    # Create a Hero sprite object to pick which button to click
    hero = centipedeSprites.Hero()
    
    # Button objects using the button object class
    label_title = centipedeSprites.Menu_button("Centipede", (0, 255, 0), 100, (320, 60))
    label_instruction1 = centipedeSprites.Menu_button("Click to shoot the bugs", (0, 0, 0), 30, (320, 200))
    label_instruction2 = centipedeSprites.Menu_button("before they reach your bottom ground", (0, 0, 0), 30, (320, 250))
    label_instruction3 = centipedeSprites.Menu_button("*** Don't let them pass this line ***", (255, 0, 0), 30, (320, 360))
    label_quit = centipedeSprites.Menu_button("Quit", (0, 255, 0), 60, (160, 430))
    label_play = centipedeSprites.Menu_button("Play", (0, 255, 0), 60, (480, 430))
    
    # Create button class
    labelGroup = pygame.sprite.OrderedUpdates(label_quit, label_play, label_title, label_instruction1, label_instruction2, label_instruction3, hero)
    
    # Music and sound effects
    pygame.mixer.music.load("main_theme.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1) 
    menu_sound = pygame.mixer.Sound("glass_breaking.mp3")
    menu_sound.set_volume(1)
    bug_sound = pygame.mixer.Sound("ganandorf.wav")
    bug_sound.set_volume(0.2)
    
    # Create bugs
    bugs = []
    for i in range(50):
        x_pos = random.randrange(50, 590)
        y_pos = random.randrange(40, 100)
        dx =  random.randrange(-6, 5, 10)
        bugs.append(centipedeSprites.Bug(screen, x_pos, y_pos, dx))
    
    # Create bug group
    bugGroup = pygame.sprite.Group(bugs)
    
    # Create score keeper object
    score_keeper = centipedeSprites.Score_keeper()
    
    # Create Shrooms
    shrooms = []
    for i in range(100):
        x_pos = random.randrange(50, 590)
        y_pos = random.randrange(30, 320) 
        shrooms.append(centipedeSprites.Shroom(screen, x_pos, y_pos))
    
    # Shroom group
    shroomGroup = pygame.sprite.Group(shrooms)
    
    # Create arrow group so that arrow objects can be added later
    arrowGroup = pygame.sprite.Group()
    
    # Create all sprites group so that all can be updated instantly and drawn
    allSprites = pygame.sprite.OrderedUpdates(score_keeper, hero, bugs, shrooms)
 
    # A - Action Broken into ALTER steps
     
    # A - Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    
    # L - Loop
    
    # Menu Loop
    keep_menuGoing = True
    
    while keep_menuGoing:       
        
        # T - Time
        clock.tick(30)
        
        # E - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exits the menu loop AND the game loop
                keep_menuGoing = False
                keepGoing = False
        # A - Action(Menu Loop)
        
        # Check to see if your mouse icon has hovered over the button and turns a purple if so
        if hero.rect.colliderect(label_quit.rect):
            label_quit.change_color_purple()
            menu_sound.play()
            
            # Check to see if player clicked on the quit button and exit both loops if so
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Fade music out to make space for the next song
                # play a click button song
                pygame.mixer.music.fadeout(2000)
                keep_menuGoing = False  
                keepGoing = False
                
        # Change color back to green if mouse icon gets off the button        
        else:
            label_quit.change_color_green()
            
        # Check to see if the icon hovers over the play button and changes it purple if it does
        if hero.rect.colliderect(label_play.rect):
            label_play.change_color_purple()
            menu_sound.play()
            
            # IF the button clicks then change the song to caravan popularized by duke ellington and clear the screen of the buttons and exit the menu loop and enter the main loop
            if event.type == pygame.MOUSEBUTTONDOWN:
                # play a click button song
                pygame.mixer.music.stop()
                pygame.mixer.music.load("game_theme.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(-1)
                keep_menuGoing = False
                label_quit.kill()
                label_play.kill()
                label_title.kill()
                label_instruction1.kill()
                label_instruction2.kill()
                label_instruction3.kill()
        
        # If the icon leaves the button then the button turns back green
        else:
            label_play.change_color_green()
                
        # R - Refresh screen
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)
         
        pygame.display.flip()
    
    # Kill Streak for the game loop (every 10 kills gives you one life)
    kill_streak = 0
    
    # L - Loop(Game Loop)
    while keepGoing:
     
        # T - Time
        clock.tick(30)
     
        # E - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create arrow when the mousebutton is pushed down to shoot
                arrow = centipedeSprites.Arrow()
                arrow.rect.center = hero.rect.center
                arrowGroup.add(arrow)
                allSprites.add(arrow)  
                
        # Check collision with bug on bug or bug on shroom
        for bug in bugGroup:
            if pygame.sprite.spritecollide(bug, shroomGroup, False):
                bug.change_direction()      
            if bug.get_yspot() > 320:
                # play you get hurt sound
                bug.reset_bug()
                score_keeper.player_died()
                bug.increase_speed()
                score_keeper.reset_killstreak()
                kill_streak = 0
        
        # Multiple-Sprite collision detection and reporting
        for arrow in arrowGroup:
            list_shroom_hit = pygame.sprite.spritecollide(arrow, shroomGroup, False)
            list_bug_hit = pygame.sprite.spritecollide(arrow, bugGroup, False)
            if arrow.get_ypos < 0:
                arrow.kill()
            for shrooms in list_shroom_hit:
                shrooms.reset_shroom()
                arrow.kill()
            for bug in list_bug_hit:
                kill_streak += 1
                bug_sound.play()
                bug.increase_speed()
                bug.reset_bug()
                score_keeper.player_scored()
                score_keeper.add_killstreak()
                
                if kill_streak == 10:
                    score_keeper.add_lives()
                    # Add one up mushroom sound
                    kill_streak = 0
                    score_keeper.reset_killstreak()
                
        
          
        if score_keeper.get_lives() <= 0:
            # play you suck sound effect
            allSprites.empty()
            screen.blit(game_over, (0, 0))
         
        # Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
         
        pygame.display.flip()
     
    # Close the game window
    pygame.quit()    
     
     
# Call the main function
main()
