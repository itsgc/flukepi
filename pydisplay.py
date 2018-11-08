# Display stats for framebuffer1 LCD
# Nov 22 2014
# Updated: Jan 18 2016
# Adding living room temp and humidity
# Uses framebuffer 1
#
# Picture of how it looks: http://imgur.com/Hm9syVQ

import pygame, sys, os, time, datetime, urllib, csv, requests
from pygame.locals import *
os.environ["SDL_FBDEV"] = "/dev/fb1"

## Globals

values = "NULL"
labels = "NULL"
timetopoll = True

## Set up the screen

pygame.init()

DISPLAYSURF = pygame.display.set_mode((480, 320))
pygame.display.set_caption('Stats')
pygame.mouse.set_visible(0)


# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (211,   35,   35)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
CYAN  = (  0, 255, 255)
ORANGE = (241, 92, 0)

def get_lldp():
    # This uses requests to get LLDP information returned

    try:
        lldp_response = requests.get("http://localhost:8080/lldp").json()
    except:
        lldp_response = {}

    myfont = pygame.font.Font(None, 30)

    textsurface = myfont.render('LLDP', False, CYAN)
    DISPLAYSURF.blit(textsurface,(10, 60))

    try:
        # draw response on the screen
        textsurface = myfont.render('Switch: ' + lldp_response['switch_name'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(10, 80))
        textsurface = myfont.render('Port: ' + lldp_response['switch_port'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(10, 100))
    except:
        # draw response on the screen
        textsurface = myfont.render('No LLDP Captured', False, ORANGE)
        DISPLAYSURF.blit(textsurface,(10, 80))

    textsurface = myfont.render('VLANS', False, CYAN)
    DISPLAYSURF.blit(textsurface,(10, 130))

    try:
        # draw response on the screen
        offset = 150 
        for vlan in lldp_response['vlans']:
            textsurface = myfont.render(vlan, False, ORANGE)
            DISPLAYSURF.blit(textsurface,(10, offset))
            offset += 20
    except:
        # draw response on the screen
        textsurface = myfont.render('No VLANS Captured', False, ORANGE)
        DISPLAYSURF.blit(textsurface,(10, 150))

def get_dhcp():

    try:
        dhcp_response = requests.get("http://localhost:8080/dhcp").json()
    except:
        dhcp_response = {}

    myfont = pygame.font.Font(None, 30)
    textsurface = myfont.render('DHCP', False, CYAN)
    DISPLAYSURF.blit(textsurface,(240, 60))

    try:
        # draw response on the screen
        myfont = pygame.font.Font(None, 30)
        textsurface = myfont.render('IP: ' + dhcp_response['ip_address'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 80))
        textsurface = myfont.render('Mask: ' + dhcp_response['subnet_mask'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 100))
        textsurface = myfont.render('Gateway: ' + dhcp_response['gateway'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 120))
    except:
        # draw response on the screen
        myfont = pygame.font.Font(None, 30)
        textsurface = myfont.render('No DHCP Captured', False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 80))

counter = 0

while True:

    # Scan touchscreen events
    for event in pygame.event.get():
        if (event.type is MOUSEBUTTONUP): 
            pos = pygame.mouse.get_pos()
            x,y = pos
            # hack - we know the button is bottom right
            if x >= 290 and y <= 110:
                print("Success! " + str(pos))


    # We need to blank the screen before drawing on it again

    black_square_that_is_the_size_of_the_screen = pygame.Surface(DISPLAYSURF.get_size())
    black_square_that_is_the_size_of_the_screen.fill((0, 0, 0))
    DISPLAYSURF.blit(black_square_that_is_the_size_of_the_screen, (0, 0))

    # an unused button, but something to play with
    # pygame.draw.rect(DISPLAYSURF, GREEN,(390, 230, 80, 80))
    # draw the slack logo
    slackImg = pygame.image.load('slack-logo.png')
    DISPLAYSURF.blit(slackImg, (380,220))


    # draw some lines to create sections on the screen
    # pygame.draw.line(DISPLAYSURF, ORANGE, [5, 140], [DISPLAYSURF.get_width()-5,140], 1)

    # draw the yelp logo
    yelpImg = pygame.image.load('yelp-logo.png')
    DISPLAYSURF.blit(yelpImg, (0,0))

    # draw text on the screen
    myfont = pygame.font.Font(None, 40)
    textsurface = myfont.render('Network Tester',False, RED)
    DISPLAYSURF.blit(textsurface,(270,10))

    # draw more text on the screen
    myfont = pygame.font.Font(None, 20)
    textsurface = myfont.render('loop counter: ' + str(counter) ,False, RED)
    DISPLAYSURF.blit(textsurface,(10,300))
    counter += 1

    # fetch and draw lldp information
    get_lldp()

    # fetch and draw dhcp information
    get_dhcp()

    # this actually updates the display
    pygame.display.update()

    clock = pygame.time.Clock()
    clock.tick(5) 
