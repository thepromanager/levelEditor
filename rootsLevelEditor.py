import pygame
import pygame_gui
import os

# C:/Users/brorb/wkspaces/Growth_Spurt/Assets/Levels
# /Users/noelearlwatson/Downloads/Growth_Spurt/Assets/Levels

levelPath = "ZenMode"

# "C:/Users/brorb/wkspaces/Growth_Spurt/Assets/Levels"
# "/Users/noelearlwatson/Downloads/Growth_Spurt/Assets/Levels"

repoToUnityPath = "C:/Users/brorb/wkspaces/Growth_Spurt/Assets/Levels" # gjorde en sånhär istället. då kan man tex ha leveleditorn i en mapp och låta denna vara "../Levels" typ
levelName = ""

resolution = (1300,800)
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
height=12
grid = [[None for i in range (height)] for j in range(width)]
waterTiles = {"start":["0000","0000","0000","0000","0000"]}
def waterGrid():
    return list(waterTiles.values())

def loadImage(name,r,r2=None):
    if not r2:
        r2=r
    print(name)
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, (r, r2))
    return image
def getFileNames(path):
    
    try:
        print("getting filenames at: " + repoToUnityPath + "/" + path)
        return [f[:-4] for f in os.listdir(repoToUnityPath + "/" + path) if f[-4:]==".txt"]
    except:
        print("failed getting filenames!")
        return []

grassImage = loadImage("levelEditorImages/dirt.png", gridSize)
starImage = loadImage("levelEditorImages/star.png", gridSize)
keyImage = loadImage("levelEditorImages/key.png", gridSize)
lockImage = loadImage("levelEditorImages/lock.png", gridSize)
riskyImage = loadImage("levelEditorImages/risky.png", gridSize)
rockImage = loadImage("levelEditorImages/stone.png", gridSize)
visiblerockImage = loadImage("levelEditorImages/visiblestone.png", gridSize)
visiblerock1Image = loadImage("levelEditorImages/visiblestone1.png", gridSize)
lavaImage = loadImage("levelEditorImages/lava.png", gridSize)
visiblelavaImage = loadImage("levelEditorImages/visiblelava.png", gridSize)
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

def loadLevel():
    print("Loading level at "+levelPath+str(levelNum)*folderNumbers+"/Level"+str(levelNum))
    try:
        levelSprite = pygame.image.load(levelPath+str(levelNum)*folderNumbers+"/Level"+str(levelNum)+".png")
        startParams = open(levelPath+str(levelNum)*folderNumbers+"/StartingHandParameter"+str(levelNum)+".txt", "r")
        waterParams = open(levelPath+str(levelNum)*folderNumbers+"/WaterTileParameters"+str(levelNum)+".txt", "r")

        width = (levelSprite.get_width()+1)//8 # always 7 tho
        height = (levelSprite.get_height()+1)//8
        grid = [[None for i in range (height)] for j in range(width)]

        waterColors = []
        rockColors = []
        mutationColors = []
        lavaColors = []

        for y in range(height):
            for x in range(width):
                color = levelSprite.get_at((x*8, y*8))[0:3] #RGBA -> RGB
                if color[2] == 255:
                    if not color in waterColors:
                        waterColors.append(color)
                    grid[x][y] = ("Water",waterColors.index(color))
                elif color[0] == 255:
                    if not color in lavaColors:
                        lavaColors.append(color)
                    grid[x][y] = ("Lava",lavaColors.index(color))
                elif color[1] == 255:
                    if not color in mutationColors:
                        mutationColors.append(color)
                    grid[x][y] = ("Mutation",mutationColors.index(color))
                elif color[0]==color[1]==color[2]:
                    if not color in rockColors:
                        rockColors.append(color)
                    grid[x][y] = ("Rock",rockColors.index(color))
                elif color[0]==136 and color[2]==21:
                    grid[x][y] = ("Visible Rock",-1)
                else:
                    pass

        paramater = startParams.read().split(",")
        while len(paramater)<5:
            paramater.append("")
        waterTiles = {"start":paramater}
        lines = waterParams.read().split("\n")
        for i in range(len(lines)):
            paramater = lines[i].split(",")
            while len(paramater)<5:
                paramater.append("")
            waterTiles[i] = paramater
        if len(lines)!=len(waterTiles)-1:
            print("something is wrong in load pls investigate"+"!!!!"*10)
        if len(lines)<len(waterColors):
            for i in range(len(waterColors)-len(waterTiles)+1):
                waterTiles[len(waterTiles)-1] = ["0000","0000","0000","0000",""]

        startParams.close()
        waterParams.close()

        print("Level loaded successfully!")

        return (width, height, grid, waterTiles, 0)
    except Exception as e:
        print("failed to load")
        print("error", e)
        return None
#does not work with new system yet, använder vi nånsin längre?


def newLoadLevel():
    print("NewLoading level at "+repoToUnityPath + "/" + levelPath+"/"+levelName)
    try:
        levelFile = open(repoToUnityPath + "/" + levelPath+"/"+levelName+".txt", "r")
        levelString = levelFile.read()
        levelList = levelString.split(".")
        startParams = levelList.pop(0)
        iceParam = int(levelList.pop(0))

        width = 7
        height = len(levelList)//7
        grid = [[None for i in range (height)] for j in range(width)]


        startParams = startParams.split(",")
        while len(startParams)<5:
            startParams.append("")
        waterTiles = {"start":startParams}

        for i in range(len(levelList)):

            x = i % width
            y = i//width
            block = levelList[i]

            blockData = block.split(":")
            if blockData[0] == "w":
                grid[x][y] = ("Water",int(blockData[1]))
                if len(blockData)>2:
                    # read water parameter
                    paramater = blockData[2].split(",")
                    while len(paramater)<5:
                        paramater.append("")
                    waterTiles[int(blockData[1])] = paramater
                elif not int(blockData[1]) in waterTiles:
                    waterTiles[int(blockData[1])] = ["0000","0000","0000","0000",""]
            elif blockData[0] == "hl":
                grid[x][y] = ("Lava",int(blockData[1]))
            elif blockData[0]=="l":
                grid[x][y] = ("Visible Lava",-1)
            elif blockData[0] == "m":
                grid[x][y] = ("Mutation",int(blockData[1]))
            elif blockData[0]=="h":
                grid[x][y] = ("Rock",int(blockData[1]))
            elif blockData[0]=="s":
                grid[x][y] = ("Visible Rock",-1)
            elif blockData[0]=="s1":
                grid[x][y] = ("Visible Rock1",-1)
            elif blockData[0]=="t":
                grid[x][y] = ("Risky",-1)
            elif blockData[0]=="st":
                grid[x][y] = ("Star",int(blockData[1]))
            elif blockData[0]=="k":
                grid[x][y] = ("Key",int(blockData[1]))
            elif blockData[0]=="kl":
                grid[x][y] = ("Lock",int(blockData[1]))
            elif blockData[0]=="r":
                grid[x][y] = (blockData[1],-1)

        levelFile.close()
        print("Level loaded successfully!")

        return (width, height, grid, waterTiles, iceParam)
    except Exception as e:
        print("failed to load")
        print("error", e)
        return None

def saveLevel():
    print("Saving level at "+levelPath+str(levelNum)*folderNumbers+"/Level"+str(levelNum))
    try:
        levelSprite = pygame.Surface((width*8-1, height*8-1)) 
        levelSprite.fill((0,0,0))
        startParams = open(levelPath+str(levelNum)*folderNumbers+"/StartingHandParameter"+str(levelNum)+".txt", "w")
        waterParams = open(levelPath+str(levelNum)*folderNumbers+"/WaterTileParameters"+str(levelNum)+".txt", "w")

        representedWaterNumbers = []

        try:
            for y in range(height):
                for x in range(width):
                    block = grid[x][y]
                    if block==None:
                        color = (185,122,87)
                    else:
                        brightness = 1+(block[1]*30)%254 # 40 and 253 are coprime dont worry!
                        if block[0]=="Visible Rock":
                            color = (136,0,21)
                        #elif block[0]=="Visible Lava":
                        #    color = (136,0,21)
                        elif block[0]=="Water":
                            color = (0,brightness,255)
                            if not block[1] in representedWaterNumbers:
                                representedWaterNumbers.append(block[1])
                        elif block[0]=="Rock":
                            color = (brightness,brightness,brightness)
                        elif block[0]=="Lava":
                            color = (255,brightness,0)
                        elif block[0]=="Mutation":
                            color = (brightness,255,0)
                        else:
                            raise Exception("Saving stars/roots/visible lava in image is not supported")
                    pygame.draw.rect(levelSprite, color, (8*x,8*y,7,7), 0)

            pygame.image.save(levelSprite, levelPath+str(levelNum)*folderNumbers+"/Level"+str(levelNum)+".png")
        except Exception as e:
            print("No image saved - cant render roots:")
            print(e)

        paramaters = waterTiles["start"]
        paramaters = [root for root in paramaters if root != ""]
        startParams.write(",".join(paramaters))
        for i in representedWaterNumbers:
            paramaters = waterTiles[i]
            paramaters = [root for root in paramaters if root != ""]
            waterParams.write(",".join(paramaters)+"\n"*(i!=representedWaterNumbers[-1]))
        print("Level saved successfully!")
    except Exception as e:
        print("failed to save")
        print("error", e)
        return None
#does not work with new system yet, använder vi nånsin längre?

def newSaveLevel():
    
    try:
        print("NewSaving level at "+repoToUnityPath + "/" + levelPath+"/"+levelName)
        levelFile = open(repoToUnityPath + "/" + levelPath+"/"+levelName+".txt", "w")

        representedWaterNumbers = []

        levelString = ""

        paramaters = waterTiles["start"]
        paramaters = [root for root in paramaters if root != ""]
        levelString += ",".join(paramaters)

        levelString += "." + str(ice_box.get_text())

        for y in range(height):
            for x in range(width):
                block = grid[x][y]
                if block==None:
                    letter = "d"
                else:
                    if block[0]=="Visible Rock":
                        letter = "s"
                    elif block[0]=="Visible Rock1":
                        letter = "s1"
                    elif block[0]=="Risky":
                        letter = "t"
                    elif block[0]=="Water":
                        letter = "w:" + str(block[1])
                        if not block[1] in representedWaterNumbers:
                            representedWaterNumbers.append(block[1])
                            paramaters = waterTiles[block[1]]
                            paramaters = [root for root in paramaters if root != ""]
                            letter += ":" + ",".join(paramaters)
                    elif block[0]=="Star":
                        letter = "st:" + str(block[1]) # 0?
                    elif block[0]=="Key":
                        letter = "k:" + str(block[1])
                    elif block[0]=="Lock":
                        letter = "kl:" + str(block[1])
                    elif block[0]=="Rock":
                        letter = "h:" + str(block[1])
                    elif block[0]=="Lava":
                        letter = "hl:" + str(block[1])
                    elif block[0]=="Visible Lava":
                        letter = "l"
                    elif block[0]=="Mutation":
                        letter = "m:" + str(block[1])
                    else:
                        letter = "r:" + str(block[0])
                levelString += "." + letter
        print(levelString)
        levelFile.write(levelString)
        levelFile.close()
        print("Level saved successfully!")
    except Exception as e:
        print("failed to save")
        print(grid)
        print("error", e)
        return None

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
                elif(block[0]=="Rock"):
                    img=rockImage
                elif(block[0]=="Star"):
                    img=starImage
                elif(block[0]=="Key"):
                    img=keyImage
                elif(block[0]=="Lock"):
                    img=lockImage
                elif(block[0]=="Visible Rock"):
                    img=visiblerockImage
                    text=None
                elif(block[0]=="Visible Rock1"):
                    img=visiblerock1Image
                    text=None
                elif(block[0]=="Risky"):
                    img=riskyImage
                    text=None
                elif(block[0]=="Lava"):
                    img=lavaImage
                elif(block[0]=="Mutation"):
                    img=mutationImage
                elif(block[0]=="Visible Lava"):
                    img=visiblelavaImage
                    text=None
                else:
                    img=rootImages[block[0]]
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
block_selector = pygame_gui.elements.UISelectionList(item_list=["Water","Rock","Visible Rock","Visible Rock1","Risky","Lava","Visible Lava","Mutation","Root","Erase","Star","Key","Lock"],relative_rect=pygame.Rect((50, 0), (200, 320)),manager=manager)
auto_increment = pygame_gui.elements.UISelectionList(item_list=["Auto-increment","Same Number"],relative_rect=pygame.Rect((50, 300), (200, 96)),manager=manager)

rock_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 390), (200, 40)),html_text="Rock group index:",manager=manager)
rock_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 420), (200, 50)),manager=manager)
rock_number_box.set_allowed_characters("numbers")
rock_number_box.set_text("0")

water_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 460), (200, 40)),html_text="Water group index:",manager=manager)
water_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 490), (200, 50)),manager=manager)
water_number_box.set_allowed_characters("numbers")
water_number_box.set_text("0")

lava_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 530), (200, 40)),html_text="Lava group index:",manager=manager)
lava_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 560), (200, 50)),manager=manager)
lava_number_box.set_allowed_characters("numbers")
lava_number_box.set_text("0")

mutation_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 600), (200, 40)),html_text="Mutation group index:",manager=manager)
mutation_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 630), (200, 50)),manager=manager)
mutation_number_box.set_allowed_characters("numbers")
mutation_number_box.set_text("0")

key_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((50, 670), (200, 40)),html_text="Lock/key group index:",manager=manager)
key_number_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 700), (200, 50)),manager=manager)
key_number_box.set_allowed_characters("numbers")
key_number_box.set_text("0")

water_selector = pygame_gui.elements.UISelectionList(item_list=["0000","0100","0010","1100","1010","1001","0110","0101","0011","1110","1101","1011","0111","1111",""],relative_rect=pygame.Rect((900, 105), (100, 550)),manager=manager)

less_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240,20), (80, 40)),text='Less',manager=manager)
more_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240,60), (80, 40)),text='More',manager=manager)
flip_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((240,100), (80, 40)),text='Flip X',manager=manager)

load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100,20), (80, 40)),text='Load',manager=manager)
newload_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100,120), (80, 40)),text='NewLoad',manager=manager)
save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000,20), (80, 40)),text='Save',manager=manager)
newsave_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000,120), (80, 40)),text='NewSave',manager=manager)
path_text_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1000, 180), (100, 50)),manager=manager)
path_text_box.set_text(levelPath)
level_text_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1100, 180), (100, 50)),manager=manager)
level_text_box.set_text("")
lava_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((1100, 300), (100, 40)),html_text="Ice:",manager=manager)
ice_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1100, 350), (100, 50)),manager=manager)
ice_box.set_allowed_characters("numbers")
ice_box.set_text("0")

level_selector = pygame_gui.elements.UISelectionList(item_list=getFileNames(levelPath),relative_rect=pygame.Rect((1000, 400), (200, 250)),manager=manager)
level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1000,350), (80, 40)),text='Load Files',manager=manager)



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
            (mouseX,mouseY)=pygame.mouse.get_pos()
            mouseX=int((mouseX-topLeft[0])//gridSize)
            mouseY=int((mouseY-topLeft[1])//gridSize)
            if(inBuildGrid(mouseX,mouseY)): # inbounds
                block=grid[mouseX][mouseY]
                if(mouseDown or event.button == 1):
                    selected=block_selector.get_single_selection()
                    if selected:
                        if(not (block and selected==block[0] and mouseDown)):
                            mouseDown=True
                            if(selected=="Water"):
                                waterInt=int(water_number_box.get_text())
                                if waterInt not in waterTiles:
                                    waterTiles[waterInt]=["0000","0000","0000","0000",""]
                                #add to scren grid and List
                                if(auto_increment.get_single_selection()=="Auto-increment"):
                                    water_number_box.set_text(str(waterInt+1))
                                grid[mouseX][mouseY]=("Water",waterInt)
                            elif(selected=="Rock"):
                                rockInt=int(rock_number_box.get_text())
                                grid[mouseX][mouseY]=(selected,rockInt)
                                if(auto_increment.get_single_selection()=="Auto-increment"):
                                    rock_number_box.set_text(str(rockInt+1))
                            elif(selected=="Key"):
                                keyInt=int(key_number_box.get_text())
                                grid[mouseX][mouseY]=(selected,keyInt)
                                if(auto_increment.get_single_selection()=="Auto-increment"):
                                    key_number_box.set_text(str(keyInt+1))
                            elif(selected=="Lock"):
                                keyInt=int(key_number_box.get_text())
                                grid[mouseX][mouseY]=(selected,keyInt)
                                if(auto_increment.get_single_selection()=="Auto-increment"):
                                    key_number_box.set_text(str(keyInt+1))
                            elif(selected=="Star"):
                                starInt=0
                                grid[mouseX][mouseY]=(selected,starInt)
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
                            elif(selected=="Root"):
                                selected=water_selector.get_single_selection()
                                if(selected!=None):
                                    grid[mouseX][mouseY]=(selected,-1)
                            elif(selected=="Erase"):
                                grid[mouseX][mouseY]=None
                            else:
                                grid[mouseX][mouseY]=(selected,-1)
                if not mouseDown and event.button == 3 and block:
                    selected = block[0]
                    #block_selector.set_single_selection(selected)
                    if(selected=="Water"):
                        water_number_box.set_text(str(block[1]))
                    elif(selected=="Rock"):
                        rock_number_box.set_text(str(block[1]))
                    elif(selected=="Lava"):
                        lava_number_box.set_text(str(block[1]))
                    elif(selected=="Mutation"):
                        mutation_number_box.set_text(str(block[1]))
                    elif(selected=="Key"):
                        key_number_box.set_text(str(block[1]))
                    elif(selected=="Lock"):
                        key_number_box.set_text(str(block[1]))
            if(inWaterGrid(mouseX,mouseY)):
                g=waterGrid()
                selected=water_selector.get_single_selection()
                block=g[mouseY][mouseX-width-2]
                if(selected!=None):
                    waterTiles[list(waterTiles.keys())[mouseY]][mouseX-width-2]=selected
                    



        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == level_button:
                    levelPath=path_text_box.get_text()
                    level_selector.set_item_list(getFileNames(levelPath))
                    level_selector.rebuild()
                if event.ui_element == save_button:
                    levelName=level_text_box.get_text()
                    levelPath=path_text_box.get_text()
                    saveLevel()
                if event.ui_element == newsave_button:
                    levelName=level_text_box.get_text()
                    levelPath=path_text_box.get_text()
                    newSaveLevel()
                if event.ui_element == load_button:
                    levelName=level_text_box.get_text()
                    levelPath=path_text_box.get_text()
                    level = loadLevel()
                    if(level):
                        (width, height, grid, waterTiles, ice) = level
                        ice_box.set_text(str(ice))
                if event.ui_element == newload_button:
                    levelName=level_text_box.get_text()
                    levelPath=path_text_box.get_text()
                    level = newLoadLevel()
                    if(level):
                        (width, height, grid, waterTiles, ice) = level
                        ice_box.set_text(str(ice))
                if event.ui_element == more_button:
                    for col in grid:
                        col.append(None)
                    height += 1
                if event.ui_element == less_button:
                    for col in grid:
                        col.pop()
                    height -= 1
                if event.ui_element == flip_button:
                    grid.reverse()
            if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == level_selector:
                    level_text_box.set_text(event.text)
        manager.process_events(event)

    manager.update(time_delta)

    game_display.fill((100,100,200))
    manager.draw_ui(game_display)
    drawGrid()
    drawWaterGrid()
    drawSelectorBlocks()
    pygame.display.flip()

#saveLevel()
#jag gillar inte autosave men dunno

pygame.quit()
quit()