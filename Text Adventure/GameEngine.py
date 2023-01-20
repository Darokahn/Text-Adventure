import keyboard
from time import sleep
UID = 2
AirRes = 0.9
Frict = 0.1
Gravity = 3

def Master(charID):
    for i in range(len(sprites)):
        if sprites[i][-1] == charID:
            char = i
    if keyboard.is_pressed("left"):
        sprites[char][1][0] = sprites[char][1][0] + 1
    if keyboard.is_pressed("right"):
        sprites[char][1][0] = sprites[char][1][0] - 1
    if keyboard.is_pressed("up"):
        sprites[char][1][1] = sprites[char][1][1] + 1
    if keyboard.is_pressed("down"):
        sprites[char][1][1] = sprites[char][1][1] - 1
    

def exportTexture(newTexture):
    lits = []
    for i in sprites:
        lits.append(i[1])
    miniX = lits[0][0]
    maxiX = lits[0][0]
    miniY = lits[0][1]
    maxiY = lits[0][1]
    for i in lits:
        if i[0] < miniX:
            miniX = i[0]
        if i[0] < miniY:
            miniY = i[1]
    for i in lits:
        i[0] = i[0] - miniX
        i[1] = i[1] - miniY
    from TextureSaves import TextureList
    proxy = TextureList()
    proxy.update({newTexture: lits})
    with open("TextureSaves.py", "w") as file:
        file.write(f"""def TextureList():
    return {proxy}""")
    
def start(stage = "default", mode = 1):
    global p
    global t
    global sprites
    global Texture
    from TextureSaves import TextureList
    t = 1
    p = mode
    wasd = [0, 0, 0, 0]
    sprites = importStage(stage)
    Texture = TextureList()
    while t == 1:
        while p == 1:
            speed()
            move("placer", 1)
            sleep(0.015)
            printscreen()
            if win(0):
                return True
        while p == -1:
            Master(0)
            wasd = putblock(0, wasd)
            printscreen()
            sleep(0.05)
            wasd = putblock(0, wasd)
            erase(0)

def pause():
    global p
    p = p*-1
def terminate():
    global t
    t = t*-1
          #["Texture", [position], collision, [speed], [[Vectors]], gravity, onground, carry, ID]
#sprites = [["placer", [5, 4], 1, [0,0], [[10,10]], 1, 0, [0, 0], 0], ["enemy", [5, 9], 0, [0,0], [[0, -1]], 1, 0, [0, 0], 1]]
"""Texture = {"placer": [[0,0]],
           "enemy": [[0,0, "!!"]],
           "null": [[0,0]],
           "block": [[0,0]],
           "bomb": [[0,0]]}
"""
def importStage(a_string):
    position = 0
    with open("stages.py") as file:
        content = file.readlines()
        proxy = content.copy()
        for i in range(len(content)):
            if "def "+a_string+"():" in content[i]:
                content[i] = "def Main():"
                file = open("stages.py", "w")
                for i in content:
                    file.write(i+"\n")
                file.close()
                from stages import Main
        with open("stages.py", "w") as file:
            for i in proxy:
                file.write(i)
        file.close()
    try:
        return (Main())
    except:
        return None

def exportStage(newStage):
    with open("stages.py", "a") as file:
        file.write(f"""
def {newStage}():
    return {sprites}""")
    file.close()

def ID():
    global UID
    UID += 1
    return UID

def distance(point, dist):
    lits = []
    for i in sprites:
        if (i[1][0] - point[0])**2 + (i[1][1] - point[1])**2 <= dist**2:
            lits.append(i[6])
    return lits

def colliders(charID):
    proxy = []
    for i in range(len(sprites)):
        i = sprites[i]
        if i[-1] != charID:
            if i[2] == 1:
                Xcoor = i[1][0]
                Ycoor = i[1][1]
                for i in Texture[i[0]]:
                    proxy.append([i[0]+Xcoor, i[1]+Ycoor])
    return proxy

def speed():
    global onground
    for i in sprites:
        vectorX = 0
        vectorY = 0
        char = i
        if char[2] == 1:
            if len(i[4]) > 0:
                for i in i[4]:
                    vectorX = vectorX +i[0]
                    vectorY = vectorY +i[1]
            char[3][0] = char[3][0] + vectorX
            char[3][1] = char[3][1] + vectorY
            moveDirX = 1 if char[3][0] > 0 else 0
            moveDirX = -1 if char[3][0] < 0 else moveDirX
            moveDirY = 1 if char[3][1] > 0 else 0
            moveDirY = -1 if char[3][1] < 0 else moveDirY
            frictionX = 0
            frictionY = 0
            if [char[1][0] + moveDirX, char[1][1]] in colliders(char[-1]):
                char[3][0] = 0
                frictionY = 1
            if [char[1][0], char[1][1]+moveDirY] in colliders(char[-1]):
                char[3][1] = 0
                frictionX = 1
            if [char[1][0], char[1][1]-1] in colliders(char[-1]):
                char[6] = 2
            else:
                char[6] -= 1
            char[3][0] = 0 if abs(char[3][0]) < 1 else char[3][0]
            char[3][1] = 0 if abs(char[3][1]) < 1 else char[3][1]
            if char[3][0] > 0:
                char[3][0] = char[3][0]*(AirRes - (frictionX*Frict))
                #- (char[3][0]**2)/(200-(155*frictionX))
            else:
                char[3][0] = char[3][0]*(AirRes - (frictionX*Frict))
                #+ (char[3][0]**2)/(200-(155*frictionX))
            if char[3][1] > 0:
                char[3][1] = char[3][1]*(AirRes - (frictionY*Frict))
                #- (char[3][1]**2)/(200-(155*frictionY))
            else:
                char[3][1] = char[3][1]*(AirRes - (frictionY*Frict))
                #+ (char[3][1]**2)/(200-(155*frictionY))
            char[7][0] = char[7][0] + char[3][0]
            char[7][1] = char[7][1] + char[3][1]
            if char[7][0] > 20:
                if [char[1][0] + moveDirX, char[1][1]] not in colliders(char[-1]):
                    char[1][0] = char[1][0] + 1
                    char[7][0] = 0
            if char[7][0] < -20:
                if [char[1][0] + moveDirX, char[1][1]] not in colliders(char[-1]):
                    char[1][0] = char[1][0] - 1
                    char[7][0] = 0
            if char[7][1] > 20:
                if [char[1][0], char[1][1] +moveDirY] not in colliders(char[-1]):
                    char[1][1] = char[1][1] + 1
                    char[7][1] = 0
            if char[7][1] < -20:
                if [char[1][0], char[1][1] +moveDirY] not in colliders(char[-1]):
                    char[1][1] = char[1][1] - 1
                    char[7][1] = 0
            if char[5] == 1:
                char[4] = [[0, Gravity*-1]]
            else:
                char[4] = [[0, 0]]
        return char[7]
            
def putblock(char, wasd):
    w = wasd[0]
    a = wasd[1]
    s = wasd[2]
    d = wasd[3]
    directionX = 0
    directionY = 0
    for i in sprites:
        if i[-1] == char:
            Xcoor = i[1][0]
            Ycoor = i[1][1]
            break
    if keyboard.is_pressed("d"):
        d += 1
        if d == 2:
            directionX = -1
            d = 0
    elif keyboard.is_pressed("a"):
        a += 1
        if a == 2:
            directionX = 1
            a = 0
    if keyboard.is_pressed("s"):
        s += 1
        if s == 2:
            directionY = -1
            s = 0
    elif keyboard.is_pressed("w"):
        w += 1
        if w == 2:
            directionY = 1
            w = 0
    if keyboard.is_pressed("r"):
        if not [Xcoor, Ycoor] in colliders(char):
            sprites.append(["enemy", [Xcoor, Ycoor], 0, [0,0], [], 0, 0, [0,0], ID()])
    if (directionX in [-1, 1]) or (directionY in [-1, 1]):
        if not [Xcoor+directionX,Ycoor+directionY] in colliders(char):
            sprites.append(["block", [Xcoor+(directionX),Ycoor+(directionY)], 1, [0,0], [], 1, 0, [0,0], ID()])
    return [w, a, s, d]

def erase(charID):
    for i in sprites:
        if i[-1] == charID:
            char = i
            break
    if keyboard.is_pressed("space"):
        for i in range(len(sprites)):
            if (sprites[i][1] == char[1]) and (sprites[i][-1] != charID):
                del sprites[i]
                break
        
def bomb():
    bombs = []
    for i in sprites:
        if i[0] == "bomb":
            bombs.append(i)
    for i in bombs:
        bombid = i
        for i in sprites:
            if i[-1] in distance(bombid[1], 4):
                i[4].append([(bombid[1][0]-i[1][0])*-10, (bombid[1][1]-i[1][1])*-10])
                
def win(charID):
    for i in sprites:
        if i[-1] == charID:
            position = i[1]
        if i[0] == "winTile":
            winPosition = i[1]
        else:
            winPosition = []
    if position == winPosition:
        print("win")
        return True

def printscreen():
    pixelarrayblack = []
    pixelarraylight = []
    pixelarrayalt = []
    for i in sprites:
        name = i[0]
        Xcoor = i[1][0]
        Ycoor = i[1][1]
        for i in Texture[name]:
            if len(i) == 2:
                pixelarrayblack.append([Xcoor+i[0], Ycoor+i[1]])
            elif i[2] == "||":
                pixelarraylight.append([Xcoor+i[0], Ycoor+i[1]])
            elif i[2] == "!!":
                pixelarrayalt.append([Xcoor+i[0], Ycoor+i[0]])

    screen = "\n__________________________________________"
    for i in range(sprites[0][1][1]-12,sprites[0][1][1]+13):
        y = i
        for i in range(sprites[0][1][0]-20,sprites[0][1][0]+21):
            x = i
            if [x, y] in pixelarrayblack:
                screen = "██" +screen
            elif [x, y] in pixelarraylight:
                screen = "||" +screen
            elif [x, y] in pixelarrayalt:
                screen = "!!" + screen
            else:
                screen = "  " + screen
        screen = "\n" + screen
    print(screen)

def move(sprite, speed):
    for i in range(len(sprites)):
        if sprites[i][0] == sprite:
            char = i
            break
    if keyboard.is_pressed("left"):
        sprites[char][4].append([3, 0])
    if keyboard.is_pressed("right"):
        sprites[char][4].append([-3, 0])
    if keyboard.is_pressed("up"):
        if sprites[char][5] == 0:
            sprites[char][4].append([0, 3])
        elif sprites[char][6] >= 0:
            sprites[char][4].append([0, 15])
    if keyboard.is_pressed("down"):
        sprites[char][4].append([0, -3])