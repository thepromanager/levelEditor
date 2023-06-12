import pygame
import pygame_gui


resolution = (1200,700)
gridSize = 32
topLeft = [350,gridSize]
pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode(resolution)#, pygame.FULLSCREEN)
pygame.display.set_caption('Roots - Level Editor')
manager=pygame_gui.UIManager(resolution,"selection_list.json")
pygame.font.init()
my_font = pygame.font.Font("Arial.ttf", 20)

width=7
height=20
grid = [[None for i in range (20)] for j in range(7)]
waterTiles = {"start":["0000","0000","0100","0010","0010"]}
def waterGrid():
    return list(waterTiles.values())

def loadImage(name,r,r2=None):
    if not r2:
        r2=r
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, (r, r2))
    return image

grassImage = loadImage("levelEditorImages/dirt.png", gridSize)
rockImage = loadImage("levelEditorImages/stone.png", gridSize)
visiblerockImage = loadImage("levelEditorImages/visiblestone.png", gridSize)
lavaImage = loadImage("levelEditorImages/lava.png", gridSize)
waterImage = loadImage("levelEditorImages/water.png", gridSize)
mutationImage = loadImage("levelEditorImages/mutation.png", gridSize)
rootImages = {
"0000":loadImage("levelEditorImages/random.png", gridSize),
"0100":loadImage("levelEditorImages/randomBad.png", gridSize),
"0010":loadImage("levelEditorImages/randomGood.png", gridSize),
"1100":loadImage("levelEditorImages/GreenUpLeft.png", gridSize),
"1010":loadImage("levelEditorImages/GreenHorizontal.png", gridSize),
"1001":loadImage("levelEditorImages/GreenDownLeft.png", gridSize),
"0110":loadImage("levelEditorImages/GreenUpRight.png", gridSize),
"0101":loadImage("levelEditorImages/GreenVertical.png", gridSize),
"0011":loadImage("levelEditorImages/GreenDownRight.png", gridSize),
"1110":loadImage("levelEditorImages/GreenTri2.png", gridSize),
"1101":loadImage("levelEditorImages/GreenTri1.png", gridSize),
"1011":loadImage("levelEditorImages/GreenTri4.png", gridSize),
"0111":loadImage("levelEditorImages/GreenTri3.png", gridSize),
"1111":loadImage("levelEditorImages/GreenQuad.png",gridSize),
"":grassImage
}
def inBuildGrid(x,y):
    if(x>=0 and x<width and y>=0 and y<height):
        return True
    else:
        return False
def inWaterGrid(x,y):
    if(x>=width+2 and x<width+7 and y>=0 and y<len(waterGrid())):
        return True
    else:
        return False
def drawGrid():
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            block = grid[x][y]
            img=None
            text=None
            if(block):
                text=my_font.render(str(block[1]), False, (0, 0, 0))
                if(block[0]=="Water"):
                    img=waterImage
                if(block[0]=="Rock"):
                    img=rockImage
                    #Show letter
                if(block[0]=="Visible Rock"):
                    img=visiblerockImage
                    text=None
                if(block[0]=="Lava"):
                    img=lavaImage
                    #Show letter
                if(block[0]=="Mutation"):
                    img=mutationImage
                    #Show letter
                if(block[0]=="Visible Lava"):
                    img=lavaImage
                    text=None
            else:
                img=grassImage
            
            game_display.blit(img, (x*gridSize+topLeft[0], y*gridSize+topLeft[1]))
            if(text):
                game_display.blit(text, (x*gridSize+topLeft[0]+10, y*gridSize+topLeft[1]+10))
def drawWaterGrid():
    g=waterGrid()
    k=list(waterTiles.keys())
    for y in range(len(g)):
        text=my_font.render(str(k[y]), False, (0, 0, 0))
        game_display.blit(text, ((1+width)*gridSize+topLeft[0], y*gridSize+topLeft[1]))
        for x in range(len(g[0])):
            block = g[y][x]
            img=None
            if(block):
                img=rootImages[block]
            else:
                img=grassImage
            game_display.blit(img, ((x+2+width)*gridSize+topLeft[0], y*gridSize+topLeft[1]))
def drawSelectorBlocks():
    for y in range(len(rootImages)):
        img=list(rootImages.values())[y]
        game_display.blit(img, (882, y*gridSize+122))
block_selector = pygame_gui.elements.UISelectionList(item_list=["Water","Rock","Visible Rock","Lava","Mutation","Erase"],relative_rect=pygame.Rect((50, 10), (200, 224)),manager=manager)
auto_increment = pygame_gui.elements.UISelectionList(item_list=["Auto-increment","Same Number"],relative_rect=pygame.Rect((50, 210), (200, 96)),manager=manager)

rock_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 300), (200, 40)),html_text="Rock group index:",manager=manager)
rock_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 330), (200, 50)),manager=manager)
rock_number_box.set_allowed_characters("numbers")
rock_number_box.set_text("0")

water_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 400), (200, 40)),html_text="Water group index:",manager=manager)
water_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 430), (200, 50)),manager=manager)
water_number_box.set_allowed_characters("numbers")
water_number_box.set_text("0")

lava_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 500), (200, 40)),html_text="Lava group index:",manager=manager)
lava_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 530), (200, 50)),manager=manager)
lava_number_box.set_allowed_characters("numbers")
lava_number_box.set_text("0")

mutation_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 600), (200, 40)),html_text="Mutation group index:",manager=manager)
mutation_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 630), (200, 50)),manager=manager)
mutation_number_box.set_allowed_characters("numbers")
mutation_number_box.set_text("0")

water_selector = pygame_gui.elements.UISelectionList(item_list=["0000","0100","0010","1100","1010","1001","0110","0101","0011","1110","1101","1011","0111","1111",""],relative_rect=pygame.Rect((900, 105), (100, 550)),manager=manager)


mouseDown = False
jump_out=False
while jump_out == False:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
        if mouseDown or (event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3) ):
            #mouseDown = True
            (mouseX,mouseY)=pygame.mouse.get_pos()
            mouseX=int((mouseX-topLeft[0])//gridSize)
            mouseY=int((mouseY-topLeft[1])//gridSize)
            if(inBuildGrid(mouseX,mouseY)): # inbounds
                block=grid[mouseX][mouseY]
                if(event.button == 1):
                    selected=block_selector.get_single_selection()
                    if selected:
                        if(selected=="Water"):
                            waterInt=int(water_number_box.get_text())
                            waterTiles[waterInt]=["0000","0000","0100","0010",""]
                            #add to scren grid and List
                            if(auto_increment.get_single_selection()=="Auto-increment"):
                                water_number_box.set_text(str(waterInt+1))
                            grid[mouseX][mouseY]=("Water",waterInt)
                        elif(selected=="Rock"):
                            rockInt=int(rock_number_box.get_text())
                            grid[mouseX][mouseY]=(selected,rockInt)
                            if(auto_increment.get_single_selection()=="Auto-increment"):
                                rock_number_box.set_text(str(rockInt+1))
                        elif(selected=="Lava"):
                            lavaInt=int(lava_number_box.get_text())
                            grid[mouseX][mouseY]=(selected,lavaInt)
                            if(auto_increment.get_single_selection()=="Auto-increment"):
                                lava_number_box.set_text(str(lavaInt+1))
                        elif(selected=="Mutation"):
                            mutationInt=int(mutation_number_box.get_text())
                            grid[mouseX][mouseY]=(selected,mutationInt)
                            if(auto_increment.get_single_selection()=="Auto-increment"):
                                mutation_number_box.set_text(str(mutationInt+1))
                        elif(selected=="Erase"):
                            grid[mouseX][mouseY]=None
                        else:
                            grid[mouseX][mouseY]=(selected,-1)
                if(event.button == 3) and block:
                    selected = block[0]
                    #block_selector.set_single_selection(selected)
                    if(selected=="Water"):
                        water_number_box.set_text(str(block[1]))
                    elif(selected=="Rock"):
                        rock_number_box.set_text(str(block[1]))
                    elif(selected=="Lava"):
                        lava_number_box.set_text(str(block[1]))
            if(inWaterGrid(mouseX,mouseY)):
                g=waterGrid()
                selected=water_selector.get_single_selection()
                block=g[mouseY][mouseX-width-2]
                print(selected)
                if(selected!=None):
                    waterTiles[list(waterTiles.keys())[mouseY]][mouseX-width-2]=selected
                    



        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pass
        manager.process_events(event)

    manager.update(time_delta)

    game_display.fill((100,100,200))
    manager.draw_ui(game_display)
    drawGrid()
    drawWaterGrid()
    drawSelectorBlocks()
    pygame.display.flip()



pygame.quit()
quit()