#sets it so i can write pg rather than pygame
import pygame as pg
#importing library "time" for timed events
import time
from pygame import mixer
from os import path
pg.init()
#initialises the game

#RGB values for colours used throughout the code
CYAN = (52,78,91)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

#screen size settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
#clock
clock = pg.time.Clock()
#setting frames per second
FPS = 120
#CLASSES
#button class
class Button():
    def __init__(self, x , y , image , scale):
        #seeting the width and hight to the size of the image used
        width = image.get_width()
        height = image.get_height()
        #setting the size
        self.image = pg.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        #setting it to be not clicked (will change when clicked)
        self.clicked = False
    def draw(self, surface):
        #draw button on screen
        action = False
		#get mouse position
        pos = pg.mouse.get_pos()

		#check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            #if mouse is pressed and button isnt clicked then button is set to clicked
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                #if it is clicked then action is set to true
                action = True
                #if button isnt pressed then button doesnt activate
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

		#draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

#class for fighters in my game
class Fighter():
    def __init__ (self,player, x, y,flip,data,sprite_sheet,AnimSteps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_image(sprite_sheet,AnimSteps)
        #0 = idle   1 = run   2 = jump  3 = attack
        #4 = attack2    5 = hit    6 = death
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        #update for time for ticks
        self.update_time = pg.time.get_ticks()
        #character position when game start, first number is x second is y
        self.rect = pg.Rect((x, y, 80, 180))
        self.vel_y = 0
        #setting different variables to false so it does not begin doing an animation
        self.running = False
        #setting jmp to false
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        #setting the heath of the character, for other characters i will make it higher or lower but for the default it will be 100
        self.health = 100

    def load_image(self,sprite_sheet,AnimSteps):
        animation_list = []
        for y, animation in enumerate(AnimSteps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size,y * self.size, self.size, self.size)
                temp_img_list.append(pg.transform.scale(temp_img, (self.size*self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, surface, target,):
        SPEED = 20
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        #keypress for movement/attacks and abilities
        key = pg.key.get_pressed()
            #player 1 controls
        if self.player == 1 and fighter_1.health > 0:
                if key[pg.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pg.K_d]:
                    dx = SPEED
                    self.running = True
                if key[pg.K_w] and self.jump == False:
                    self.vel_y = -50
                    self.jump = True

                if key[pg.K_r] and self.attacking == False or key[pg.K_t] and self.attacking == False:
                    self.attack(surface,target)
                    if key[pg.K_r]:
                        time = 0
                        self.attack_type = 1

                        self.attacking == True
                    if key[pg.K_t]:
                        self.attack_type = 2
                        self.attacking == True
#player 2 controls
        if self.player == 2 and fighter_2.health > 0:
                    if key[pg.K_LEFT]:
                        dx = -SPEED
                        self.running = True
                    if key[pg.K_RIGHT]:
                        dx = SPEED
                        self.running = True
                    if key[pg.K_UP] and self.jump == False:
                        self.vel_y = -50
                        self.jump = True

                    if key[pg.K_k] and self.attacking == False or key[pg.K_l] and self.attacking == False:
                        self.attack(surface,target)
                        if key[pg.K_k]:
                            self.attack_type = 1
                        if key[pg.K_l]:
                            self.attack_type = 2



        #gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #ensureing the character does not fall/walk off of the game screen
        if self.rect.left + dx <0:
            dx = -self.rect.left
        if self.rect.right + dx >SCREEN_WIDTH:
            dx = SCREEN_WIDTH -self.rect.right
        if self.rect.bottom + dy > SCREEN_HEIGHT - 110:
            self.vel_y = 0
            self.jump = False
            dy = SCREEN_HEIGHT - 110 - self.rect.bottom


        #players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #player position
        self.rect.x += dx
        self.rect.y += dy
    #handle animation updates
    def update(self):
        #check what action the character is peforming
        if self.running == True:
            self.action = -1


        animation_cooldown = 100
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed
        if pg.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 2
            self.update_time = pg.time.get_ticks()
        if self.frame_index >=len(self.animation_list[self.action]):
            self.frame_index = 0
            self.attacking = False
    #attack
    def attack(self, surface,target):
        self.attacking = True
        #attack hit box
        attacking_rect = pg.Rect(self.rect.centerx - (5 * self.rect.width * self.flip), self.rect.y+50, 5 * self.rect.width, self.rect.height/3)
        pg.draw.rect(surface,(YELLOW), attacking_rect)
        #what happens when attacked
        if attacking_rect.colliderect(target.rect):
            target.health -= (10)#==============================================================
            self.attacking = True


#drawing character into game
    def draw(self, surface):
        img = pg.transform.flip(self.image, self.flip, False)
#        pg.draw.rect(surface,(GREEN), self.rect)
        surface.blit(img, (self.rect.x-(self.offset[0]*self.image_scale),self.rect.y - (self.offset[1]*self.image_scale)))

#game screen and name
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Elemental guardians")

#game variables
game_paused = False
menu_state = "main"
map_selected = ""

#define font
font = pg.font.SysFont("arialblack", 40)
font2 = pg.font.SysFont("impact", 200)
#load button image
resume_img = pg.image.load("PYGAME.IMG/Button/button_resume.png").convert_alpha()
options_img = pg.image.load("PYGAME.IMG/Button/button_mapselect.png").convert_alpha()
quit_img = pg.image.load("PYGAME.IMG/Button/button_quit.png").convert_alpha()
back_img = pg.image.load("PYGAME.IMG/Button/button_back.png").convert_alpha()
verses_img = pg.image.load("PYGAME.IMG/Button/button_VERSES.png").convert_alpha()
solo_img = pg.image.load("PYGAME.IMG/Button/button_SOLO.png").convert_alpha()
CharSelect_img = pg.image.load("PYGAME.IMG/Button/button_CharSelect.png").convert_alpha()

#backround image
#source of images
#https://www.freepik.com/free-photos-vectors/pixel-art
backround = pg.image.load("PYGAME.IMG/Backrounds/Campfire_backround.png")
waterbackround = pg.image.load("PYGAME.IMG/Backrounds/WaterBackround.jpg")
firebackround = pg.image.load("PYGAME.IMG/Backrounds/FireBackround.jpg")
earthbackround = pg.image.load("PYGAME.IMG/Backrounds/TempleBackround.png")
lifebackround = pg.image.load("PYGAME.IMG/Backrounds/LeafBackround.jpg")
metalbackround = pg.image.load("PYGAME.IMG/Backrounds/MetalBackround.jpg")
windbackround = pg.image.load("PYGAME.IMG/Backrounds/WindBackround.jpg")

#creating option buttons
resume_button = Button(760, 50, resume_img, 1)
options_button = Button(760, 250, options_img, 1)
quit_button = Button(760, 650, quit_img, 1)
back_button = Button(760, 900, back_img, 1)
back_button2 = Button(760, 900, back_img, 1)
verses_button = Button(760, 650, verses_img, 1)
solo_button = Button(760, 250, solo_img, 1)
CharSelect_button = Button(760, 450, CharSelect_img, 1)

#map images
#fire volcano map
FBG_scaled = pg.transform.scale(firebackround, (300, 300))
firebackround_button = Button(500, 50, FBG_scaled, 1)
#underwater map
WBG_scaled = pg.transform.scale(waterbackround, (300, 300))
waterbackround_button = Button(830, 50, WBG_scaled, 1)
#earth / shaolin temple map
EBG_scaled = pg.transform.scale(earthbackround, (300, 300))
earthbackround_button = Button(500, 450, EBG_scaled, 1)
#metal / collosium arena mao
MBG_scaled = pg.transform.scale(metalbackround, (300, 300))
metalbackround_button = Button(830, 450, MBG_scaled, 1)
#life / forrest map
LBG_scaled = pg.transform.scale(lifebackround, (300, 300))
lifebackround_button = Button(1160, 450, LBG_scaled, 1)
#wind / desert map
WDBG_scaled = pg.transform.scale(windbackround, (300, 300))
windbackround_button = Button(1160, 50, WDBG_scaled, 1)
#there is a map for each character this opens up opertunity for lore and personality


#characters
#sourced from cherit on itch.io
#WIND HASHASIN  WIND HASHASIN   WIND HASHASIN   #WIND HASHASIN  WIND HASHASIN   WIND HASHASIN   #WIND HASHASIN  WIND HASHASIN   WIND HASHASIN
#===================================================================================================================================================
#character picture for character selection screen
WindCharacterPicture = pg.image.load("PYGAME.IMG/Characters/Wind/wind_hashashin.png").convert_alpha()
WCharPic_scaled = pg.transform.scale(WindCharacterPicture, (200, 200))
WindChar_button = Button(100, 50, WCharPic_scaled, 1)
WindChar_button2 = Button(1660, 50, WCharPic_scaled, 1)

#character idle animation
#wind character idle animations
WCharSheet = pg.image.load("PYGAME.IMG/Characters/Wind/wind_SpriteSheet2.png").convert_alpha()
WCharAnim = [16]
WChar_SIZE = 144
#152
#143
#288
WChar_SCALE = 4
#135,85
WChar_OFFSET = [60,45]
WChar_DATA = [WChar_SIZE,WChar_SCALE,WChar_OFFSET]
#===================================================================================================================================================
#WIND HASHASIN  WIND HASHASIN   WIND HASHASIN   #WIND HASHASIN  WIND HASHASIN   WIND HASHASIN   #WIND HASHASIN  WIND HASHASIN   WIND HASHASIN




#Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight
#===================================================================================================================================================
#character picture for character selection screen
FireCharacterPicture = pg.image.load("PYGAME.IMG/Characters/Fire/fire_knight.png").convert_alpha()
FCharPic_scaled = pg.transform.scale(FireCharacterPicture, (200, 200))
FireChar_button = Button(100, 650, FCharPic_scaled, 1)
FireChar_button2 = Button(1660, 650, FCharPic_scaled, 1)
#character idle animation
#Fire character idle animations
FCharSheet = pg.image.load("PYGAME.IMG/Characters/Fire/fire_SpriteSheet.png").convert_alpha()
FCharAnim = [16]
FChar_SIZE = 144
#152
#143
#288
FChar_SCALE = 4
#135,85
FChar_OFFSET = [60,40]
FChar_DATA = [FChar_SIZE,FChar_SCALE,FChar_OFFSET]
#===================================================================================================================================================
#Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight Fire Knight


#Water wizzard  Water wizzard   Water wizzard   Water wizzard   Water wizzard   Water wizzard   Water wizzard   Water wizzard   Water wizzard
#===================================================================================================================================================
#character picture for character selection screen
WaterCharacterPicture = pg.image.load("PYGAME.IMG/Characters/Water/water_wiz.png").convert_alpha()
WaterCharPic_scaled = pg.transform.scale(WaterCharacterPicture, (200, 200))
WaterChar_button = Button(100, 350, WaterCharPic_scaled, 1)
WaterChar_button2 = Button(1660, 350, WaterCharPic_scaled, 1)
#character idle animation
#Water character idle animations
WaCharSheet = pg.image.load("PYGAME.IMG/Characters/Water/water_spritesheet.png").convert_alpha()
WaCharAnim = [16]
WaChar_SIZE = 144
#152
#143
#288
WaChar_SCALE = 4
#135,85
WaChar_OFFSET = [60,55]
WaChar_DATA = [WaChar_SIZE,WaChar_SCALE,WaChar_OFFSET]
#===================================================================================================================================================
#Water wizzard  Water wizzard   Water wizzard   Water wizzard   Water wizzard   Water wizzard   Water wizzard   Water wizzard   Water wizzard


#Leaf Ranger Leaf Ranger    Leaf Ranger Leaf Ranger Leaf Ranger Leaf Ranger Leaf Ranger Leaf Ranger Leaf Ranger
#===================================================================================================================================================
#character picture for character selection screen
LeafCharacterPicture = pg.image.load("PYGAME.IMG/Characters/Leaf/Leaf_ranger.png").convert_alpha()
LeafCharPic_scaled = pg.transform.scale(LeafCharacterPicture, (200, 200))
LeafChar_button = Button(400, 350, LeafCharPic_scaled, 1)
LeafChar_button2 = Button(1360, 350, LeafCharPic_scaled, 1)
#character idle animation
#Leaf character idle animations
LCharSheet = pg.image.load("PYGAME.IMG/Characters/Leaf/Leaf_rangerSpritesheet.png").convert_alpha()
LCharAnim = [16]
LChar_SIZE = 144
#152
#143
#288
LChar_SCALE = 4
#135,85
LChar_OFFSET = [60,55]
LChar_DATA = [LChar_SIZE,LChar_SCALE,LChar_OFFSET]
#===================================================================================================================================================
#Leaf Ranger Leaf Ranger    Leaf Ranger Leaf Ranger Leaf Ranger Leaf Ranger Leaf Ranger Leaf Ranger Leaf Ranger



#Earth Monk Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk
#===================================================================================================================================================
#character picture for character selection screen
EarthCharacterPicture = pg.image.load("PYGAME.IMG/Characters/Earth/Earth_monk.png").convert_alpha()
EarthCharPic_scaled = pg.transform.scale(EarthCharacterPicture, (200, 200))
EarthChar_button = Button(400, 650, EarthCharPic_scaled, 1)
EarthChar_button2 = Button(1360, 650, EarthCharPic_scaled, 1)
#character idle animation
#Earth character idle animations
ECharSheet = pg.image.load("PYGAME.IMG/Characters/Earth/Earth_monkSpritesheet.png").convert_alpha()
ECharAnim = [16]
EChar_SIZE = 144
#152
#143
#288
EChar_SCALE = 4
#135,85
EChar_OFFSET = [60,45]
EChar_DATA = [EChar_SIZE,EChar_SCALE,EChar_OFFSET]
#===================================================================================================================================================
#Earth Monk Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk  Earth Monk


#Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf
#===================================================================================================================================================
#character picture for character selection screen
CrystCharacterPicture = pg.image.load("PYGAME.IMG/Characters/Crystal/Crystal_dwarf.png").convert_alpha()
CrystCharPic_scaled = pg.transform.scale(CrystCharacterPicture, (200, 200))
CrystChar_button = Button(400, 50, CrystCharPic_scaled, 1)
CrystChar_button2 = Button(1360, 50, CrystCharPic_scaled, 1)
#character idle animation
#crystal character idle animations
CCharSheet = pg.image.load("PYGAME.IMG/Characters/Crystal/Crystal_dwarfSpritesheet.png").convert_alpha()
CCharAnim = [16]
CChar_SIZE = 144
CChar_SCALE = 6
#135,85
CChar_OFFSET = [60,55]
CChar_DATA = [CChar_SIZE,CChar_SCALE,CChar_OFFSET]
#===================================================================================================================================================
#Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf Crytal Dwarf


#==================================music===============================================music================================
mixer.init()
menu_music = mixer.music.load("music/Pixel 12.mp3")

mixer.music.set_volume(1)

#Play the music

mixer.music.play()

#Infinite loop



#==================================music===============================================music================================


gamebackround = metalbackround
gmbg = False
game_paused = True
player1Char = ""
player2Char = ""
#drawing functions
#text
def draw_text(text,font,text_colour,x,y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x,y))
#backround
def draw_bg():
    scaled_bg = pg.transform.scale(backround, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg,(0,0))
def draw_heathbar(health, x, y):
    ratio = health / 100
    pg.draw.rect(screen, BLACK,(x - 10, y - 10, 720,120))
    pg.draw.rect(screen, RED,(x, y, 700,100))
    pg.draw.rect(screen, GREEN,(x, y, 700 * ratio, 100))
def draw_gamebg():
    scaled_bg = pg.transform.scale(gamebackround, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg,(0,0))
def get_image(sheet,width,height):
    image = pg.Surface((width,height)).convert_alpha()
    image.blit(sheet,(0,0),(0,0,width,height))
    return image

#default character will be wind character
fighter_1 = Fighter(1, 200,800,False,WChar_DATA, WCharSheet,WCharAnim)
fighter_2 = Fighter(2, 1400,800,False,WChar_DATA, WCharSheet,WCharAnim)
#gameloop
run = True
while run:
    clock.tick(FPS)
    #setting the backround
    screen.fill(CYAN)
    if gmbg == True:
        draw_gamebg()
        #move fighters
        fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT, screen,fighter_2)
        fighter_2.move(SCREEN_WIDTH,SCREEN_HEIGHT, screen,fighter_1)
        #update fighters
        fighter_1.update()
        fighter_2.update()

#        fighter_2.move(SCREEN_WIDTH)
        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        #draw heathbars
        draw_heathbar(fighter_1.health,20, 80)
        draw_heathbar(fighter_2.health,1200, 80)
    else:
        draw_bg()



    #things to happen while the game is paused/menu screen


    if game_paused == True:
        fighter_2.frame_index = 10

        #music when game screen is in play
        #text for characters to allow player to know who they are
        if player1Char == "Wind":
            draw_text("player 1:Wind Warrior",font,WHITE,10,900)
        if player1Char == "Fire":
            draw_text("player 1:Fire Fighter",font,WHITE,10,900)
        if player1Char == "Water":
            draw_text("player 1:Water Wizard",font,WHITE,10,900)
        if player2Char == "Wind":
            draw_text("player 2:Wind Warrior",font,WHITE,1300,900)
        if player2Char == "Fire":
            draw_text("player 2:Fire Fighter",font,WHITE,1300,900)
        if player2Char == "Water":
            draw_text("player 2:Water Wizard",font,WHITE,1300,900)
        if player2Char == "Leaf":
            draw_text("player 2:Forest Folk",font,WHITE,1300,900)
        if player1Char == "Leaf":
            draw_text("player 1:Forest Folk",font,WHITE,10,900)
        if player1Char == "Earth":
            draw_text("player 1:Mountain Monk",font,WHITE,10,900)
        if player2Char == "Earth":
            draw_text("player 2:Mountain Monk",font,WHITE,1300,900)
        if player2Char == "Cryst":
            draw_text("player 2:Viktor",font,WHITE,1300,900)
        if player1Char == "Cryst":
            draw_text("player 1:Viktor",font,WHITE,10,900)







        #changing variable and allowing the player to understand what map they are playing on
        draw_text("Map:",font,WHITE,10,10)
        if map_selected == "Fire":
            draw_text("Mount Magma",font,WHITE,10,50)
            gamebackround = firebackround
        elif map_selected == "Water":
            draw_text("Poseidons Playground",font,WHITE,10,50)
            gamebackround = waterbackround
        elif map_selected == "Life":
            draw_text("Forest of Farvalian",font,WHITE,10,50)
            gamebackround = lifebackround
        elif map_selected == "Metal":
            draw_text("Chrome Colloseum",font,WHITE,10,50)
            gamebackround = metalbackround
        elif map_selected == "Earth":
            draw_text("Shaolin Sanctuary",font,WHITE,10,50)
            gamebackround = earthbackround
        elif map_selected == "Wind":
            draw_text("Terra Nullius",font,WHITE,10,50)
            gamebackround = windbackround
        else:
            draw_text("default",font,WHITE,10,50)


        #things to occour when the menu screen is up / when menu state is "main"
        if menu_state == "main":
            if resume_button.draw(screen):
                mixer.music.rewind()
                mixer.music.pause()
                battle_music = mixer.music.load("music/battle music.mp3")
                mixer.music.play()
                game_paused = False
                gmbg = True
            #button to change menu states to map select or character select
            elif options_button.draw(screen):
                menu_state = "map_select"
            elif CharSelect_button.draw(screen):
                menu_state = "CharSelect"
            #button for closing the game
            elif quit_button.draw(screen):
                pg.quit()
        #things to happen when the map select screen is up / when menu state is "map select
        if menu_state == "map_select":
            if back_button.draw(screen):
                menu_state = "main"
            if firebackround_button.draw(screen):
                map_selected = "Fire"
            if waterbackround_button.draw(screen):
                map_selected = "Water"
            if earthbackround_button.draw(screen):
                map_selected = "Earth"
            if metalbackround_button.draw(screen):
                map_selected = "Metal"
            if windbackround_button.draw(screen):
                map_selected = "Wind"
            if lifebackround_button.draw(screen):
                map_selected = "Life"
        #things to occour when the menu state is character select
        if menu_state == "CharSelect":
            if solo_button.draw(screen):
                pass
            if verses_button.draw(screen):
                menu_state = "MultiCharSelect"
            if back_button.draw(screen):
                menu_state = "main"
        #things to happen when the menu state is multiplayer character selection screen
        if menu_state == "MultiCharSelect":
            if back_button2.draw(screen):
                menu_state = "CharSelect"
            if WindChar_button.draw(screen):
                fighter_1 = Fighter(1, 200,800,False,WChar_DATA, WCharSheet,WCharAnim)
                player1Char = "Wind"
            if WindChar_button2.draw(screen):
                fighter_2 = Fighter(2, 1400,800,False,WChar_DATA, WCharSheet,WCharAnim)
                player2Char = "Wind"
            if FireChar_button.draw(screen):
                fighter_1 = Fighter(1, 200,800,True,FChar_DATA, FCharSheet,FCharAnim)
                player1Char = "Fire"
            if FireChar_button2.draw(screen):
                fighter_2 = Fighter(2, 1400,800,True,FChar_DATA, FCharSheet,FCharAnim)
                player2Char = "Fire"
            if WaterChar_button.draw(screen):
                fighter_1 = Fighter(1, 200,800,True,WaChar_DATA, WaCharSheet,WaCharAnim)
                player1Char = "Water"
            if WaterChar_button2.draw(screen):
                fighter_2 = Fighter(2, 1400,800,True,WaChar_DATA, WaCharSheet,WaCharAnim)
                player2Char = "Water"
            if LeafChar_button.draw(screen):
                fighter_1 = Fighter(1, 200,800,True,LChar_DATA, LCharSheet,LCharAnim)
                player1Char = "Leaf"
            if LeafChar_button2.draw(screen):
                fighter_2 = Fighter(2, 1400,800,True,LChar_DATA, LCharSheet,LCharAnim)
                player2Char = "Leaf"
            if EarthChar_button.draw(screen):
                fighter_1 = Fighter(1, 200,800,True,EChar_DATA, ECharSheet,ECharAnim)
                player1Char = "Earth"
            if EarthChar_button2.draw(screen):
                fighter_2 = Fighter(2, 1400,800,True,EChar_DATA, ECharSheet,ECharAnim)
                player2Char = "Earth"
            if CrystChar_button.draw(screen):
                fighter_1 = Fighter(1, 200,800,True,CChar_DATA, CCharSheet,CCharAnim)
                player1Char = "Cryst"
            if CrystChar_button2.draw(screen):
                fighter_2 = Fighter(2, 1400,800,True,CChar_DATA, CCharSheet,CCharAnim)
                player2Char = "Cryst"



        #things to happen when the menu state is solo character seleciton screen


    #display menu
    #the gameplay part
    else:
            draw_text("press SPACE to end game",font,BLACK,10,10)
            if fighter_1.health <= 0:
                draw_text("Player 2 wins",font2,BLACK,((SCREEN_WIDTH/2)-400),(SCREEN_HEIGHT/2)-100)
            if fighter_2.health <= 0:
                draw_text("Player 1 wins",font2,BLACK,((SCREEN_WIDTH/2)-400),(SCREEN_HEIGHT/2)-100)



    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                mixer.music.rewind()
                mixer.music.pause()
                mixer.music.load("music/Pixel 12.mp3")
                mixer.music.play()
                fighter_1.health = 100
                fighter_2.health = 100
                game_paused = True
                gmbg = False
        if event.type == pg.QUIT:
            pg.quit()
            #run = False

    pg.display.update()

pg.quit()
