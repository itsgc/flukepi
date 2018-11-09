# Display stats for framebuffer1 LCD
# Nov 22 2014
# Updated: Jan 18 2016
# Adding living room temp and humidity
# Uses framebuffer 1
#
# Picture of how it looks: http://imgur.com/Hm9syVQ

import pygame, sys, os, time, datetime, urllib, csv, requests, collections, subprocess, json
from pygame.locals import *
os.environ["SDL_FBDEV"] = "/dev/fb1"

import calendar
import time
from functools import lru_cache

## Globals

f = open('/etc/network-tester-slack.json')
data = f.read()
slack_url = json.loads(data)['url']
f.close()

slack_data = dict()

values = "NULL"
labels = "NULL"
timetopoll = True
console_data = collections.deque(maxlen=10)
ifconfig = subprocess.check_output(["ip", "netns", "exec", "dp", "/sbin/ifconfig", "eth0"])
console_data.extend(ifconfig.decode("utf-8").split('\n'))

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


@lru_cache(maxsize=1)
def get_lldp_http(timestamp):
    # This uses requests to get LLDP information returned
    lldp_response = {}
    try:
        lldp_response = requests.get("http://localhost:8080/lldp").json()
    except:
        pass
    slack_data['lldp_data'] = lldp_response
    return lldp_response

def send_slack_data(slack_data):
    str_slack_data = json.dumps(slack_data, indent=2)
    response = requests.post(
        slack_url, data="{ 'text': 'NEW RESULTS INCOMING!' }",
        headers={'Content-Type': 'application/json'}
    )
    response = requests.post(
        slack_url, data="{ 'text': '%s' }" % str_slack_data,
        headers={'Content-Type': 'application/json'}
    )

def get_lldp():
    global timestamp
    lldp_response = get_lldp_http(timestamp)

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

@lru_cache(maxsize=1)
def get_dhcp_http(timestamp):
    dhcp_response = {}
    try:
        dhcp_response = requests.get("http://localhost:8080/dhcp").json()
    except:
        pass
    slack_data['dhcp_data'] = dhcp_response
    return dhcp_response


def get_dhcp():
    global timestamp
    dhcp_response = get_dhcp_http(timestamp)

    myfont = pygame.font.Font(None, 30)
    textsurface = myfont.render('DHCP', False, CYAN)
    DISPLAYSURF.blit(textsurface,(240, 60))
    try:
        # draw response on the screen
        myfont = pygame.font.Font(None, 30)
        textsurface = myfont.render('MAC: ' + dhcp_response['mac_address'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 80))
        textsurface = myfont.render('IP: ' + dhcp_response['ip_address'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 100))
        textsurface = myfont.render('Mask: ' + dhcp_response['subnet_mask'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 120))
        textsurface = myfont.render('Gateway: ' + dhcp_response['gateway'], False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 140))
    except:
        # draw response on the screen
        myfont = pygame.font.Font(None, 30)
        textsurface = myfont.render('No DHCP Captured', False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 80))



@lru_cache(maxsize=1)
def get_link_http(timestamp):
    link_response = {}
    try:
        link_response = requests.get("http://localhost:8080/link").json()
    except:
        pass
    slack_data['link_data'] = link_response
    return link_response


def get_link():
    global timestamp
    link_response = get_link_http(timestamp)

    myfont = pygame.font.Font(None, 30)
    textsurface = myfont.render('LINK', False, CYAN)
    DISPLAYSURF.blit(textsurface,(240, 170))
    try:
        if link_response['link'] == 'Link detected: yes':
            # draw response on the screen
            myfont = pygame.font.Font(None, 30)
            textsurface = myfont.render(link_response['speed'], False, ORANGE)
            DISPLAYSURF.blit(textsurface,(240, 190))
            textsurface = myfont.render(link_response['duplex'], False, ORANGE)
            DISPLAYSURF.blit(textsurface,(240, 210))
        else:
            # draw no link info on screen 
            myfont = pygame.font.Font(None, 30)
            textsurface = myfont.render('No link info', False, ORANGE)
            DISPLAYSURF.blit(textsurface,(240, 190))

    except:
        # draw response on the screen
        myfont = pygame.font.Font(None, 30)
        textsurface = myfont.render('No link info', False, ORANGE)
        DISPLAYSURF.blit(textsurface,(240, 170))


counter = 0

# https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
#--

def page1(disp_surface, counter):
        # draw some lines to create sections on the screen
        # pygame.draw.line(disp_surface, ORANGE, [5, 140], [disp_surface.get_width()-5,140], 1)

        # the button to show page 2
        pygame.draw.rect(disp_surface, ORANGE, (370, 230, 100, 80))
        # draw text on the button
        myfont = pygame.font.Font(None, 24)
        textsurface = myfont.render('Next Page',False, WHITE)
        disp_surface.blit(textsurface,(380, 260))


        # draw the yelp logo
        yelpImg = pygame.image.load('yelp-logo.png')
        disp_surface.blit(yelpImg, (0,0))

        # draw text on the screen
        myfont = pygame.font.Font(None, 40)
        textsurface = myfont.render('Network Tester',False, RED)
        disp_surface.blit(textsurface,(270,10))

        # fetch and draw lldp information
        get_lldp()

        # fetch and draw dhcp information
        get_dhcp()

        # fetch and draw link information
        get_link()

        # draw the slack logo
        slackImg = pygame.image.load('slack-logo.png')
        disp_surface.blit(slackImg, (120,220))

        # draw the fast.com logo
        fastcomImg = pygame.image.load('fast.com.jpeg')
        disp_surface.blit(fastcomImg, (10,220))



def page2(disp_surface, counter):
        # an unused button, but something to play with
        # pygame.draw.rect(disp_surface, GREEN,(390, 230, 80, 80))
        # draw some lines to create sections on the screen
        # pygame.draw.line(disp_surface, ORANGE, [5, 140], [disp_surface.get_width()-5,140], 1)
        # draw the yelp logo


        yelpImg = pygame.image.load('yelp-logo.png')
        disp_surface.blit(yelpImg, (0,0))

        # draw text on the screen
        myfont = pygame.font.Font(None, 40)
        textsurface = myfont.render('Network Tester',False, RED)
        disp_surface.blit(textsurface,(270,10))

        # draw more text on the screen
        myfont = pygame.font.Font(None, 18)
        consoleSurface = pygame.Surface((disp_surface.get_width(), disp_surface.get_height()))
        consoleSurface.fill((BLACK))
        big_sentence = "\n".join(console_data)
        blit_text(consoleSurface, big_sentence, (10,10), myfont, WHITE)
        disp_surface.blit(consoleSurface, (0,0))
# the button to show page 1 pygame.draw.rect(disp_surface, ORANGE, (370, 230, 100, 80))
        # draw text on the button
        myfont = pygame.font.Font(None, 24)
        textsurface = myfont.render('Next Page',False, WHITE)
        disp_surface.blit(textsurface,(380, 260))


pass

page_one = True
while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if (event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            x,y = pos
            # hack - we know the button is bottom right
            if x >= 290 and y <= 110:
                print("Success! " + str(pos))
                page_one = not page_one

    timestamp = calendar.timegm(time.gmtime())
    # We need to blank the screen before drawing on it again
    black_square_that_is_the_size_of_the_screen = pygame.Surface(DISPLAYSURF.get_size())
    black_square_that_is_the_size_of_the_screen.fill((0, 0, 0))
    DISPLAYSURF.blit(black_square_that_is_the_size_of_the_screen, (0, 0))

    if page_one:
        page1(DISPLAYSURF, counter)
    else:
        page2(DISPLAYSURF, counter)
    myfont = pygame.font.Font(None, 18)
    # this actually updates the display
    console_data.append(json.dumps(slack_data, indent=2))
    pygame.display.update()

    # send to slack and life is good :)
    if int(counter) % 60 == 0:
        send_slack_data(slack_data)

    counter += 1
    clock = pygame.time.Clock()
    clock.tick(5)
