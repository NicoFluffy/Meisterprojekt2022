import socketio
import time
import time
import board
import neopixel


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.D18
# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of
#  NeoPixels
num_pixels = 11

muted = False

num_mute = 2
mute_offset = 1



# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# asyncio
sio = socketio.Client()
namespace = '/licht'
@sio.event(namespace=namespace)
def connect():
    print("I'm connected!")

@sio.event(namespace=namespace)
def connect_error(data):
    print("The connection failed!")

@sio.event(namespace=namespace)
def disconnect():
    print("I'm disconnected!")


@sio.event(namespace=namespace)
def message(data):
    print('I received a message!', data)

def lichtaus():
    print("licht aus")
    pixels.fill((0,0,0))
    lichtMute()
    pixels.show()

def lichtan():
    print("licht an")
    pixels.fill((255,255,255))
    lichtMute()
    pixels.show()

def lichtMute():
    global muted
    if muted:
        print("muted pixels")
        for i in range(num_mute):
            pixels[i + mute_offset] = (255,0,0)

def main():
    lichtan()
    while True:
        try: 
            time.sleep(1)
            sio.connect('http://192.168.0.180:5000', namespaces=[namespace])
            sio.wait()
        except KeyboardInterrupt:
            sio.disconnect()
            break
        except:
            print("keine Verbindung")


if __name__ == '__main__':
    main()
