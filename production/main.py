print("init")

# You import all the IOs of your board
import board
import busio

# These are imports from the kmk library
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.layers import Layers
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.holdtap import HoldTap
from kmk.scanners.matrix import DiodeOrientation
from kmk.extensions.RGB import RGB
from kmk.extension.display.ssd1306 import Display, SSD1306, TextEntry, ImageEntry

keyboard = KMKKeyboard()

keyboard.matrix = [
    [board.D9, board.D8, board.D7], # col
    [board.D0, board.D1, board.D2]  # row
]

keyboard.diode_orientation = DiodeOrientation.COL2ROW


#PINS = [board.D0, board.D1, board.D2, board.D7, board.D8, board.D9, board.D10]


### OLED ###
i2c_bus = busio.I2C(board.D_SCL, board.D_SDA)

driver = SSD1306(i2c=i2c_bus, device_address=0x3C,)

display = Display(
    display=driver,
    width=128,
    height=32,
    dim_time=10,
    dim_target=0.2,
    off_time=30,
    brightness=0.8,
)

display.entries = [
    TextEntry(text="hello world <**>/", x=64, y=16, x_anchor='M', y_anchor='M'),
    TextEntry(text="lbase", x=5, y=5, inverted=True, layer=0, x_anchor='L', y_anchor='T'),
    TextEntry(text="lutil", x=5, y=5, inverted=True, layer=1, x_anchor='L', y_anchor='T')
]
keyboard.extensions.append(display)


### RGB ###
RGB_PIN = board.D10
N_PIX = 9

rgb = RGB(pin=RGB_PIN, num_leds=N_PIX)
keyboard.extensions.append(rgb)


### MACROS ###
macros = Macros()
keyboard.modules.append(macros)

holdtap = HoldTap(tap_time=300)
keyboard.modules.append(holdtap)

LINE = simple_key_sequence(KC.LSHIFT(KC.END),)
SLEEP = simple_key_sequence(KC.LGUI(KC.U(KC.S)),)
COPY = KC.HT(simple_key_sequence(KC.LCTL(KC.C),), KC.TG(1))
PASTE = simple_key_sequence(KC.LCTLKC.V)
LANG = simple_key_sequence(KC.LGUI(KC.SPACE),) # switch languages
PRINT = simple_key_sequence(KC.LCTL(KC.P))
SAVE = simple_key_sequence(KC.LCTL(KC.S))


### MAPS ###
keyboard.modules.append(Layers())

TRANS = KC.TRNS
# RAISE = KC.TG(1)

keyboard.keymap = [
    # LAYER 0: BASE
    [
     COPY,      PASTE,      LINE,
     PRINT,     SAVE,       KC.RGB_TOG,
     KC.RGB_MODE_BREATHE_RAINBOW, KC.RGB_MODE_KNIGHT, KC.RGB_MODE_SWIRL
    ],
    
    # LAYER 1: UTILS
    [
     TRANS,     TRANS,      KC.F11,
     KC.UP,     LANG,       KC.F10,
     KC.DOWN,   KC.LEFT,    KC.RIGHT
    ],
]

# Start kmk!
if __name__ == '__main__':
    keyboard.go()