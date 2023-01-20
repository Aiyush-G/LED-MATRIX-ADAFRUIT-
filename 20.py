# LED MATRIX PROJECT - Shows Spotify Album Art, Reminders etc...
import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio

WIDTH =64
HEIGHT = 64
BIT_DEPTH = 4

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=WIDTH, height=HEIGHT, bit_depth=BIT_DEPTH,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD,
        board.MTX_ADDRE
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

loadingSplash = displayio.Group()
mainScreen = displayio.Group()
centerImage= displayio.Group()
header= displayio.Group()
footer= displayio.Group()


# HEADER
"""
headerConfig = {
    "text" : "HELLO WORLD ", 
    "font" : terminalio.FONT, 
    "color" : 0x0000FF, 
    "padding" 2,
    "x" : 2, 
    "y" : 2 ,
}
"""

# Implementation
# 1) If the song title length is less than the screen width then center it
# 2)          ""                 greater than the screen width then scroll it

headerText = adafruit_display_text.label.Label(
    font = terminalio.FONT,
    color=0x1DB954,
    text = "HEATWAVES", 
)
# Center Middle
headerText.x = (display.width // 2) - (headerText.width // 2)
header.y = 5

#headerText.x = display.width // 2
header.append(headerText)

# Center Image
bitmap = displayio.OnDiskBitmap("/heatwaves-processed.bmp")
albumArt = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
centerImage.append(albumArt)

#text_area = adafruit_display_text.label.Label(font = terminalio.FONT, text=text, color=color)
#text_area.x = 2
#text_area.y = 3

line1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xff0000,
    text="Hi Aiyush")
line1.x = display.width
line1.y = 8

line2 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0x0080ff,
    text="<3")
line2.x = display.width
line2.y = 24

# Put each line of text into a Group, then show that group.
g = displayio.Group()
#g.x = 5
#g.y = 5
#g.append(tile_grid)
g.append(line1)
g.append(line2)
#g.append(text_area)

mainScreen.append(g)
mainScreen.append(header)
mainScreen.append(centerImage)
display.show(mainScreen)


# This function will scoot one label a pixel to the left and send it back to
# the far right if it's gone all the way off screen. This goes in a function
# because we'll do exactly the same thing with line1 and line2 below.
def scroll(line):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width

# This function scrolls lines backwards.  Try switching which function is
# called for line2 below!
def reverse_scroll(line):
    line.x = line.x + 1
    line_width = line.bounding_box[2]
    if line.x >= display.width:
        line.x = -line_width

# You can add more effects in this loop. For instance, maybe you want to set the
# color of each label to a different value.
while True:
    scroll(line1)
    scroll(line2)
    #reverse_scroll(line2)
    display.refresh(minimum_frames_per_second=0)
