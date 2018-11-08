# Display stats for framebuffer1 LCD
# Nov 22 2014
# Updated: Jan 18 2016
# Adding living room temp and humidity
# Uses framebuffer 1
#
# Picture of how it looks: http://imgur.com/Hm9syVQ

import pygame, sys, os, time, datetime, urllib, csv
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
    # This would normally use requests to get LLDP information returned
    # but for now we'll just fake it

    lldp_response = { 'switch_name': 'hamasw4-1', 'switch_port': 'ge-0/2/45' }    

    myfont = pygame.font.Font(None, 30)
    textsurface = myfont.render('LLDP', False, CYAN)
    DISPLAYSURF.blit(textsurface,(10, 60))

    try:
        # draw response on the screen
        myfont = pygame.font.Font(None, 30)
        textsurface = myfont.render('Switch: ' + lldp_response['switch_name'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(10, 80))
        textsurface = myfont.render('Port: ' + lldp_response['switch_port'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(10, 100))
    except:
        # draw response on the screen
        myfont = pygame.font.Font(None, 30)
        textsurface = myfont.render('No LLDP Captured', False, ORANGE)
        DISPLAYSURF.blit(textsurface,(10, 80))

def get_dhcp():
    # This would normally use requests to get DHCP information returned
    # but for now we'll just fake it

    dhcp_response = { 'ip_address': '10.20.20.30', 'subnet_mask': '255.255.252.0', 'gateway': '10.20.20.1' }    

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

while True:

    # We need to blank the screen before drawing on it again

    black_square_that_is_the_size_of_the_screen = pygame.Surface(DISPLAYSURF.get_size())
    black_square_that_is_the_size_of_the_screen.fill((0, 0, 0))
    DISPLAYSURF.blit(black_square_that_is_the_size_of_the_screen, (0, 0))

    # draw some lines to create sections on the screen
    # pygame.draw.line(DISPLAYSURF, ORANGE, [5, 140], [DISPLAYSURF.get_width()-5,140], 1)

    # draw the yelp logo
    yelpImg = pygame.image.load('yelp-logo.png')
    DISPLAYSURF.blit(yelpImg, (0,0))

    # draw text on the screen
    myfont = pygame.font.Font(None, 40)
    textsurface = myfont.render('Network Tester',False, RED)
    DISPLAYSURF.blit(textsurface,(270,10))

    # fetch and draw lldp information
    get_lldp()

    # fetch and draw dhcp information
    get_dhcp()

    # rotate 180 degrees so HDMI plug is at the top of the case
    # this isn't strictly needed but is nice for development ;-)

    DISPLAYSURF.blit(pygame.transform.rotate(DISPLAYSURF, 180), (0, 0))

    # this actually updates the display
    pygame.display.update()

    # sleep a wee bit since we don't need insanely fast reactions (yet)
    time.sleep(1)

