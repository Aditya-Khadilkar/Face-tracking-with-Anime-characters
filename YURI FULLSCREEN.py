import cv2
import os
from math import sin, cos, radians
import ctypes
import time
import pygame

pygame.init()
black = (0,0,0)
ix = 1920
iy = 1080

ge = pygame.image.load('F:\Machine Learning\mwo.png')
eye = pygame.image.load('F:\Machine Learning\meye.png')
def pos(gameDisplay,ge,x,y):
    gameDisplay.blit(ge,(x,y))

def eyeloc(gameDisplay,eye,ex,ey):
    gameDisplay.blit(eye,(ex,ey))

def move_eyes(gameDisplay, xcord, ycord,):
    w = scl
    h = scb
    x = (w-ix)/2
    y = h-iy
    ex = (w-ix)/2
    ey = h-iy
    nx = ex+ xcord/20 -10
    ny = ey + ycord/20 -10
    gameDisplay.blit(eye,(nx,ny))
    gameDisplay.blit(ge,(x,y))
    #code to redraw images
    pygame.display.update()
    
def show_yuri_image(w, h):
    w = scl
    h = scb
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    gameDisplay = pygame.display.set_mode((w,h))
    print(gameDisplay)
    pygame.display.set_caption("Yuri")
    

    x = (w-ix)/2
    y = h-iy
    ex = (w-ix)/2
    ey = h-iy
    gameDisplay.fill(black)
    eyeloc(gameDisplay, eye, ex, ey)
    pos(gameDisplay, ge, x, y)
    
    pygame.display.update()
    return gameDisplay
    

user32 = ctypes.windll.user32
scl,scb = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print("Width: ",scl,"Height: ",scb) #screen metrics

camera =  cv2.VideoCapture(0)

w = camera.set(3, scl/2)
h = camera.set(4, scb/2)
face = cv2.CascadeClassifier("F:\Machine Learning\haarcascade_frontalface_alt2.xml")
fps = camera.get(cv2.CAP_PROP_FPS)
print("fps: ",fps)
settings = {
    'scaleFactor': 1.3, 
    'minNeighbors': 3, 
    'minSize': (50, 50), 
}

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

gameDisplay = show_yuri_image(scl, scb)
running = True
while running:
##    event = pygame.event.wait ()
##    pressed = pygame.key.get_pressed()
##    if(pressed[pygame.K_q]):
##        running = False

    ret, imgn = camera.read()
    img = cv2.flip(imgn, +1)

    for angle in [0, -25, 25]:
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings)
        if len(detected):
            detected = [rotate_point(detected[-1], img, -angle)]
            break

    # Make a copy as we don't want to draw on the original image:
    for x, y, w, h in detected[-1:]:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
        xcord = (x+w)/2
        ycord = 2*(y+h)/3 # to look at the eyes
        move_eyes(gameDisplay, xcord, ycord,)
        
    #cv2.imshow('facedetect', img)
    if cv2.waitKey(5) != -1:
        break

cv2.destroyWindow("facedetect")
pygame.quit()
quit()

    
