import pygame, math, random, threading
from pygame.locals import *
global gameExit

gameExit = False

width = 800
height = 600

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Tetris Clone")

normalisedX = 0

fps = 30

clock = pygame.time.Clock()

i = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),
    (255,0,0),(255,0,0),(255,0,0),(255,0,0),
    (0,0,0),(0,0,0),(0,0,0),(0,0,0),
    (0,0,0),(0,0,0),(0,0,0),(0,0,0)]

o = [(0,255,0),(0,255,0),(0,0,0),
    (0,255,0),(0,255,0),(0,0,0),
    (0,0,0),(0,0,0),(0,0,0)]

s = [(0,0,0),(0,0,255),(0,0,255),
    (0,0,255),(0,0,255),(0,0,0),
    (0,0,0),(0,0,0),(0,0,0)]

z = [(0,255,255),(0,255,255),(0,0,0),
    (0,0,0),(0,255,255),(0,255,255),
    (0,0,0),(0,0,0),(0,0,0)]

l = [(255,0,255),(255,0,255),(255,0,255),
    (255,0,255),(0,0,0),(0,0,0),
    (0,0,0),(0,0,0),(0,0,0)]

j = [(255,255,0),(255,255,0),(255,255,0),
    (0,0,0),(0,0,0),(255,255,0),
    (0,0,0),(0,0,0),(0,0,0)]

t = [(255,128,0),(255,128,0),(255,128,0),
    (0,0,0),(255,128,0),(0,0,0),
    (0,0,0),(0,0,0),(0,0,0)]

collided = False
lWallCollided = False
rWallCollided = False
floorCollided = False

objectPos = 0
dropCounter = 0

initShape = True

currentShape = []
currentPos = (3,0)
tempBuffer = []
gridBuffer = []

cellX = 0
cellY = 0

rotC = False
rotCC = False
moveLeft = False
moveRight = False
moveDown = False

for x in range(0, 200):
  gridBuffer.append((0,0,0))
  tempBuffer.append((0,0,0))

def render():
  pygame.draw.rect(screen, (0,0,255), [0, 0, 800, 600])
  for y in range(0, 20):
    for x in range(0, 10):
      pygame.draw.rect(
        screen, gridBuffer[(y * 10) + x], [x * 20, y * 20, 20, 20])
  pygame.display.update()

def rotateC(shape):
  newShape = shape
  if len(shape) == 9:
    newShape = (shape[6],shape[3],shape[0]
              ,shape[7],shape[4],shape[1]
              ,shape[8],shape[5],shape[2])
  elif len(shape) == 16:
    newShape = (shape[12],shape[8],shape[4],shape[0]
              ,shape[13],shape[9],shape[5],shape[1]
              ,shape[14],shape[10],shape[6],shape[2]
              ,shape[15],shape[11],shape[7],shape[3])
  return newShape

def rotateCC(shape):
  newShape = shape
  if len(shape) == 9:
    newShape = (shape[2],shape[5],shape[8]
              ,shape[1],shape[4],shape[7]
              ,shape[0],shape[3],shape[6])
  elif len(shape) == 16:
    newShape = (shape[3],shape[7],shape[11],shape[15]
              ,shape[2],shape[6],shape[10],shape[14]
              ,shape[1],shape[5],shape[9],shape[13]
              ,shape[0],shape[4],shape[8],shape[12])
  return newShape

currentShape = j

while not gameExit:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameExit = True
    if event.type == KEYDOWN:
      if event.key == K_UP:
        rotC = True
      elif event.key == K_DOWN:
        rotCC = True
      elif event.key == K_LEFT:
        moveLeft = True
      elif event.key == K_RIGHT:
        moveRight = True
      elif event.key == K_SPACE:
        moveDown = True
    if event.type == KEYUP:
      if event.key == K_UP:
        rotC = False
      elif event.key == K_DOWN:
        rotCC = False
      elif event.key == K_LEFT:
        moveLeft = False
      elif event.key == K_RIGHT:
        moveRight = False
      elif event.key == K_SPACE:
        moveDown = False

  if initShape == True:
    for y in range(20):
      clearRow = True
      for x in range(10):
        if gridBuffer[(y * 10) + x] == (0,0,0):
          clearRow = False
          break
      if clearRow:
        for yStart in range(y, 0, -1):
          for x in range(10):
            gridBuffer[(yStart * 10) + x] = gridBuffer[((yStart - 1) * 10) + x]

    for x in range(200):
      tempBuffer[x] = gridBuffer[x]

    initShape = False
    collided = False
    lWallCollided = False
    rWallCollided = False
    floorCollided = False

    currentPos = (3,0)
    randomShape = random.randint(0,6)
    if randomShape == 0:
      currentShape = i
    elif randomShape == 1:
      currentShape = o
    elif randomShape == 2:
      currentShape = z
    elif randomShape == 3:
      currentShape = s
    elif randomShape == 4:
      currentShape = j
    elif randomShape == 5:
      currentShape = l
    elif randomShape == 6:
      currentShape = t

  for x in range(0, 200):
    gridBuffer[x] = tempBuffer[x]
  
  if rotC == True:
    currentShape = rotateC(currentShape)
    rotC = False
  if rotCC == True:
    currentShape = rotateCC(currentShape)
    rotCC = False

  if moveLeft == True:
    if lWallCollided == False:
      currentPos =(currentPos[0] - 1, currentPos[1])
      moveLeft = False
  if moveRight == True:
    if rWallCollided == False:
      currentPos = (currentPos[0] + 1, currentPos[1])
      moveRight = False
  if moveDown == True:
    if floorCollided == False:
      currentPos = (currentPos[0], currentPos[1] + 1)

  for x in range(len(currentShape)):
    if len(currentShape) == 9:
      if x > 2 and x < 6:
        normalisedX = x + 7
      elif x > 5:
        normalisedX = x + 14
      else:
        normalisedX = x

    if len(currentShape) == 16:
      if x > 3 and x < 8:
        normalisedX = x + 6
      elif x > 7 and x < 12:
        normalisedX = x + 12
      elif x > 11:
        normalisedX = x + 18
      else:
        normalisedX = x
        
    if len(currentShape) == 4:
      if x == 2:
        normalisedX = 10
      elif x == 3: 
        normalisedX = 11

    objectPos = (currentPos[1] * 10) + currentPos[0] + normalisedX
    if currentShape[x] != (0,0,0):
      if objectPos > 189:
        floorCollided = True
      if objectPos + 10 > 199:
        initShape = True
        
      if objectPos + 10 < 199:
        if gridBuffer[objectPos + 10] != (0,0,0):
          initShape = True
          
#       if objectPos + 1 > ((objectPos / 10) * 10) + 9:
#         rWallCollided = True
# ##      if gridBuffer[objectPos + 1] != (0,0,0):
# ##        rWallCollided = True
        
#       if objectPos - 1 < (objectPos / 10) * 10:
#         lWallCollided = True
##      if gridBuffer[objectPos - 1] != (0,0,0):
##        lWallCollided = True     

      gridBuffer[objectPos] = currentShape[x]

  dropCounter += 1
  if dropCounter >= fps/4:
    if floorCollided == False:
      currentPos = (currentPos[0], currentPos[1] + 1)
    dropCounter = 0
  render()
  clock.tick(fps)
pygame.quit()
quit()
