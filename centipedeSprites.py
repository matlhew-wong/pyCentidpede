import pygame, random
 
class Hero(pygame.sprite.Sprite):
    '''Our Hero class inherits from the Sprite class'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the hero
        self.image = pygame.image.load("hero.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (320, 448)
        
    def update(self):
        ''' Updates the hero to where the mouse position is '''
        self.rect.center = pygame.mouse.get_pos()
        # Check to make sure you can't go through the walls
        if self.rect.centerx < 32:
            self.rect.centerx = 32
        if self.rect.centerx > 608:
            self.rect.centerx = 608
        if self.rect.centery > 448:
            self.rect.centery = 448
        if self.rect.centery < 352:
            self.rect.centery = 352
            
class Arrow(pygame.sprite.Sprite):
    '''Our Arrow class inherite from the Sprite class'''
    def __init__(self):
        ''' Call the parent __init__() method '''
        pygame.sprite.Sprite.__init__(self) 
        
        # Set the image and rect attributes for the arrow
        self.image = pygame.Surface((1, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        
    def get_ypos(self):
        ''' Returns the current center y position '''
        return self.rect.centery
        
    def update(self):
        ''' Update the position of the arrow and make sure it keeps moving up '''
        self.rect.centery -= 5
            
class Shroom(pygame.sprite.Sprite):
    '''Our Bricks class inherits from the Sprite class'''
    def __init__(self, screen, x_pos, y_pos):
        ''' Call the parent __init__() method 
            accepts the screen and x, pos and y pos as parameters '''
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the shrooms
        self.image = pygame.image.load("shroom.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        
    def reset_shroom(self):
        ''' Resets the shroom to a random position on the screen '''
        self.rect.centerx = random.randrange(40, 600)
        self.rect.centery = random.randrange(30, 320)
        
class Bug(pygame.sprite.Sprite):
    '''Our Bug class inherits from the Sprite class'''
    def __init__(self, screen, x_pos, y_pos, dx):
        ''' Call the parent __init__() method 
            accepts the screen, x_pos, y_pos and dx as parameters '''
        pygame.sprite.Sprite.__init__(self)
        
        # Set the image and rect attributes for the bugs
        # Random image for the bug
        self.__buglist = [pygame.image.load("bug.gif"), pygame.image.load("bug2.gif"), pygame.image.load("bug3.gif"), pygame.image.load("bug4.gif")]
        self.image = random.choice(self.__buglist)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.__dx = dx
        
    def increase_speed(self):
        ''' Increase speed of the bug exponentially '''
        self.__dx ** 3

    def change_direction(self):
        ''' Change the direction of the direction and move it down 5 pixels '''
        self.rect.centery += 5
        self.__dx = -self.__dx
        
    def get_yspot(self):
        ''' get the y position of the bug '''
        return self.rect.centery
    
    def get_xspot(self):
        ''' Get the x position of the bug and returns it'''
        return self.rect.centerx
    
    def reset_bug(self):
        ''' Reset the bug near the top of the screen '''
        self.rect.centerx = random.randrange(40, 600)
        self.rect.centery = random.randrange(40, 100)
        self.image = random.choice(self.__buglist)
        if self.__dx < 0:
            self.__dx -= 1
        else:
            self.__dx += 1
        
    def update(self):
        ''' Updates the bug and keeps them moving across the screen '''
        self.rect.centerx += self.__dx
        # Checks to see if the bug hit the end of the screen and changes direction if it does 
        if self.rect.centerx > 625 or self.rect.centerx < 15:
            self.rect.centery += 5
            self.__dx = -self.__dx
            
class Score_keeper(pygame.sprite.Sprite):
    ''' Our score keeper class inherits from the Sprite class '''
    def __init__(self):
        ''' Call the parent __init__() method '''
        pygame.sprite.Sprite.__init__(self) 
        
        self.__myCustomFont = pygame.font.Font("mango_smoothie.otf", 60)
        self.__player_score = 0
        self.__player_lives = 10
        self.__kill_streak = 0
        
    def player_scored(self):
        ''' Add one to the score '''
        self.__player_score += 1
        
    def player_died(self):
        ''' Subtracts a life '''
        self.__player_lives -= 1
        
    def get_lives(self):
        ''' Return the number of lives '''
        return self.__player_lives
    
    def add_lives(self):
        self.__player_lives += 1
        
    def add_killstreak(self):
        ''' Add to the kill streak on the board '''
        self.__kill_streak += 1
        
    def reset_killstreak(self):
        ''' Reset the kill streak on the score board '''
        self.__kill_streak = 0
           
    def update(self):
        '''This method will be called to deisplay the score and lives'''
        message = "Score: %d / %d Lives / Kill Streak: %d" % (self.__player_score, self.__player_lives, self.__kill_streak)
        self.image = self.__myCustomFont.render(message, 1, (255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 400)
        
class Menu_button(pygame.sprite.Sprite):
    ''' Our menu button class inherits from the sprite class '''
    def __init__(self, label, color, size, location):
        ''' Inherits the label, the color, 
            the size and the location of the label '''
        # Call the parent __init() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the custom font and make it bold
        self.__myCustomFont = pygame.font.Font("mango_smoothie.otf", size)
        self.__myCustomFont.set_bold(True)
        self.__labelName = label
        self.__color = color
        self.__location = location
        
        # Set the label image
        self.image = self.__myCustomFont.render(self.__labelName, 1, self.__color)
        self.rect = self.image.get_rect()

        
    def change_color_purple(self):
        '''Change font color purple'''
        self.__color = (255, 0, 255)
        
    def change_color_green(self):
        '''Change font color green'''
        self.__color = (0, 255, 0)
        
    def update(self):
        '''This method will be called to display the menu item'''
        self.image = self.__myCustomFont.render(self.__labelName, 1, self.__color)
        self.rect = self.image.get_rect()
        self.rect.center = self.__location
    
        
        
            
    
            
