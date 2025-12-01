import curses as c
import time
PAD_HEIGHT = 30
PAD_WIDTH = 86
pairs = []
debugPairs = []
fieldChars = []
fieldColors = []
debugPairBool = False
cursorDown = True
paintColor = 1
reverseColor = 8

def pad_ref(pad):
    pad.refresh(0,0,0,0,min(PAD_HEIGHT-1,c.LINES-1),min(PAD_WIDTH,c.COLS)-1)
def cursor_move(y,x,stdscr):
    global cursorY,cursorX
    if y >= c.LINES:
        y = 0
    elif y < 0:
        y = c.LINES-1
    if x >= c.COLS:
        x = 0
    elif x < 0:
        x = c.COLS-1
    cursorY = y
    cursorX = x
    stdscr.move(y,x)

def relMove(y,x,stdscr):
    cursor_move(y+cursorY,x+cursorX,stdscr)

def color_pos(color: int,pad,char: str = " "):
    fieldChars[cursorY][cursorX] = char
    fieldColors[cursorY][cursorX] = color
    pad.addstr(cursorY,cursorX,char,c.color_pair(color))


def init(stdscr):
    global fieldChars, fieldColors
    c.curs_set(1)
    c.start_color()
    stdscr.keypad(True)
    fieldChars = [["" for x in range(PAD_WIDTH)] for y in range(PAD_HEIGHT)]
    fieldColors = [[-1 for x in range(PAD_WIDTH)] for y in range(PAD_HEIGHT)]

def main(stdscr):
    global cursorX,cursorY
    pad = c.newpad(PAD_HEIGHT,PAD_WIDTH)
    cursorY = round(PAD_HEIGHT/2)
    cursorX = round(c.COLS/2)
    cursor_move(cursorY,cursorX,stdscr)
    init(stdscr)
    for i in range(7):
        pairs.append(c.init_pair(i+1,i+1,0))
        debugPairs.append((i+1,i+1,0))
    for i in range(7):
        pairs.append(c.init_pair(8+i,0,i+1))
        debugPairs.append((8+i,0,i+1))
    for i in range(PAD_WIDTH-1):
        try:
            stdscr.addstr(c.LINES-1,i,'b',c.color_pair(i%16))
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
    cursor_move(cursorY,cursorX,stdscr)
    pad_ref(pad)
    while True:
        k = stdscr.getkey()
        if k == "q" or k == "Q":
            break
        elif k == c.KEY_UP or k == "w":
            relMove(-1,0,stdscr)
        elif k == c.KEY_DOWN or k == "s":
            relMove(1,0,stdscr)
        elif k == c.KEY_LEFT or k == "a":
            relMove(0,-1,stdscr)
        elif k == c.KEY_RIGHT or k == "d":
            relMove(0,1,stdscr)
        elif k == "f":
            color_pos(9,pad)
        elif k == "g":
            color_pos(12,pad)
        elif k == "h":
            color_pos(15,pad)
        elif k == "b":
            color_pos(5,pad,"#")
        elif k == "p":
            stdscr.refresh()
        pass
        pad_ref(pad)
        cursor_move(cursorY,cursorX,stdscr)
        stdscr.refresh()
    time.sleep(1)

c.wrapper(main)
if debugPairBool:
    for i in range(round(len(debugPairs)/2)):
        print(f"{debugPairs[2*i]}    {debugPairs[2*i+1]}")