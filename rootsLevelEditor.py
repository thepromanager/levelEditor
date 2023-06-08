import pygame
import pygame_gui


resolution = (1200,700)
gridSize = 32
topLeft = [350,gridSize]
pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode(resolution)#, pygame.FULLSCREEN)
pygame.display.set_caption('Roots - Level Editor')

width=7
height=20
grid = [[None for i in range (20)] for j in range(7)]
waterTiles = {"start":["0000","0000","0100","0010","0010"]}
def waterGrid():
    pass
    # return grid of waterTiles
manager=pygame_gui.UIManager(resolution)
def loadImage(name,r,r2=None):
    if not r2:
        r2=r
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, (r, r2))
    return image

grassImage = loadImage("levelEditorImages/dirt.png", gridSize)
rockImage = loadImage("levelEditorImages/stone.png", gridSize)
lavaImage = loadImage("levelEditorImages/lava.png", gridSize)
waterImage = loadImage("levelEditorImages/water.png", gridSize)
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
}
def inBuildGrid(x,y):
    if(x>=0 and x<width and y>=0 and y<height):
        return True
    else:
        return False


def drawGrid():
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            block = grid[x][y]
            img=None
            if(block):
                if(block[0]=="Water"):
                    img=waterImage
                    #Show letter
                if(block[0]=="Rock"):
                    img=rockImage
                    #Show letter
                if(block[0]=="Visible Rock"):
                    img=rockImage
                if(block[0]=="Lava"):
                    img=lavaImage
                    #Show letter
                if(block[0]=="Visible Lava"):
                    img=lavaImage
            else:
                img=grassImage
            game_display.blit(img, (x*gridSize+topLeft[0], y*gridSize+topLeft[1]))


block_selector = pygame_gui.elements.UISelectionList(item_list=["Water","Rock","Visible Rock","Lava","Erase"],relative_rect=pygame.Rect((50, 105), (200, 126)),manager=manager)
auto_increment = pygame_gui.elements.UISelectionList(item_list=["Auto-increment","Same Number"],relative_rect=pygame.Rect((50, 250), (200, 46)),manager=manager)

rock_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 350), (200, 40)),html_text="Rock group index:",manager=manager)
rock_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 380), (200, 50)),manager=manager)
rock_number_box.set_allowed_characters("numbers")
rock_number_box.set_text("0")

water_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 450), (200, 50)),html_text="Water group index:",manager=manager)
water_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 500), (200, 50)),manager=manager)
water_number_box.set_allowed_characters("numbers")
water_number_box.set_text("0")

lava_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 550), (200, 50)),html_text="Lava group index:",manager=manager)
lava_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 600), (200, 50)),manager=manager)
lava_number_box.set_allowed_characters("numbers")
lava_number_box.set_text("0")



jump_out=False
while jump_out == False:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True    
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3) :
            (mouseX,mouseY)=pygame.mouse.get_pos()
            mouseX=int((mouseX-topLeft[0])//gridSize)
            mouseY=int((mouseY-topLeft[1])//gridSize)
            if(inBuildGrid(mouseX,mouseY)): # inbounds
                block=grid[mouseX][mouseY]
                if(event.button == 1):
                    selected=block_selector.get_single_selection()
                    print((selected,0))
                    if(selected=="Water"):
                        waterInt=int(water_number_box.get_text())
                        waterTiles[waterInt]=["0000","0000","0100","0010"]
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
                        grid[mouseX][mouseY]=(selected,rockInt)
                        if(auto_increment.get_single_selection()=="Auto-increment"):
                            lava_number_box.set_text(str(lavaInt+1))
                    elif(selected=="Erase"):
                        grid[mouseX][mouseY]=None
                    else:
                        grid[mouseX][mouseY]=(selected,0)
                if(event.button == 3):
                    pass                 
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pass
        manager.process_events(event)

    manager.update(time_delta)

    game_display.fill((100,100,200))
    manager.draw_ui(game_display)
    drawGrid()

    pygame.display.flip()



pygame.quit()
quit()