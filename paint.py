import curses as c
import time
import PIL.Image
import math
import sys
PAD_HEIGHT = 31
PAD_WIDTH = 88
X_MARGIN = 30
Y_MARGIN = 10
COLORFIX = [1,2,3,4,5,6,7]
INFO_BG = 9
xOffset = 0
yOffset = 0
filename = "[unnamed]"
pairs = []
debugPairs = []
fieldChars = [] #list[list[str]]
fieldColors = [] #list[list[int]]
debugPairBool = False
debug16Pair = True
cursorDown = True
paintColor = 1
reverseColor = 8
currentColor = 0

def pad_ref(pad: c.window):
    pad.noutrefresh(yOffset,xOffset,0,0,min(PAD_HEIGHT-1,lines),min(PAD_WIDTH,c.COLS)-1)
def cursor_move(y,x,stdscr):
    global cursorY,cursorX
    if False:
        if y >= lines:
            y = 0
        elif y < 0:
            y = lines-1 #cursor can not move into the infobar
        if x >= c.COLS:
            x = 0
        elif x < 0:
            x = c.COLS-1
    #protection replaced by the relMove() boundaries
    cursorY = y
    cursorX = x
    stdscr.move(y,x)

def relMove(y,x,stdscr,pad = None,doColor=False,doRefresh=True):
    global xOffset,yOffset
    nextY = y+cursorY
    nextX = x+cursorX
    if (nextX > c.COLS-X_MARGIN) and (xOffset+c.COLS < PAD_WIDTH-1):
        nextX = cursorX
        xOffset += 1
    elif (nextX < X_MARGIN) and (xOffset > 0):
        nextX = cursorX
        xOffset -= 1
    if (nextY > lines-Y_MARGIN) and (yOffset+lines < PAD_HEIGHT-1):
        nextY = cursorY
        yOffset += 1
    if (nextY < Y_MARGIN) and (yOffset > 0):
        nextY = cursorY
        yOffset -= 1
    pass #fix from pad image edges, handle offset moving
    if (nextX >= c.COLS) or (nextX < 0):
        nextX = cursorX
    if (nextY >= lines) or (nextY < 0):
        nextY = cursorY
    pass #block moving past edges of screen
    if (yOffset + nextY >= PAD_HEIGHT):
        nextY = cursorY
    if (yOffset+nextY >= PAD_HEIGHT-1):
        safetyAdj = -1
    else:
        safetyAdj = 0
    if (xOffset + nextX >= PAD_WIDTH+safetyAdj):
        nextX = PAD_WIDTH-xOffset-1+safetyAdj
    cursor_move(nextY,nextX,stdscr)
    stdscr.addstr(nextY,nextX,fieldChars[yOffset+nextY][xOffset+nextX],
                  c.color_pair(fieldColors[yOffset+nextY][xOffset+nextX])) #attempt to show the cursor
    if doColor:
        color_pos(currentColor,pad)
    stdscr.move(nextY,nextX)
    stdscr.refresh()

def color_pos(color: int,pad,char: str = " "):
    fieldChars[yOffset+cursorY][xOffset+cursorX] = char
    fieldColors[yOffset+cursorY][xOffset+cursorX] = color
    pad.addstr(yOffset+cursorY,xOffset+cursorX,char,c.color_pair(color))

def save(colors,chars):
    #colormap = [(0,0,0),(0xff,0,0),(0,0xff,0),(0xff,0xff,0),(0,0,0xff),(0xff,0,0xff),(0,0xFF,0xFF),(0xC0,0xC0,0xC0)]
    colormap = [
        (12, 12, 12),      # Black
        (197, 15, 31),     # Red
        (19, 161, 14),     # Green
        (193, 156, 0),     # Yellow
        (0, 55, 218),      # Blue
        (136, 23, 152),    # Magenta
        (58, 150, 221),    # Cyan
        (204, 204, 204),   # White/Gray
    ]
    img = PIL.Image.new("RGB",(len(chars[0]),len(chars)),"black")
    imgPixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            colorNum = colors[y][x]
            if colorNum > 7:
                colorNum -= 7
            if colorNum >= len(colormap):
                colorNum = -1
            imgPixels[x,y] = colormap[colorNum] #type: ignore
    img.show()

def updateInfo(stdscr: c.window):
    stdscr.addstr(lines,c.COLS-21,f"off x {xOffset}, y {yOffset}",c.color_pair(INFO_BG))

def init(stdscr):
    global fieldChars, fieldColors, COLORFIX
    c.curs_set(1)
    c.start_color()
    stdscr.keypad(True)
    if sys.platform == "win32":
        COLORFIX = [4,2,6,1,5,3,7]
    fieldChars = [["" for x in range(PAD_WIDTH)] for y in range(PAD_HEIGHT)]
    fieldColors = [[0 for x in range(PAD_WIDTH)] for y in range(PAD_HEIGHT)]

def main(stdscr: c.window):
    global cursorX,cursorY, currentColor, lines
    pad = c.newpad(PAD_HEIGHT,PAD_WIDTH)
    cursorY = round(c.LINES/2)
    cursorX = round(c.COLS/2)
    if cursorY >= PAD_HEIGHT:
        cursorY = round(PAD_HEIGHT/2)
    if cursorX >= PAD_WIDTH:
        cursorX = round(PAD_WIDTH/2)
    lines = c.LINES-1
    cursor_move(cursorY,cursorX,stdscr)
    drawBool = False
    init(stdscr)
    for i in range(7):
        pairs.append(c.init_pair(i+1,COLORFIX[i],0))
        debugPairs.append((i+1,COLORFIX[i],0))
    for i in range(7):
        pairs.append(c.init_pair(8+i,0,COLORFIX[i]))
        debugPairs.append((8+i,0,COLORFIX[i]))
    for i in range(min(PAD_WIDTH,c.COLS)-1):
        try:
            pass
            #stdscr.addstr(lines,i,'b',c.color_pair(i%16))
        except Exception:
            pass
    stdscr.refresh()
    time.sleep(1)
    pad_ref(pad)
    if debugPairBool:
        for i in range(128-8):
            pairs.append(c.init_pair(i+16,2*i,0))
            debugPairs.append((i+16,2*i,0))
            pairs.append(c.init_pair(i+16+120,0,2*i))
            debugPairs.append((i+16+120,0,2*i))
        for y in range(0, min(c.LINES-2,PAD_HEIGHT-1)):
            for x in range(0, min(c.COLS-1,PAD_WIDTH-1)):
                pad.addstr(y,x, 'a',c.color_pair(16+round((3*x) % 255)))
    pad_ref(pad)
    for x in range(c.COLS-1):
        stdscr.addstr(lines,x," ",c.color_pair(INFO_BG))
    cursor_move(cursorY,cursorX,stdscr)
    pad_ref(pad)
    adjColorSet = 1
    lastColor = 0
    colorReg = 1
    debugColorInput = False
    while True:
        lines = c.LINES-1
        k = stdscr.getkey()
        stdscr.addstr(lines,c.COLS-21-7,k,c.color_pair(INFO_BG))
        if k == "q" or k == "Q":
            break
        if k in "wasd":
            color_pos(currentColor,pad)
        if k == c.KEY_UP or k == "w":
            relMove(-1,0,stdscr,pad,drawBool)
        elif k == c.KEY_DOWN or k == "s":
            relMove(1,0,stdscr,pad,drawBool)
        elif k == c.KEY_LEFT or k == "a":
            relMove(0,-1,stdscr,pad,drawBool)
        elif k == c.KEY_RIGHT or k == "d":
            relMove(0,1,stdscr,pad,drawBool)
        elif k == "e":
            drawBool = (not drawBool)
        elif k == "f" and debugColorInput:
            color_pos(9,pad)
        elif k == "g" and debugColorInput:
            color_pos(12,pad)
        elif k == "h" and debugColorInput:
            color_pos(15,pad)
        elif k == "j" and debugColorInput:
            color_pos(5,pad,"#")
        elif k == "p":
            stdscr.refresh()
        elif k == "l":
            pass
        elif k == "b":
            save(fieldColors,fieldChars)
        elif k == "v":
            colorReg = 0
        elif k == "1":
            currentColor = 0+7*colorReg+adjColorSet #cooked if statement because the smarter way to do this did not work idk
        elif k == "2":
            currentColor = 1+7*colorReg+adjColorSet
        elif k == "3":
            currentColor = 2+7*colorReg+adjColorSet
        elif k == "4":
            currentColor = 3+7*colorReg+adjColorSet
        elif k == "5":
            currentColor = 4+7*colorReg+adjColorSet
        elif k == "6":
            currentColor = 5+7*colorReg+adjColorSet
        elif k == "7":
            currentColor = 6+7*colorReg+adjColorSet
        elif k == "8" and False:
            currentColor = 7+7*colorReg+adjColorSet
        elif k == "9" and False:
            currentColor = 8+7*colorReg+adjColorSet
        elif k == "0":
            currentColor = 0
        elif k == "" or k == None:
            pass
        else:
            pass
        pass
        if lastColor != currentColor:
            lastColor = currentColor
            color_pos(currentColor,pad)
            colorReg = 1
        stdscr.addstr(lines,9," ",c.color_pair(0))
        stdscr.addstr(lines,11," ",c.color_pair(currentColor))
        stdscr.addstr(lines,12," ",c.color_pair(currentColor))
        stdscr.addstr(lines,10,str(currentColor),c.color_pair(currentColor))
        stdscr.addstr(lines,13," ",c.color_pair(0))
        updateInfo(stdscr)
        pad_ref(pad)
        stdscr.move(cursorY,cursorX)
        stdscr.noutrefresh()
        c.doupdate()
    time.sleep(1)

c.wrapper(main)

if debugPairBool or debug16Pair:
    for i in range(math.floor(len(debugPairs)/2)):
        print(f"{debugPairs[2*i]}    {debugPairs[2*i+1]}")
    print(f"last {debugPairs[-1]}")