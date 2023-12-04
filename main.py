import js as p5

# Base class for creating instances of screens. There are two child classes of this class: MainScreen and WinScreen. It abstracts the drawing so that the two child screens can reuse it's code.
class Screen:
  
  def __init__(self, filename, title, subtext):
    self.img = p5.loadImage(filename)
    self.title = title
    self.subtext = subtext
  def draw(self):
    p5.background(0)
    p5.image(self.img,50,0,320,320)
    p5.fill(0)
    p5.textSize(24)
    p5.textFont('Courier')
    p5.text(self.title, 150, 265)
    p5.textSize(14)
    p5.text(self.subtext, 130, 286)

# Child of "Screen"
class MainScreen(Screen):
  def __init__(self):
    super().__init__("maze-start.png", "MAZE BY WILL", "PRESS RETURN TO START")

# Child of "Screen"
class WinScreen(Screen):
  def __init__(self):
    super().__init__("maze-exit.png", "YOU ESCAPE!", "PRESS RETURN TO RESTART")

# Contains a single string that represents the map.
# This allows for editing or custom levels via editor.
class Map:
  def __init__(self, h, w, map_string):
    self.original_map = map_string
    self.h = h
    self.w = w
    self.map_string = list(map_string)
    self.img_b = p5.loadImage("blank.png")
    self.img_d = p5.loadImage("door.png")
    self.img_e = p5.loadImage("exit.png")
    self.img_k = p5.loadImage("key.png")
    self.img_w = p5.loadImage("wall.png")

  # Reset the starting position and replace the key
  def reset(self):
    self.map_string = list(self.original_map)

  def get(self, x, y):
    index = y * self.w + x
    return self.map_string[index]

  def set(self, x, y, value):
    index = y * self.w + x
    self.map_string[index] = value

  # Each character in the string represents a type of tile. 
  # B = Blank
  # D = Door
  # E = Exit
  # K = Key
  # W = Wall
  def draw(self, x, y):
    if (self.get(x,y)=="B"): 
      p5.image(self.img_b,x*52,y*52)
    if (self.get(x,y)=="D"): 
      p5.image(self.img_d,x*52,y*52)
    if (self.get(x,y)=="E"): 
      p5.image(self.img_e,x*52,y*52)
    if (self.get(x,y)=="K"): 
      p5.image(self.img_k,x*52,y*52)
    if (self.get(x,y)=="W"): 
      p5.image(self.img_w,x*52,y*52)

# Player class contains location of character and inventory. Functions include moving and collision detection.
class Player:
  def __init__(self, x, y, has_key):
    self.x = x
    self.y = y
    self.startx = x
    self.starty = y
    self.has_key = has_key
    self.img_a = p5.loadImage("adventurer.png")

  # This defines what happens when a player interacts with a tile type.
  def check(self, x, y, gamemap):
    global game_state
    if (gamemap.get(x,y) == "B"): 
      return True
    if (gamemap.get(x,y) == "D" and self.has_key == True): 
      gamemap.set(x,y,"B")
      return True
    if (gamemap.get(x,y) == "K"):
      gamemap.set(x,y,"B") # Remove key from map, make it a blank tile.
      self.has_key = True
      return True
    if (gamemap.get(x,y) == "E"):
      game_state = "win"
      return True
    return False

  # Revert the player to their starting position.
  def reset(self):
    self.x = self.startx
    self.y = self.starty
    self.has_key = False
    
  def move(self, x, y):
    self.x = x
    self.y = y

  def draw(self):
    p5.image(self.img_a,self.x*52, self.y*52)

# Global instances of classes to create the game menus, game map, and single variable to control game state
win_screen = WinScreen()
main_screen = MainScreen()
game_state = "start"
img_menu = p5.loadImage("img_start.png")
gamemap = Map(6, 8, "WWWWWWWW""WBBBBKBW""WBBBBBBW""WWWDWWWW""WBBBBBBW""WWWEWWWW")
player = Player(2,1,False) # Player starts at 2,1 with no key

# p5 functions to set up the draw loop
def setup():
  p5.createCanvas(52*gamemap.w, 52*gamemap.h)

# Draw loop 
def draw():
  if game_state == "start":
    main_screen.draw()
    return None

  if game_state == "win":
    win_screen.draw()
    return None

  p5.background(0)
  # Draw the board
  for y in range(gamemap.h):
    for x in range(gamemap.w):
      gamemap.draw(x,y)
  # Draw the player
  player.draw()

# Control starting, restarting, and character movement
def keyPressed(event):
  global game_state
  if (p5.keyCode == p5.RETURN):
    player.reset()
    gamemap.reset()
    game_state = "play"

  if (game_state != "play"):
    return None

  if(p5.keyCode == p5.LEFT_ARROW):
    if (player.check(player.x - 1, player.y, gamemap)):
      player.move(player.x - 1, player.y)
  if(p5.keyCode == p5.RIGHT_ARROW):
    if player.check(player.x + 1, player.y, gamemap):
      player.move(player.x + 1, player.y)
  if(p5.keyCode == p5.UP_ARROW):
    if player.check(player.x, player.y - 1, gamemap):
      player.move(player.x, player.y - 1)
  if(p5.keyCode == p5.DOWN_ARROW):
    if player.check(player.x, player.y + 1, gamemap):
      player.move(player.x, player.y + 1)


def keyReleased(event):
  pass

def mousePressed(event):
  pass

def mouseReleased(event):
  pass