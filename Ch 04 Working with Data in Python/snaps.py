# Some pygame helper functions for simple image display
# and sound effect playback
# Rob Miles July 2017
# Version 1.0

import pygame

surface = None


def setup(width=800, height=600, title=''):
    '''
    Sets up the pygame environment
    '''
    global window_size
    global back_color
    global text_color
    global image
    global surface

    # Don't initialise if we already have

    if surface is not None:
        return

    window_size = (width, height)
    back_color = (255, 255, 255)
    text_color = (255, 0, 0)
    image = None

    # pre initialise pyGame's audio engine to avoid sound latency issues
    pygame.mixer.pre_init(frequency=44100)
    pygame.init()

    # initialise pyGame's audio engine
    pygame.mixer.init()

    # Create the game surface
    surface = pygame.display.set_mode(window_size)

    clear_display()

    pygame.display.set_caption(title)


def handle_events():
    '''
    Consume events that are generated by the pygame window
    These are not presntly used for anything
    '''
    setup()
    for event in pygame.event.get():
        pass


def play_sound(filepath):
    '''
    Plays the specified sound file
    '''
    pygame.mixer.init()
    sound = pygame.mixer.Sound(filepath)
    sound.play()


def display_image(filepath):
    '''
    Displays the image from the given filepath
    Starts pygame if required
    May throw exceptions
    '''
    global surface
    global window_size
    global image

    handle_events()
    image = pygame.image.load(filepath)
    image = pygame.transform.smoothscale(image, window_size)
    surface.blit(image, (0, 0))
    pygame.display.flip()


def clear_display():
    '''
    Clears the display to the background colour
    and the image (if any) on top of it
    '''

    global surface
    global image
    global back_color

    handle_events()

    surface.fill(back_color)
    if image is not None:
        surface.blit(image, (0, 0))


def get_display_lines(text, font, width):
    '''
    Returns a list of strings which have been split
    to fit the given window width using the supplied font
    '''
    space_width = font.size(' ')[0]
    result = []
    text_lines = text.splitlines()
    for text_line in text_lines:
        words = text_line.split()
        x = 0
        line = ''
        for word in words:
            word_width = font.size(word)[0]
            if x + word_width > width:
                # Remove the trailing space from the line
                # before adding to the list of lines to return
                line = line.strip()
                result.append(line)
                line = word + ' '
                x = word_width + space_width
            else:
                line = line + word + ' '
                x = x + word_width + space_width

        if line != '':
            # Got a partial line to add to the end
            # Remove the trailing space from the line
            # before adding to the list of lines to return
            line = line.strip()
            result.append(line)
    return result


def display_message(text, size=200, margin=20, horiz='center', vert='center',
                    color=(255, 0, 0)):
    '''
    Displays the text as a message
    Sice can be used to select the size of the
    text
    '''
    global window_size
    global surface

    handle_events()

    clear_display()

    # Get the text version of the input
    text = str(text)

    font = pygame.font.Font(None, size)

    available_width = window_size[0] - (margin * 2)

    lines = get_display_lines(text, font, available_width)

    rendered_lines = []

    height = 0

    for line in lines:
        rendered_line = font.render(line, 1, color)
        height += rendered_line.get_height()
        rendered_lines.append(rendered_line)

    if height > window_size[1]:
        raise Exception('Text too large for window')

    if vert == 'center':
        y = (window_size[1] - height) / 2.0
    elif vert == 'top':
        y = margin
    elif vert == 'bottom':
        y=(window_size[1]-margin) - height

    for rendered_line in rendered_lines:
        width = rendered_line.get_width()
        height = rendered_line.get_height()
        if horiz == 'center':
            x = (available_width - width) / 2.0 + margin
        elif horiz == 'left':
            x = margin
        elif horiz == 'right':
            x = self.window_size[0] - width - margin
        surface.blit(rendered_line, (x, y))
        y += height
    pygame.display.flip()

import urllib.request
import xml.etree.ElementTree


def get_weather_temp(latitude,longitude):
    '''
    Uses forecast.weather.gov to get the weather
    for the specified latitude and longitude
    '''
    url="http://forecast.weather.gov/MapClick.php?lat={0}&lon={1}&unit=0&lg=english&FcstType=dwml".format(latitude,longitude)
    req=urllib.request.urlopen(url)
    page=req.read()
    doc=xml.etree.ElementTree.fromstring(page)
    # I'm not proud of this, but by gum it works...
    for child in doc:
        if child.tag == 'data':
            if child.attrib['type'] == 'current observations':
                for item in child:
                    if item.tag == 'parameters':
                        for i in item:
                            if i.tag == 'temperature':
                                if i.attrib['type'] == 'apparent':
                                    for t in i:
                                        if t.tag =='value':
                                            return int(t.text)


def get_weather_desciption(latitude,longitude):
    '''
    Uses forecast.weather.gov to get the weather
    for the specified latitude and longitude
    '''
    url="http://forecast.weather.gov/MapClick.php?lat={0}&lon={1}&unit=0&lg=english&FcstType=dwml".format(latitude,longitude)
    req=urllib.request.urlopen(url)
    page=req.read()
    doc=xml.etree.ElementTree.fromstring(page)
    # I'm not proud of this, but by gum it works...
    for child in doc:
        if child.tag == 'data':
            if child.attrib['type'] == 'current observations':
                for item in child:
                    if item.tag == 'parameters':
                        for i in item:
                            if i.tag == 'weather':
                                for t in i:
                                    if t.tag == 'weather-conditions':
                                        if t.get('weather-summary') is not None:
                                            return t.get('weather-summary')
